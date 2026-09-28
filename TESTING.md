# Testing Guide

## Domoticz Pollen Forecast

This document describes how to test the **Domoticz Pollen Forecast** plugin.

The project is designed to be testable without a running Domoticz installation for most of its logic.

Current version:

```text
0.2.0-alpha
```

---

## 1. Testing Goals

Testing should verify:

* pollen threshold calculations
* API response parsing
* daily pollen aggregation
* missing and invalid API values
* unknown pollen variables
* translations
* Domoticz device mapping
* Domoticz Alert levels
* configuration handling
* Python syntax
* plugin integration on a real Domoticz installation

The tests should not depend on live Open-Meteo data.

---

## 2. Testing Philosophy

The plugin separates responsibilities into independent modules:

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

The preferred testing approach is therefore:

```text
Unit tests
    ↓
Module integration tests
    ↓
Static/syntax checks
    ↓
Optional live API test
    ↓
Real Domoticz test
```

---

## 3. Test Dependencies

The project intentionally uses the Python standard library only.

The test suite therefore uses:

```text
unittest
unittest.mock
```

No third-party test framework is required.

In particular, the project does not require:

```text
pytest
requests
httpx
```

or any other external Python package.

---

## 4. Supported Python Versions

The plugin targets Python 3.

The primary development environment should use the Python version supported by the target Domoticz installation.

The CI workflow should test the Python version selected by the project.

Before a release, the plugin should also be tested using the Python interpreter actually used by the production Domoticz installation.

Check the local version with:

```bash
python3 --version
```

---

## 5. Repository Test Structure

The recommended test structure is:

```text
tests/
├── __init__.py
├── test_pollen.py
├── test_translations.py
├── test_api.py
└── test_devices.py
```

Each test module should focus on one logical component.

---

## 6. Running All Tests

From the repository root:

```bash
python3 -m unittest discover -s tests -v
```

A successful test run should end with output similar to:

```text
----------------------------------------------------------------------
Ran XX tests in X.XXXs

OK
```

The exact number of tests depends on the current implementation.

---

## 7. Running a Single Test Module

For example:

```bash
python3 -m unittest tests.test_pollen -v
```

Translations:

```bash
python3 -m unittest tests.test_translations -v
```

API handling:

```bash
python3 -m unittest tests.test_api -v
```

Device handling:

```bash
python3 -m unittest tests.test_devices -v
```

---

## 8. Python Syntax Check

Before running the test suite, check all production Python files:

```bash
python3 -m py_compile \
    plugin.py \
    config.py \
    api.py \
    pollen.py \
    devices.py \
    translations.py
```

A successful command produces no output.

Check the exit status:

```bash
echo $?
```

Expected:

```text
0
```

---

# 9. Pollen Logic Tests

The `pollen.py` module contains the pollen definitions and concentration-to-level conversion.

These are deterministic functions and should have comprehensive unit tests.

---

## 9.1 Test No Data

`None` must produce level `0`.

Expected:

```text
level_for("grass_pollen", None)
    → 0
```

---

## 9.2 Test Zero Concentration

A concentration below `1.0` is classified as `None`.

Expected:

```text
level_for("grass_pollen", 0.0)
    → 1
```

---

## 9.3 Test Low Level

For grass pollen:

```text
1.0–10.0 → Low
```

Examples:

```text
1.0  → 2
5.0  → 2
10.0 → 2
```

---

## 9.4 Test Medium Level

For grass pollen:

```text
>10.0–30.0 → Medium
```

Examples:

```text
10.1 → 3
20.0 → 3
30.0 → 3
```

---

## 9.5 Test High Level

For grass pollen:

```text
>30.0 → High
```

Examples:

```text
30.1 → 4
50.0 → 4
100.0 → 4
```

---

## 9.6 Test Alder and Birch Thresholds

Alder and birch use:

```text
Low maximum:    16.0
Medium maximum: 50.0
```

Boundary tests should include:

```text
0.0   → None
0.99  → None
1.0   → Low
16.0  → Low
16.01 → Medium
50.0  → Medium
50.01 → High
```

---

## 9.7 Test Grass Thresholds

Grass uses:

```text
Low maximum:    10.0
Medium maximum: 30.0
```

