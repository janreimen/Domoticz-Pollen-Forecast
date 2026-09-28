# Domoticz Pollen Forecast

A Domoticz Python plugin that retrieves pollen forecasts from the **Open-Meteo Air Quality API** using the **CAMS European Air Quality Forecast** and exposes individual pollen levels as native Domoticz Alert devices.

The plugin is designed for simple Domoticz automation:

* one device per pollen species
* separate devices for today and tomorrow
* native Domoticz Alert levels
* native Domoticz alert colours
* no cumulative text sensor
* no external Python packages required
* multilingual user interface

## Status

**Current version:** `0.2.0-alpha`

This is an **alpha release**.

The device model is intentionally still subject to change before the first stable release.

The planned version policy is:

| Version     | Meaning                                         |
| ----------- | ----------------------------------------------- |
| `0.x-alpha` | Development / architecture phase                |
| `0.x-beta`  | Real-world testing                              |
| `1.0.0`     | First stable release with a frozen device model |

---

# Features

* Pollen forecast from Open-Meteo
* CAMS European Air Quality Forecast data
* Forecast for today and tomorrow
* Individual Domoticz device for each pollen species
* Native Domoticz `Alert` device type
* Native Domoticz alert colours
* Five supported languages:

  * English
  * Lëtzebuergesch
  * Deutsch
  * Français
  * Nederlands
* Configurable latitude and longitude
* Configurable refresh interval
* Debug logging
* No third-party Python dependencies
* Automatic handling of unknown future pollen variables
* Daily pollen level calculated from the maximum hourly concentration

---

# Pollen Species

The current release handles the following pollen species:

| API key          | Species |
| ---------------- | ------- |
| `alder_pollen`   | Alder   |
| `birch_pollen`   | Birch   |
| `grass_pollen`   | Grass   |
| `mugwort_pollen` | Mugwort |
| `olive_pollen`   | Olive   |
| `ragweed_pollen` | Ragweed |

The API client dynamically detects pollen variables ending in:

```text
_pollen
```

This allows future Open-Meteo pollen variables to be detected without breaking the plugin.

Known species have explicitly defined thresholds.

Unknown species use the default thresholds until they are explicitly defined.

---

# Domoticz Device Model

The plugin creates **12 native Domoticz Alert devices**.

There are six pollen species and two forecast days.

```text
Unit  1  Alder Today
Unit  2  Alder Tomorrow

Unit  3  Birch Today
Unit  4  Birch Tomorrow

Unit  5  Grass Today
Unit  6  Grass Tomorrow

Unit  7  Mugwort Today
Unit  8  Mugwort Tomorrow

Unit  9  Olive Today
Unit 10  Olive Tomorrow

Unit 11  Ragweed Today
Unit 12  Ragweed Tomorrow
```

The unit numbering is deterministic and is calculated from the pollen species and forecast day.

## Why individual devices?

Earlier versions used cumulative text sensors containing information such as:

```text
Birch: High | Alder: Medium | Grass: Low | ...
```

This is inconvenient for Domoticz automation because automation rules have to interpret text.

The current architecture instead exposes every pollen species independently.

For example:

```text
Birch Today
    nValue = 4
```

can directly be used by Domoticz automation.

No text parsing is required.

---

# Alert Levels

Each device uses the native Domoticz `Alert` device type.

The `nValue` represents the pollen level:

| nValue | Level   | Domoticz colour |
| -----: | ------- | --------------- |
|    `0` | No data | Grey            |
|    `1` | None    | Green           |
|    `2` | Low     | Yellow          |
|    `3` | Medium  | Orange          |
|    `4` | High    | Red             |

This makes the devices directly useful for visual dashboards and automation.

For example:

```text
Birch Today
    nValue = 4
```

means:

```text
Birch pollen
High
Red
```

A Domoticz event can therefore react directly to the device value.

---

# Pollen Thresholds

The current thresholds are:

