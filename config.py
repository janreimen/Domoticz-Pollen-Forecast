# -*- coding: utf-8 -*-
"""
Configuration handling for the Pollen Forecast plugin.
"""

import Domoticz


SUPPORTED_LANGUAGES = (
    "en",
    "it",
    "es",
    "pt",
    "pl",
    "ro",
    "lb",
    "de",
    "fr",
    "nl"
)

SUPPORTED_ALLERGENS = (
    "alder",
    "birch",
    "grass",
    "mugwort",
    "olive",
    "ragweed",
)


class PluginConfig:

    def __init__(
        self,
        latitude,
        longitude,
        language,
        refresh_minutes,
        allergens,
        debug,
    ):
        self.latitude = latitude
        self.longitude = longitude
        self.language = language
        self.refresh_minutes = refresh_minutes
        self.allergens = allergens
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

        allergens = cls._allergens_parameter(
            parameters
        )

        debug = (
            parameters.get(
                "Mode6",
                "0",
            ) == "1"
        )

        return cls(
            latitude=latitude,
            longitude=longitude,
            language=language,
            refresh_minutes=refresh_minutes,
            allergens=allergens,
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

    @staticmethod
    def _allergens_parameter(
        parameters,
    ):

        value = parameters.get(
            "Mode5",
            "",
        )

        if value is None:
            value = ""

        value = value.strip().lower()

        # Empty input means all supported allergens.
        if not value:
            return SUPPORTED_ALLERGENS

        requested = [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

        valid = []
        invalid = []

        for allergen in requested:

            if allergen in SUPPORTED_ALLERGENS:

                if allergen not in valid:
                    valid.append(allergen)

            else:

                invalid.append(allergen)

        if invalid:

            Domoticz.Error(
                "PollenForecast: Unsupported allergen(s): {}. "
                "Permitted values: {}.".format(
                    ", ".join(invalid),
                    ", ".join(SUPPORTED_ALLERGENS),
                )
            )

        # If the user supplied only invalid values,
        # use all allergens rather than creating no devices.
        if not valid:

            Domoticz.Error(
                "PollenForecast: No valid allergens configured, "
                "using all allergens."
            )

            return SUPPORTED_ALLERGENS

        return tuple(valid)
