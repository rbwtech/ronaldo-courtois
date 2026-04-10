"""Monte Carlo simulation engine for penalty kicks."""

from __future__ import annotations
import numpy as np
from core.models import Direction, KickResult, Scenario, SimulationResult


_DIRECTIONS = list(Direction)


def pick_direction(probs: list[float], rng: np.random.Generator) -> Direction:
    """Sample a direction using the given probability distribution."""
    idx = rng.choice(3, p=probs)
    return _DIRECTIONS[idx]


def simulate_single(scenario: Scenario, rng: np.random.Generator) -> KickResult:
    """Simulate one penalty kick."""
    kick_dir = pick_direction(scenario.kicker_prob.as_list(), rng)
    keeper_dir = pick_direction(scenario.keeper_prob.as_list(), rng)
    return KickResult(kick_direction=kick_dir, keeper_direction=keeper_dir)


def run_simulation(scenario: Scenario, n: int = 1000, seed: int | None = None) -> SimulationResult:
    """
    Run N penalty kick simulations for a given scenario.
    Uses numpy RNG for reproducibility when seed is provided.
    """
    rng = np.random.default_rng(seed)
    results = [simulate_single(scenario, rng) for _ in range(n)]
    return SimulationResult(scenario=scenario, total_kicks=n, results=results)


def run_all_scenarios(
    scenarios: list[Scenario], n: int = 1000, seed: int | None = None
) -> list[SimulationResult]:
    """Run simulations for all scenarios and return collected results."""
    return [run_simulation(s, n, seed) for s in scenarios]
