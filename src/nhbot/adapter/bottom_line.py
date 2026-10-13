"""The hero's status values, as on the two bottom lines of the screen."""

from dataclasses import dataclass


@dataclass(frozen=True)
class BottomLine:
    # The field order is the NLE blstats order. ObservationReader depends on it.
    x: int
    y: int
    strength: int
    strength_with_percentile: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    score: int
    hit_points: int
    max_hit_points: int
    depth: int
    gold: int
    energy: int
    max_energy: int
    armor_class: int
    monster_level: int
    experience_level: int
    experience_points: int
    turn: int
    hunger_state: int
    carrying_capacity: int
    dungeon_number: int
    level_number: int
    conditions: int
    alignment: int
