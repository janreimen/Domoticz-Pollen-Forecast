# Security Policy

## Domoticz Pollen Forecast

This document describes the security policy for the **Domoticz Pollen Forecast** plugin.

The project is currently in the `0.x-alpha` development phase.

---

## Supported Versions

Security fixes are primarily applied to the current development release.

| Version                         | Supported   |
| ------------------------------- | ----------- |
| `0.2.x-alpha`                   | Yes         |
| Older `0.x-alpha` releases      | Best effort |
| Unsupported / modified versions | No          |

Because the project is currently in alpha development, the internal architecture and device model may change between releases.

Once version `1.0.0` is released, the support policy will be updated to cover the stable release series explicitly.

---

## Reporting a Security Vulnerability

Please **do not report security vulnerabilities through a public GitHub issue**.

For vulnerabilities that could expose credentials, execute arbitrary code, compromise the Domoticz installation, or otherwise create a security risk, please contact the project maintainer privately.

GitHub repository:

`janreimen/Domoticz-Pollen-Forecast`

If GitHub Security Advisories are enabled for the repository, please use the repository's **Security → Advisories → Report a vulnerability** mechanism.

If private reporting is not available, contact the maintainer through the contact information associated with the GitHub repository.

---

## What to Include

Please provide enough information to reproduce and assess the vulnerability.

Ideally include:

* affected version
* affected file or component
* operating system
* Python version
* Domoticz version
* reproduction steps
* relevant configuration
* expected behaviour
* actual behaviour
* security impact
* proof of concept, if available

Please remove passwords, API keys, tokens, private keys, personal information, and other sensitive information before submitting a report.

---

## Security Scope

The plugin has a relatively small security surface.

The plugin:

* communicates with the Open-Meteo API over HTTPS
* accepts latitude and longitude as configuration parameters
* accepts a language selection
* accepts a refresh interval
* accepts a debug setting
* creates and updates Domoticz devices
* processes JSON returned by the remote API

The plugin does **not**:

* provide an HTTP server
* open inbound network ports
* require an API key
* store user credentials
* execute shell commands
* execute code received from the API
* install Python packages automatically
* provide remote control of external equipment
* accept arbitrary user input over a network service

---

## Network Security

The plugin communicates with the Open-Meteo Air Quality API using HTTPS.

The API endpoint is:

```text
https://air-quality-api.open-meteo.com/v1/air-quality
```

The plugin uses Python's standard-library HTTPS functionality.

The expected network direction is:

```text
Domoticz
    |
    | HTTPS / TCP 443
    v
Open-Meteo
```

No inbound connection to the Domoticz host is required by this plugin.

---

## TLS / HTTPS

API communication uses HTTPS.

The plugin does not intentionally disable TLS certificate verification.

The plugin does not implement its own TLS protocol.

TLS handling is provided by Python's standard networking libraries and the underlying operating system's certificate infrastructure.

Users should keep their operating system and Python installation appropriately maintained.

---

## API Data Handling

The plugin receives JSON data from Open-Meteo.

The response is treated as untrusted external input.

The plugin validates basic response structure before processing it.

For example, it checks that:

* the API response is JSON
* the response does not report an API error
* the `hourly` object exists
* the `time` series exists
* pollen values can be converted to numeric values before they are used

Invalid or unusable pollen values are ignored rather than executed or interpreted as code.

---

## No Dynamic Code Execution

The plugin does not use external API data as executable Python code.

It does not use mechanisms such as:

```python
eval()
exec()
```

to process API responses.

Pollen variable names are treated as data.

---

## Configuration Security

The following configuration values are supplied by the Domoticz plugin configuration:

```text
Latitude
Longitude
Language
Refresh interval
Debug
```

These values are validated before use.

Latitude and longitude are converted to floating-point values.

The language is restricted to the supported language list.

The refresh interval is converted to an integer and has a minimum value.

The debug setting is explicitly interpreted as an enabled/disabled option.

---

## Privacy

The configured geographical coordinates are transmitted to Open-Meteo because they are required to obtain the forecast for the selected location.

For example:

```text
Latitude:  49.6116
Longitude: 6.1319
```

The plugin itself does not collect:

* names
* email addresses
* passwords
* API credentials
* authentication tokens
* account information

The plugin does not intentionally send Domoticz device information to Open-Meteo.

Users should review the current Open-Meteo privacy and data policies independently.

---

## Logging

Debug logging may include:

* plugin version
* configured coordinates
* selected language
* refresh interval
* API request URL
* pollen variables returned by the API
* pollen concentrations
* calculated pollen levels
* Domoticz device updates

Because the API request contains the configured latitude and longitude, debug logs may reveal the configured geographical location.

Users who consider their coordinates sensitive should disable debug logging when it is no longer required.

The plugin does not intentionally log credentials or authentication tokens.

---

## API URL Logging

When debug mode is enabled, the plugin currently logs the constructed API URL.

The URL contains the configured latitude and longitude and requested API parameters.

Example:

```text
https://air-quality-api.open-meteo.com/v1/air-quality?latitude=49.6116&longitude=6.1319&...
```

This is useful during development but should be considered location-sensitive information.

---

## File Permissions

The plugin should be installed with permissions appropriate to the Domoticz installation.

Example:

```bash
ls -ld /srv/domoticz/plugins/Domoticz-Pollen-Forecast
```

Plugin source files should not be writable by untrusted users.

A typical installation should allow the Domoticz service account to read the plugin files.

The plugin does not require its source files to be writable at runtime.

---

## Python Dependencies

The plugin currently uses only the Python standard library.

There are no third-party runtime dependencies.

This intentionally reduces the dependency and supply-chain attack surface.

The project should avoid adding external dependencies unless there is a clear technical req

