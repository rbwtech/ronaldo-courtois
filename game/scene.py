"""3D scene — pitch, goal, markings, stadium, and environment."""

import math
import random
from ursina import Entity, DirectionalLight, AmbientLight, Sky, color, Vec3, camera


def build_pitch() -> Entity:
    return Entity(
        model="plane", scale=(40, 1, 50),
        color=color.hex("#2d8a4e"),
        texture="assets/grass_texture.png",
        texture_scale=(6, 8),
    )


def build_goal() -> list[Entity]:
    post_col = color.white
    net_col = color.rgba(200, 200, 200, 100)
    gz, gw, gh, pr, nd = 14, 5.5, 2.2, 0.08, 1.2
    hw = gw / 2
    parts = []

    for x in (-hw, hw):
        parts.append(Entity(model="cube", color=post_col, scale=(pr, gh, pr), position=(x, gh / 2, gz)))

    parts.append(Entity(model="cube", color=post_col, scale=(gw + pr * 2, pr * 2, pr * 2), position=(0, gh, gz)))

    net_cfg = [
        ((gw, gh, 0.02),  (0, gh / 2, gz + nd),       (8, 4)),
        ((gw, 0.02, nd),  (0, gh, gz + nd / 2),        (8, 2)),
        ((0.02, gh, nd),  (-hw, gh / 2, gz + nd / 2),  (2, 4)),
        ((0.02, gh, nd),  (hw, gh / 2, gz + nd / 2),   (2, 4)),
    ]
    for sc, pos, ts in net_cfg:
        parts.append(Entity(
            model="cube", color=net_col,
            texture="assets/net_texture.png", texture_scale=ts,
            scale=sc, position=pos,
        ))

    return parts


def build_markings() -> list[Entity]:
    lc = color.rgba(255, 255, 255, 200)
    thin = 0.06
    parts = []

    # Goal line (full width of pitch)
    parts.append(Entity(model="cube", color=lc, scale=(40, 0.01, thin), position=(0, 0.005, 14)))

    # Penalty area box — side lines go from goal line (z=14) down to z=2
    bw, bd = 12, 12
    parts.append(Entity(model="cube", color=lc, scale=(thin, 0.01, bd), position=(-bw / 2, 0.005, 14 - bd / 2)))
    parts.append(Entity(model="cube", color=lc, scale=(thin, 0.01, bd), position=(bw / 2, 0.005, 14 - bd / 2)))
    parts.append(Entity(model="cube", color=lc, scale=(bw, 0.01, thin), position=(0, 0.005, 14 - bd)))

    # Six-yard box
    sw, sd = 6, 4
    parts.append(Entity(model="cube", color=lc, scale=(thin, 0.01, sd), position=(-sw / 2, 0.005, 14 - sd / 2)))
    parts.append(Entity(model="cube", color=lc, scale=(thin, 0.01, sd), position=(sw / 2, 0.005, 14 - sd / 2)))
    parts.append(Entity(model="cube", color=lc, scale=(sw, 0.01, thin), position=(0, 0.005, 14 - sd)))

    # Penalty spot
    parts.append(Entity(model="sphere", color=color.white, scale=0.1, position=(0, 0.02, 4)))

    # Penalty arc
    arc_r = 3.5
    for i in range(40):
        a = math.radians(-70 + i * (140 / 39))
        x = arc_r * math.sin(a)
        z = 4 + arc_r * math.cos(a)
        if z < 2:
            parts.append(Entity(model="sphere", color=lc, scale=0.04, position=(x, 0.006, z)))

    # Touchlines (full-length sidelines)
    pitch_len = 40
    parts.append(Entity(model="cube", color=lc, scale=(thin, 0.01, pitch_len), position=(-15, 0.005, 14 - pitch_len / 2)))
    parts.append(Entity(model="cube", color=lc, scale=(thin, 0.01, pitch_len), position=(15, 0.005, 14 - pitch_len / 2)))

    # Halfway line
    parts.append(Entity(model="cube", color=lc, scale=(30, 0.01, thin), position=(0, 0.005, -6)))

    # Center circle
    cc_r = 4
    for i in range(48):
        a = math.radians(i * (360 / 48))
        parts.append(Entity(model="sphere", color=lc, scale=0.04, position=(cc_r * math.cos(a), 0.006, -6 + cc_r * math.sin(a))))

    parts.append(Entity(model="sphere", color=color.white, scale=0.1, position=(0, 0.02, -6)))

    return parts


