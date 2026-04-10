"""UI panels — direction buttons, scenario selector, and simulation controls."""

from __future__ import annotations
from ursina import Entity, Text, Button, color, destroy, camera
from core.models import Direction
from core.distributions import SCENARIOS


class DirectionPanel:
    def __init__(self, on_select):
        self.on_select = on_select
        self.root = Entity(parent=camera.ui)

        btn_data = [
            ("[1] Kiri", Direction.LEFT, -0.22),
            ("[2] Tengah", Direction.CENTER, 0.0),
            ("[3] Kanan", Direction.RIGHT, 0.22),
        ]

        self.buttons = []
        for label, direction, x_pos in btn_data:
            btn = Button(
                text=label, parent=self.root,
                scale=(0.18, 0.06), position=(x_pos, -0.42),
                color=color.hex("#1a1a2e"),
                highlight_color=color.hex("#16213e"),
                pressed_color=color.hex("#0f3460"),
                text_color=color.white,
                on_click=lambda d=direction: self._handle_click(d),
            )
            self.buttons.append(btn)

    def _handle_click(self, d: Direction):
        self.on_select(d)

    def set_enabled(self, enabled: bool):
        for btn in self.buttons:
            btn.disabled = not enabled
            btn.color = color.hex("#1a1a2e") if enabled else color.hex("#444444")


class ScenarioSelector:
    def __init__(self, on_change):
        self.on_change = on_change
        self.current_index = 0
        # z=-80 ensures this renders on top of dashboard (z=-50)
        self.root = Entity(parent=camera.ui, z=-80)

        # Dark header background behind controls
        Entity(parent=self.root, model="quad", color=color.hex("#0a0a14"),
               scale=(2, 0.14), position=(0, 0.44), z=0.1)

        Text(text="Skenario:", parent=self.root, position=(-0.72, 0.47), scale=0.8, color=color.white)

        self.name_text = Text(
            text=SCENARIOS[0].name, parent=self.root,
            position=(-0.72, 0.43), scale=1.0, color=color.hex("#FFD700"),
        )
        self.desc_text = Text(
            text=SCENARIOS[0].description, parent=self.root,
            position=(-0.72, 0.39), scale=0.7, color=color.hex("#E0E0E0"),
        )

        Button(text="Prev", parent=self.root, scale=(0.06, 0.035), position=(-0.55, 0.47),
               color=color.hex("#1a1a2e"), text_color=color.white, on_click=self._prev)
        Button(text="Next", parent=self.root, scale=(0.06, 0.035), position=(-0.48, 0.47),
               color=color.hex("#1a1a2e"), text_color=color.white, on_click=self._next)

    def _prev(self):
        self.current_index = (self.current_index - 1) % len(SCENARIOS)
        self._update()

    def _next(self):
        self.current_index = (self.current_index + 1) % len(SCENARIOS)
        self._update()

    def _update(self):
        s = SCENARIOS[self.current_index]
        self.name_text.text = s.name
        self.desc_text.text = s.description
        self.on_change(s)

    @property
    def selected(self):
        return SCENARIOS[self.current_index]


class SimulationPanel:
    def __init__(self, on_run_single, on_run_all):
        self.on_run_single = on_run_single
        self.on_run_all = on_run_all
        # z=-80 to stay on top of dashboard
        self.root = Entity(parent=camera.ui, z=-80)
        self.n_kicks = 1000

        Text(text="Simulasi Batch", parent=self.root, position=(0.50, 0.47),
             scale=0.9, color=color.white, origin=(0, 0))

        counts = [100, 500, 1000, 5000]
        for i, n in enumerate(counts):
            Button(
                text=str(n), parent=self.root,
                scale=(0.07, 0.035), position=(0.38 + i * 0.085, 0.42),
                color=color.hex("#1a1a2e") if n != 1000 else color.hex("#0f3460"),
                text_color=color.white,
                on_click=lambda val=n: self._set_n(val),
                name=f"n_btn_{n}",
            )

        Button(
            text="Skenario Ini", parent=self.root,
            scale=(0.18, 0.045), position=(0.42, 0.355),
            color=color.hex("#0f3460"), highlight_color=color.hex("#1a4a8a"),
            text_color=color.white, on_click=self._run_single,
        )

        Button(
            text="Semua", parent=self.root,
            scale=(0.12, 0.045), position=(0.60, 0.355),
            color=color.hex("#C4161C"), highlight_color=color.hex("#e63946"),
            text_color=color.white, on_click=self._run_all,
        )

    def _set_n(self, n: int):
        self.n_kicks = n
        for child in self.root.children:
            if hasattr(child, "name") and child.name.startswith("n_btn_"):
                val = int(child.name.split("_")[-1])
                child.color = color.hex("#0f3460") if val == n else color.hex("#1a1a2e")

    def _run_single(self):
        self.on_run_single(self.n_kicks)

    def _run_all(self):
        self.on_run_all(self.n_kicks)


class ResultBanner:
    def __init__(self):
        self.text_entity = Text(text="", scale=3, origin=(0, 0), position=(0, 0.15),
                                color=color.white, visible=False)

    def show_goal(self):
        self.text_entity.text = "GOAL!"
        self.text_entity.color = color.hex("#00FF88")
        self.text_entity.visible = True

    def show_save(self):
        self.text_entity.text = "SAVED!"
        self.text_entity.color = color.hex("#FF4444")
        self.text_entity.visible = True

    def hide(self):
        self.text_entity.visible = False
