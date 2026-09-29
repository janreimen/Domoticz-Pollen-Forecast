# Deployment Guide

## Domoticz Pollen Forecast

This document describes how to install, configure, update, verify, and remove the **Domoticz Pollen Forecast** plugin.

Current version:

```text
0.2.0-beta
```

The plugin uses only the Python standard library and does not require additional Python packages.

---

## 1. Requirements

### Domoticz

A current Domoticz installation with Python plugin support is required.

The plugin is intended for Domoticz installations using the Python plugin framework.

### Python

The plugin uses Python 3 and the Python standard library.

No additional packages are required.

The following standard-library modules are used:

```text
dataclasses
json
time
urllib.parse
urllib.request
```

### Network access

The Domoticz host must be able to access:

```text
https://air-quality-api.open-meteo.com
```

over HTTPS.

DNS resolution and outbound HTTPS connectivity must be available.

---

## 2. Plugin Directory

Domoticz Python plugins are normally installed below:

```text
<domoticz userdata>/plugins/
```

The exact path depends on the Domoticz installation.

For example:

```text
/opt/domoticz/userdata/plugins/
```

or:

```text
/var/lib/domoticz/plugins/
```

Use the plugin directory configured by your Domoticz installation.

---

## 3. Repository

The project repository is:

```text
https://github.com/janreimen/Domoticz-Pollen-Forecast
```

Clone the repository directly into the Domoticz plugin directory.

Example:

```bash
cd /opt/domoticz/userdata/plugins

git clone \
    https://github.com/janreimen/Domoticz-Pollen-Forecast.git \
    PollenForecast
```

The resulting structure should be:

```text
plugins/
└── PollenForecast/
    ├── plugin.py
    ├── config.py
    ├── api.py
    ├── pollen.py
    ├── devices.py
    └── translations.py
```

The directory name does not have to match the repository name, but:

```text
PollenForecast
```

is recommended because it clearly identifies the Domoticz plugin.

---

## 4. Installing from a Release

For a reproducible installation, a released version can be checked out instead of using the development branch.

Example:

```bash
cd /opt/domoticz/userdata/plugins

git clone \
    https://github.com/janreimen/Domoticz-Pollen-Forecast.git \
    PollenForecast

cd PollenForecast

git checkout 0.2.0-beta
```

If the project uses a release tag with a `v` prefix, use:

```bash
git checkout v0.2.0-beta
```

The actual tag name should always be verified against the GitHub release.

---

## 5. Verify the Installation

Before restarting Domoticz, verify that the plugin files are present:

```bash
cd /opt/domoticz/userdata/plugins/PollenForecast

ls -la
```

Expected core files:

```text
plugin.py
config.py
api.py
pollen.py
devices.py
translations.py
```

---

## 6. Python Syntax Check

The plugin can be checked for Python syntax without running Domoticz.

From the plugin directory:

```bash
python3 -m py_compile \
    plugin.py \
    config.py \
    api.py \
    pollen.py \
    devices.py \
    translations.py
```

A successful command produces no output and returns exit code `0`.

You can verify the exit status with:

```bash
echo $?
```

Expected:

```text
0
```

---

## 7. File Ownership and Permissions

The Domoticz service account must be able to read the plugin files.

Check ownership:

```bash
ls -la /opt/domoticz/userdata/plugins/PollenForecast
```

If Domoticz runs as a dedicated user, make sure that user has read and execute access to the directory and read access to the Python files.

Do not make the plugin world-writable.

Avoid using:

```bash
chmod -R 777 PollenForecast
```

This is unnecessary and weakens the security of the installation.

---

## 8. Restart Domoticz

After installing the plugin, restart Domoticz.

For a systemd installation:

```bash
sudo systemctl restart domoticz
```

Then verify the service:

```bash
sudo systemctl status domoticz --no-pager
```

The Domoticz service should return to an active state.

---

## 9. Add the Hardware

Open the Domoticz web interface.

Navigate to:

```text
Setup
    → Hardware
```

Add a new hardware entry and select:

```text
Pollen Forecast
```

The exact appearance of the hardware list depends on the Domoticz version.

---

## 10. Plugin Configuration

The plugin provides the following configuration parameters.

| Parameter        | Description               | Default      |
| ---------------- | ------------------------- | ------------ |
| Latitude         | Forecast latitude         | `49.6116`    |
| Longitude        | Forecast longitude        | `6.1319`     |
| Language         | Display language          | `en`         |
| Refresh interval | API update interval       | `60` minutes |
| Debug            | Enable diagnostic logging | `Off`        |

Supported languages:

```text
en
lb
de
fr
nl
```

---

## 11. Location

Enter the latitude and longitude for the location for which the pollen forecast is required.

Example:

```text
Latitude:
49.6116

Longitude:
6.1319
```

The coordinates are sent to the Open-Meteo API.

The plugin does not perform address lookup or geocoding.

---

## 12. Refresh Interval

The available refresh intervals are:

```text
30 minutes
60 minutes
3 hours
6 hours
```

The plugin enforces a minimum interval of:

```text
30 minutes
```

The default is:

```text
60 minutes
```

A shorter interval is not supported by the current configuration model.

---

## 13. Language

The following languages are currently supported:

| Code | Language       |
| ---- | -------------- |
| `en` | English        |
| `lb` | Lëtzebuergesch |
| `de` | Deutsch        |
| `fr` | Français       |
| `nl` | Nederlands     |

The language affects the names and displayed level text of the Domoticz devices.

It does not affect the API request.

---

## 14. Debug Mode

Debug mode can be enabled during installation or troubleshooting.

Set:

```text
Debug = On
```

The plugin then provides additional log messages.

These include:

* startup information
* configured location
* selected language
* refresh interval
* API request information
* pollen variables returned by the API
* daily pollen processing
* Domoticz device updates

Debug mode should normally be disabled after troubleshooting.

---

## 15. Created Devices

After the first successful startup, the plugin creates twelve native Domoticz `Alert` devices.

| Unit | Device  | Forecast |
| ---: | ------- | -------- |
|    1 | Alder   | Today    |
|    2 | Alder   | Tomorrow |
|    3 | Birch   | Today    |
|    4 | Birch   | Tomorrow |
|    5 | Grass   | Today    |
|    6 | Grass   | Tomorrow |
|    7 | Mugwort | Today    |
|    8 | Mugwort | Tomorrow |
|    9 | Olive   | Today    |
|   10 | Olive   | Tomorrow |
|   11 | Ragweed | Today    |
|   12 | Ragweed | Tomorrow |

The actual device names depend on the configured language.

---

## 16. Alert Levels

The devices use native Domoticz `Alert` values.

| `nValue` | Meaning |
| -------: | ------- |
|      `0` | No data |
|      `1` | None    |
|      `2` | Low     |
|      `3` | Medium  |
|      `4` | High    |

This allows Domoticz events and scripts to use the numeric value directly.

For example:

```text
nValue >= 3
```

can be used to detect a medium or high pollen level.

---

## 17. First Update

The plugin performs an update during `onStart()`.

Therefore, after adding the hardware, it should immediately attempt to retrieve the pollen forecast.

The Domoticz log should contain messages similar to:

```text
PollenForecast: Starting version 0.2.0-beta
```

and, when debug mode is enabled:

```text
PollenForecast: Location: 49.611600, 6.131900
PollenForecast: Language: en
PollenForecast: Refresh interval: 60 minutes
PollenForecast: Updating pollen forecast
```

A successful update should end with a message similar to:

```text
PollenForecast: Pollen forecast updated successfully
```

---

## 18. Checking the Domoticz Log

For a systemd-based installation:

```bash
sudo journalctl -u domoticz -f
```

Then restart the plugin or Domoticz and observe the output.

For a limited recent log:

```bash
sudo journalctl -u domoticz --since "10 minutes ago"
```

To filter for the plugin:

```bash
sudo journalctl -u domoticz --since "10 minutes ago" \
    | grep PollenForecast
```