Boundary tests should include:

```text
0.0   → None
0.99  → None
1.0   → Low
10.0  → Low
10.01 → Medium
30.0  → Medium
30.01 → High
```

---

## 9.8 Test Mugwort, Olive and Ragweed

These species use:

```text
Low maximum:    5.0
Medium maximum: 25.0
```

Boundary tests should include:

```text
0.0   → None
0.99  → None
1.0   → Low
5.0   → Low
5.01  → Medium
25.0  → Medium
25.01 → High
```

---

## 9.9 Test Invalid Concentrations

Invalid values must result in:

```text
0 = No data
```

Examples:

```text
None
"invalid"
object()
```

The test should verify that these values do not raise unexpected exceptions.

---

## 9.10 Test Numeric Strings

Numeric strings should be convertible by the current implementation.

For example:

```text
"5.0"
```

should behave like:

```text
5.0
```

Expected:

```text
level_for("grass_pollen", "5.0")
    → 2
```

---

## 10. Unknown Pollen Tests

The plugin supports detection of pollen variables using the:

```text
*_pollen
```

convention.

Test:

```text
is_pollen_key("new_pollen")
    → True
```

and:

```text
is_pollen_key("temperature")
    → False
```

---

## 10.1 Unknown Thresholds

Unknown pollen species currently use:

```text
Low maximum:    5.0
Medium maximum: 25.0
```

Test:

```text
level_for("new_pollen", 1.0)
    → 2
```

and:

```text
level_for("new_pollen", 10.0)
    → 3
```

and:

```text
level_for("new_pollen", 30.0)
    → 4
```

These defaults are provisional and should not be interpreted as official thresholds for newly discovered species.

---

# 11. Translation Tests

The translation module supports:

```text
en
lb
de
fr
nl
```

---

## 11.1 Supported Languages

Test that every supported language returns a translation dictionary:

```python
get_translation("en")
get_translation("lb")
get_translation("de")
get_translation("fr")
get_translation("nl")
```

---

## 11.2 Translation Structure

Every supported language should contain:

```text
today
tomorrow
unknown_pollen
no_data
levels
pollen
```

The test should verify that these keys exist.

---

## 11.3 Alert Levels

Every language must contain level translations for:

```text
0
1
2
3
4
```

---

## 11.4 Pollen Names

Every supported language should contain labels for:

```text
alder_pollen
birch_pollen
grass_pollen
mugwort_pollen
olive_pollen
ragweed_pollen
```

---

## 11.5 Invalid Language

An unsupported language should fall back to English.

Example:

```python
get_translation("xx")
```

must return the English translation dictionary.

---

# 12. API Tests

The API client must be tested without depending on the live Open-Meteo service.

Live API calls are unsuitable for deterministic unit tests because:

* forecast values change
* network connectivity can fail
* external services can change
* API availability is outside the test suite
* tests would be slower

Use mocked HTTP responses instead.

---

## 12.1 Successful API Response

Create a representative API response containing:

```text
hourly
time
alder_pollen
birch_pollen
grass_pollen
mugwort_pollen
olive_pollen
ragweed_pollen
```

Verify that:

```python
PollenApi.fetch()
```

returns a Python dictionary.

---

## 12.2 HTTP Error

Mock an HTTP response with a non-200 status.

The API client must raise an exception rather than silently accepting the response.

---

## 12.3 Invalid JSON

Return invalid JSON from the mocked HTTP response.

The API client must fail cleanly.

---

## 12.4 API Error Response

Test a response such as:

```json
{
  "error": true,
  "reason": "Example API error"
}
```

The client should raise an appropriate exception containing the API reason.

---

## 12.5 Missing Hourly Data

Test:

```json
{
  "latitude": 49.6116,
  "longitude": 6.1319
}
```

The client must reject the response because:

```text
hourly
```

is missing.

---

## 12.6 Missing Time Data

Test:

```json
{
  "hourly": {}
}
```

The client must reject the response because:

```text
time
```

is missing.

---

## 12.7 Null Pollen Values

Example:

```json
{
  "hourly": {
    "time": [
      "2026-09-28T00:00",
      "2026-09-28T01:00",
      "2026-09-28T02:00"
    ],
    "grass_pollen": [
      2.0,
      null,
      5.0
    ]
  }
}
```

