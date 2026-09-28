# Development Guide

## Domoticz Pollen Forecast

This document describes the development environment, project architecture, coding conventions, local workflow, and contribution process for the **Domoticz Pollen Forecast** plugin.

Current development version:

```text
0.2.0-alpha
```

The project is intentionally lightweight and uses the Python standard library only.

---

## 1. Development Goals

The plugin is designed around the following principles:

* simple deployment
* no external Python dependencies
* clear separation of responsibilities
* deterministic behaviour
* defensive API handling
* native Domoticz devices
* testable modules
* minimal network access
* readable source code
* predictable Git history

The plugin should remain easy to install on a Raspberry Pi or other Domoticz host without maintaining a separate Python environment.

---

# 2. Repository Structure

The recommended repository structure is:

```text
Domoticz-Pollen-Forecast/
├── plugin.py
├── config.py
├── api.py
├── pollen.py
├── devices.py
├── translations.py
│
├── tests/
│   ├── __init__.py
│   ├── test_pollen.py
│   ├── test_translations.py
│   ├── test_api.py
│   └── test_devices.py
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── workflows/
│       └── tests.yml
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
├── LICENSE
├── VERSION
├── requirements.txt
└── .gitignore
```

---

# 3. Module Responsibilities

The plugin is intentionally split into several modules.

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

Each module should have one primary responsibility.

---

## 3.1 `plugin.py`

`plugin.py` is the Domoticz plugin entry point.

It is responsible for:

* Domoticz lifecycle callbacks
* plugin startup
* plugin shutdown
* heartbeat handling
* scheduling updates
* connecting the other modules
* error reporting

The main class is:

```python
BasePlugin
```

Domoticz calls:

```python
onStart()
onStop()
onHeartbeat()
```

The module should not contain detailed API parsing or pollen threshold logic.

---

## 3.2 `config.py`

`config.py` handles Domoticz configuration parameters.

It converts the Domoticz `Parameters` dictionary into a structured configuration object.

The main class is:

```python
PluginConfig
```

Configuration currently includes:

```text
latitude
longitude
language
refresh_minutes
debug
```

The configuration module should validate user input before passing it to the API or device layers.

---

## 3.3 `api.py`

`api.py` contains the Open-Meteo API client.

The main class is:

```python
PollenApi
```

Responsibilities include:

* constructing the API request
* performing the HTTPS request
* decoding JSON
* validating the basic response structure
* identifying pollen variables
* aggregating hourly values into daily values

The API client should not create Domoticz devices.

---

## 3.4 `pollen.py`

`pollen.py` contains the pollen data model.

It defines:

* supported pollen species
* pollen thresholds
* pollen level calculation
* pollen variable detection
* fallback handling for unknown pollen variables

The central data structure is:

```python
PollenDefinition
```

The central definitions are stored in:

```python
KNOWN_POLLEN
```

The concentration-to-level conversion is performed by:

```python
level_for()
```

---

## 3.5 `devices.py`

`devices.py` handles Domoticz devices.

The main class is:

```python
PollenDevices
```

Responsibilities include:

* creating Domoticz devices
* assigning unit numbers
* generating translated device names
* updating Alert levels
* avoiding unnecessary device updates

It should not perform HTTP requests.

---

## 3.6 `translations.py`

`translations.py` contains user-visible translations.

Supported languages are currently:

```text
en
lb
de
fr
nl
```

The module should contain presentation text only.

Pollen threshold logic must not be implemented in the translation module.

---

# 4. Data Flow

The intended data flow is:

```text
Domoticz
    |
    | configuration
    v
plugin.py
    |
    +--------------------+
    |                    |
    v                    v
config.py             api.py
                         |
                         | HTTPS / JSON
                         v
                    Open-Meteo
                         |
                         | hourly data
                         v
                    daily data
                         |
                         v
                    pollen.py
                         |
                         | level 0..4
                         v
                    devices.py
                         |
                         v
                  Domoticz Alert
```

