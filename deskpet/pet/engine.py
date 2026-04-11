"""Desktop pet engine - manages pet state machine and behaviors."""

from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from queue import Queue
from threading import Lock
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


class Behavior(Enum):
    IDLE = auto()
    WALK = auto()
    SLEEP = auto()
    EAT = auto()
    PLAY = auto()
    CHAT = auto()


@dataclass
class BehaviorConfig:
    idle_frames: int = 16
    idle_fps: float = 6.0
    walk_frames: int = 16
    walk_fps: float = 10.0
    sleep_frames: int = 8
    sleep_fps: float = 3.0
    eat_frames: int = 16
    eat_fps: float = 8.0
    play_frames: int = 16
    play_fps: float = 10.0
    walk_speed: int = 3
    walk_duration: float = 5.0
    sleep_duration: float = 8.0
    eat_duration: float = 3.0
    play_duration: float = 6.0


@dataclass
class ScreenBounds:
    width: int = 1920
    height: int = 1080
    margin: int = 64


@dataclass
class PetState:
    name: str
    sprite_path: "Path"
    behavior: Behavior = Behavior.IDLE
    position_x: int = 100
    position_y: int = 100
    target_x: int = 100
    target_y: int = 100
    velocity_x: int = 0
    velocity_y: int = 0
    last_update: float = field(default_factory=time.time)
    behavior_duration: float = 0.0
    facing_right: bool = True

    @property
    def position(self) -> tuple[int, int]:
        return (self.position_x, self.position_y)

    def update_behavior(self, new_behavior: Behavior, duration: float = 0.0) -> None:
        self.behavior = new_behavior
        self.behavior_duration = duration
        self.last_update = time.time()

    def is_behavior_complete(self) -> bool:
        if self.behavior_duration <= 0:
            return False
        return time.time() - self.last_update >= self.behavior_duration


@dataclass
class TickResult:
    sprite: str
    position: tuple[int, int]
    behavior: Behavior
    facing_right: bool