The daily maximum must be:

```text
5.0
```

---

## 12.8 Invalid Pollen Values

Example:

```json
{
  "hourly": {
    "time": [
      "2026-09-28T00:00",
      "2026-09-28T01:00"
    ],
    "grass_pollen": [
      2.0,
      "invalid"
    ]
  }
}
```

The invalid value must be ignored.

The resulting maximum must remain:

```text
2.0
```

---

# 13. Daily Aggregation Tests

`build_daily_data()` converts hourly data into daily maximum values.

---

## 13.1 One Day

Given:

```text
00:00 → 1.0
01:00 → 5.0
02:00 → 3.0
```

the result must be:

```text
5.0
```

---

## 13.2 Multiple Days

Given:

```text
2026-09-28 00:00 → 2.0
2026-09-28 01:00 → 8.0
2026-09-29 00:00 → 3.0
2026-09-29 01:00 → 6.0
```

the resulting daily values must be:

```text
2026-09-28 → 8.0
2026-09-29 → 6.0
```

---

## 13.3 Missing Series

If a pollen series is missing from the API response, the resulting value should be:

```text
None
```

The API processing must not fail solely because an optional pollen series is missing.

---

## 13.4 Unknown Pollen Series

If the response contains:

```text
new_pollen
```

it should be recognized because it ends with:

```text
_pollen
```

and included in the processed daily data.

---

# 14. Device Tests

Device tests should not require a running Domoticz installation.

The Domoticz module should be mocked or replaced with a test double.

The tests should verify the behaviour of `PollenDevices`.

---

## 14.1 Device Creation

A fresh device collection should result in twelve devices being created.

Expected units:

```text
1
2
3
4
5
6
7
8
9
10
11
12
```

---

## 14.2 Existing Devices

If a unit already exists, the plugin must not create a duplicate device.

---

## 14.3 Unit Mapping

Verify the deterministic mapping:

```text
Alder:
    Today    → 1
    Tomorrow → 2

Birch:
    Today    → 3
    Tomorrow → 4

Grass:
    Today    → 5
    Tomorrow → 6

Mugwort:
    Today    → 7
    Tomorrow → 8

Olive:
    Today    → 9
    Tomorrow → 10

Ragweed:
    Today    → 11
    Tomorrow → 12
```

---

## 14.4 Alert Values

For a known concentration, verify that the correct `nValue` is written.

Example:

```text
Grass = 5.0
```

must produce:

```text
nValue = 2
```

---

## 14.5 No Data

A missing concentration:

```text
None
```

must result in:

```text
nValue = 0
```

---

## 14.6 Avoid Unnecessary Updates

If a device already contains the correct:

```text
nValue
sValue
```

the plugin should not issue another `Update()` call.

This avoids unnecessary Domoticz database/device updates.

---

# 15. Configuration Tests

The `config.py` module should be tested independently from Domoticz where practical.

---

## 15.1 Default Configuration

An empty parameter dictionary should result in:

```text
Latitude:
49.6116

Longitude:
6.1319

Language:
en

Refresh:
60 minutes

Debug:
False
```

---

## 15.2 Custom Location

Test custom coordinates:

```text
Mode1 = 49.7000
Mode2 = 6.2000
```

The resulting configuration should contain the corresponding floating-point values.

---

## 15.3 Invalid Coordinates

Invalid values should fall back to their configured defaults.

Example:

```text
Mode1 = invalid
```

must not cause an unhandled exception.

---

## 15.4 Language

Test each supported language:

```text
en
lb
de
fr
nl
```

---

## 15.5 Invalid Language

An unsupported language must fall back to:

```text
en
```

---

## 15.6 Refresh Interval

Test:

```text
30
60
180
360
```

and verify that the configured values are accepted.

Values below the supported minimum must be clamped to:

```text
30
```

---

## 15.7 Debug

Test:

```text
Mode5 = 0
```

produces:

```text
False
```

and:

```text
Mode5 = 1
```

produces:

```text
True
```

---

# 16. Plugin Integration Testing

The complete `plugin.py` requires the Domoticz Python plugin environment.

Therefore, the complete lifecycle should be tested on a real or dedicated test Domoticz installation.