Translations are applied when device names and displayed level text are generated.

---

# 5. Pollen Data Model

The current supported pollen variables are:

```text
alder_pollen
birch_pollen
grass_pollen
mugwort_pollen
olive_pollen
ragweed_pollen
```

They are represented using:

```python
PollenDefinition
```

Example:

```python
PollenDefinition(
    key="grass_pollen",
    thresholds=(10.0, 30.0),
    label_key="grass_pollen",
)
```

The two threshold values represent:

```text
low maximum
medium maximum
```

---

# 6. Pollen Level Model

The plugin uses the following internal levels:

| Level | Meaning |
| ----: | ------- |
|   `0` | No data |
|   `1` | None    |
|   `2` | Low     |
|   `3` | Medium  |
|   `4` | High    |

The mapping is implemented by:

```python
level_for()
```

in:

```text
pollen.py
```

Do not duplicate this logic in `devices.py`, `plugin.py`, or the translation module.

---

# 7. Current Thresholds

The current thresholds are:

| Species | Low maximum | Medium maximum |
| ------- | ----------: | -------------: |
| Alder   |          16 |             50 |
| Birch   |          16 |             50 |
| Grass   |          10 |             30 |
| Mugwort |           5 |             25 |
| Olive   |           5 |             25 |
| Ragweed |           5 |             25 |

A concentration below:

```text
1.0
```

is classified as:

```text
None
```

A `None` concentration is:

```text
No data
```

and therefore maps to level:

```text
0
```

---

# 8. Adding a New Pollen Species

Adding a new pollen species should be done systematically.

### Step 1 — Add the definition

Update:

```text
pollen.py
```

Add a `PollenDefinition` to:

```python
KNOWN_POLLEN
```

Example:

```python
"example_pollen": PollenDefinition(
    key="example_pollen",
    thresholds=(5.0, 25.0),
    label_key="example_pollen",
),
```

Use verified thresholds appropriate to the data source.

Do not invent thresholds solely to make a new API variable fit the existing model.

---

### Step 2 — Add translations

Add the new pollen key to every supported language in:

```text
translations.py
```

For example:

```text
en
lb
de
fr
nl
```

---

### Step 3 — Review device handling

The current device implementation contains an explicit species list.

Before expanding the supported species list, review:

```text
devices.py
```

The long-term architecture should use `pollen.py` as the single source of truth for supported pollen species.

Until that cleanup is implemented, a new species must be added consistently wherever the current device implementation maintains the list.

---

### Step 4 — Add tests

Add tests for:

* pollen definition
* threshold boundaries
* translation
* API handling
* device mapping

---

### Step 5 — Update documentation

Update:

```text
README.md
API.md
CHANGELOG.md
```

---

# 9. Adding a New Language

To add a language:

### 1. Add the language code

Update:

```text
config.py
```

and add the new language to:

```python
SUPPORTED_LANGUAGES
```

### 2. Add translations

Update:

```text
translations.py
```

The translation should provide the same structural keys as the existing languages.

### 3. Test all required keys

Every language should provide:

```text
today
tomorrow
unknown_pollen
no_data
levels
pollen
```

### 4. Update documentation

Update:

```text
README.md
DEPLOY.md
API.md
CHANGELOG.md
```

---

# 10. API Development

The API endpoint is defined in:

```text
api.py
```

Current endpoint:

```text
https://air-quality-api.open-meteo.com/v1/air-quality
```

The client uses:

```text
timezone=auto
forecast_days=4
domains=cams_europe
```

The plugin currently exposes:

```text
Today
Tomorrow
```

even though four forecast days are requested.

Do not change API parameters without verifying the corresponding Open-Meteo API documentation.

---

# 11. API Error Handling

The API layer should treat external data as untrusted input.

Always handle:

* HTTP errors
* connection errors
* timeout
* invalid JSON
* API error responses
* missing `hourly`
* missing `time`
* missing pollen series
* `null` values
* invalid numeric values

