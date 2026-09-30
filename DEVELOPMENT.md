# Development

**Version:** 0.2.1-alpha

## Architecture

The plugin deliberately uses a modular architecture:

```text
plugin.py
    |
    +-- config.py
    |
    +-- api.py
    |
    +-- pollen.py
    |
    +-- devices.py
    |
    +-- translations.py
```

### plugin.py

Domoticz lifecycle integration:

- `onStart`
- `onStop`
- `onHeartbeat`

It coordinates configuration, API access and device updates.

### config.py

Responsible for:

- location parsing and validation
- language validation
- refresh interval
- allergen selection
- debug configuration

The location is entered as:

```text
longitude,latitude
```

### api.py

Responsible for:

- Open-Meteo HTTP requests
- JSON decoding
- response validation
- daily pollen aggregation
- discovery of returned `_pollen` variables

### pollen.py

Responsible for:

- pollen definitions
- thresholds
- concentration-to-level conversion
- known pollen keys

### devices.py

Responsible for:

- fixed individual device units
- selected-pollen aggregate devices
- global pollen situation devices
- Domoticz `Alert` updates

### translations.py

Contains all user-visible translations.

No translation logic should be embedded in the device implementation.

## Version

Current development version:

```text
0.2.1-alpha
```

Version consistency should be checked across:

- plugin XML metadata
- `VERSION`
- API User-Agent
- README
- CHANGELOG
- release documentation

## Location model

The unified location field uses:

```text
longitude,latitude
```

This ordering is intentional because the first component accepts the longitude range:

```text
-180..180
```

and the second component accepts the latitude range:

```text
-90..90
```

Internally, the API client receives named `latitude` and `longitude` arguments, avoiding ambiguity.

## Allergen model

Supported allergen identifiers:

```text
alder
birch
grass
mugwort
olive
ragweed
```

They map to API variables:

```text
alder_pollen
birch_pollen
grass_pollen
mugwort_pollen
olive_pollen
ragweed_pollen
```

The configuration stores the short allergen names. The pollen model stores API pollen keys.

## Device model

Individual devices use a fixed internal unit map:

```text
Alder    Today=1   Tomorrow=2
Birch    Today=3   Tomorrow=4
Grass    Today=5   Tomorrow=6
Mugwort  Today=7   Tomorrow=8
Olive    Today=9   Tomorrow=10
Ragweed  Today=11  Tomorrow=12
```

The complete map is intentionally stable, but only allergens selected in `Mode4` are created and updated. Existing devices for deselected allergens are not deleted.

Selected-pollen aggregate devices:

```text
100  Today
101  Tomorrow
```

Global pollen situation:

```text
110  Today
111  Tomorrow
```

## Global situation

The global situation is a general-information device model inspired by the upstream project, but implemented independently within this modular architecture.

It is not affected by the user's selected allergens.

The calculation is:

```text
max(all available supported pollen levels)
```

This is deliberately different from the selected-pollen aggregate:

```text
sum(selected nValues) / number of selected allergens
```

## Languages

Current target set:

```text
en lb de fr nl es pt ro it pl cs bg hu sv sk hr sl sr fi no da el sk hr sl sr fi no da el
```

New language additions should be added to:

1. `SUPPORTED_LANGUAGES` in `config.py`
2. plugin XML language options
3. `translations.py`
4. README documentation
5. tests when available

## Coding principles

- Prefer small, testable functions.
- Avoid duplicating configuration rules.
- Keep Domoticz-specific code in the plugin/device layer.
- Keep API transport separate from data processing.
- Do not add external dependencies without a documented reason.
- Do not silently guess invalid configuration.
- Preserve stable device units.
- Keep user-visible strings in `translations.py`.

## Compatibility

This is an alpha release.

Device creation and configuration behavior may still change before 1.0.0.

Existing Domoticz automation should not depend on experimental aggregate units until the device model is declared stable.
