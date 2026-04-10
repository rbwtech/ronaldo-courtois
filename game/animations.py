"""Kick, ball flight, and goalkeeper dive animations."""

import random
from ursina import Entity, Vec3, invoke, curve
from core.models import Direction

RONALDO_ORIGIN = Vec3(0, 0, 2)
KEEPER_ORIGIN = Vec3(0, 0, 13.5)

_GOAL_BASE: dict[Direction, Vec3] = {
    Direction.LEFT:   Vec3(-2.2, 1.0, 14.5),
    Direction.CENTER: Vec3(0.0, 0.8, 14.5),
    Direction.RIGHT:  Vec3(2.2, 1.0, 14.5),
}

_DIVE_BASE: dict[Direction, Vec3] = {
    Direction.LEFT:   Vec3(-1.0, 0, 0),
    Direction.CENTER: Vec3(0, 0, 0),
    Direction.RIGHT:  Vec3(1.0, 0, 0),
}


def _rand_goal_target(d: Direction) -> Vec3:
    """Ball flies into the net. Keeper already dived wrong so no avoidance needed."""
    b = _GOAL_BASE[d]
    return Vec3(b.x + random.uniform(-0.2, 0.2), b.y + random.uniform(-0.1, 0.35), b.z)


def _rand_dive_offset(d: Direction) -> Vec3:
    b = _DIVE_BASE[d]
    return Vec3(b.x + random.uniform(-0.15, 0.15), b.y, 0)


def _save_target(keeper_x: float, dive_dir: Direction) -> Vec3:
    """Ball stops at keeper's upper body, shifted by tilt direction."""
    # 40° tilt shifts upper body ~0.35 further in dive direction
    tilt_offset = {
        Direction.LEFT: -0.8,
        Direction.CENTER: 0,
        Direction.RIGHT: 0.8,
    }[dive_dir]

    return Vec3(
        keeper_x + tilt_offset + random.uniform(-0.08, 0.08),
        random.uniform(0.9, 1.3),
        KEEPER_ORIGIN.z - 0.12,
    )


def _child(entity: Entity, name: str):
    return next((c for c in entity.children if getattr(c, "name", "") == name), None)


def animate_kick(ronaldo: Entity, ball: Entity, kick_dir: Direction,
                 is_goal: bool, keeper_x: float, keeper_dive_dir: Direction) -> float:
    """Run-up, leg swing, ball flight. Returns total duration."""
    leg = _child(ronaldo, "right_leg")

    ronaldo.animate_position(ronaldo.position + Vec3(0, 0, 1.5), duration=0.4, curve=curve.in_out_quad)

    if leg:
        invoke(lambda: leg.animate_rotation(Vec3(-45, 0, 0), duration=0.12, curve=curve.out_quad), delay=0.3)
        invoke(lambda: leg.animate_rotation(Vec3(30, 0, 0), duration=0.1, curve=curve.in_quad), delay=0.42)
        invoke(lambda: leg.animate_rotation(Vec3(0, 0, 0), duration=0.2), delay=0.55)

    if is_goal:
        target, dur, c = _rand_goal_target(kick_dir), 0.55, curve.out_quad
    else:
        target, dur, c = _save_target(keeper_x, keeper_dive_dir), 0.42, curve.out_cubic

    invoke(lambda: ball.animate_position(target, duration=dur, curve=c), delay=0.45)
    return 1.1


def animate_keeper_dive(courtois: Entity, dive_dir: Direction) -> tuple[Vec3, float]:
    """Dive animation. Returns (offset, final_x) for save interception."""
    offset = _rand_dive_offset(dive_dir)
    pos = KEEPER_ORIGIN + offset
    final_x = pos.x

    if dive_dir != Direction.CENTER:
        pos = Vec3(pos.x, pos.y - 0.25, pos.z)

    invoke(lambda: courtois.animate_position(pos, duration=0.45, curve=curve.out_quad), delay=0.30)

    if dive_dir == Direction.LEFT:
        invoke(lambda: courtois.animate_rotation(Vec3(0, 180, 40), duration=0.4, curve=curve.out_quad), delay=0.30)
    elif dive_dir == Direction.RIGHT:
        invoke(lambda: courtois.animate_rotation(Vec3(0, 180, -40), duration=0.4, curve=curve.out_quad), delay=0.30)
    else:
        invoke(lambda: courtois.animate_position(Vec3(pos.x, -0.15, pos.z), duration=0.35, curve=curve.out_quad), delay=0.30)

    return offset, final_x


def reset_entities(ronaldo: Entity, courtois: Entity, ball: Entity):
    ronaldo.position = RONALDO_ORIGIN
    ronaldo.rotation = Vec3(0, 0, 0)
    courtois.position = KEEPER_ORIGIN
    courtois.rotation = Vec3(0, 180, 0)
    ball.reset()
    for e in (ronaldo, courtois):
        for c in e.children:
            c.rotation = Vec3(0, 0, 0)
