# API

**Version:** 0.2.1-beta

## Data source

The plugin uses the Open-Meteo Air Quality API and requests the CAMS European Air Quality Forecast domain.

Endpoint:

```text
https://air-quality-api.open-meteo.com/v1/air-quality
```

The plugin does not require an API key.

## Request

The request contains:

- `latitude`
- `longitude`
- `hourly`
- `timezone=auto`
- `forecast_days=4`
- `domains=cams_europe`

The requested hourly pollen variables are:

```text
alder_pollen
birch_pollen
grass_pollen
mugwort_pollen
olive_pollen
ragweed_pollen
```

The API client also discovers additional returned variables whose names end in `_pollen`. Unknown pollen variables are handled with the configured fallback threshold model rather than causing the update to fail.

## Location

The plugin configuration uses one location field:

```text
longitude,latitude
```

Example:

```text
177.33,-30.23
```

Validation:

```text
-180 <= longitude <= 180
-90 <= latitude <= 90
```

The configuration parser converts the two values to numeric values and passes them to the API as latitude and longitude.

If Mode1 is empty, the plugin reads the Domoticz system location from the Python plugin `Settings` dictionary and uses that location automatically. An invalid explicit Mode1 value is an error and does not fall back to the Domoticz location.

## Daily processing

The API returns hourly values.

For each pollen variable and calendar day, the plugin calculates the daily concentration as the maximum valid hourly concentration for that day.

Example:

```text
hourly values:
0.0, 1.2, 4.8, 3.1

daily concentration:
4.8
```

Today and tomorrow are taken from the resulting daily data.

## Pollen levels

Concentrations are converted into Domoticz Alert levels.

### Level 0

No usable concentration data is available.

### Level 1

Concentration is below `1.0`.

### Level 2

Low concentration.

Thresholds:

| Pollen | Low upper limit | Medium upper limit |
|---|---:|---:|
| Alder | 16 | 50 |
| Birch | 16 | 50 |
| Grass | 10 | 30 |
| Mugwort | 5 | 25 |
| Olive | 5 | 25 |
| Ragweed | 5 | 25 |

### Level 3

Concentration is above the low threshold and at or below the medium threshold.

### Level 4

Concentration is above the medium threshold.

## Individual device selection

The plugin keeps a fixed internal unit map for all six supported allergens, but device creation and updates are driven by the configured `Mode4` selection.

For example, `alder,birch` creates and updates only Alder units 1/2 and Birch units 3/4. The remaining individual pollen units are not created. If a device for a previously selected allergen already exists, changing the configuration does not delete it; it simply stops updating that device.

The global pollen situation is an exception: units 110/111 are always created and are calculated from all supported pollen types, independent of `Mode4`.

## Selected pollen aggregate

The allergen configuration accepts a blank value or a CSV list.

Blank means:

```text
alder,birch,grass,mugwort,olive,ragweed
```

Example:

```text
birch,grass
```

For more than one selected allergen, the aggregate is calculated from the individual allergen `nValue`s:

```text
average = sum(nValues) / number_of_selected_allergens
```

The result is rounded using:

```text
fraction < 0.50  -> round down
fraction >= 0.50 -> round up
```

Because `nValue` is non-negative and limited to 0..4, this is equivalent to:

```text
floor(average + 0.5)
```

No-data values (`0`) are included in the calculation because the aggregation is explicitly based on the selected devices' `nValue`s.

If only one allergen is selected, no aggregate device is required; the individual device already represents that allergen.

## Global pollen situation

The global situation is intentionally independent of the selected allergen list.

For each day:

```text
global_level = max(level for all available supported pollen types)
```

Thus a user can select specific allergens for a personalized aggregate while still having a general indication of the highest pollen level forecast for the day.

## Forecast horizon

The plugin requests four forecast days internally. Only today and tomorrow are currently exposed as Domoticz devices.

The extra forecast days provide API processing headroom and future extensibility.

## Error handling

The API client raises an exception for:

- HTTP errors
- invalid JSON
- API-reported errors
- missing hourly data
- missing time data

The plugin logs the update failure and keeps the previous device state.

## Dependencies

The API client uses only Python standard-library modules:

- `json`
- `urllib.parse`
- `urllib.request`

No external package installation is required.