The test environment should preferably not be the primary production Domoticz installation.

---

## 16.1 Integration Test Procedure

1. Install the plugin.
2. Restart Domoticz.
3. Add the Pollen Forecast hardware.
4. Configure a valid location.
5. Enable debug logging.
6. Wait for the initial update.
7. Inspect the Domoticz log.
8. Check all twelve devices.
9. Verify Today and Tomorrow.
10. Verify Alert levels.
11. Disable debug logging after testing.

---

# 17. Real API Test

A live API test may be performed manually.

Example:

```bash
curl -sS \
    'https://air-quality-api.open-meteo.com/v1/air-quality?latitude=49.6116&longitude=6.1319&hourly=alder_pollen,birch_pollen,grass_pollen,mugwort_pollen,olive_pollen,ragweed_pollen&timezone=auto&forecast_days=4&domains=cams_europe'
```

The response should contain:

```text
hourly
time
```

and the available pollen variables.

Live API tests are diagnostic tests and should not replace the mocked unit tests.

---

# 18. Network Failure Testing

The plugin should be tested with the API temporarily unavailable.

Possible test methods include:

* blocking outbound HTTPS temporarily
* using an invalid endpoint in a test environment
* mocking `urlopen()` to raise an exception

Expected behaviour:

```text
API request fails
       ↓
plugin logs update failure
       ↓
Domoticz remains running
       ↓
next scheduled update can retry
```

The plugin should not crash Domoticz because of a temporary API failure.

---

# 19. Malformed API Testing

Test malformed responses including:

```text
invalid JSON
missing hourly
missing time
missing pollen series
null values
non-numeric values
unexpected pollen variables
empty arrays
```

The plugin should handle these conditions without terminating the Domoticz process.

---

# 20. Regression Testing

Every bug fix should ideally receive a regression test.

The preferred process is:

```text
Bug discovered
      ↓
Reproduce with test
      ↓
Fix implementation
      ↓
Run regression test
      ↓
Run complete test suite
```

Do not rely solely on manually checking the original problem after the fix.

---

# 21. Test Before Commit

Before committing normal development changes:

```bash
python3 -m unittest discover -s tests -v
```

Then:

```bash
python3 -m py_compile \
    plugin.py \
    config.py \
    api.py \
    pollen.py \
    devices.py \
    translations.py
```

Then:

```bash
git status
```

---

# 22. Test Before Release

Before every release, run:

```bash
python3 -m unittest discover -s tests -v
```

followed by:

```bash
python3 -m py_compile \
    plugin.py \
    config.py \
    api.py \
    pollen.py \
    devices.py \
    translations.py
```

Then inspect:

```bash
git diff
git status
```

A release should not be created with unexpected changes.

See `RELEASE.md` for the complete release procedure.

---

# 23. Continuous Integration

The repository should run automated tests through GitHub Actions.

The CI workflow should:

1. check out the repository
2. install the selected Python version
3. run the unit tests
4. run Python syntax checks

The CI environment must not require:

* Domoticz
* a live Open-Meteo connection
* an API key
* external Python packages

This keeps CI deterministic.

---

# 24. Test Isolation

Tests must not modify:

* the production Domoticz database
* production devices
* production configuration
* external API data
* user files

API tests should use mocks.

Domoticz device tests should use test doubles.

---

# 25. Test Data

Test data should be deterministic.

Use fixed timestamps and fixed pollen concentrations.

For example:

```json
{
  "hourly": {
    "time": [
      "2026-09-28T00:00",
      "2026-09-28T01:00",
      "2026-09-29T00:00"
    ],
    "grass_pollen": [
      2.0,
      8.0,
      4.0
    ]
  }
}
```

Do not use the current date or current forecast values in unit tests.

---

# 26. Test Coverage Priorities

The most important areas to test are:

### High priority

```text
pollen level boundaries
daily aggregation
API response validation
missing values
device unit mapping
Domoticz Alert nValue
configuration parsing
```

### Medium priority

```text
translations
unknown pollen variables
debug logging
existing device handling
```

### Integration

```text
Domoticz startup
API connectivity
device creation
device updates
scheduled refresh
```

---

# 27. Manual Domoticz Test Checklist

