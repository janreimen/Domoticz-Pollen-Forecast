# Changelog

All notable changes to **Domoticz Pollen Forecast** are documented in this file.

The format of this file is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**.

This project follows **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

Changes that are planned or currently under development but are not yet part of a released version.

### Planned

* Additional pollen species where supported by the Open-Meteo API.
* More extensive automated tests.
* Additional API response validation.
* Improved API failure handling.
* Configurable pollen thresholds.
* Additional forecast days.
* Further documentation improvements.
* Stable device-model compatibility before `1.0.0`.

---

## [0.2.0-alpha] - 2026-09-28

### Added

* Modular plugin architecture.
* Dedicated configuration module.
* Dedicated Open-Meteo API client.
* Dedicated pollen definition and level calculation module.
* Dedicated Domoticz device handling module.
* Dedicated translation module.
* Support for English (`en`).
* Support for Lëtzebuergesch (`lb`).
* Support for Deutsch (`de`).
* Support for Français (`fr`).
* Support for Nederlands (`nl`).
* Configurable latitude.
* Configurable longitude.
* Configurable language.
* Configurable refresh interval.
* Configurable debug logging.
* Open-Meteo Air Quality API integration.
* CAMS European Air Quality Forecast integration.
* Four forecast days retrieved from the API.
* Today and tomorrow exposed to Domoticz.
* Dynamic detection of pollen variables ending in `_pollen`.
* Support for the following pollen species:

  * Alder
  * Birch
  * Grass
  * Mugwort
  * Olive
  * Ragweed.
* Daily pollen concentration calculation using the maximum hourly value.
* Native Domoticz `Alert` devices.
* Separate Domoticz device for every pollen species and forecast day.
* Twelve deterministic Domoticz devices:

  * Alder Today
  * Alder Tomorrow
  * Birch Today
  * Birch Tomorrow
  * Grass Today
  * Grass Tomorrow
  * Mugwort Today
  * Mugwort Tomorrow
  * Olive Today
  * Olive Tomorrow
  * Ragweed Today
  * Ragweed Tomorrow.
* Native Domoticz alert-level representation:

  * `0` = No data
  * `1` = None
  * `2` = Low
  * `3` = Medium
  * `4` = High.
* Native Domoticz alert colours through the `Alert` device type.
* Explicit pollen thresholds for the currently supported species.
* Fallback thresholds for unknown pollen species.
* Error handling for failed API requests.
* Debug logging for API discovery and device updates.
* Python standard-library-only implementation.
* No external Python runtime dependencies.

### Changed

* Replaced the previous cumulative pollen text-sensor model.
* Pollen information is no longer combined into a single text sensor.
* Pollen species are now represented by independent Domoticz devices.
* Today and tomorrow are represented independently.
* `PollenDevices` now receives the Domoticz `Devices` collection explicitly.
* `PluginConfig` now receives the Domoticz `Parameters` collection explicitly.
* API processing was separated from Domoticz device handling.
* Translation handling was separated from the main plugin lifecycle.
* Pollen-level calculation was separated from API processing.
* Daily pollen values are calculated from hourly API values.
* Unknown `_pollen` variables are handled without terminating the plugin.
* API failures no longer cause a retry on every 30-second Domoticz heartbeat.

### Removed

* Cumulative pollen detail text as the primary device representation.
* The previous four-device model:

  * Pollen Alert Today
  * Pollen Alert Tomorrow
  * Pollen Today
  * Pollen Tomorrow.
* Dependency on implicit Domoticz globals inside the configuration module.
* Dependency on implicit Domoticz globals inside the device module.

### Fixed

* Configuration parsing no longer relies on an undefined `Parameters` name inside `config.py`.
* Device handling no longer relies on an undefined `Devices` name inside `devices.py`.
* Translation access is now consistent between `translations.py` and `devices.py`.
* Pollen-level calculation handles missing and invalid concentration values.
* API response validation handles missing `hourly` data.
* API response validation handles missing `time` data.
* Plugin update failures are logged without causing continuous heartbeat retries.

### Security

* API communication uses HTTPS.
* No API credentials are required by the plugin.
* No inbound network service is opened by the plugin.
* No shell commands are executed by the plugin.
* No dynamic execution of API-provided data is performed.
* Runtime dependencies are limited to the Python standard library.

### Breaking Changes

This alpha release changes the Domoticz device model.

Previous development versions used four devices with cumulative pollen information.

This release uses twelve individual `Alert`