A malformed API response must not crash the Domoticz process.

---

# 12. Network Access

The plugin uses Python's standard library:

```python
urllib.request
urllib.parse
```

Do not add `requests` or another HTTP library unless there is a documented technical reason.

The current implementation has no external Python dependencies.

The request timeout is:

```text
10 seconds
```

---

# 13. Unknown API Variables

The API client identifies pollen variables using:

```text
*_pollen
```

This permits the API to return additional pollen variables without causing the parser to fail.

Unknown pollen variables currently use fallback thresholds:

```text
5.0
25.0
```

These fallback thresholds are not necessarily scientifically appropriate for every species.

A newly supported species should receive an explicit definition before being presented as a fully supported feature.

---

# 14. Daily Aggregation

The API provides hourly values.

The plugin calculates one daily concentration per pollen species:

```text
daily concentration =
maximum valid hourly concentration
```

Example:

```text
00:00 → 2.0
01:00 → 4.0
02:00 → 7.5
03:00 → 3.2
```

Result:

```text
7.5
```

Do not change the aggregation method without updating:

```text
API.md
README.md
TESTING.md
CHANGELOG.md
```

and the associated tests.

---

# 15. Domoticz Device Model

The current model uses twelve native Domoticz `Alert` devices.

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

Alert values:

```text
0 = No data
1 = None
2 = Low
3 = Medium
4 = High
```

The native Domoticz Alert device provides the visual colour representation.

The plugin does not implement its own colour system.

---

# 16. Device Unit Stability

Unit numbers are important because Domoticz automations may refer to the resulting devices.

Do not change the unit mapping casually.

If the unit mapping must change:

1. document the change
2. update tests
3. update `README.md`
4. update `API.md`
5. update `DEPLOY.md`
6. update `CHANGELOG.md`
7. clearly mark the change as breaking if appropriate

---

# 17. Configuration Development

Configuration values enter through the Domoticz `Parameters` dictionary.

The current parameters are:

```text
Mode1 = Latitude
Mode2 = Longitude
Mode3 = Language
Mode4 = Refresh interval
Mode5 = Debug
```

`config.py` converts these values into:

```python
PluginConfig
```

The rest of the application should use the structured configuration object rather than reading `Parameters` directly.

---

# 18. Logging

Logging should be useful without becoming excessive.

Normal operation should not produce unnecessary debug output.

Debug output is controlled by the configured:

```text
Debug
```

setting.

Use:

```python
self.log(...)
```

for debug information.

Use:

```python
self.error(...)
```

for actual plugin errors.

Do not use `print()` for normal plugin logging.

---

# 19. Logging Sensitive Information

Do not log:

* passwords
* API keys
* authentication tokens
* credentials
* private configuration data

The current API request contains latitude and longitude.

Debug logging can therefore reveal the configured forecast location.

This should be considered when copying logs into public GitHub issues.

---

# 20. Coding Style

The code should remain readable and conservative.

Preferred characteristics:

* explicit names
* small functions
* clear module boundaries
* standard-library functionality
* straightforward control flow
* defensive validation
* minimal magic
* no unnecessary abstractions

Avoid overly compressed code such as:

```python
x = [f(v) for v in data if v]
```

when a longer form makes the behaviour clearer and easier to debug.

---

# 21. Python Compatibility

Use Python 3 syntax supported by the target Domoticz environment.

Avoid unnecessary dependencies on the newest Python features.

Before introducing a newer language feature, verify the Python version available in the target Domoticz installation.

---

# 22. External Dependencies

The production plugin currently has no third-party Python dependencies.

Therefore:

```text
requirements.txt
```

is intentionally empty.

Do not add packages merely for convenience.

Any new dependency should have:

* a documented reason
* compatibility review
* security review
* deployment documentation
* test coverage
* release notes

---

# 23. Local Development Environment

A separate Python virtual environment is optional because the plugin has no third-party dependencies.

For isolated development, a virtual environment can still be useful:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

