# -*- coding: utf-8 -*-
"""
Configuration handling for the Pollen Forecast plugin.
"""

import Domoticz


SUPPORTED_LANGUAGES = (
    "en",
    "lb",
    "de",
    "fr",
    "nl",
)


class PluginConfig:

    def __init__(
        self,
        latitude,
        longitude,
        language,
        refresh_minutes,
        debug,
    ):
        self.latitude = latitude
        self.longitude = longitude
        self.language = language
        self.refresh_minutes = refresh_minutes
        self.debug = debug

    @classmethod
    def from_domoticz(
        cls,
        parameters,
    ):

        latitude = cls._float_parameter(
            parameters,
            "Mode1",
            49.6116,
        )

        longitude = cls._float_parameter(
            parameters,
            "Mode2",
            6.1319,
        )

        language = parameters.get(
            "Mode3",
            "en",
        ).strip().lower()

        if language not in SUPPORTED_LANGUAGES:

            Domoticz.Error(
                "PollenForecast: Unsupported language '{}', "
                "using English.".format(language)
            )

            language = "en"

        try:

            refresh_minutes = int(
                parameters.get(
                    "Mode4",
                    "60",
                )
            )

        except (TypeError, ValueError):

            Domoticz.Error(
                "PollenForecast: Invalid refresh interval, "
                "using 60 minutes."
            )

            refresh_minutes = 60

        refresh_minutes = max(
            30,
            refresh_minutes,
        )

        debug = (
            parameters.get(
                "Mode5",
                "0",
            ) == "1"
        )

        return cls(
            latitude=latitude,
            longitude=longitude,
            language=language,
            refresh_minutes=refresh_minutes,
            debug=debug,
        )

    @staticmethod
    def _float_parameter(
        parameters,
        name,
        default,
    ):

        try:

            return float(
                parameters.get(
                    name,
                    str(default),
                ).strip()
            )

        except (
            TypeError,
            ValueError,
        ):

            Domoticz.Error(
                "PollenForecast: Invalid {}. "
                "Using default {}.".format(
                    name,
                    default,
                )
            )

            return float(default)