| Species |  None |    Low |   Medium |  High |
| ------- | ----: | -----: | -------: | ----: |
| Alder   | `< 1` | `1–16` | `>16–50` | `>50` |
| Birch   | `< 1` | `1–16` | `>16–50` | `>50` |
| Grass   | `< 1` | `1–10` | `>10–30` | `>30` |
| Mugwort | `< 1` |  `1–5` |  `>5–25` | `>25` |
| Olive   | `< 1` |  `1–5` |  `>5–25` | `>25` |
| Ragweed | `< 1` |  `1–5` |  `>5–25` | `>25` |

These thresholds are implemented in:

```text
pollen.py
```

The level calculation is:

```text
0 = no data
1 = concentration < 1
2 = low
3 = medium
4 = high
```

---

# Daily Forecast Calculation

Open-Meteo returns hourly pollen concentrations.

The plugin converts the hourly values into one daily value per pollen species.

For each day:

```text
daily concentration = maximum hourly concentration
```

For example:

```text
Birch hourly values:

00:00  2
01:00  4
02:00  7
...
12:00  23
...
20:00  8

Daily value:

23
```

The daily value is then converted into the Domoticz Alert level.

---

# Data Source

The plugin uses:

**Open-Meteo Air Quality API**

with the:

**CAMS European Air Quality Forecast**

domain.

The API endpoint is:

```text
https://air-quality-api.open-meteo.com/v1/air-quality
```

The request contains:

```text
latitude
longitude
hourly pollen variables
timezone=auto
forecast_days=4
domains=cams_europe
```

The plugin currently requests four forecast days but only publishes:

```text
Today
Tomorrow
```

The additional forecast days are available internally for future functionality.

---

# Requirements

## Domoticz

A Domoticz installation with Python plugin support.

The plugin is designed for current Domoticz Python plugin APIs.

## Python

The plugin uses Python 3 and the Python standard library only.

No external Python packages are required.

The following standard-library modules are used:

```text
json
urllib
dataclasses
time
```

Therefore:

```text
requirements.txt
```

does not need any external dependencies.

---

# Installation

Clone the repository into the Domoticz plugins directory:

```bash
cd /srv/domoticz/plugins

git clone \
    git@github.com:janreimen/Domoticz-Pollen-Forecast.git \
    Domoticz-Pollen-Forecast
```

Alternatively, copy the plugin directory manually:

```text
/srv/domoticz/plugins/Domoticz-Pollen-Forecast/
```

The directory must contain at least:

```text
plugin.py
api.py
config.py
devices.py
pollen.py
translations.py
```

Restart Domoticz:

```bash
sudo systemctl restart domoticz
```

---

# Configuration

After restarting Domoticz:

1. Open **Setup**
2. Open **Hardware**
3. Add the plugin
4. Select **Pollen Forecast**
5. Configure the parameters

## Latitude

Your geographical latitude.

Example:

```text
49.6116
```

The default is Luxembourg City.

## Longitude

Your geographical longitude.

Example:

```text
6.1319
```

## Language

Available languages:

```text
en
lb
de
fr
nl
```

The Domoticz hardware configuration provides a human-readable selection.

## Refresh interval

Available values:

```text
30 minutes
60 minutes
3 hours
6 hours
```

The default is:

```text
60 minutes
```

## Debug

Enable debug logging when troubleshooting.

```text
Off
On
```

---

# Example Configuration

For Luxembourg City:

```text
Latitude:          49.6116
Longitude:          6.1319
Language:           English
Refresh interval:   60 minutes
Debug:              Off
```

---

# Architecture

The plugin is intentionally split into small modules.

```text
Domoticz
    │
    ├── Parameters
    │       │
    │       ▼
    │   config.py
    │
    ├── Devices
    │       │
    │       ▼
    │   devices.py
    │       │
    │       ├── pollen.py
    │       └── translations.py
    │
    └── plugin.py
            │
            ▼
         api.py
            │
            ▼
       Open-Meteo
            │
            ▼
       CAMS forecast
```