The project should continue to work without installing additional packages.

Deactivate:

```bash
deactivate
```

Do not commit:

```text
.venv/
venv/
__pycache__/
*.pyc
```

---

# 24. Running Tests During Development

After making changes:

```bash
python3 -m unittest discover -s tests -v
```

Then run the syntax check:

```bash
python3 -m py_compile \
    plugin.py \
    config.py \
    api.py \
    pollen.py \
    devices.py \
    translations.py
```

Run both before committing significant changes.

See:

```text
TESTING.md
```

for the complete test procedure.

---

# 25. Testing Without Domoticz

Most modules should be testable without Domoticz installed.

These modules should be independently testable:

```text
pollen.py
translations.py
api.py
config.py
```

`devices.py` can use a mocked or test-double `Domoticz` environment.

`plugin.py` is primarily an integration layer and should be tested in a real Domoticz environment.

---

# 26. Test Doubles

Tests should use mocks rather than real external services.

For API tests:

```python
unittest.mock
```

should be used to replace the HTTP request.

For device tests, use fake Domoticz devices or mock the Domoticz module.

Do not make the unit test suite depend on:

```text
Open-Meteo
Domoticz
internet connectivity
production devices
```

---

# 27. Development Branch

The recommended branch model is:

```text
master
    |
    +-- stable releases

development
    |
    +-- active development
```

Feature work can use separate branches when appropriate:

```text
feature/<name>
fix/<name>
```

Examples:

```text
feature/new-pollen-species
fix/api-error-handling
```

---

# 28. Commit Style

Commits should describe one logical change.

Good examples:

```text
Add pollen threshold tests
Fix API response validation
Add Dutch translations
Improve device update handling
Update deployment documentation
```

Avoid commits such as:

```text
changes
fix
test
stuff
update
```

unless the repository history is being rewritten during private development.

---

# 29. Keep Commits Focused

Avoid combining unrelated changes.

For example, a commit should not simultaneously:

* change API handling
* reformat every Python file
* rename unrelated devices
* modify documentation
* change GitHub Actions

unless those changes are genuinely part of one logical feature.

Focused commits make review and troubleshooting easier.

---

# 30. Working With Releases

Release preparation should follow:

```text
development
    ↓
tests
    ↓
documentation
    ↓
release commit
    ↓
Git tag
    ↓
GitHub Release
```

Do not manually modify a published release tag.

See:

```text
RELEASE.md
```

for the complete release procedure.

---

# 31. Version Updates

When changing the version, keep all version references synchronized.

Check:

```text
VERSION
plugin.py
api.py
CHANGELOG.md
```

Also check the plugin XML metadata in `plugin.py`.

For example:

```xml
version="0.2.0-alpha"
```

and:

```python
VERSION = "0.2.0-alpha"
```

must refer to the same release.

---

# 32. Documentation Changes

A functional change may require changes to several documents.

Examples:

### New pollen species

Update:

```text
README.md
API.md
TESTING.md
CHANGELOG.md
```

### New configuration parameter

Update:

```text
README.md
DEPLOY.md
DEVELOPMENT.md
TESTING.md
CHANGELOG.md
```

### Device model change

Update:

```text
README.md
API.md
DEPLOY.md
TESTING.md
CHANGELOG.md
```

### Security-related change

Also review:

```text
SECURITY.md
```

---

# 33. Debugging the Plugin on Domoticz

Enable the plugin's Debug option.

Then monitor the Domoticz log.

For systemd:

```bash
sudo journalctl -u domoticz -f
```

Filter for the plugin:

```bash
sudo journalctl -u domoticz -f \
    | grep PollenForecast
```

Look for the sequence:

```text
Starting version ...
Location: ...
Language: ...
Refresh interval: ...
Updating pollen forecast
API: GET ...
Pollen variables returned by API: ...
Pollen forecast updated successfully
```

---

# 34. Debugging Startup Errors

If the plugin fails during startup, first verify Python syntax:

