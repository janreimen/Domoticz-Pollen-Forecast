Domoticz Pollen Forecast

Version: 0.2.2
Author: 4D, blooesky, janreimen

A modular Domoticz Python plugin that retrieves pollen forecasts from the Open-Meteo Air Quality API using the CAMS European Air Quality Forecast.

No API key and no external Python packages are required.

Highlights

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
- Twenty-two supported languages:
  - English ("en")
  - Lëtzebuergesch ("lb")
  - Deutsch ("de")
  - Français ("fr")
  - Nederlands ("nl")
  - Español ("es")
  - Português ("pt")
  - Română ("ro")
  - Italiano ("it")
  - Polski ("pl")
  - Čeština ("cs")
  - Български ("bg")
  - Magyar ("hu")
  - Svenska ("sv")
  - Slovenčina ("sk")
  - Hrvatski ("hr")
  - Slovenščina ("sl")
  - Srpski ("sr")
  - Suomi ("fi")
  - Norsk ("no")
  - Dansk ("da")
  - Ελληνικά ("el")
- Standard-library-only implementation.
- Flexible location resolution using plugin configuration, Domoticz system coordinates, or configured defaults.

0.2.2 changes

Location resolution

Location handling has been extended so that an empty "Mode1" no longer requires Domoticz coordinates to be available.

The plugin resolves the effective location in this order:

1. Mode1 explicit location
2. Domoticz system location
3. Plugin .env default location
4. Error if none is valid

1. Explicit Mode1 location

When "Mode1" contains a value, it must be entered as:

longitude,latitude

Example:

6.1319,49.6116

The first value is validated as longitude:

-180 <= longitude <= 180

The second value is validated as latitude:

-90 <= latitude <= 90

An explicitly configured but invalid "Mode1" value is rejected. The plugin does not silently replace an invalid explicit location with another location.

2. Domoticz system location

When "Mode1" is empty, the plugin first attempts to use the location configured in Domoticz.

Current Domoticz installations may provide the system location through:

Settings["Location"] = "latitude;longitude"

For example:

49.71492;6.247261

The plugin converts this to the internal/API representation:

longitude,latitude

The Domoticz coordinates are therefore used automatically when available and valid.

3. ".env" default location

If "Mode1" is empty and Domoticz does not provide a valid location, the plugin can use configured default coordinates from the plugin environment:

POLLEN_DEFAULT_LONGITUDE=6.1319
POLLEN_DEFAULT_LATITUDE=49.6116

These values are fallback defaults only.

They do not override:

- an explicitly configured "Mode1" location, or
- a valid Domoticz system location.

See ".env.example" for the configuration template.

Location source logging

When debug logging is enabled, the effective location and its source are logged:

Location: longitude=6.247261, latitude=49.714920 (source: domoticz)

Possible sources are:

Source| Meaning
"plugin"| Explicit "Mode1" location
"domoticz"| Domoticz system location
"default"| ".env" fallback location

If none of these locations is valid, the plugin reports a configuration error and does not start the forecast update process.

Allergen selection

The allergen field accepts:

- blank: all six supported allergens
- a comma-separated list, for example:

alder,birch,grass

Valid values are:

alder
birch
grass
mugwort
olive
ragweed

Whitespace is ignored and duplicate values are removed.

When more than one allergen is selected, the plugin creates an aggregate pollen level for today and tomorrow.

The aggregate is calculated from the selected individual allergen "nValue"s:

sum(nValues) / number_of_selected_allergens

The result is rounded to the nearest integer with ".50" rounded upward.

The aggregate is independent from the global pollen situation.

Global pollen situation

The plugin also provides a general-information view of pollen conditions.

For each day, the global pollen situation is the maximum pollen level across all available supported pollen types. It is intentionally independent from the user's allergen selection.

This provides two different views:

- Selected pollen: personalized aggregate based on "Mode4".
- Global pollen situation: overall highest pollen level available for the day.

Devices

The fixed individual device layout is:

Unit| Pollen| Day
1| Alder| Today
2| Alder| Tomorrow
3| Birch| Today
4| Birch| Tomorrow
5| Grass| Today
6| Grass| Tomorrow
7| Mugwort| Today
8| Mugwort| Tomorrow
9| Olive| Today
10| Olive| Tomorrow
11| Ragweed| Today
12| Ragweed| Tomorrow

Aggregate devices:

Unit| Purpose
100| Selected pollen Today
101| Selected pollen Tomorrow
110| Global pollen situation Today
111| Global pollen situation Tomorrow