## `plugin.py`

Responsible for:

* Domoticz lifecycle
* startup
* heartbeat
* scheduling
* orchestration
* error handling

It does not contain the pollen calculation logic.

## `config.py`

Responsible for:

* reading Domoticz parameters
* validating latitude
* validating longitude
* validating language
* validating refresh interval
* handling debug mode

## `api.py`

Responsible for:

* constructing the Open-Meteo request
* performing the HTTP request
* validating the API response
* discovering pollen variables
* converting hourly data into daily data

## `pollen.py`

Responsible for:

* pollen definitions
* pollen thresholds
* level calculation
* identification of pollen API variables

## `devices.py`

Responsible for:

* creating Domoticz devices
* assigning deterministic unit numbers
* converting pollen levels to Domoticz `Alert` values
* updating the devices

## `translations.py`

Responsible for:

* language strings
* pollen names
* alert-level names
* Today / Tomorrow labels

---

# Error Handling

A failed API update must not cause the plugin to repeatedly retry every Domoticz heartbeat.

If an update fails:

```text
API request
    │
    ├── success → update devices
    │
    └── failure → log error
                    │
                    └── wait for next configured interval
```

The plugin therefore records the failed update time and waits for the normal refresh interval.

---

# Debug Logging

Enable the `Debug` parameter in the Domoticz hardware configuration.

The plugin then reports information such as:

```text
PollenForecast: Starting version 0.2.0-alpha
PollenForecast: Location: 49.611600, 6.131900
PollenForecast: Language: en
PollenForecast: Refresh interval: 60 minutes
PollenForecast: Updating pollen forecast
PollenForecast: API: GET ...
PollenForecast: API: Pollen variables returned by API: ...
PollenForecast: Devices: today birch_pollen: concentration=...
```

To monitor the plugin:

```bash
journalctl -u domoticz -f | grep -E 'Pollen'
```

Or:

```bash
journalctl -u domoticz -f
```

---

# Testing Before Restarting Domoticz

Always perform a Python syntax check after modifying the plugin.

From the plugin directory:

```bash
cd /srv/domoticz/plugins/Domoticz-Pollen-Forecast
```

Run:

```bash
python3 -m py_compile \
    plugin.py \
    config.py \
    api.py \
    pollen.py \
    devices.py \
    translations.py
```

A successful check produces no output.

---

# Testing the Translation System

Run:

```bash
python3 -c "
from translations import get_translation

t = get_translation('de')

print(t['today'])
print(t['tomorrow'])
print(t['levels'][4])
print(t['pollen']['birch_pollen'])
"
```

Expected output:

```text
Heute
Morgen
Hoch
Birke
```

---

# Testing Pollen Levels

Run:

```bash
python3 -c "
from pollen import level_for

print(level_for('alder_pollen', 0))
print(level_for('alder_pollen', 10))
print(level_for('alder_pollen', 20))
print(level_for('alder_pollen', 60))
"
```

Expected:

```text
1
2
3
4
```

Test no data:

```bash
python3 -c "
from pollen import level_for

print(level_for('alder_pollen', None))
"
```

Expected:

```text
0
```

---

# Testing the API

The plugin can be tested against the real Open-Meteo API by instantiating the API class.

Example:

```bash
python3 -c "
from api import PollenApi

api = PollenApi(
    latitude=49.6116,
    longitude=6.1319,
    debug=True,
    log_fn=print,
)

data = api.fetch()
days = api.build_daily_data(data)

for day in days[:2]:
    print(day)
"
```

This requires network access from the Domoticz host.

---

# Updating the Plugin

For a Git installation:

```bash
cd /srv/domoticz/plugins/Domoticz-Pollen-Forecast

git status
git pull
```

Then check syntax:

```bash
python3 -m py_compile \
    plugin.py \
    config.py \
    api.py \
    pollen.py \
    devices.py \
    translations.py
```

Restart Domoticz:

```bash
sudo systemctl restart domoticz
```

