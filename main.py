"""
Penalty Kick Simulator — Ronaldo vs Courtois
3D interactive simulation with probability analysis.
"""

from ursina import Ursina, window, color, invoke

from core.models import Direction
from core.distributions import SCENARIOS
from core.simulator import run_simulation, run_all_scenarios

from game.scene import build_scene
from game.entities import Ball, build_ronaldo, build_courtois
from game.state import GameState, GamePhase

from ui.panels import DirectionPanel, ScenarioSelector, SimulationPanel, ResultBanner
from ui.dashboard import StatsDashboard


app = Ursina(
    title="Penalty Simulator - Ronaldo vs Courtois",
    borderless=False, fullscreen=False,
    size=(1280, 720), development_mode=False,
)

window.color = color.hex("#0a0a14")
window.fps_counter.enabled = False

try:
    from panda3d.core import WindowProperties, Filename
    wp = WindowProperties()
    wp.setIconFilename(Filename.fromOsSpecific("assets/icon.ico"))
    base.win.requestProperties(wp)
except Exception:
    pass


scene_refs = build_scene()
ball = Ball()
ronaldo = build_ronaldo()
courtois = build_courtois()
banner = ResultBanner()


def _on_dashboard_close():
    direction_panel.root.visible = True
    direction_panel.set_enabled(True)


dashboard = StatsDashboard(on_close=_on_dashboard_close)


def on_kick_result(result):
    if result.is_goal:
        banner.show_goal()
    else:
        banner.show_save()
    invoke(reset_for_next_kick, delay=1.8)


def reset_for_next_kick():
    banner.hide()
    game_state.reset()
    direction_panel.set_enabled(True)


game_state = GameState(ronaldo, courtois, ball, on_result_callback=on_kick_result)
game_state.set_scenario(SCENARIOS[0])


def on_direction_selected(direction: Direction):
    if dashboard.is_visible or game_state.phase != GamePhase.IDLE:
        return
    direction_panel.set_enabled(False)
    game_state.execute_kick(direction)


def on_scenario_changed(scenario):
    game_state.set_scenario(scenario)


def on_run_single(n_kicks: int):
    scenario = scenario_selector.selected
    result = run_simulation(scenario, n=n_kicks)
    direction_panel.root.visible = False
    dashboard.show([result])


def on_run_all(n_kicks: int):
    results = run_all_scenarios(SCENARIOS, n=n_kicks)
    direction_panel.root.visible = False
    dashboard.show(results)


direction_panel = DirectionPanel(on_select=on_direction_selected)
scenario_selector = ScenarioSelector(on_change=on_scenario_changed)
sim_panel = SimulationPanel(on_run_single=on_run_single, on_run_all=on_run_all)


_SCROLL_STEP = 0.06

def input(key):
    if dashboard.is_visible:
        if key == "escape":
            dashboard.hide()
        # Wheel down (toward user) = scroll down = see content below = positive
        elif key == "scroll down":
            dashboard.scroll(_SCROLL_STEP)
        # Wheel up (away from user) = scroll up = see content above = negative
        elif key == "scroll up":
            dashboard.scroll(-_SCROLL_STEP)
        return

    if game_state.phase != GamePhase.IDLE:
        return

    key_map = {"1": Direction.LEFT, "2": Direction.CENTER, "3": Direction.RIGHT}
    if key in key_map:
        on_direction_selected(key_map[key])


app.run()