```bash
python3 -m py_compile \
    plugin.py \
    config.py \
    api.py \
    pollen.py \
    devices.py \
    translations.py
```

Then inspect the Domoticz log:

```bash
sudo journalctl -u domoticz --since "10 minutes ago"
```

Pay particular attention to the first Python exception.

Fix the first actual exception before investigating secondary errors.

---

# 35. Debugging API Errors

Separate API problems from plugin problems.

First test the endpoint independently:

```bash
curl -sS \
    'https://air-quality-api.open-meteo.com/v1/air-quality?latitude=49.6116&longitude=6.1319&hourly=alder_pollen,birch_pollen,grass_pollen,mugwort_pollen,olive_pollen,ragweed_pollen&timezone=auto&forecast_days=4&domains=cams_europe'
```

Then inspect:

```text
HTTP response
JSON
hourly
time
pollen variables
```

If the external request works but the plugin fails, investigate `api.py`.

---

# 36. Debugging Device Problems

If the API succeeds but devices do not update, inspect:

```text
devices.py
```

Check:

```text
pollen key
forecast day
unit number
concentration
level
nValue
sValue
```

The current mapping is:

```text
pollen index × 2 + day index + 1
```

with:

```text
Today    = 0
Tomorrow = 1
```

---

# 37. Cleaning the Working Tree

Before committing, check:

```bash
git status
```

Remove generated Python caches:

```bash
find . \
    -type d \
    -name '__pycache__' \
    -prune \
    -exec rm -rf {} +
```

Check for bytecode:

```bash
find . \
    -type f \
    -name '*.pyc' \
    -print
```

Check for unexpected files:

```bash
git status --short
```

---

# 38. Pre-Commit Checklist

Before committing a functional change:

```text
[ ] Change is limited to the intended scope
[ ] No credentials or secrets added
[ ] No unnecessary dependencies added
[ ] Python syntax check passes
[ ] Unit tests pass
[ ] Documentation updated where necessary
[ ] CHANGELOG.md updated when appropriate
[ ] No __pycache__ files
[ ] No *.pyc files
[ ] git diff reviewed
[ ] git status reviewed
```

---

# 39. Pull Request Checklist

For a pull request, verify:

```text
[ ] Clear description of the change
[ ] Reason for the change documented
[ ] Tests added or updated
[ ] Existing tests pass
[ ] Documentation updated
[ ] No unrelated formatting changes
[ ] No credentials or private data
[ ] Backwards compatibility considered
[ ] Device changes documented
[ ] Breaking changes explicitly identified
```

---

# 40. Breaking Changes

Changes that can affect existing users include:

* changing Domoticz unit numbers
* removing devices
* renaming devices
* changing configuration parameters
* changing Alert level meanings
* changing pollen thresholds
* changing the API data model
* changing supported languages
* removing supported pollen species

These changes must be clearly documented.

During the `0.x` phase, breaking changes may be acceptable, but they should never be silent.

---

# 41. Database Considerations

The plugin does not maintain its own database.

Persistent device data is managed by Domoticz.

Therefore, changes to the plugin's device model can affect existing Domoticz devices and automations even though the plugin itself has no database migration system.

Device model changes must therefore be treated carefully.

---

# 42. Privacy Considerations

The plugin sends the configured:

```text
latitude
longitude
```

to Open-Meteo as part of the forecast request.

No user account or authentication information is required by the current API integration.

Debug logs may contain the configured location.

Avoid publishing production logs containing exact coordinates unless they are intentionally being shared.

See:

```text
SECURITY.md
```

for additional security information.

---

# 43. API Documentation

Changes to API handling should be documented in:

```text
API.md
```

When changing:

* endpoint
* query parameters
* pollen variables
* response handling
* timeout
* aggregation
* error handling

update the corresponding API documentation and tests.

---

# 44. Code Review Principles

When reviewing code, prioritize:

1. correctness
2. predictable behaviour
3. error handling
4. backwards compatibility
5. test coverage
6. security
7. maintainability
8. readability

