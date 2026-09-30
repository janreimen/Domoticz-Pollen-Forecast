# Security Policy

**Project:** Domoticz Pollen Forecast  
**Current development version:** 0.2.1-beta

## Supported versions

This project is under active development.

| Version | Status |
|---|---|
| 0.2.1-beta | Development |
| 0.2.0-beta | Previous beta |
| Older versions | Unsupported |

## Reporting a security issue

Please do not publish sensitive security information in a public issue.

For a security-sensitive problem, contact the project maintainer privately through the GitHub repository's available private contact mechanism.

Include:

- affected version
- affected file/component
- reproduction steps
- expected behavior
- actual behavior
- relevant logs with secrets or personal information removed

## Data handling

The plugin sends the configured geographic coordinates to the Open-Meteo Air Quality API.

The coordinates are required to obtain a local pollen forecast.

The plugin does not require:

- an API key
- a user account
- a password
- a cloud account

## Network security

The plugin communicates with Open-Meteo over HTTPS.

No inbound network service is opened by the plugin.

## Input validation

The unified location field validates:

```text
longitude: -180..180
latitude:   -90..90
```

Allergen selection is restricted to the supported identifiers.

The plugin should reject or safely handle malformed configuration rather than constructing arbitrary API requests from unchecked values.

## Dependencies

The plugin intentionally uses Python's standard library only.

This reduces the third-party dependency surface.

## Logs

Debug logging may include:

- API request information
- discovered pollen variables
- configuration information
- calculated pollen levels

Do not enable Debug permanently if logs are being collected or forwarded to systems where location information should not be retained.

## API availability

The plugin depends on the availability of Open-Meteo.

If the API is unavailable, the plugin logs the update failure and does not intentionally expose a new network service.

## Responsible disclosure

Security issues should be reported privately where possible so they can be assessed and corrected before public disclosure.
