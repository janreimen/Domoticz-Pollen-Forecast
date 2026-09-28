# -*- coding: utf-8 -*-
"""
Domoticz device handling for the Pollen Forecast plugin.
"""

import Domoticz

from pollen import (
    get_definition,
    level_for,
)
from translations import get_translation


class PollenDevices:

    ALERT_TODAY = 1
    ALERT_TOMORROW = 2
    TEXT_TODAY = 3
    TEXT_TOMORROW = 4

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

        t = self.translation

        self._create_if_missing(
            self.ALERT_TODAY,
            t["device_alert_today"],
            "Alert",
        )

        self._create_if_missing(
            self.ALERT_TOMORROW,
            t["device_alert_tomorrow"],
            "Alert",
        )

        self._create_if_missing(
            self.TEXT_TODAY,
            t["device_today"],
            "Text",
        )

        self._create_if_missing(
            self.TEXT_TOMORROW,
            t["device_tomorrow"],
            "Text",
        )

    def _create_if_missing(
        self,
        unit,
        name,
        type_name,
    ):

        if unit not in self.devices:

            Domoticz.Device(
                Name=name,
                Unit=unit,
                TypeName=type_name,
                Used=1,
            ).Create()

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update_day(
        self,
        alert_unit,
        text_unit,
        day,
    ):

        levels = {}

        for (
            pollen_key,
            concentration,
        ) in day["values"].items():

            levels[pollen_key] = level_for(
                pollen_key,
                concentration,
            )

        available_levels = [
            level
            for level in levels.values()
            if level > 0
        ]

        overall = (
            max(available_levels)
            if available_levels
            else 0
        )

        level_text = self.translation[
            "levels"
        ][overall]

        details = []

        for (
            pollen_key,
            concentration,
        ) in day["values"].items():

            level = levels[
                pollen_key
            ]

            if concentration is None:

                species_level_text = (
                    self.translation[
                        "no_data"
                    ]
                )

            else:

                species_level_text = (
                    self.translation[
                        "levels"
                    ][level]
                )

            label = self._pollen_label(
                pollen_key
            )

            details.append(
                "{}: {}".format(
                    label,
                    species_level_text,
                )
            )

        details_text = " | ".join(
            details
        )

        self._update(
            alert_unit,
            overall,
            level_text,
        )

        self._update(
            text_unit,
            0,
            details_text,
        )

        self.log(
            "{} -> {} | {}".format(
                day["date"],
                level_text,
                details_text,
            )
        )

    # ------------------------------------------------------------------
    # Labels
    # ------------------------------------------------------------------

    def _pollen_label(
        self,
        pollen_key,
    ):

        labels = self.translation[
            "pollen"
        ]

        if pollen_key in labels:
            return labels[pollen_key]

        definition = get_definition(
            pollen_key
        )

        return "{} ({})".format(
            self.translation.get(
                "unknown_pollen",
                "Unknown pollen",
            ),
            definition.key,
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

        device = self.devices[unit]

        if (
            device.nValue != nvalue
            or device.sValue != svalue
        ):

            device.Update(
                nValue=nvalue,
                sValue=svalue,
            )
