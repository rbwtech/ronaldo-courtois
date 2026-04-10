"""Statistics dashboard — full screen overlay with scroll support."""

from __future__ import annotations
from ursina import Entity, Text, Button, color, camera, destroy

from core.models import SimulationResult, Direction

# Content starts below the top control bar (scenario + sim panel)
_CONTENT_TOP = 0.32


def _print_results(results: list[SimulationResult]):
    print("\n" + "=" * 80)
    print("HASIL SIMULASI vs MODEL MATEMATIKA")
    print("=" * 80)
    print(f"{'No':<4} {'Skenario':<26} {'N':>6} {'Gol':>6} {'Sim%':>8} {'Mat%':>8} {'Dev%':>8}")
    print("-" * 80)
    for i, r in enumerate(results):
        sim = r.simulated_goal_rate * 100
        mat = r.mathematical_goal_rate * 100
        dev = r.deviation * 100
        print(f"{i+1:<4} {r.scenario.name:<26} {r.total_kicks:>6} {r.goals:>6} {sim:>7.2f}% {mat:>7.2f}% {dev:>7.3f}%")
    print("-" * 80)
    print("P(goal) = Sum P(kick=d) x (1 - P(keeper=d))")
    for r in results:
        s = r.scenario
        print(f"\n[{s.name}]")
        print(f"  Ronaldo  : Ki={s.kicker_prob.left:.0%} Te={s.kicker_prob.center:.0%} Ka={s.kicker_prob.right:.0%}")
        print(f"  Courtois : Ki={s.keeper_prob.left:.0%} Te={s.keeper_prob.center:.0%} Ka={s.keeper_prob.right:.0%}")
        kc, gc = r.direction_counts("kicker"), r.direction_counts("keeper")
        for d in Direction:
            kp = kc[d] / r.total_kicks * 100
            gp = gc[d] / r.total_kicks * 100
            print(f"  {d.value:>6}: Tend={kc[d]:>4}({kp:5.1f}%) Kiper={gc[d]:>4}({gp:5.1f}%)")
    print("=" * 80 + "\n")