Avoid refactoring unrelated code while implementing a small functional change unless the refactoring is necessary.

---

# 45. No Guessing in API Changes

The Open-Meteo response should be verified before changing the parser.

Do not assume that:

* a variable exists
* a variable has a particular unit
* a variable has a particular threshold
* a response field always exists
* a future pollen variable behaves identically to an existing one

Verify external API behaviour first and then add tests based on the verified response.

---

# 46. Adding Dependencies

Before adding any third-party Python dependency, ask:

```text
Can the standard library solve this reliably?
```

If yes, prefer the standard library.

If a dependency is genuinely required:

1. document why
2. add it to `requirements.txt`
3. update `DEPLOY.md`
4. update `SECURITY.md`
5. update CI
6. test supported Python versions
7. document the change in `CHANGELOG.md`

---

# 47. Local Installation Test

A useful development workflow is to test the actual plugin files in a dedicated Domoticz test installation.

Copy or link the repository into:

```text
<domoticz userdata>/plugins/PollenForecast
```

Then restart Domoticz.

Avoid developing directly inside a production plugin directory when possible.

---

# 48. Production Development Warning

Do not use the production Domoticz installation as the primary development environment.

Development changes can:

* create devices
* modify device values
* change device names
* affect automations
* generate database entries
* expose debug information

Use a dedicated test Domoticz installation where practical.

---

# 49. Standard Development Workflow

A normal feature workflow is:

```text
1. Create or switch to development branch
        ↓
2. Implement one logical change
        ↓
3. Add/update tests
        ↓
4. Run unit tests
        ↓
5. Run syntax checks
        ↓
6. Test in Domoticz if required
        ↓
7. Update documentation
        ↓
8. Review git diff
        ↓
9. Commit
        ↓
10. Push development branch
```

---

# 50. Before Merging to Master

Before merging development work into the stable branch:

```text
[ ] All unit tests pass
[ ] Syntax checks pass
[ ] CI passes
[ ] Domoticz integration tested where applicable
[ ] Documentation complete
[ ] CHANGELOG.md updated
[ ] Version is correct
[ ] No debug-only code remains
[ ] No credentials or private data
[ ] Git history reviewed
```

Release preparation then follows `RELEASE.md`.

---

# 51. Current Architecture Limitation

The current `devices.py` implementation maintains its own explicit pollen species list.

The intended long-term architecture is for:

```text
pollen.py
```

to be the single source of truth for supported pollen species.

Until that refactoring is completed, developers must keep the species lists synchronized between the relevant modules.

This is an intentional documented technical-debt item rather than an assumption that the current code already implements centralization.

---

# 52. Current Device Model

Version `0.2.0-alpha` uses:

```text
12 native Domoticz Alert devices
```

for:

```text
6 pollen species
×
2 forecast days
```

The device model is:

```text
Alder
    Today
    Tomorrow

Birch
    Today
    Tomorrow

Grass
    Today
    Tomorrow

Mugwort
    Today
    Tomorrow

Olive
    Today
    Tomorrow

Ragweed
    Today
    Tomorrow
```

This is the current development model and may change before `1.0.0`.

---

# 53. Related Documentation

| Document          | Purpose                      |
| ----------------- | ---------------------------- |
| `README.md`       | Project overview             |
| `API.md`          | Open-Meteo API integration   |
| `DEPLOY.md`       | Installation and deployment  |
| `TESTING.md`      | Automated and manual testing |
| `RELEASE.md`      | Release procedure            |
| `CONTRIBUTING.md` | Contribution guidelines      |
| `SECURITY.md`     | Security policy              |
| `CHANGELOG.md`    | Release history              |

---

# 54. Development Version

This document currently describes:

```text
Domoticz Pollen Forecast 0.2.0-alpha
```

The architecture, device model, API integration, and development workflow may evolve during the `0.x` development phase.

Changes that affect users or contributors should be reflected in the appropriate project documentation.