Use this checklist when testing a release manually:

```text
[ ] Plugin appears in Domoticz hardware list
[ ] Hardware can be created
[ ] Latitude accepted
[ ] Longitude accepted
[ ] English works
[ ] Lëtzebuergesch works
[ ] Deutsch works
[ ] Français works
[ ] Nederlands works
[ ] Debug logging works
[ ] Initial API update succeeds
[ ] Alder Today created
[ ] Alder Tomorrow created
[ ] Birch Today created
[ ] Birch Tomorrow created
[ ] Grass Today created
[ ] Grass Tomorrow created
[ ] Mugwort Today created
[ ] Mugwort Tomorrow created
[ ] Olive Today created
[ ] Olive Tomorrow created
[ ] Ragweed Today created
[ ] Ragweed Tomorrow created
[ ] Alert levels are populated
[ ] No-data state works
[ ] Today updates correctly
[ ] Tomorrow updates correctly
[ ] Scheduled refresh works
[ ] Temporary API failure does not crash Domoticz
[ ] Plugin restarts correctly
[ ] Existing devices are reused
[ ] Debug mode can be disabled
```

---

# 28. Test Failure Investigation

When a test fails, first identify the layer involved.

```text
Test failure
    |
    +-- pollen.py
    |      → level/threshold logic
    |
    +-- api.py
    |      → HTTP/JSON/data processing
    |
    +-- translations.py
    |      → language data
    |
    +-- devices.py
    |      → Domoticz device model
    |
    +-- config.py
    |      → configuration parsing
    |
    +-- plugin.py
           → Domoticz lifecycle/integration
```

Avoid changing multiple unrelated modules to fix a single failing test.

---

# 29. Debugging Failed API Tests

When an API test fails, inspect:

1. mocked HTTP response
2. response status
3. JSON structure
4. `hourly`
5. `time`
6. pollen series
7. date grouping
8. numeric conversion
9. daily maximum calculation

The API client should not be modified merely to accommodate an invalid test fixture.

---

# 30. Debugging Device Tests

When a device test fails, inspect:

1. expected unit
2. pollen key
3. forecast day
4. concentration
5. calculated level
6. existing `nValue`
7. existing `sValue`
8. expected `Update()` call

The current mapping is:

```text
pollen index × 2 + day index + 1
```

where:

```text
Today    = day index 0
Tomorrow = day index 1
```

---

# 31. Clean Test Environment

Before a complete local test run, optionally remove Python cache directories:

```bash
find . \
    -type d \
    -name '__pycache__' \
    -prune \
    -exec rm -rf {} +
```

Then run:

```bash
python3 -m unittest discover -s tests -v
```

---

# 32. Release Test Record

For every published release, record at least:

```text
Version:
________________________

Python version:
________________________

Operating system:
________________________

Test date:
________________________

Unit tests:
PASS / FAIL

Syntax checks:
PASS / FAIL

Live API test:
PASS / FAIL / NOT RUN

Domoticz integration test:
PASS / FAIL / NOT RUN

Notes:
________________________
```

This information is useful when diagnosing regressions later.

---

# 33. Known Testing Boundary

The automated test suite cannot guarantee that every Domoticz version behaves identically.

Domoticz provides the runtime environment for:

```text
plugin.py
Domoticz.Device
Domoticz.Heartbeat
Domoticz.Log
Domoticz.Error
```

Therefore, compatibility with a particular Domoticz version must ultimately be verified in that Domoticz environment.

---

# 34. Related Documentation

| Document          | Purpose                     |
| ----------------- | --------------------------- |
| `README.md`       | Project overview            |
| `API.md`          | Open-Meteo API integration  |
| `DEPLOY.md`       | Installation and deployment |
| `DEVELOPMENT.md`  | Development environment     |
| `RELEASE.md`      | Release procedure           |
| `CONTRIBUTING.md` | Contribution guidelines     |
| `SECURITY.md`     | Security policy             |
| `CHANGELOG.md`    | Release history             |

---

## 35. Current Version

This testing guide currently applies to:

```text
Domoticz Pollen Forecast 0.2.0-alpha
```

The test suite and procedures may evolve as the plugin architecture and device model develop toward `1.0.0`.