class StatsDashboard:
    def __init__(self, on_close=None):
        self.root = None
        self._content = None
        self._scroll_y = 0
        self._max_scroll = 0
        self._on_close = on_close

    def show(self, results: list[SimulationResult]):
        self.hide()
        # z=-50 — behind the panels (z=-80) but in front of 3D scene
        self.root = Entity(parent=camera.ui, z=-50)
        self._scroll_y = 0

        # Full-screen black backdrop
        Entity(parent=self.root, model="quad", color=color.black, scale=(2, 2), z=0.5)

        # Scrollable content
        self._content = Entity(parent=self.root, z=-0.5)

        if len(results) == 1:
            self._render_single(results[0])
        else:
            self._render_all(results)

        _print_results(results)

        # Close button — fixed position, always on top
        Button(
            text="Tutup [ESC]", parent=self.root,
            scale=(0.16, 0.045), position=(0, -0.46), z=-1,
            color=color.hex("#1a1a2e"), text_color=color.white,
            on_click=self.hide,
        )

    def scroll(self, amount: float):
        """amount > 0 = reveal content below, amount < 0 = reveal content above."""
        if not self._content or self._max_scroll <= 0:
            return
        self._scroll_y = max(0, min(self._max_scroll, self._scroll_y + amount))
        self._content.y = self._scroll_y

    def _set_max_scroll(self, bottom_y: float):
        visible_bottom = -0.48
        overflow = visible_bottom - bottom_y
        self._max_scroll = max(0, overflow)

    def _render_all(self, results: list[SimulationResult]):
        c = self._content
        y = _CONTENT_TOP

        Text(text="HASIL SIMULASI vs MODEL MATEMATIKA", parent=c,
             position=(0, y), origin=(0, 0), scale=1.3, color=color.hex("#FFD700"))
        y -= 0.04
        Entity(parent=c, model="quad", color=color.hex("#333333"), scale=(1.5, 0.002), position=(0, y))
        y -= 0.03

        # Table headers
        cols = [
            ("No", -0.68), ("Skenario", -0.60), ("N", -0.12),
            ("Gol", 0.00), ("Sim%", 0.12), ("Mat%", 0.26), ("Dev", 0.42),
        ]
        for label, x in cols:
            Text(text=label, parent=c, position=(x, y), scale=0.8, color=color.hex("#888888"))
        y -= 0.03

        for i, r in enumerate(results):
            sim = r.simulated_goal_rate * 100
            mat = r.mathematical_goal_rate * 100
            dev = r.deviation * 100
            dev_col = color.hex("#4ADE80") if dev < 2 else color.hex("#FACC15") if dev < 5 else color.hex("#F87171")

            if i % 2 == 0:
                Entity(parent=c, model="quad", color=color.hex("#0d0d0d"),
                       scale=(1.3, 0.038), position=(-0.05, y), z=0.1)

            row = [
                (f"{i+1}.", -0.68, color.hex("#666666")),
                (r.scenario.name[:24], -0.60, color.hex("#E5E5E5")),
                (str(r.total_kicks), -0.12, color.hex("#CCCCCC")),
                (str(r.goals), 0.00, color.hex("#CCCCCC")),
                (f"{sim:.1f}%", 0.12, color.hex("#60A5FA")),
                (f"{mat:.1f}%", 0.26, color.hex("#FFD700")),
                (f"{dev:.2f}%", 0.42, dev_col),
            ]
            for text, x, clr in row:
                Text(text=text, parent=c, position=(x, y), scale=0.7, color=clr)
            y -= 0.043

        # Bar chart section
        y -= 0.035
        Entity(parent=c, model="quad", color=color.hex("#333333"), scale=(1.3, 0.001), position=(-0.05, y))
        y -= 0.035
        Text(text="Perbandingan Goal Rate (%)", parent=c,
             position=(0, y), origin=(0, 0), scale=1.0, color=color.hex("#E5E5E5"))
        y -= 0.04

        cl, cw = -0.48, 0.65
        for r in results:
            sim = r.simulated_goal_rate * 100
            mat = r.mathematical_goal_rate * 100

            Text(text=r.scenario.name[:15], parent=c,
                 position=(cl - 0.02, y), scale=0.5, color=color.hex("#CCCCCC"), origin=(1, 0))

            sw = (sim / 100) * cw
            Entity(parent=c, model="quad", color=color.hex("#3B82F6"),
                   scale=(sw, 0.015), position=(cl + sw / 2, y + 0.01))
            Text(text=f"{sim:.1f}%", parent=c,
                 position=(cl + sw + 0.01, y + 0.01), scale=0.45, color=color.hex("#60A5FA"))

            mw = (mat / 100) * cw
            Entity(parent=c, model="quad", color=color.hex("#D97706"),
                   scale=(mw, 0.015), position=(cl + mw / 2, y - 0.01))
            Text(text=f"{mat:.1f}%", parent=c,
                 position=(cl + mw + 0.01, y - 0.01), scale=0.45, color=color.hex("#FFD700"))
            y -= 0.05

        y -= 0.01
        Entity(parent=c, model="quad", color=color.hex("#3B82F6"), scale=(0.03, 0.01), position=(cl + 0.15, y))
        Text(text="Simulasi", parent=c, position=(cl + 0.18, y), scale=0.55, color=color.hex("#60A5FA"))
        Entity(parent=c, model="quad", color=color.hex("#D97706"), scale=(0.03, 0.01), position=(cl + 0.38, y))
        Text(text="Matematika", parent=c, position=(cl + 0.42, y), scale=0.55, color=color.hex("#FFD700"))

        y -= 0.035
        Text(text="P(goal) = Sum P(kick=d) x (1 - P(keeper=d))", parent=c,
             position=(0, y), origin=(0, 0), scale=0.6, color=color.hex("#666666"))
        y -= 0.025
        Text(text="[scroll untuk navigasi | data lengkap di console]", parent=c,
             position=(0, y), origin=(0, 0), scale=0.5, color=color.hex("#444444"))

        self._set_max_scroll(y - 0.03)

    def _render_single(self, r: SimulationResult):
        c = self._content
        sim = r.simulated_goal_rate * 100
        mat = r.mathematical_goal_rate * 100
        dev = r.deviation * 100
        s = r.scenario
        y = _CONTENT_TOP

        Text(text=s.name, parent=c, position=(0, y), origin=(0, 0), scale=1.3, color=color.hex("#FFD700"))
        y -= 0.03
        Text(text=s.description, parent=c, position=(0, y), origin=(0, 0), scale=0.75, color=color.hex("#E0E0E0"))
        y -= 0.035
        Entity(parent=c, model="quad", color=color.hex("#333333"), scale=(1.4, 0.002), position=(0, y))
        y -= 0.03

        stats = [
            ("Total Tendangan", str(r.total_kicks), color.hex("#E5E5E5")),
            ("Gol", str(r.goals), color.hex("#4ADE80")),
            ("Diselamatkan", str(r.saves), color.hex("#F87171")),
            ("Sim Goal Rate", f"{sim:.2f}%", color.hex("#60A5FA")),
            ("Math Goal Rate", f"{mat:.2f}%", color.hex("#FFD700")),
            ("Deviasi", f"{dev:.3f}%",
             color.hex("#4ADE80") if dev < 2 else color.hex("#FACC15") if dev < 5 else color.hex("#F87171")),
        ]
        for label, val, vc in stats:
            Text(text=label, parent=c, position=(-0.55, y), scale=0.8, color=color.hex("#AAAAAA"))
            Text(text=val, parent=c, position=(-0.10, y), scale=0.8, color=vc)
            y -= 0.04

        y -= 0.02
        Text(text="Distribusi Probabilitas:", parent=c, position=(-0.55, y), scale=0.8, color=color.hex("#FFD700"))
        y -= 0.035
        Text(text=f"Ronaldo   Ki:{s.kicker_prob.left:.0%}  Te:{s.kicker_prob.center:.0%}  Ka:{s.kicker_prob.right:.0%}",
             parent=c, position=(-0.50, y), scale=0.7, color=color.hex("#CCCCCC"))
        y -= 0.03
        Text(text=f"Courtois  Ki:{s.keeper_prob.left:.0%}  Te:{s.keeper_prob.center:.0%}  Ka:{s.keeper_prob.right:.0%}",
             parent=c, position=(-0.50, y), scale=0.7, color=color.hex("#CCCCCC"))

        y -= 0.045
        Entity(parent=c, model="quad", color=color.hex("#333333"), scale=(1.4, 0.001), position=(0, y))
        y -= 0.03
        Text(text="Distribusi Arah", parent=c, position=(0, y), origin=(0, 0), scale=0.9, color=color.hex("#E5E5E5"))
        y -= 0.04

        kc, gc = r.direction_counts("kicker"), r.direction_counts("keeper")
        bw = 0.45
        for d in Direction:
            kp = kc[d] / r.total_kicks * 100 if r.total_kicks else 0
            gp = gc[d] / r.total_kicks * 100 if r.total_kicks else 0

            Text(text=d.value, parent=c, position=(-0.50, y + 0.01), scale=0.8, color=color.hex("#E5E5E5"))

            kw = (kp / 100) * bw
            Entity(parent=c, model="quad", color=color.hex("#C4161C"),
                   scale=(kw, 0.018), position=(-0.25 + kw / 2, y + 0.018))
            Text(text=f"{kp:.1f}%", parent=c, position=(-0.25 + kw + 0.01, y + 0.018), scale=0.5, color=color.hex("#F87171"))

            gw = (gp / 100) * bw
            Entity(parent=c, model="quad", color=color.hex("#CCFF00"),
                   scale=(gw, 0.018), position=(-0.25 + gw / 2, y - 0.005))
            Text(text=f"{gp:.1f}%", parent=c, position=(-0.25 + gw + 0.01, y - 0.005), scale=0.5, color=color.hex("#CCFF00"))
            y -= 0.065

        y -= 0.01
        Entity(parent=c, model="quad", color=color.hex("#C4161C"), scale=(0.03, 0.01), position=(-0.30, y))
        Text(text="Ronaldo", parent=c, position=(-0.26, y), scale=0.55, color=color.hex("#F87171"))
        Entity(parent=c, model="quad", color=color.hex("#CCFF00"), scale=(0.03, 0.01), position=(-0.05, y))
        Text(text="Courtois", parent=c, position=(-0.01, y), scale=0.55, color=color.hex("#CCFF00"))

        y -= 0.045
        Entity(parent=c, model="quad", color=color.hex("#333333"), scale=(1.4, 0.001), position=(0, y))
        y -= 0.03
        Text(text="Perbandingan Goal Rate", parent=c, position=(0, y), origin=(0, 0), scale=0.9, color=color.hex("#E5E5E5"))
        y -= 0.04

        fw = 0.9
        sw = (sim / 100) * fw
        Entity(parent=c, model="quad", color=color.hex("#3B82F6"),
               scale=(sw, 0.028), position=(-fw / 2 + sw / 2, y))
        Text(text=f"Simulasi: {sim:.2f}%", parent=c, position=(-fw / 2, y + 0.028), scale=0.6, color=color.hex("#60A5FA"))

        mw = (mat / 100) * fw
        Entity(parent=c, model="quad", color=color.hex("#D97706"),
               scale=(mw, 0.028), position=(-fw / 2 + mw / 2, y - 0.04))
        Text(text=f"Matematika: {mat:.2f}%", parent=c, position=(-fw / 2, y - 0.012), scale=0.6, color=color.hex("#FFD700"))

        y -= 0.09
        Text(text="P(goal) = Sum P(kick=d) x (1 - P(keeper=d))", parent=c,
             position=(0, y), origin=(0, 0), scale=0.6, color=color.hex("#666666"))

        self._set_max_scroll(y - 0.03)

    def hide(self):
        if self.root:
            destroy(self.root)
            self.root = None
            self._content = None
            self._scroll_y = 0
            if self._on_close:
                self._on_close()

    @property
    def is_visible(self) -> bool:
        return self.root is not None
