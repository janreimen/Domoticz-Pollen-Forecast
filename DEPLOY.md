# Deployment

**Version:** 0.2.1-beta

## Requirements

- Domoticz with Python plugin support.
- Python 3.
- Network connectivity to Open-Meteo.
- No external Python packages.

## Installation directory

Example:

```text
/srv/domoticz/plugins/Domoticz-Pollen-Forecast
```

The directory must contain at least:

```text
plugin.py
config.py
api.py
pollen.py
devices.py
translations.py
```

## Install or update

From the Domoticz plugins directory:

```bash
cd /srv/domoticz/plugins
```

Clone:

```bash
git clone git@github.com:janreimen/Domoticz-Pollen-Forecast.git
```

Or update an existing checkout:

```bash
cd /srv/domoticz/plugins/Domoticz-Pollen-Forecast
git fetch origin
git checkout main
git pull --ff-only origin main
```

For a tagged release:

```bash
git fetch --tags
git checkout v0.2.1-beta
```

## File ownership

If Domoticz runs as a dedicated user, ensure that user can read the plugin files.

Example:

```bash
ls -la /srv/domoticz/plugins/Domoticz-Pollen-Forecast
```

## Pre-restart validation

Before restarting Domoticz:

```bash
cd /srv/domoticz/plugins/Domoticz-Pollen-Forecast

python3 -m py_compile     plugin.py     config.py     api.py     pollen.py     devices.py     translations.py

git diff --check
```

Generated Python bytecode must not be committed:

```text
__pycache__/
*.py[cod]
```

## Domoticz restart

After installing a new plugin version, restart Domoticz so the plugin is loaded from the updated files.

The Domoticz documentation notes that plugin installation requires a Domoticz restart. See the Domoticz plugin documentation.

## Configuration

Configure the plugin from the Domoticz hardware/plugin UI.

### Location

Use:

```text
longitude,latitude
```

Example:

```text
6.246450,49.714753
```

Validation:

```text
-180 <= longitude <= 180
-90 <= latitude <= 90
```

### Language

Select one of the supported languages.

### Refresh interval

Available values:

```text
30 minutes
60 minutes
3 hours
6 hours
```

### Allergens

Blank:

```text
```

means all supported allergens.

A CSV list can be used:

```text
birch,grass
```

Valid values:

```text
alder,birch,grass,mugwort,olive,ragweed
```

### Debug

Debug is configured separately from the allergen field.

## Logs

The plugin writes messages using the Domoticz plugin logging mechanism.

Typical successful update:

```text
PollenForecast: Pollen forecast updated successfully (4 forecast days received)
```

## Troubleshooting

### Plugin does not appear

Check:

```bash
python3 -m py_compile plugin.py
```

and inspect the Domoticz log.

### API update fails

Test network access independently:

```bash
curl -I https://air-quality-api.open-meteo.com/
```

Then inspect the Domoticz plugin log with Debug enabled.

### Configuration rejected

Verify the location syntax:

```text
longitude,latitude
```

For example:

```text
6.246450,49.714753
```

Do not enter:

```text
latitude,longitude
```

### Old devices remain

Device units are deliberately stable for individual pollen devices, but only selected allergens are created and updated. Aggregate devices use separate fixed unit ranges.

For example, selecting `alder,birch` creates/updates individual units 1-4 plus the applicable aggregate/global units. Grass, Mugwort, Olive and Ragweed are not created. If they existed from an earlier configuration, they remain in Domoticz but are no longer updated.

Do not delete or recreate devices automatically as part of normal updates, because that could break existing Domoticz automation references.


## Location

For `0.2.1-beta`, Mode1 may be left empty. In that case the plugin automatically uses the latitude and longitude configured under Domoticz system settings. Enter `longitude,latitude` only when an explicit override is required.
