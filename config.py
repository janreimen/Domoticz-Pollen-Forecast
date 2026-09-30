# -*- coding: utf-8 -*-
"""Configuration handling for the Pollen Forecast plugin."""

import Domoticz

from pollen import ALLERGENS

SUPPORTED_LANGUAGES = (
    "en", "lb", "de", "fr", "nl", "es", "pt", "ro", "it", "pl",
    "cs", "bg", "hu", "sv", "sk", "hr", "sl", "sr", "fi", "no", "da", "el",
)
SUPPORTED_ALLERGENS = ALLERGENS


class PluginConfig:
    def __init__(self, longitude, latitude, location_source, language, refresh_minutes, allergens, debug):
        self.longitude = longitude
        self.latitude = latitude
        self.location_source = location_source
        self.language = language
        self.refresh_minutes = refresh_minutes
        self.allergens = allergens
        self.debug = debug

    @property
    def valid_location(self):
        return self.longitude is not None and self.latitude is not None

    @classmethod
    def from_domoticz(cls, parameters, settings=None):
        longitude, latitude, location_source = cls._location_parameter(parameters, settings or {})

        language = parameters.get("Mode2", "en").strip().lower()
        if language not in SUPPORTED_LANGUAGES:
            Domoticz.Error("PollenForecast: Unsupported language '{}'; using en.".format(language))
            language = "en"

        try:
            refresh_minutes = int(parameters.get("Mode3", "60"))
        except (TypeError, ValueError):
            Domoticz.Error("PollenForecast: Invalid refresh interval; using 60 minutes.")
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
        raw = parameters.get("Mode1", "")
        raw = "" if raw is None else raw.strip()

        # An empty Mode1 explicitly means: use Domoticz system coordinates.
        if not raw:
            longitude, latitude = cls._domoticz_location(settings)
            if longitude is None or latitude is None:
                Domoticz.Error(
                    "PollenForecast: Mode1 is empty, but valid Domoticz system "
                    "latitude/longitude could not be read."
                )
                return None, None, "domoticz"
            return longitude, latitude, "domoticz"

        longitude, latitude = cls._parse_location(raw)
        if longitude is None or latitude is None:
            return None, None, "plugin"
        return longitude, latitude, "plugin"

    @staticmethod
    def _parse_location(raw):
        parts = [part.strip() for part in raw.split(",")]
        if len(parts) != 2 or not all(parts):
            Domoticz.Error(
                "PollenForecast: Location must be entered as longitude,latitude "
                "(example: 177.33,-30.23)."
            )
            return None, None
        try:
            longitude = float(parts[0])
            latitude = float(parts[1])
        except ValueError:
            Domoticz.Error("PollenForecast: Location contains invalid numeric values.")
            return None, None
        if not -180.0 <= longitude <= 180.0:
            Domoticz.Error("PollenForecast: Longitude must be between -180 and 180.")
            return None, None
        if not -90.0 <= latitude <= 90.0:
            Domoticz.Error("PollenForecast: Latitude must be between -90 and 90.")
            return None, None
        return longitude, latitude

    @classmethod
    def _domoticz_location(cls, settings):
        """Return Domoticz system longitude/latitude from the Settings dict."""
        location = settings.get("Location")
        if isinstance(location, dict):
            latitude = location.get("Latitude")
            longitude = location.get("Longitude")
        else:
            latitude = settings.get("Latitude")
            longitude = settings.get("Longitude")

        try:
            latitude = float(latitude)
            longitude = float(longitude)
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
            Domoticz.Error("PollenForecast: No valid allergen selected; using all supported allergens.")
            return SUPPORTED_ALLERGENS
        return tuple(valid)
