# -*- coding: utf-8 -*-
"""Pollen definitions and concentration-level handling."""

from dataclasses import dataclass

ALLERGENS = (
    "alder", "birch", "grass", "mugwort", "olive", "ragweed",
)
POLLEN_KEYS = tuple("{}_pollen".format(a) for a in ALLERGENS)
DEFAULT_UNKNOWN_THRESHOLDS = (5.0, 25.0)

@dataclass(frozen=True)
class PollenDefinition:
    key: str
    thresholds: tuple
    label_key: str

    @property
    def low_max(self):
        return self.thresholds[0]

    @property
    def medium_max(self):
        return self.thresholds[1]

KNOWN_POLLEN = {
    "alder_pollen": PollenDefinition("alder_pollen", (16.0, 50.0), "alder_pollen"),
    "birch_pollen": PollenDefinition("birch_pollen", (16.0, 50.0), "birch_pollen"),
    "grass_pollen": PollenDefinition("grass_pollen", (10.0, 30.0), "grass_pollen"),
    "mugwort_pollen": PollenDefinition("mugwort_pollen", (5.0, 25.0), "mugwort_pollen"),
    "olive_pollen": PollenDefinition("olive_pollen", (5.0, 25.0), "olive_pollen"),
    "ragweed_pollen": PollenDefinition("ragweed_pollen", (5.0, 25.0), "ragweed_pollen"),
}
REQUESTED_POLLEN = POLLEN_KEYS


def pollen_key_for_allergen(allergen):
    return "{}_pollen".format(allergen)


def get_definition(pollen_key):
    return KNOWN_POLLEN.get(
        pollen_key,
        PollenDefinition(pollen_key, DEFAULT_UNKNOWN_THRESHOLDS, "unknown_pollen"),
    )


def is_pollen_key(key):
    return isinstance(key, str) and key.endswith("_pollen")


def level_for(pollen_key, concentration):
    if concentration is None:
        return 0
    try:
        concentration = float(concentration)
    except (TypeError, ValueError):
        return 0
    if concentration < 1.0:
        return 1
    definition = get_definition(pollen_key)
    if concentration <= definition.low_max:
        return 2
    if concentration <= definition.medium_max:
        return 3
    return 4
