# -*- coding: utf-8 -*-
"""
Pollen definitions and concentration-level handling.
"""

from dataclasses import dataclass


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

    "alder_pollen": PollenDefinition(
        key="alder_pollen",
        thresholds=(16.0, 50.0),
        label_key="alder_pollen",
    ),

    "birch_pollen": PollenDefinition(
        key="birch_pollen",
        thresholds=(16.0, 50.0),
        label_key="birch_pollen",
    ),

    "grass_pollen": PollenDefinition(
        key="grass_pollen",
        thresholds=(10.0, 30.0),
        label_key="grass_pollen",
    ),

    "mugwort_pollen": PollenDefinition(
        key="mugwort_pollen",
        thresholds=(5.0, 25.0),
        label_key="mugwort_pollen",
    ),

    "olive_pollen": PollenDefinition(
        key="olive_pollen",
        thresholds=(5.0, 25.0),
        label_key="olive_pollen",
    ),

    "ragweed_pollen": PollenDefinition(
        key="ragweed_pollen",
        thresholds=(5.0, 25.0),
        label_key="ragweed_pollen",
    ),
}


REQUESTED_POLLEN = tuple(
    KNOWN_POLLEN.keys()
)


DEFAULT_UNKNOWN_THRESHOLDS = (
    5.0,
    25.0,
)


def get_definition(
    pollen_key,
):

    definition = KNOWN_POLLEN.get(
        pollen_key
    )

    if definition is not None:
        return definition

    return PollenDefinition(
        key=pollen_key,
        thresholds=DEFAULT_UNKNOWN_THRESHOLDS,
        label_key="unknown_pollen",
    )


def is_pollen_key(
    key,
):

    return (
        isinstance(key, str)
        and key.endswith("_pollen")
    )


def level_for(
    pollen_key,
    concentration,
):

    # 0 = no data
    if concentration is None:
        return 0

    try:

        concentration = float(
            concentration
        )

    except (
        TypeError,
        ValueError,
    ):

        return 0

    # < 1.0 = none
    if concentration < 1.0:
        return 1

    definition = get_definition(
        pollen_key
    )

    # Low
    if concentration <= definition.low_max:
        return 2

    # Medium
    if concentration <= definition.medium_max:
        return 3

    # High
    return 4