The unit numbers are fixed internally to keep Domoticz automation references stable, but only the allergens selected in "Mode4" are created and updated.

For example, selecting:

alder,birch

creates and updates units 1-4, not units 5-12.

Existing devices for allergens that are later deselected are not deleted. They are simply no longer updated.

This prevents changes to the allergen selection from breaking existing Domoticz device references or automation configurations.

Alert levels

All Alert devices use:

nValue| Meaning
0| No data
1| None
2| Low
3| Medium
4| High

These values are directly usable in Domoticz automation.

Configuration

The plugin configuration consists of:

1. Location — "longitude,latitude" ("Mode1")
2. Language ("Mode2")
3. Refresh interval ("Mode3")
4. Allergens ("Mode4")
5. Debug ("Mode5")

Mode1 — Location

Optional location override in:

longitude,latitude

Example:

6.1319,49.6116

Leave the field empty to use:

Domoticz location

and, if that is unavailable or invalid:

POLLEN_DEFAULT_LONGITUDE
POLLEN_DEFAULT_LATITUDE

from the plugin environment.

Mode2 — Language

The forecast text and device names can be presented in one of the supported languages:

en
lb
de
fr
nl
es
pt
ro
it
pl
cs
bg
hu
sv
sk
hr
sl
sr
fi
no
da
el

English ("en") is used if an unsupported language is configured.

Mode3 — Refresh interval

The forecast refresh interval is configured in minutes.

The minimum supported interval is:

30

Example:

60

for an hourly update.

Mode4 — Allergens

Comma-separated list of allergens:

alder,birch,grass

Leave empty to use all six supported allergens.

Mode5 — Debug

Enable debug logging when required:

1

Disable it with:

0

Example configuration:

Location: 6.246450,49.714753
Language: en
Refresh: 60
Allergens: birch,grass
Debug: 0

Environment defaults

The optional ".env" configuration can define the fallback location:

POLLEN_DEFAULT_LONGITUDE=6.1319
POLLEN_DEFAULT_LATITUDE=49.6116

These values are only used when:

1. "Mode1" is empty, and
2. Domoticz does not provide a valid system location.

The expected precedence is:

Mode1
  ↓
Domoticz system location
  ↓
POLLEN_DEFAULT_* environment values

Do not commit a private ".env" file containing local configuration or secrets.

Use ".env.example" as the repository template.

Data source

Open-Meteo Air Quality API with the CAMS European domain is used for pollen forecast data.

The plugin requests four forecast days internally and exposes today and tomorrow.

PyPluginStore compatibility

The repository is structured as a standard Domoticz Python plugin and keeps its plugin metadata embedded in "plugin.py".

The metadata identifies the project as:

PollenForecast

with version:

0.2.2

and authors:

4D, blooesky, janreimen

The metadata also points to the GitHub repository.

This allows Git-based plugin-store tooling such as PyPluginStore to identify the plugin and its version.

Requirements

- Domoticz with Python plugin support.
- Python 3.
- Network access to Open-Meteo.
- No third-party Python package.

Installation

Copy the plugin directory to the Domoticz plugins directory:

<domoticz>/plugins/Domoticz-Pollen-Forecast

Then restart Domoticz and add the hardware plugin from the Domoticz UI.

See "DEPLOY.md" (DEPLOY.md).

Development

See:

- "DEVELOPMENT.md" (DEVELOPMENT.md)
- "TESTING.md" (TESTING.md)
- "API.md" (API.md)
- "RELEASE.md" (RELEASE.md)

Troubleshooting

Mode1 is empty

An empty "Mode1" is valid.

The plugin will attempt:

Mode1
  ↓
Domoticz system coordinates
  ↓
.env defaults

If all three are unavailable or invalid, the plugin reports a location configuration error.

Explicit Mode1 location is rejected

Check that the value uses:

longitude,latitude

and not:

latitude,longitude

For Luxembourg, for example:

6.1319,49.6116

is valid.

Domoticz coordinates are not being used

Enable debug logging and check the reported location source.

The plugin expects the current Domoticz representation:

Settings["Location"] = "latitude;longitude"

For example:

49.71492;6.247261

The plugin converts this internally to:

longitude=6.247261
latitude=49.71492

".env" defaults are not being used

Verify that the environment contains both:

POLLEN_DEFAULT_LONGITUDE=6.1319
POLLEN_DEFAULT_LATITUDE=49.6116

Both values must be valid numeric coordinates.

Remember that ".env" defaults are only a fallback. A valid Domoticz system location takes precedence.

License

MIT. See "LICENSE" (LICENSE).
