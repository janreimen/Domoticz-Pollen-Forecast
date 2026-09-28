# -*- coding: utf-8 -*-
"""
Domoticz device handling for the Pollen Forecast plugin.

One native Domoticz Alert device is created for each pollen species
and each forecast day.

Device model:

    Unit 1  = Alder Today
    Unit 2  = Alder Tomorrow
    Unit 3  = Birch Today
    Unit 4  = Birch Tomorrow
    ...

The Alert device nValue represents the pollen level:

    0 = No data
    1 = None
    2 = Low
    3 = Medium
    4 = High

Domoticz renders these values using its native Alert colors.
"""

import Domoticz

from pollen import get_definition, level_for
from translations import get_translation


class PollenDevices:

    # ------------------------------------------------------------------
    # Device layout
    # ------------------------------------------------------------------

    DAYS = (
        "today",
        "tomorrow",
    )

    def __init__(
        self,
        devices,
        language,
        debug=False,
        log_fn=None,
    ):

        self.devices = devices
        self.language = language
        self.translation = get_translation(
            language
        )
        self.debug = debug
        self.log_fn = log_fn

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Device creation
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Update all forecast devices
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Pollen definitions
    # ------------------------------------------------------------------

    @staticmethod
    def _pollen_keys():

        return (
            "alder_pollen",
            "birch_pollen",
            "grass_pollen",
            "mugwort_pollen",
            "olive_pollen",
            "ragweed_pollen",
        )

    # ------------------------------------------------------------------
    # Device naming
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Unit mapping
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Level text
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Domoticz update
    # ------------------------------------------------------------------

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
