# Changelog

All notable changes to this project are documented here.

The project follows Semantic Versioning-style versioning during pre-1.0 development.

## [0.2.1-beta] - 2026-09-30

### Added

- Use Domoticz system latitude/longitude automatically when Mode1 Location is left empty.
- Keep explicit `longitude,latitude` input as a location override.
- Log whether the effective location came from Mode1 or Domoticz.

### Changed

- Remove the hard-coded Luxembourg coordinates as the plugin default.
- Make Mode1 Location optional.

### Validation

- Invalid explicit coordinates remain an error and do not silently fall back to Domoticz coordinates.
- Existing allergen-driven device provisioning, fixed unit mapping, selected-pollen units and global-situation units are unchanged from `0.2.1-alpha`.

## [0.2.1-alpha] - 2026-09-30

### Added

- Unified location configuration field using `longitude,latitude`.
- Validation of longitude in the range `-180..180`.
- Validation of latitude in the range `-90..90`.
- Czech (`cs`) language support.
- Bulgarian (`bg`) language support.
- Hungarian (`hu`) language support.
- Swedish (`sv`) language support.
- Slovak (`sk`) language support.
- Croatian (`hr`) language support.
- Slovenian (`sl`) language support.
- Serbian (`sr`) language support.
- Finnish (`fi`) language support.
- Norwegian (`no`) language support.
- Danish (`da`) language support.
- Greek (`el`) language support.
- Global pollen situation for today.
- Global pollen situation for tomorrow.
- General-information pollen devices independent from allergen selection.

### Changed

- Configuration fields are shifted after combining latitude and longitude into one field.
- The internal API continues to use named latitude and longitude values after configuration parsing.
- The global pollen situation is calculated as the highest pollen level among the available supported pollen types.
- The modular architecture is retained; upstream functionality is integrated as isolated features rather than copied as a monolithic implementation.

### Compatibility

- Individual pollen device units remain stable internally, while device creation/update is limited to allergens selected in Mode4.
- Selected-pollen aggregate devices remain separate from the global situation devices.
- This is an alpha release; configuration and device models may still change before 1.0.0.

## [0.2.0-beta] - 2026-09-29

### Added

- Configurable allergen selection through the dedicated allergen field.
- Support for alder, birch, grass, mugwort, olive and ragweed selection.
- Blank allergen selection means all supported allergens.
- CSV allergen selection.
- Selected-pollen aggregate devices for today and tomorrow when more than one allergen is selected.
- Aggregate calculation from selected individual allergen `nValue`s.
- `.50` half-up rounding for aggregate levels.
- Spanish (`es`) support.
- Portuguese (`pt`) support.
- Romanian (`ro`) support.
- Italian (`it`) support.
- Polish (`pl`) support.

### Changed

- Configuration consolidated into five fields: Mode1 location, Mode2 language, Mode3 refresh interval, Mode4 allergens, Mode5 debug.
- Expanded language support.
- Continued modular separation of configuration, API, pollen processing, devices and translations.

## [0.2.0-alpha]

### Added

- Modular plugin architecture.
- Open-Meteo CAMS pollen forecast integration.
- Native Domoticz Alert devices for individual pollen types.
- Today and tomorrow pollen levels.
- Dynamic discovery of additional `_pollen` API variables.
- Fallback thresholds for unknown pollen variables.
- Initial translations for English, Lëtzebuergesch, German, French and Dutch.

## Earlier development

Earlier versions originated from the upstream Domoticz Pollen Forecast plugin and were progressively refactored into a modular implementation.

[0.2.1-beta]: https://github.com/janreimen/Domoticz-Pollen-Forecast/releases/tag/v0.2.1-beta
[0.2.0-beta]: https://github.com/janreimen/Domoticz-Pollen-Forecast/releases/tag/v0.2.0-beta
