"""Domain models for penalty kick simulation."""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class Direction(Enum):
    """Three possible directions for kick and goalkeeper dive."""
    LEFT = "Kiri"
    CENTER = "Tengah"
    RIGHT = "Kanan"


@dataclass(frozen=True)
class DirectionProbability:
    """Probability distribution across three directions. Must sum to 1.0."""
    left: float
    center: float
    right: float

    def __post_init__(self):
        total = round(self.left + self.center + self.right, 4)
        if total != 1.0:
            raise ValueError(f"Probabilities must sum to 1.0, got {total}")

    def as_list(self) -> list[float]:
        return [self.left, self.center, self.right]

    def get(self, direction: Direction) -> float:
        return {
            Direction.LEFT: self.left,
            Direction.CENTER: self.center,
            Direction.RIGHT: self.right,
        }[direction]


@dataclass(frozen=True)
class Scenario:
    """A probability scenario defining kicker and goalkeeper behavior."""
    name: str
    description: str
    kicker_prob: DirectionProbability
    keeper_prob: DirectionProbability

    def mathematical_goal_probability(self) -> float:
        """
        Calculate exact goal probability using conditional probability.
        P(goal) = sum over all directions: P(kick=d) * (1 - P(keeper=d))
        A goal occurs when the keeper dives to a different direction than the ball.
        """
        total = 0.0
        for direction in Direction:
            p_kick = self.kicker_prob.get(direction)
            p_save = self.keeper_prob.get(direction)
            total += p_kick * (1 - p_save)
        return total


@dataclass
class KickResult:
    """Result of a single penalty kick."""
    kick_direction: Direction
    keeper_direction: Direction

    @property
    def is_goal(self) -> bool:
        return self.kick_direction != self.keeper_direction


@dataclass
class SimulationResult:
    """Aggregated results from a batch simulation run."""
    scenario: Scenario
    total_kicks: int
    results: list[KickResult] = field(default_factory=list)

    @property
    def goals(self) -> int:
        return sum(1 for r in self.results if r.is_goal)

    @property
    def saves(self) -> int:
        return self.total_kicks - self.goals

    @property
    def simulated_goal_rate(self) -> float:
        if self.total_kicks == 0:
            return 0.0
        return self.goals / self.total_kicks

    @property
    def mathematical_goal_rate(self) -> float:
        return self.scenario.mathematical_goal_probability()

    @property
    def deviation(self) -> float:
        """Absolute difference between simulated and mathematical rates."""
        return abs(self.simulated_goal_rate - self.mathematical_goal_rate)

    def direction_counts(self, role: str = "kicker") -> dict[Direction, int]:
        """Count occurrences per direction for kicker or keeper."""
        counts = {d: 0 for d in Direction}
        for r in self.results:
            d = r.kick_direction if role == "kicker" else r.keeper_direction
            counts[d] += 1
        return counts
