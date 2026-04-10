"""Game state machine controlling the penalty kick flow."""

from __future__ import annotations
from enum import Enum, auto
from ursina import invoke
import numpy as np

from core.models import Direction, KickResult, Scenario
from core.simulator import pick_direction
from game.animations import animate_kick, animate_keeper_dive, reset_entities


class GamePhase(Enum):
    IDLE = auto()
    KICKING = auto()
    RESULT = auto()


class GameState:
    """Manages single-kick game flow between phases."""

    def __init__(self, ronaldo, courtois, ball, on_result_callback=None):
        self.ronaldo = ronaldo
        self.courtois = courtois
        self.ball = ball
        self.phase = GamePhase.IDLE
        self.on_result = on_result_callback
        self.rng = np.random.default_rng()
        self.current_scenario: Scenario | None = None
        self.last_result: KickResult | None = None

    def set_scenario(self, scenario: Scenario):
        self.current_scenario = scenario

    def execute_kick(self, kick_dir: Direction):
        if self.phase != GamePhase.IDLE or self.current_scenario is None:
            return

        self.phase = GamePhase.KICKING

        keeper_dir = pick_direction(
            self.current_scenario.keeper_prob.as_list(), self.rng
        )

        self.last_result = KickResult(
            kick_direction=kick_dir,
            keeper_direction=keeper_dir,
        )

        _offset, keeper_x = animate_keeper_dive(self.courtois, keeper_dir)

        animate_kick(
            self.ronaldo, self.ball, kick_dir,
            is_goal=self.last_result.is_goal,
            keeper_x=keeper_x,
            keeper_dive_dir=keeper_dir,
        )

        invoke(self._show_result, delay=1.4)

    def _show_result(self):
        self.phase = GamePhase.RESULT
        if self.on_result:
            self.on_result(self.last_result)

    def reset(self):
        reset_entities(self.ronaldo, self.courtois, self.ball)
        self.phase = GamePhase.IDLE
        self.last_result = None
