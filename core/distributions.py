"""
10 probability scenarios for penalty kick simulation.
Each scenario defines kicker and goalkeeper probability distributions.
"""

from core.models import DirectionProbability, Scenario

# Ordering: LEFT, CENTER, RIGHT

SCENARIOS: list[Scenario] = [
    Scenario(
        name="Distribusi Uniform",
        description="Semua arah peluang sama rata 33.3%",
        kicker_prob=DirectionProbability(1/3, 1/3, 1/3),
        keeper_prob=DirectionProbability(1/3, 1/3, 1/3),
    ),
    Scenario(
        name="Ronaldo Dominan Kanan",
        description="Ronaldo 50% ke kanan, Courtois seimbang",
        kicker_prob=DirectionProbability(0.25, 0.25, 0.50),
        keeper_prob=DirectionProbability(1/3, 1/3, 1/3),
    ),
    Scenario(
        name="Ronaldo Dominan Kiri",
        description="Ronaldo 55% ke kiri, Courtois seimbang",
        kicker_prob=DirectionProbability(0.55, 0.20, 0.25),
        keeper_prob=DirectionProbability(1/3, 1/3, 1/3),
    ),
    Scenario(
        name="Courtois Baca Pola",
        description="Courtois mengikuti kecenderungan Ronaldo ke kanan 60%",
        kicker_prob=DirectionProbability(0.25, 0.25, 0.50),
        keeper_prob=DirectionProbability(0.20, 0.20, 0.60),
    ),
    Scenario(
        name="Panenka High-Risk",
        description="Ronaldo 60% tengah (Panenka), Courtois jarang diam",
        kicker_prob=DirectionProbability(0.20, 0.60, 0.20),
        keeper_prob=DirectionProbability(0.45, 0.10, 0.45),
    ),
    Scenario(
        name="Strategi Konservatif",
        description="Keduanya bermain aman, dominan ke kiri gawang",
        kicker_prob=DirectionProbability(0.50, 0.30, 0.20),
        keeper_prob=DirectionProbability(0.50, 0.30, 0.20),
    ),
    Scenario(
        name="Counter-Strategy",
        description="Courtois sengaja berlawanan dari pola Ronaldo",
        kicker_prob=DirectionProbability(0.20, 0.30, 0.50),
        keeper_prob=DirectionProbability(0.50, 0.30, 0.20),
    ),
    Scenario(
        name="All-or-Nothing",
        description="Ronaldo 90% kanan, Courtois 90% kiri — pure gamble",
        kicker_prob=DirectionProbability(0.05, 0.05, 0.90),
        keeper_prob=DirectionProbability(0.90, 0.05, 0.05),
    ),
    Scenario(
        name="Nash Equilibrium",
        description="Strategi optimal game theory — mixed equilibrium",
        kicker_prob=DirectionProbability(0.40, 0.20, 0.40),
        keeper_prob=DirectionProbability(0.40, 0.20, 0.40),
    ),
    Scenario(
        name="Psikologi Tekanan",
        description="Ronaldo acak di bawah tekanan, Courtois fokus tengah 50%",
        kicker_prob=DirectionProbability(0.35, 0.30, 0.35),
        keeper_prob=DirectionProbability(0.25, 0.50, 0.25),
    ),
]