Monitor:

```bash
journalctl -u domoticz -f | grep -E 'Pollen'
```

---

# Device Model Compatibility

The project is currently in the alpha stage.

The device model is:

```text
12 Alert devices
```

with:

```text
6 species × 2 days
```

The device model may change during the `0.x-alpha` development phase.

Once the project reaches:

```text
1.0.0
```

the intention is to treat the device model as stable.

Existing installations should therefore be treated as development installations until the first stable release.

---

# Automation Examples

Because every pollen species is represented by a native Domoticz Alert device, automation can use the numerical alert level directly.

For example:

```text
Birch Today
nValue = 4
```

represents:

```text
High
Red
```

A Domoticz automation can therefore trigger on the device state without parsing text.

Conceptually:

```text
IF Birch Today >= High
THEN send notification
```

or:

```text
IF Grass Today >= Medium
THEN enable air purifier
```

The exact automation syntax depends on the Domoticz automation mechanism being used.

---

# Future Extensions

Possible future functionality includes:

* additional pollen species
* additional forecast days
* concentration sensors
* numerical concentration values
* configurable pollen thresholds
* configurable notification levels
* configurable species
* pollen forecast history
* dashboard integration
* Home Assistant MQTT discovery
* per-species concentration devices
* configurable device naming
* API response caching
* API retry/backoff handling

These should only be introduced without unnecessarily changing the established device model once the project approaches `1.0.0`.

---

# Development

The project is structured so that individual components can be tested independently.

Recommended development order:

```text
pollen.py
    ↓
api.py
    ↓
devices.py
    ↓
translations.py
    ↓
plugin.py
```

When changing the device model, update:

1. `devices.py`
2. `translations.py`
3. `plugin.py`
4. tests
5. documentation
6. changelog

before creating the release.

---

# Repository Structure

The planned repository structure is:

```text
Domoticz-Pollen-Forecast/
│
├── plugin.py
├── api.py
├── config.py
├── pollen.py
├── devices.py
├── translations.py
│
├── tests/
│
├── README.md
├── CHANGELOG.md
├── DEPLOY.md
├── DEVELOPMENT.md
├── TESTING.md
├── RELEASE.md
├── API.md
├── SECURITY.md
├── CONTRIBUTING.md
│
├── requirements.txt
├── VERSION
├── LICENSE
└── .gitignore
```

---

# Dependencies

The plugin deliberately uses only the Python standard library.

Therefore there are currently no external Python dependencies.

`requirements.txt` is intentionally empty apart from documentation.

For example:

```text
# No external Python dependencies.
# The plugin uses Python's standard library only.
```

---

# Privacy

The plugin sends the configured geographical coordinates to the Open-Meteo API.

The coordinates are required to obtain the forecast for the configured location.

No account or API key is required by the plugin.

The plugin does not collect personal information.

The plugin does not implement remote control functionality.

---

# Network Access

The plugin requires outbound HTTPS access to:

```text
air-quality-api.open-meteo.com
```

Port:

```text
443/TCP
```

No inbound network connection is required by the plugin.

---

# Security

The plugin:

* uses HTTPS for API communication
* does not require credentials
* does not execute remote code
* does not install external Python packages
* does not expose an HTTP server
* does not accept inbound network connections

Security issues should be reported privately before public disclosure where possible.

See:

```text
SECURITY.md
```

for the project's security policy.

---

# API Limitations

The availability and content of pollen data depends on the Open-Meteo/CAMS data source.

The plugin does not generate pollen forecasts itself.

If a pollen variable is missing or contains no usable data, the corresponding Domoticz device is set to:

```text
nValue = 0
```

which represents:

```text
No data
```

This is intentionally different from:

```text
nValue = 1
```

which represents:

```text
None
```

---

# Troubleshooting

## Plugin does not start

Check the Domoticz log:

```bash
journalctl -u domoticz -n 100 --no-pager
```

Look for:

```text
Pollen:
```

