# Release Guide

## Domoticz Pollen Forecast

This document defines the release process for the **Domoticz Pollen Forecast** plugin.

The goal is to make every release:

* reproducible
* traceable
* tested
* documented
* correctly versioned
* safe to deploy

Current development version:

```text
0.2.0-alpha
```

---

## 1. Versioning

The project follows **Semantic Versioning**:

```text
MAJOR.MINOR.PATCH
```

Pre-release identifiers are used during development.

Examples:

```text
0.1.0-alpha
0.2.0-alpha
0.3.0-beta
1.0.0
1.0.1
```

### Version meanings

#### MAJOR

A major release may contain incompatible changes.

Example:

```text
1.0.0 → 2.0.0
```

#### MINOR

A minor release adds functionality while maintaining compatibility where practical.

Example:

```text
0.2.0 → 0.3.0
```

#### PATCH

A patch release contains backwards-compatible fixes.

Example:

```text
0.2.0 → 0.2.1
```

---

## 2. Pre-release Versions

During the `0.x` development phase, the API and device model are not considered permanently stable.

Common pre-release identifiers are:

```text
-alpha
-beta
-rc
```

Examples:

```text
0.2.0-alpha
0.2.0-beta
0.2.0-rc1
```

A pre-release may change:

* device names
* device unit assignments
* configuration parameters
* API handling
* translations
* internal interfaces
* supported pollen species

Such changes must be documented in `CHANGELOG.md`.

---

## 3. Single Source of Release Version

The release version must be consistent across the repository.

At minimum, check:

```text
VERSION
plugin.py
api.py
CHANGELOG.md
Git tag
GitHub release
```

The plugin XML metadata must contain the same version as the release.

For example:

```xml
version="0.2.0-alpha"
```

The Python version constant must match:

```python
VERSION = "0.2.0-alpha"
```

The API User-Agent must also identify the release:

```python
USER_AGENT = (
    "Domoticz-PollenForecast/0.2.0-alpha"
)
```

The `VERSION` file should contain only:

```text
0.2.0-alpha
```

---

## 4. Release Branch

Releases should be created from a clean, reviewed branch.

For a normal release:

```text
development
    ↓
release preparation
    ↓
master
    ↓
Git tag
    ↓
GitHub Release
```

Do not create a release from a working tree containing unrelated changes.

---

## 5. Before Starting a Release

Check the repository:

```bash
git status
```

Expected:

```text
```

