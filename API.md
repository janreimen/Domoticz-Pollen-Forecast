# API Documentation

## Domoticz Pollen Forecast

This document describes the external API used by the **Domoticz Pollen Forecast** plugin and how API data is transformed into Domoticz pollen forecast devices.

---

## 1. External API

The plugin uses the **Open-Meteo Air Quality API**.

API endpoint:

```text
https://air-quality-api.open-meteo.com/v1/air-quality
```

The plugin uses the European CAMS forecast domain:

```text
domains=cams_europe
```

The API is accessed over HTTPS.

No API key is required by the plugin.

---

## 2. API Request

The plugin sends an HTTP `GET` request.

The request parameters currently include:

| Parameter       | Value                | Description                       |
| --------------- | -------------------- | --------------------------------- |
| `latitude`      | configured latitude  | Forecast latitude                 |
| `longitude`     | configured longitude | Forecast longitude                |
| `hourly`        | pollen variables     | Requested hourly pollen data      |
| `timezone`      | `auto`               | API determines the local timezone |
| `forecast_days` | `4`                  | Request four forecast days        |
| `domains`       | `cams_europe`        | European CAMS forecast domain     |

Example request:

```text
https://air-quality-api.open-meteo.com/v1/air-quality?latitude=49.6116&longitude=6.1319&hourly=alder_pollen%2Cbirch_pollen%2Cgrass_pollen%2Cmugwort_pollen%2Colive_pollen%2Cragweed_pollen&timezone=auto&forecast_days=4&domains=cams_europe
```

The exact URL is generated dynamically from the configured location and requested pollen variables.

---

## 3. User-Agent

The plugin identifies itself using the following HTTP User-Agent:

```text
Domoticz-PollenForecast/0.2.0-beta
```

The User-Agent should be updated when the plugin release version changes.

---

## 4. Requested Pollen Variables

The initial plugin version requests the following Open-Meteo pollen variables:

```text
alder_pollen
birch_pollen
grass_pollen
mugwort_pollen
olive_pollen
ragweed_pollen
```

These are defined centrally in:

```text
pollen.py
```

The request is constructed from the configured pollen definitions rather than duplicating the list inside the API client.

---

## 5. Pollen Variable Naming

The plugin identifies pollen variables using the following convention:

```text
*_pollen
```

For example:

```text
alder_pollen
birch_pollen
grass_pollen
```

This allows the plugin to detect additional pollen variables returned by the API without requiring the API client itself to know every possible species.

Unknown pollen variables are treated as data and do not cause the API processing to fail.

---

## 6. API Response

The API returns JSON.

A simplified response structure is:

```json
{
  "latitude": 49.6116,
  "longitude": 6.1319,
  "timezone": "Europe/Luxembourg",
  "hourly": {
    "time": [
      "2026-09-28T00:00",
      "2026-09-28T01:00"
    ],
    "alder_pollen": [
      0.0,
      0.0
    ],
    "birch_pollen": [
      0.0,
      0.0
    ],
    "grass_pollen": [
      2.1,
      3.4
    ]
  }
}
```

The actual response can contain additional fields.

The plugin only processes the fields required for pollen forecasting.

---

## 7. Response Validation

The API client validates the basic response structure before processing it.

The following conditions are checked:

### HTTP status

The response must have HTTP status `200`.

Otherwise the request fails.

### JSON

The response must contain valid JSON.

### API error

If the API returns an error indication, the plugin raises an API error using the supplied API reason where available.

### `hourly`

The response must contain an `hourly` object.

### `time`

The `hourly` object must contain a `time` series.

If these required structures are missing, the response is considered invalid.

---

## 8. Error Handling

The following conditions may cause an update to fail:

* DNS failure
* network failure
* connection timeout
* TLS failure
* HTTP error
* invalid JSON
* API-reported error
* missing `hourly` data
* missing `time` data

The plugin does not execute arbitrary retry loops.

The next normal scheduled update will attempt the request again.

---

## 9. Timeout

The API request currently uses a network timeout of:

```text
10 seconds
```

This prevents the Domoticz plugin from waiting indefinitely for an external API request.

---

## 10. Hourly Data Processing

Open-Meteo returns pollen values on an hourly basis.

The plugin converts these hourly values into one daily value for each pollen species.

The daily value is:

```text
maximum hourly concentration for that day
```

For example:

```text
00:00 → 2.0
01:00 → 4.5
02:00 → 7.2
03:00 → 5.1
```

The resulting daily concentration is:

```text
7.2
```

This represents the maximum predicted pollen concentration during that day.

---

## 11. Date Handling

The API provides timestamps through:

```text
hourly.time
```

The plugin extracts the date from each timestamp.

For example:

```text
2026-09-28T14:00
```

becomes:

```text
2026-09-28
```

The plugin groups hourly values by date.

The first returned date is treated as:

```text
Today
```

The second returned date is treated as:

```text
Tomorrow
```

The plugin requires at least two forecast days for a successful Domoticz update.

---

## 12. Missing Values

Pollen values may be missing or `null`.

Example:

```json
{
  "grass_pollen": [
    2.4,
    null,
    5.1
  ]
}
```

`null` values are ignored.

The valid values are:

```text
2.4
5.1
```

and the resulting daily maximum is:

```text
5.1
```

If no valid value exists for a pollen species on a particular day, the resulting concentration is:

```text
None
```

This is subsequently represented by Domoticz as:

```text
Level 0 = No data
```

---

## 13. Numeric Validation

Pollen values are converted to floating-point numbers.

Values that cannot be converted to a number are ignored.

For example:

```text
5.4
```

is accepted.

Whereas:

```text
"invalid"
```

is ignored.

The plugin does not execute or interpret pollen values as code.

---

## 14. Pollen Levels

The plugin converts concentrations into five logical levels.

| Level | Meaning |
| ----: | ------- |
|   `0` | No data |
|   `1` | None    |
|   `2` | Low     |
|   `3` | Medium  |
|   `4` | High    |

A concentration below:

```text
1.0
```

is considered:

```text
None
```

---

## 15. Pollen Thresholds

The current thresholds are defined in:

```text
pollen.py
```

### Alder

```text
< 1.0      None
1.0–16.0   Low
> 16–50.0  Medium
> 50.0     High
```

### Birch

```text
< 1.0      None
1.0–16.0   Low
> 16–50.0  Medium
> 50.0     High
```

### Grass

```text
< 1.0      None
1.0–10.0   Low
> 10–30.0  Medium
> 30.0     High
```

### Mugwort

```text
< 1.0      None
1.0–5.0    Low
> 5–25.0   Medium
> 25.0     High
```

### Olive

```text
< 1.0      None
1.0–5.0    Low
> 5–25.0   Medium
> 25.0     High
```

### Ragweed

```text
< 1.0      None
1.0–5.0
```

