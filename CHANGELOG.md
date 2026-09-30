Changelog

All notable changes to Domoticz Pollen Forecast are documented here.

"0.2.2" (https://github.com/janreimen/Domoticz-Pollen-Forecast/releases/tag/v0.2.2) - 2026-09-30

Added

- Robust location resolution with a defined fallback order:
  1. Explicit "Mode1" "longitude,latitude"
  2. Domoticz system coordinates
  3. Plugin defaults from ".env"
- Support for the current Domoticz Python plugin representation:
  "Settings["Location"] = "latitude;longitude"".
- Validation of ".env" default longitude and latitude values.
- Location source reporting through the existing debug logging.

Changed

- Leaving "Mode1" empty now uses the Domoticz system location.
- If the Domoticz system location is unavailable or invalid, the plugin falls back to:
  - "POLLEN_DEFAULT_LONGITUDE"
  - "POLLEN_DEFAULT_LATITUDE"
- Explicitly configured "Mode1" values remain authoritative.
- An invalid explicitly configured "Mode1" value is reported as a configuration error rather than silently falling back.
- Location handling remains isolated in "config.py".

Fixed

- Fixed the failure where an empty "Mode1" produced:
  "Mode1 is empty, but valid Domoticz system latitude/longitude could not be read."
- Fixed parsing of the Domoticz "Settings["Location"]" string.
- Correctly handles Domoticz's "latitude;longitude" representation.
- Prevented valid Domoticz coordinates from being rejected because the configuration handler expected a dictionary representation.

Configuration

The plugin accepts an explicit location in the format:

longitude,latitude

For example:

6.247261,49.714920

When "Mode1" is empty, the plugin first uses the location configured in Domoticz.

If no valid Domoticz system location is available, the plugin uses the defaults from ".env":

POLLEN_DEFAULT_LONGITUDE=6.1319
POLLEN_DEFAULT_LATITUDE=49.6116

An error is reported only when no valid location can be obtained from any source.

---

"0.2.1-beta" (https://github.com/janreimen/Domoticz-Pollen-Forecast/releases/tag/v0.2.1-beta)

Added

- Individual pollen devices can be created only for the selected allergens.
- Fixed internal unit mapping for all pollen types is preserved.
- Existing pollen devices are preserved when the selected allergens change.
- Selected-pollen aggregate devices use units "100" and "101".
- Global pollen situation devices use units "110" and "111".
- Expanded language support.
- Modular configuration and device handling.

---

[0.2.0]

Added

- Open-Meteo Air Quality / CAMS European Air Quality pollen forecast integration.
- Individual pollen forecast devices.
- Today and tomorrow pollen information.
- Configurable refresh interval.
- Configurable allergen selection.
- Multi-language support.
- Debug logging.

:::

### README — location/configuration section

:::writing{variant="document" id="92751" title="README.md — v0.2.2 configuration section"}
## Location configuration

The plugin supports explicit coordinates, the Domoticz system location, and configurable fallback coordinates.

### Location priority

The location is resolved in this order:

```text
1. Mode1
      ↓
2. Domoticz system location
      ↓
3. .env defaults
      ↓
4. Configuration error

1. Explicit plugin location

The Location (longitude,latitude) field ("Mode1") can be used to override the Domoticz system location.

Enter coordinates as:

longitude,latitude

Example:

6.247261,49.714920

The order is always longitude first, latitude second.

If "Mode1" contains a value but that value is invalid, the plugin reports a configuration error. It does not silently use another location.

2. Domoticz system location

Leave "Mode1" empty to use the location configured in Domoticz.

The current Domoticz Python plugin interface provides this through:

Settings["Location"]

with the format:

latitude;longitude

For example:

49.71492;6.247261

The plugin converts this internally to its normal longitude/latitude representation.

3. ".env" fallback

If "Mode1" is empty and Domoticz does not provide a valid system location, the plugin uses the following environment variables:

POLLEN_DEFAULT_LONGITUDE=6.1319
POLLEN_DEFAULT_LATITUDE=49.6116

These values are fallback defaults only. They do not override a valid Domoticz system location.

Location source

When debug logging is enabled, the plugin reports the selected source:

PollenForecast: Location: longitude=6.247261, latitude=49.714920 (source: domoticz)

or:

PollenForecast: Location: longitude=6.131900, latitude=49.611600 (source: default)

or:

PollenForecast: Location: longitude=6.247261, latitude=49.714920 (source: plugin)

Environment configuration

The ".env" file should contain:

POLLEN_DEFAULT_LONGITUDE=6.1319
POLLEN_DEFAULT_LATITUDE=49.6116

Do not commit a production ".env" file if it contains other private configuration. Use ".env.example" as the template.

Configuration summary

Setting| Purpose
"Mode1"| Optional explicit "longitude,latitude"
"Mode2"| Forecast language
"Mode3"| Refresh interval
"Mode4"| Selected allergens
"Mode5"| Debug logging
"POLLEN_DEFAULT_LONGITUDE"| Fallback longitude
"POLLEN_DEFAULT_LATITUDE"| Fallback latitude

The ".env" location is used only when "Mode1" is empty and no valid Domoticz system location is available.
