# -*- coding: utf-8 -*-
"""Configuration handling for the Pollen Forecast plugin."""

import os

import Domoticz

from pollen import ALLERGENS


SUPPORTED_LANGUAGES = (
    "en", "lb", "de", "fr", "nl", "es", "pt", "ro", "it", "pl",
    "cs", "bg", "hu", "sv", "sk", "hr", "sl", "sr", "fi", "no", "da", "el",
)

SUPPORTED_ALLERGENS = ALLERGENS


class PluginConfig:
    def __init__(
        self,
        longitude,
        latitude,
        location_source,
        language,
        refresh_minutes,
        allergens,
        debug,
    ):
        self.longitude = longitude
        self.latitude = latitude
        self.location_source = location_source
        self.language = language
        self.refresh_minutes = refresh_minutes
        self.allergens = allergens
        self.debug = debug

    @property
    def valid_location(self):
        return (
            self.longitude is not None
            and self.latitude is not None
        )

    @classmethod
    def from_domoticz(cls, parameters, settings=None):
        longitude, latitude, location_source = cls._location_parameter(
            parameters,
            settings or {},
        )

        language = parameters.get("Mode2", "en").strip().lower()

        if language not in SUPPORTED_LANGUAGES:
            Domoticz.Error(
                "PollenForecast: Unsupported language '{}'; using en.".format(
                    language
                )
            )
            language = "en"

        try:
            refresh_minutes = int(
                parameters.get("Mode3", "60")
            )
        except (TypeError, ValueError):
            Domoticz.Error(
                "PollenForecast: Invalid refresh interval; "
                "using 60 minutes."
            )
            refresh_minutes = 60

        refresh_minutes = max(30, refresh_minutes)

        allergens = cls._allergens_parameter(parameters)

        debug = parameters.get("Mode5", "0") == "1"

        return cls(
            longitude,
            latitude,
            location_source,
            language,
            refresh_minutes,
            allergens,
            debug,
        )

    @classmethod
    def _location_parameter(cls, parameters, settings):
        """
        Resolve the plugin location.

        Priority:

            1. Explicit Mode1 longitude,latitude
            2. Domoticz system coordinates
            3. .env default coordinates
            4. No valid location
        """
        raw = parameters.get("Mode1", "")
        raw = "" if raw is None else raw.strip()

        # 1. Explicit plugin location.
        #
        # If Mode1 contains a value, it must be valid.
        # Do not silently fall back if the user explicitly
        # entered an invalid location.
        if raw:
            longitude, latitude = cls._parse_location(raw)

            if longitude is None or latitude is None:
                return None, None, "plugin"

            return longitude, latitude, "plugin"

        # 2. Domoticz system location.
        longitude, latitude = cls._domoticz_location(settings)

        if longitude is not None and latitude is not None:
            return longitude, latitude, "domoticz"

        # 3. Plugin default location from .env.
        longitude, latitude = cls._default_location()

        if longitude is not None and latitude is not None:
            Domoticz.Log(
                "PollenForecast: Using default location from .env: "
                "longitude={:.6f}, latitude={:.6f}".format(
                    longitude,
                    latitude,
                )
            )

            return longitude, latitude, "default"

        # 4. No usable location.
        Domoticz.Error(
            "PollenForecast: No valid location available; "
            "configure Mode1 as longitude,latitude, configure valid "
            "Domoticz coordinates, or set "
            "POLLEN_DEFAULT_LONGITUDE and "
            "POLLEN_DEFAULT_LATITUDE in .env."
        )

        return None, None, "none"

    @staticmethod
    def _parse_location(raw):
        """
        Parse an explicit plugin location.

        Expected format:

            longitude,latitude
        """
        parts = [
            part.strip()
            for part in raw.split(",")
        ]

        if len(parts) != 2 or not all(parts):
            Domoticz.Error(
                "PollenForecast: Location must be entered as "
                "longitude,latitude "
                "(example: 177.33,-30.23)."
            )
            return None, None

        try:
            longitude = float(parts[0])
            latitude = float(parts[1])
        except ValueError:
            Domoticz.Error(
                "PollenForecast: Location contains "
                "invalid numeric values."
            )
            return None, None

        if not -180.0 <= longitude <= 180.0:
            Domoticz.Error(
                "PollenForecast: Longitude must be between "
                "-180 and 180."
            )
            return None, None

        if not -90.0 <= latitude <= 90.0:
            Domoticz.Error(
                "PollenForecast: Latitude must be between "
                "-90 and 90."
            )
            return None, None

        return longitude, latitude

    @classmethod
    def _domoticz_location(cls, settings):
        """
        Return Domoticz system longitude/latitude from Settings.

        Current Domoticz Python plugin API provides:

            Settings["Location"] = "latitude;longitude"

        Example:

            "49.71492;6.247261"

        Dictionary-style and legacy Latitude/Longitude
        representations are also supported.
        """
        location = settings.get("Location")

        # Current Domoticz representation:
        #
        #     Location = "latitude;longitude"
        if isinstance(location, str):
            parts = [
                part.strip()
                for part in location.split(";", 1)
            ]

            if len(parts) != 2:
                return None, None

            try:
                latitude = float(parts[0])
                longitude = float(parts[1])
            except (TypeError, ValueError):
                return None, None

        # Dictionary-style representation.
        elif isinstance(location, dict):
            try:
                latitude = float(
                    location.get("Latitude")
                )
                longitude = float(
                    location.get("Longitude")
                )
            except (TypeError, ValueError):
                return None, None

        # Legacy/fallback representation.
        else:
            try:
                latitude = float(
                    settings.get("Latitude")
                )
                longitude = float(
                    settings.get("Longitude")
                )
            except (TypeError, ValueError):
                return None, None

        if not -90.0 <= latitude <= 90.0:
            return None, None

        if not -180.0 <= longitude <= 180.0:
            return None, None

        return longitude, latitude

    @staticmethod
    def _default_location():
        """
        Return the plugin default longitude/latitude from .env.

        Expected variables:

            POLLEN_DEFAULT_LONGITUDE=6.1319
            POLLEN_DEFAULT_LATITUDE=49.6116
        """
        try:
            longitude = float(
                os.environ.get(
                    "POLLEN_DEFAULT_LONGITUDE",
                    "",
                )
            )

            latitude = float(
                os.environ.get(
                    "POLLEN_DEFAULT_LATITUDE",
                    "",
                )
            )
        except (TypeError, ValueError):
            return None, None

        if not -180.0 <= longitude <= 180.0:
            return None, None

        if not -90.0 <= latitude <= 90.0:
            return None, None

        return longitude, latitude

    @staticmethod
    def _allergens_parameter(parameters):
        raw = parameters.get("Mode4", "")
        raw = "" if raw is None else raw.strip().lower()

        if not raw:
            return SUPPORTED_ALLERGENS

        valid = []
        invalid = []

        for item in raw.split(","):
            allergen = item.strip().lower()

            if not allergen:
                continue

            if allergen in SUPPORTED_ALLERGENS:
                if allergen not in valid:
                    valid.append(allergen)
            else:
                invalid.append(allergen)

        if invalid:
            Domoticz.Error(
                "PollenForecast: Ignoring unsupported allergens: {}".format(
                    ", ".join(invalid)
                )
            )

        if not valid:
            Domoticz.Error(
                "PollenForecast: No valid allergen selected; "
                "using all supported allergens."
            )
            return SUPPORTED_ALLERGENS

        return tuple(valid)