class PetEngine:
    def __init__(
        self,
        pet_type: str,
        resource_dir: "Path",
        bounds: ScreenBounds | None = None,
        config: BehaviorConfig | None = None,
    ):
        from deskpet.pet.sprites import SpriteManager

        self.state = PetState(pet_type, resource_dir / pet_type)
        self.sprite_manager = SpriteManager(self.state.sprite_path)
        self.config = config or BehaviorConfig()
        self.bounds = bounds or ScreenBounds()
        self._running = False
        self._lock = Lock()
        self._command_queue: Queue[tuple[Behavior, float]] = Queue()
        self._on_behavior_change: Callable[[Behavior], None] | None = None

    def set_behavior_callback(self, callback: Callable[[Behavior], None]) -> None:
        self._on_behavior_change = callback

    def start(self) -> None:
        self._running = True
        self._set_behavior(Behavior.IDLE)

    def stop(self) -> None:
        self._running = False

    def _set_behavior(
        self, behavior: Behavior, duration: float = 0.0, lock_held: bool = False
    ) -> None:
        if lock_held:
            self._do_set_behavior(behavior, duration)
        else:
            with self._lock:
                self._do_set_behavior(behavior, duration)

    def _do_set_behavior(self, behavior: Behavior, duration: float = 0.0) -> None:
        old_behavior = self.state.behavior
        self.state.update_behavior(behavior, duration)
        logger.info(
            f"Behavior changed: {old_behavior.name} -> {behavior.name} (duration={duration}s)"
        )
        if behavior == Behavior.WALK and duration == 0:
            self._set_walk_target()
        if self._on_behavior_change:
            self._on_behavior_change(behavior)

    def command(self, behavior: Behavior, duration: float = 0.0) -> None:
        if not self._running:
            return
        self._command_queue.put((behavior, duration))

    def walk_to(self, x: int, y: int) -> None:
        with self._lock:
            self.state.target_x = max(
                self.bounds.margin, min(x, self.bounds.width - self.bounds.margin)
            )
            self.state.target_y = max(
                self.bounds.margin, min(y, self.bounds.height - self.bounds.margin)
            )
            self._set_behavior(Behavior.WALK, self.config.walk_duration, lock_held=True)

    def walk_random(self) -> None:
        import random

        x = random.randint(self.bounds.margin, self.bounds.width - self.bounds.margin)
        y = random.randint(self.bounds.margin, self.bounds.height - self.bounds.margin)
        self.walk_to(x, y)

    def _set_walk_target(self) -> None:
        import random

        x = random.randint(self.bounds.margin, self.bounds.width - self.bounds.margin)
        y = random.randint(self.bounds.margin, self.bounds.height - self.bounds.margin)
        self.state.target_x = x
        self.state.target_y = y

    def _process_command_queue(self) -> None:
        try:
            while not self._command_queue.empty():
                behavior, duration = self._command_queue.get_nowait()
                self._set_behavior(behavior, duration)
        except Exception:
            pass

    def _update_walk(self, dt: float) -> None:
        dx = self.state.target_x - self.state.position_x
        dy = self.state.target_y - self.state.position_y
        distance = (dx * dx + dy * dy) ** 0.5

        if distance < self.config.walk_speed:
            self.state.position_x = self.state.target_x
            self.state.position_y = self.state.target_y
            if self.state.is_behavior_complete():
                self._set_behavior(Behavior.IDLE)
            return

        if dx != 0:
            self.state.facing_right = dx > 0

        self.state.velocity_x = int(dx / distance * self.config.walk_speed)
        self.state.velocity_y = int(dy / distance * self.config.walk_speed)
        self.state.position_x += self.state.velocity_x
        self.state.position_y += self.state.velocity_y

    def _update_idle(self, dt: float) -> None:
        if random.random() < 0.001:
            self.walk_random()

    def tick(self) -> TickResult:
        current_time = time.time()
        dt = current_time - self.state.last_update
        self.state.last_update = current_time

        self._process_command_queue()

        if self.state.is_behavior_complete() and self.state.behavior != Behavior.IDLE:
            self._set_behavior(Behavior.IDLE)

        behavior = self.state.behavior

        if behavior == Behavior.WALK:
            self._update_walk(dt)
        elif behavior == Behavior.IDLE:
            self._update_idle(dt)

        fps = self._get_fps_for_behavior(behavior)
        frame_duration = 1.0 / fps if fps > 0 else 0.1
        frame = int(current_time / frame_duration) % self._get_frames_for_behavior(behavior)

        sprite = self.sprite_manager.get_sprite(behavior, frame)

        if frame == 0:
            logger.debug(
                f"Behavior: {behavior.name}, Frame: {frame}, Sprite: {sprite}, Position: {self.state.position}"
            )

        return TickResult(
            sprite=sprite,
            position=(self.state.position_x, self.state.position_y),
            behavior=behavior,
            facing_right=self.state.facing_right,
        )

    def _get_fps_for_behavior(self, behavior: Behavior) -> float:
        return {
            Behavior.IDLE: self.config.idle_fps,
            Behavior.WALK: self.config.walk_fps,
            Behavior.SLEEP: self.config.sleep_fps,
            Behavior.EAT: self.config.eat_fps,
            Behavior.PLAY: self.config.play_fps,
            Behavior.CHAT: self.config.idle_fps,
        }.get(behavior, 2.0)

    def _get_frames_for_behavior(self, behavior: Behavior) -> int:
        return {
            Behavior.IDLE: self.config.idle_frames,
            Behavior.WALK: self.config.walk_frames,
            Behavior.SLEEP: self.config.sleep_frames,
            Behavior.EAT: self.config.eat_frames,
            Behavior.PLAY: self.config.play_frames,
            Behavior.CHAT: self.config.idle_frames,
        }.get(behavior, 4)

    @property
    def current_behavior(self) -> Behavior:
        return self.state.behavior

    def set_bounds(self, width: int, height: int) -> None:
        self.bounds.width = width
        self.bounds.height = height

    def set_position(self, x: int, y: int) -> None:
        with self._lock:
            self.state.position_x = x
            self.state.position_y = y
            self.state.target_x = x
            self.state.target_y = y

    def get_state(self) -> PetState:
        return self.state
