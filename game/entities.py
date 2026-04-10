"""3D entities for Ronaldo (kicker) and Courtois (goalkeeper)."""

from ursina import Entity, color, Vec3


class Ball(Entity):
    """Football with texture applied for visibility against any background."""

    PENALTY_SPOT = Vec3(0, 0.2, 4)

    def __init__(self):
        super().__init__(
            model="sphere",
            color=color.hex("#e6e6e6"),
            texture="assets/ball_texture.png",
            scale=0.22,
            position=self.PENALTY_SPOT,
        )

    def reset(self):
        self.position = self.PENALTY_SPOT
        self.visible = True


def _build_humanoid(pos: Vec3, body_color, shorts_color, sock_color, name: str) -> Entity:
    """Build a stylized humanoid from primitives."""
    root = Entity(position=pos, name=name)

    Entity(
        parent=root, model="cube", color=body_color,
        scale=(0.5, 0.6, 0.3), position=(0, 1.3, 0),
        name="torso",
    )
    Entity(
        parent=root, model="sphere", color=color.hex("#D2A67D"),
        scale=0.3, position=(0, 1.85, 0),
        name="head",
    )
    Entity(
        parent=root, model="cube", color=shorts_color,
        scale=(0.5, 0.3, 0.3), position=(0, 0.9, 0),
        name="shorts",
    )
    Entity(
        parent=root, model="cube", color=sock_color,
        scale=(0.15, 0.5, 0.15), position=(-0.15, 0.45, 0),
        name="left_leg",
    )
    Entity(
        parent=root, model="cube", color=sock_color,
        scale=(0.15, 0.5, 0.15), position=(0.15, 0.45, 0),
        name="right_leg",
    )
    Entity(
        parent=root, model="cube", color=body_color,
        scale=(0.12, 0.45, 0.12), position=(-0.35, 1.3, 0),
        name="left_arm",
    )
    Entity(
        parent=root, model="cube", color=body_color,
        scale=(0.12, 0.45, 0.12), position=(0.35, 1.3, 0),
        name="right_arm",
    )

    return root


def build_ronaldo() -> Entity:
    return _build_humanoid(
        pos=Vec3(0, 0, 2),
        body_color=color.hex("#C4161C"),
        shorts_color=color.hex("#1B4D3E"),
        sock_color=color.hex("#C4161C"),
        name="ronaldo",
    )


def build_courtois() -> Entity:
    entity = _build_humanoid(
        pos=Vec3(0, 0, 13.5),
        body_color=color.hex("#CCFF00"),
        shorts_color=color.hex("#1a1a1a"),
        sock_color=color.hex("#1a1a1a"),
        name="courtois",
    )
    entity.rotation_y = 180
    return entity