Then run:

```bash
python3 -m py_compile \
    plugin.py \
    config.py \
    api.py \
    pollen.py \
    devices.py \
    translations.py
```

---

## Devices are not created

Enable debug mode and check:

```bash
journalctl -u domoticz -f | grep -E 'Pollen'
```

The plugin should report the creation of the devices.

---

## All devices show `No data`

Check the API response:

```bash
python3 -c "
from api import PollenApi

api = PollenApi(
    49.6116,
    6.1319,
    debug=True,
    log_fn=print,
)

data = api.fetch()

print(data['hourly'].keys())
"
```

The response should contain pollen variables.

---

## API request fails

Check outbound HTTPS connectivity:

```bash
curl -I \
    https://air-quality-api.open-meteo.com/v1/air-quality
```

The plugin itself uses Python's HTTPS implementation and does not depend on `curl`.

---

## Wrong language

Check the Domoticz hardware configuration.

Supported language codes are:

```text
en
lb
de
fr
nl
```

Unsupported values automatically fall back to English.

---

# License

See:

```text
LICENSE
```

for the complete license text.

---

# Author

**4D, janreimen**

GitHub:

`janreimen/Domoticz-Pollen-Forecast`

---

# Data Source and Attribution

Pollen forecast data is obtained through the Open-Meteo Air Quality API and its CAMS European Air Quality Forecast data source.

Please consult the Open-Meteo documentation and the applicable CAMS data terms for current attribution and usage requirements.

---

# Version History

## 0.2.0-alpha

Current development release.

Major architecture change:

* individual pollen devices
* separate Today / Tomorrow devices
* native Domoticz Alert device type
* numerical pollen levels
* native Domoticz alert colours
* removal of cumulative pollen text as the primary device model
* modular configuration
* modular API client
* modular pollen definitions
* multilingual device names

Device model:

```text
6 pollen species × 2 forecast days = 12 Alert devices
```

---

# Roadmap

## 0.2.x-alpha

Focus:

* stabilize the new device model
* validate Open-Meteo pollen variables
* improve testing
* verify all translations
* verify Domoticz Alert behaviour
* improve error handling

## 0.3.x-alpha

Potential focus:

* additional species
* configurable thresholds
* improved API diagnostics
* additional tests

## 0.x-beta

Focus:

* real-world installations
* upgrade testing
* device model compatibility
* documentation
* long-term API reliability

## 1.0.0

First stable release.

The goal is to have:

* stable device units
* documented upgrade behaviour
* stable configuration
* stable translations
* tested API handling
* tested Domoticz behaviour

---

# Contributing

Contributions are welcome.

Before submitting changes:

1. Keep the plugin free of unnecessary external dependencies.
2. Keep modules focused on one responsibility.
3. Run the Python syntax checks.
4. Test against a real Domoticz installation when changing device behaviour.
5. Update documentation when changing configuration or devices.
6. Update `CHANGELOG.md`.
7. Do not silently change existing device units during a stable release.

For development information see:

```text
DEVELOPMENT.md
```

For release procedures see:

```text
RELEASE.md
```

---

# Quick Start

For an existing installation:

```bash
cd /srv/domoticz/plugins/Domoticz-Pollen-Forecast

python3 -m py_compile \
    plugin.py \
    config.py \
    api.py \
    pollen.py \
    devices.py \
    translations.py

sudo systemctl restart domoticz

journalctl -u domoticz -f | grep -E 'Pollen'
```

After successful startup, the plugin should provide:

```text
Alder Today
Alder Tomorrow
Birch Today
Birch Tomorrow
Grass Today
Grass Tomorrow
Mugwort Today
Mugwort Tomorrow
Olive Today
Olive Tomorrow
Ragweed Today
Ragweed Tomorrow
```

with each device using the native Domoticz Alert levels:

```text
0 = No data / Grey
1 = None    / Green
2 = Low     / Yellow
3 = Medium  / Orange
4 = High    / Red
```