---

## 19. API Connectivity Test

If the plugin reports an API connection problem, test HTTPS connectivity independently.

For example:

```bash
curl -I \
    https://air-quality-api.open-meteo.com/v1/air-quality
```

An HTTP response confirms that the host can reach the Open-Meteo endpoint.

A successful connection alone does not guarantee that a correctly formed pollen request will succeed.

---

## 20. Test the Complete API Request

A complete request can be tested with:

```bash
curl -sS \
    'https://air-quality-api.open-meteo.com/v1/air-quality?latitude=49.6116&longitude=6.1319&hourly=alder_pollen,birch_pollen,grass_pollen,mugwort_pollen,olive_pollen,ragweed_pollen&timezone=auto&forecast_days=4&domains=cams_europe'
```

The response should contain an `hourly` object and a `time` array.

---

## 21. Updating the Plugin

Before updating, check the currently installed version.

From the plugin directory:

```bash
git status
git describe --tags --always
```

If the installation contains local modifications, inspect them before pulling updates:

```bash
git status
git diff
```

Do not overwrite local modifications without understanding what they contain.

---

## 22. Update from Git

For an installation tracking a release or branch:

```bash
cd /opt/domoticz/userdata/plugins/PollenForecast

git fetch --tags

git pull --ff-only
```

Using:

```text
--ff-only
```

prevents Git from silently creating a merge commit on the production installation.

---

## 23. Update to a Specific Release

To install a specific release:

```bash
cd /opt/domoticz/userdata/plugins/PollenForecast

git fetch --tags

git checkout 0.2.0-beta
```

If the repository uses a `v` prefix:

```bash
git checkout v0.2.0-beta
```

Verify:

```bash
git describe --tags --always
```

---

## 24. Validate After an Update

Run the syntax check again:

```bash
python3 -m py_compile \
    plugin.py \
    config.py \
    api.py \
    pollen.py \
    devices.py \
    translations.py
```

Then restart Domoticz:

```bash
sudo systemctl restart domoticz
```

Monitor the log:

```bash
sudo journalctl -u domoticz -f
```

Check that:

1. Domoticz starts normally.
2. The Pollen Forecast plugin loads.
3. The plugin creates or finds its devices.
4. The API request succeeds.
5. Today and tomorrow receive updated values.

---

## 25. Device Persistence During Updates

The plugin uses fixed Domoticz unit numbers.

The current mapping is:

```text
1  Alder Today
2  Alder Tomorrow
3  Birch Today
4  Birch Tomorrow
5  Grass Today
6  Grass Tomorrow
7  Mugwort Today
8  Mugwort Tomorrow
9  Olive Today
10 Olive Tomorrow
11 Ragweed Today
12 Ragweed Tomorrow
```

Do not manually delete these devices before a normal plugin update.

The plugin will find existing devices by unit number and update them.

---

## 26. Version Changes and Device Compatibility

The plugin is currently:

```text
0.2.0-beta
```

The device model is still considered subject to change during the `0.x` development phase.

A future release may:

* add pollen species
* remove pollen species
* change device names
* change device units
* change alert handling
* change translations
* change configuration parameters

Such changes must be documented in:

```text
CHANGELOG.md
```

before a release.

---

## 27. Removing the Plugin

To remove the plugin cleanly:

### 1. Stop or disable the hardware

In Domoticz:

```text
Setup
    → Hardware
```

Remove or disable the Pollen Forecast hardware entry.

### 2. Remove the plugin directory

For a Git installation:

```bash
cd /opt/domoticz/userdata/plugins

rm -rf PollenForecast
```

Only run this command after confirming the directory is the correct plugin directory.

### 3. Restart Domoticz

```bash
sudo systemctl restart domoticz
```

---

## 28. Removing Created Devices

Removing the plugin files does not necessarily remove the Domoticz devices that were previously created.

If the devices are no longer required, remove them through the Domoticz interface after removing the hardware.

Before deleting devices, verify that no Domoticz events, scripts, dashboards, or automations