def _crowd_dots(x_range, y_range, z, count, face="back") -> list[Entity]:
    """Scatter colored dots to simulate spectators on a stand."""
    crowd_colors = [
        "#c4161c", "#e8e8e8", "#1a3a5c", "#FFD700",
        "#ff6b6b", "#4ecdc4", "#f5f5f5", "#2a4a6a",
    ]
    dots = []
    for _ in range(count):
        cx = random.uniform(*x_range)
        cy = random.uniform(*y_range)
        cz = z if face == "back" else random.uniform(*z) if isinstance(z, tuple) else z
        c = color.hex(random.choice(crowd_colors))

        if face == "back":
            dots.append(Entity(model="cube", color=c, scale=(0.3, 0.3, 0.05), position=(cx, cy, cz)))
        elif face == "left":
            dots.append(Entity(model="cube", color=c, scale=(0.05, 0.3, 0.3), position=(cx, cy, cz)))
        elif face == "right":
            dots.append(Entity(model="cube", color=c, scale=(0.05, 0.3, 0.3), position=(cx, cy, cz)))

    return dots


def build_stadium() -> list[Entity]:
    parts = []
    stand_col = color.hex("#2a2a3e")

    # Back stand (behind goal)
    parts.append(Entity(model="cube", color=stand_col, scale=(38, 10, 4), position=(0, 5, 21)))
    parts += _crowd_dots((-17, 17), (1.5, 9), 18.9, 250, "back")

    # Left stand
    parts.append(Entity(model="cube", color=stand_col, scale=(4, 8, 45), position=(-18, 4, -3)))
    parts += _crowd_dots((-16.1, -16.1), (1.5, 7), (-24, 18), 200, "left")

    # Right stand
    parts.append(Entity(model="cube", color=stand_col, scale=(4, 8, 45), position=(18, 4, -3)))
    parts += _crowd_dots((16.1, 16.1), (1.5, 7), (-24, 18), 200, "right")

    # Behind camera stand
    parts.append(Entity(model="cube", color=stand_col, scale=(38, 8, 4), position=(0, 4, -24)))
    parts += _crowd_dots((-17, 17), (1.5, 7), -21.9, 200, "back")

    # Perimeter wall
    wall_col = color.hex("#444444")
    wh = 0.8
    parts.append(Entity(model="cube", color=wall_col, scale=(38, wh, 0.12), position=(0, wh / 2, 17)))
    parts.append(Entity(model="cube", color=wall_col, scale=(0.12, wh, 45), position=(-15.5, wh / 2, -3)))
    parts.append(Entity(model="cube", color=wall_col, scale=(0.12, wh, 45), position=(15.5, wh / 2, -3)))

    # Floodlight towers — 4 corners, tall + bright
    tower_col = color.hex("#666666")
    light_col = color.hex("#FFFFEE")
    glow_col = color.rgba(255, 255, 220, 60)
    corners = [(-17, 19), (17, 19), (-17, -22), (17, -22)]
    for tx, tz in corners:
        # Tower pole
        parts.append(Entity(model="cube", color=tower_col, scale=(0.4, 18, 0.4), position=(tx, 9, tz)))
        # Light panel
        parts.append(Entity(model="cube", color=light_col, scale=(2.5, 0.5, 2.5), position=(tx, 18, tz)))
        # Light glow effect
        parts.append(Entity(model="cube", color=glow_col, scale=(4, 0.1, 4), position=(tx, 17.8, tz)))

    return parts


def build_ad_boards() -> list[Entity]:
    board_col = color.hex("#0f3460")
    accent_col = color.hex("#c4161c")
    parts = []

    for x_off in range(-12, 13, 4):
        c = accent_col if abs(x_off) < 5 else board_col
        parts.append(Entity(model="cube", color=c, scale=(3.8, 0.7, 0.08), position=(x_off, 0.35, 16.5)))

    for z_off in range(-15, 16, 4):
        parts.append(Entity(model="cube", color=board_col, scale=(0.08, 0.7, 3.8), position=(-14.8, 0.4, z_off)))
        parts.append(Entity(model="cube", color=board_col, scale=(0.08, 0.7, 3.8), position=(14.8, 0.4, z_off)))

    return parts


def setup_lighting():
    sun = DirectionalLight(y=14, rotation=(30, -25, 0))
    sun.color = color.rgb(255, 255, 250)

    fill = DirectionalLight(y=10, rotation=(45, 50, 0))
    fill.color = color.rgb(220, 230, 245)

    ambient = AmbientLight(color=color.rgba(200, 210, 225, 150))
    return sun, fill, ambient


def setup_camera():
    camera.position = Vec3(0, 4.5, -5)
    camera.rotation_x = 12
    camera.fov = 65


def build_scene() -> dict:
    pitch = build_pitch()
    goal = build_goal()
    markings = build_markings()
    stadium = build_stadium()
    ad_boards = build_ad_boards()
    lights = setup_lighting()
    sky = Sky(color=color.hex("#5b7fbf"))
    setup_camera()

    return {
        "pitch": pitch, "goal": goal, "markings": markings,
        "stadium": stadium, "ad_boards": ad_boards, "sky": sky,
    }
