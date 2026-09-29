# -*- coding: utf-8 -*-
"""
Domoticz device handling for the Pollen Forecast plugin.

One native Domoticz Alert device is created for each selected pollen
species and each forecast day.

When more than one allergen is selected, two additional Alert devices
are created for the aggregated pollen level:

    Selected Pollen Today
    Selected Pollen Tomorrow

The aggregate level is calculated from the individual pollen nValues:

    average = sum(nValues) / number of selected allergens

The average is rounded using normal half-up rounding:

    fraction < 0.50  -> round down
    fraction >= 0.50 -> round up

Device mapping for individual pollen:

    Alder Today
    Alder Tomorrow
    Birch Today
    Birch Tomorrow
    ...

Alert values:

    0 = No data
    1 = None
    2 = Low
    3 = Medium
    4 = High
"""

import math

import Domoticz

from pollen import (
    KNOWN_POLLEN,
    get_definition,
    level_for,
)
from translations import get_translation


class PollenDevices:

    DAYS = (
        "today",
        "tomorrow",
    )

    AGGREGATE_UNIT_START = 100

    def __init__(
        self,
        devices,
        language,
        selected_allergens,
        debug=False,
        log_fn=None,
    ):

        self.devices = devices
        self.language = language
        self.translation = get_translation(
            language
        )
        self.selected_allergens = tuple(
            selected_allergens
        )
        self.debug = debug
        self.log_fn = log_fn

    def log(
        self,
        message,
    ):

        if self.debug and self.log_fn:

            self.log_fn(
                "Devices: {}".format(
                    message
                )
            )

    def create(self):

        unit = 1

        for pollen_key in self._pollen_keys():

            for day in self.DAYS:

                name = self._device_name(
                    pollen_key,
                    day,
                )

                self._create_if_missing(
                    unit,
                    name,
                )

                unit += 1

        if self._has_aggregate():

            self._create_if_missing(
                self._aggregate_unit("today"),
                self._aggregate_device_name("today"),
            )

            self._create_if_missing(
                self._aggregate_unit("tomorrow"),
                self._aggregate_device_name("tomorrow"),
            )

    def _create_if_missing(
        self,
        unit,
        name,
    ):

        if unit in self.devices:
            return

        Domoticz.Device(
            Name=name,
            Unit=unit,
            TypeName="Alert",
            Used=1,
        ).Create()

        self.log(
            "Created device {}: {}".format(
                unit,
                name,
            )
        )

    def update_days(
        self,
        days,
    ):

        if len(days) < 2:
            raise ValueError(
                "Need today and tomorrow forecast data"
            )

        self.update_day(
            day=days[0],
            day_name="today",
        )

        self.update_day(
            day=days[1],
            day_name="tomorrow",
        )

    def update_day(
        self,
        day,
        day_name,
    ):

        if day_name not in self.DAYS:
            raise ValueError(
                "Unsupported forecast day: {}".format(
                    day_name
                )
            )

        levels = {}

        for pollen_key in self._pollen_keys():

            concentration = day[
                "values"
            ].get(
                pollen_key
            )

            level = level_for(
                pollen_key,
                concentration,
            )

            levels[pollen_key] = level

            unit = self._unit_for(
                pollen_key,
                day_name,
            )

            self._update(
                unit=unit,
                nvalue=level,
                svalue=self._level_text(
                    level
                ),
            )

            self.log(
                "{} {}: concentration={} "
                "level={} ({})".format(
                    day_name,
                    pollen_key,
                    concentration,
                    level,
                    self._level_text(level),
                )
            )

        if self._has_aggregate():

            aggregate_level = self._aggregate_level(
                levels
            )

            self._update(
                unit=self._aggregate_unit(
                    day_name
                ),
                nvalue=aggregate_level,
                svalue=self._level_text(
                    aggregate_level
                ),
            )

            self.log(
                "{} aggregate: allergens={} "
                "level={} ({})".format(
                    day_name,
                    ", ".join(
                        self.selected_allergens
                    ),
                    aggregate_level,
                    self._level_text(
                        aggregate_level
                    ),
                )
            )

    @staticmethod
    def _pollen_keys():

        return tuple(
            "{}_pollen".format(
                allergen
            )
            for allergen in KNOWN_POLLEN.keys()
        )

    def _selected_pollen_keys(self):

        return tuple(
            "{}_pollen".format(
                allergen
            )
            for allergen in self.selected_allergens
        )

    def _has_aggregate(self):

        return len(
            self.selected_allergens
        ) > 1

    def _aggregate_level(
        self,
        levels,
    ):

        selected_levels = [
            levels.get(
                pollen_key,
                0,
            )
            for pollen_key
            in self._selected_pollen_keys()
        ]

        if not selected_levels:
            return 0

        average = (
            sum(selected_levels)
            / len(selected_levels)
        )

        # Explicit half-up rounding:
        #
        # 1.49 -> 1
        # 1.50 -> 2
        # 1.51 -> 2
        return int(
            math.floor(
                average + 0.5
            )
        )

    def _device_name(
        self,
        pollen_key,
        day_name,
    ):

        labels = self.translation[
            "pollen"
        ]

        pollen_label = labels.get(
            pollen_key,
            get_definition(
                pollen_key
            ).key,
        )

        if day_name == "today":

            suffix = self.translation[
                "today"
            ]

        else:

            suffix = self.translation[
                "tomorrow"
            ]

        return "{} {}".format(
            pollen_label,
            suffix,
        )

    def _aggregate_device_name(
        self,
        day_name,
    ):

        if day_name == "today":

            suffix = self.translation[
                "today"
            ]

        else:

            suffix = self.translation[
                "tomorrow"
            ]

        return "{} {}".format(
            self.translation[
                "selected_pollen"
            ],
            suffix,
        )

    def _unit_for(
        self,
        pollen_key,
        day_name,
    ):

        keys = self._pollen_keys()

        try:

            pollen_index = keys.index(
                pollen_key
            )

        except ValueError:

            raise ValueError(
                "Unknown pollen key: {}".format(
                    pollen_key
                )
            )

        day_index = self.DAYS.index(
            day_name
        )

        return (
            pollen_index * 2
            + day_index
            + 1
        )

    def _aggregate_unit(
        self,
        day_name,
    ):

        day_index = self.DAYS.index(
            day_name
        )

        return (
            self.AGGREGATE_UNIT_START
            + day_index
        )

    def _level_text(
        self,
        level,
    ):

        return self.translation[
            "levels"
        ].get(
            level,
            self.translation[
                "no_data"
            ],
        )

    def _update(
        self,
        unit,
        nvalue,
        svalue,
    ):

        if unit not in self.devices:
            return

        device = self.devices[
            unit
        ]

        if (
            device.nValue != nvalue
            or device.sValue != svalue
        ):

            device.Update(
                nValue=nvalue,
                sValue=svalue,
            )
