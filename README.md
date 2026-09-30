# Domoticz Pollen Forecast

**Version:** 0.2.1-alpha  
**Author:** 4D, blooesky, janreimen

A modular Domoticz Python plugin that retrieves pollen forecasts from the Open-Meteo Air Quality API using the CAMS European Air Quality Forecast.

No API key and no external Python packages are required.

## Highlights

- Open-Meteo CAMS European pollen forecast.
- Forecast processing for today and tomorrow.
- Six supported pollen allergens:
  - alder
  - birch
  - grass
  - mugwort
  - olive
  - ragweed
- Individual native Domoticz Alert devices for each pollen type and day.
- User-selectable allergen aggregation.
- A separate global pollen situation for today and tomorrow.
- Twenty-two supported languages in 0.2.1-alpha:
- English (`en`)
  - Lëtzebuergesch (`lb`)
  - Deutsch (`de`)
  - Français (`fr`)
  - Nederlands (`nl`)
  - Español (`es`)
  - Português (`pt`)
  - Română (`ro`)
  - Italiano (`it`)
  - Polski (`pl`)
  - Čeština (`cs`)
  - Български (`bg`)
  - Magyar (`hu`)
  - Svenska (`sv`)
  - Slovenčina (`sk`)
  - Hrvatski (`hr`)
  - Slovenščina (`sl`)
  - Srpski (`sr`)
  - Suomi (`fi`)
  - Norsk (`no`)
  - Dansk (`da`)
  - Ελληνικά (`el`)
- Standard-library-only implementation.

## 0.2.1-alpha changes

### Unified location field

Latitude and longitude are now entered in one field as:

```text
longitude,latitude
```

Example:

```text
177.33,-30.23
```

The first value is validated as longitude:

```text
-180 <= longitude <= 180
```

The second value is validated as latitude:

```text
-90 <= latitude <= 90
```

The values are then passed to the API as latitude/longitude in the correct order.

### Allergen selection

The allergen field accepts:

- blank: all six supported allergens
- a comma-separated list, for example:

```text
alder,birch,grass
```

Valid values are:

```text
alder
birch
grass
mugwort
olive
ragweed
```

Whitespace is ignored and duplicate values are removed.

When more than one allergen is selected, the plugin creates an aggregate pollen level for today and tomorrow. The aggregate is calculated from the selected individual allergen `nValue`s:

```text
sum(nValues) / number_of_selected_allergens
```

The result is rounded to the nearest integer with `.50` rounded upward.

The aggregate is independent from the global pollen situation.

### Global pollen situation

The plugin also provides a general-information view of pollen conditions.

For each day, the global pollen situation is the maximum pollen level across all available supported pollen types. It is intentionally independent from the user's allergen selection.

This provides two different views:

- **Selected pollen**: personalized aggregate based on `Mode4`.
- **Global pollen situation**: overall highest pollen level available for the day.

## Devices

The fixed individual device layout is:

| Unit | Pollen | Day |
|---:|---|---|
| 1 | Alder | Today |
| 2 | Alder | Tomorrow |
| 3 | Birch | Today |
| 4 | Birch | Tomorrow |
| 5 | Grass | Today |
| 6 | Grass | Tomorrow |
| 7 | Mugwort | Today |
| 8 | Mugwort | Tomorrow |
| 9 | Olive | Today |
| 10 | Olive | Tomorrow |
| 11 | Ragweed | Today |
| 12 | Ragweed | Tomorrow |

Aggregate devices:

| Unit | Purpose |
|---:|---|
| 100 | Selected pollen Today |
| 101 | Selected pollen Tomorrow |
| 110 | Global pollen situation Today |
| 111 | Global pollen situation Tomorrow |

The unit numbers are fixed internally to keep Domoticz automation references stable, but **only the allergens selected in `Mode4` are created and updated**.

For example, `alder,birch` creates/updates units 1-4, not units 5-12. Existing devices for allergens that are later deselected are not deleted; they are simply no longer updated.

## Alert levels

All Alert devices use:

| nValue | Meaning |
|---:|---|
| 0 | No data |
| 1 | None |
| 2 | Low |
| 3 | Medium |
| 4 | High |

These values are directly usable in Domoticz automation.

## Configuration

The plugin configuration consists of:

1. **Location** — `longitude,latitude` (`Mode1`)
2. **Language** (`Mode2`)
3. **Refresh interval** (`Mode3`)
4. **Allergens** (`Mode4`)
5. **Debug** (`Mode5`)

Example:

```text
Location: 6.246450,49.714753
Language: en
Refresh: 60
Allergens: birch,grass
Debug: Off
```

## Data source

Open-Meteo Air Quality API with the CAMS European domain is used for pollen forecast data.

The plugin requests four forecast days internally and exposes today and tomorrow.

## PyPluginStore compatibility

The repository is structured as a standard Domoticz Python plugin and keeps its plugin metadata embedded in `plugin.py`. The metadata identifies the project as `PollenForecast`, version `0.2.1-alpha`, with authors `4D, blooesky, janreimen`, and points to the GitHub repository. This allows Git-based plugin-store tooling such as PyPluginStore to identify the plugin and its version.

## Requirements

- Domoticz with Python plugin support.
- Python 3.
- Network access to Open-Meteo.
- No third-party Python package.

## Installation

Copy the plugin directory to the Domoticz plugins directory:

```text
<domoticz>/plugins/Domoticz-Pollen-Forecast
```

Then restart Domoticz and add the hardware plugin from the Domoticz UI.

See [DEPLOY.md](DEPLOY.md).

## Development

See:

- [DEVELOPMENT.md](DEVELOPMENT.md)
- [TESTING.md](TESTING.md)
- [API.md](API.md)
- [RELEASE.md](RELEASE.md)

## License

MIT. See [LICENSE](LICENSE).
