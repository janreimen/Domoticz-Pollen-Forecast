# Testing

**Version:** 0.2.1-alpha

This document describes the minimum validation procedure before installing or releasing the plugin.

## 1. Syntax validation

From the plugin directory:

```bash
python3 -m py_compile     plugin.py     config.py     api.py     pollen.py     devices.py     translations.py
```

No output indicates successful compilation.

## 2. Compile all Python files

```bash
python3 -m compileall -q .
```

## 3. Git checks

```bash
git diff --check
git status
```

Do not commit generated files:

```text
__pycache__/
*.py[cod]
```

## 4. Location validation

Test valid examples:

```text
6.246450,49.714753
177.33,-30.23
-180,90
180,-90
```

Test invalid examples:

```text
180.1,0
-180.1,0
0,90.1
0,-90.1
0
abc,49.7
49.7,6.2
```

The last example is syntactically numeric but is interpreted according to the new `longitude,latitude` contract.

## 5. Allergen selection

Test:

```text
blank
```

Expected:

```text
alder,birch,grass,mugwort,olive,ragweed
```

Test:

```text
alder
```

Expected: one selected allergen and no selected-pollen aggregate requirement.

Test:

```text
alder,birch
```

Expected: selected-pollen aggregate devices are created/updated, and only Alder/Birch individual devices are created/updated. Grass, Mugwort, Olive and Ragweed are not created.

Test:

```text
ALDER, Birch, grass
```

Expected: normalized and deduplicated.

Test:

```text
alder,alder,birch
```

Expected:

```text
alder,birch
```

Invalid values must be reported rather than silently accepted.

## 6. Aggregate rounding

For selected `nValue`s:

```text
2, 3
```

average:

```text
2.5
```

expected result:

```text
3
```

For:

```text
2, 2, 3
```

average:

```text
2.333...
```

expected result:

```text
2
```

For:

```text
1, 2
```

average:

```text
1.5
```

expected result:

```text
2
```

## 7. Global situation

Example:

```text
Alder  = 1
Birch  = 2
Grass  = 4
Mugwort = 1
Olive  = 0
Ragweed = 2
```

Expected global level:

```text
4
```

The global level must not change when the Mode4 allergen selection changes.

## 8. API test

A minimal API test can be run without Domoticz:

```bash
python3 - <<'PY'
from api import PollenApi

api = PollenApi(
    latitude=49.714753,
    longitude=6.246450,
    debug=True,
    log_fn=print,
)

data = api.fetch()
days = api.build_daily_data(data)

print("Forecast days:", len(days))

for day in days[:2]:
    print(day["date"])
    print(day["values"])
PY
```

The API should return at least today and tomorrow.

## 9. Translation check

Verify all configured languages contain:

- today
- tomorrow
- selected pollen
- no data
- levels
- pollen labels

Current languages:

```text
en lb de fr nl es pt ro it pl cs bg hu sv sk hr sl sr fi no da el
```

## 10. Domoticz integration test

After static checks succeed:

1. Install/update the plugin.
2. Restart Domoticz.
3. Create/configure the hardware plugin.
4. Verify the location is accepted.
5. Verify the selected language.
6. Verify individual pollen devices.
7. Verify selected-pollen aggregate devices when applicable.
8. Verify global pollen situation devices.
9. Verify today's and tomorrow's values.
10. Enable Debug temporarily if diagnostics are needed.

## 11. Regression checks

Verify that:

- API errors do not crash the plugin.
- Missing pollen values produce level 0.
- Unknown `_pollen` API variables do not crash processing.
- Existing fixed unit numbers remain unchanged.
- Only selected allergens are created and updated; deselected existing devices are not deleted or updated.
- Changing Mode4 does not change the global situation.
- Changing language changes device labels without changing calculations.
