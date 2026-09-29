# -*- coding: utf-8 -*-
"""
Open-Meteo pollen API client.
"""

import json
import urllib.parse
import urllib.request

from pollen import (
    REQUESTED_POLLEN,
    is_pollen_key,
)


API_URL = (
    "https://air-quality-api.open-meteo.com/v1/air-quality"
)

USER_AGENT = (
    "Domoticz-PollenForecast/0.2.0-beta"
)


class PollenApi:

    def __init__(
        self,
        latitude,
        longitude,
        debug=False,
        log_fn=None,
    ):

        self.latitude = latitude
        self.longitude = longitude
        self.debug = debug
        self.log_fn = log_fn

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def log(self, message):

        if self.debug and self.log_fn:
            self.log_fn(
                "API: {}".format(message)
            )

    # ------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------

    def fetch(self):

        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "hourly": ",".join(
                REQUESTED_POLLEN
            ),
            "timezone": "auto",
            "forecast_days": 4,
            "domains": "cams_europe",
        }

        url = (
            API_URL
            + "?"
            + urllib.parse.urlencode(params)
        )

        self.log(
            "GET {}".format(url)
        )

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        )

        with urllib.request.urlopen(
            request,
            timeout=10,
        ) as response:

            if response.status != 200:

                raise RuntimeError(
                    "HTTP {}".format(
                        response.status
                    )
                )

            payload = response.read().decode(
                "utf-8"
            )

        data = json.loads(payload)

        if data.get("error"):

            raise RuntimeError(
                data.get(
                    "reason",
                    "Open-Meteo API error",
                )
            )

        hourly = data.get(
            "hourly"
        )

        if not isinstance(
            hourly,
            dict,
        ):

            raise ValueError(
                "Invalid API response: "
                "missing hourly data"
            )

        if "time" not in hourly:

            raise ValueError(
                "Invalid API response: "
                "missing time"
            )

        self._log_discovered_species(
            hourly
        )

        return data

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def _log_discovered_species(
        self,
        hourly,
    ):

        discovered = sorted(
            key
            for key in hourly.keys()
            if is_pollen_key(key)
        )

        self.log(
            "Pollen variables returned by API: {}".format(
                ", ".join(discovered)
                if discovered
                else "none"
            )
        )

    # ------------------------------------------------------------------
    # Daily aggregation
    # ------------------------------------------------------------------

    def build_daily_data(
        self,
        data,
    ):

        hourly = data["hourly"]

        times = hourly.get(
            "time",
            [],
        )

        if not times:
            return []

        dates = []

        for timestamp in times:

            date = timestamp[:10]

            if date not in dates:
                dates.append(date)

        pollen_keys = sorted(
            key
            for key in hourly.keys()
            if is_pollen_key(key)
        )

        result = []

        for date in dates:

            item = {
                "date": date,
                "values": {},
            }

            indices = [
                index
                for index, timestamp
                in enumerate(times)
                if timestamp.startswith(date)
            ]

            for pollen_key in pollen_keys:

                series = hourly.get(
                    pollen_key,
                    [],
                )

                values = []

                for index in indices:

                    if index >= len(series):
                        continue

                    value = series[index]

                    if value is None:
                        continue

                    try:

                        values.append(
                            float(value)
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):

                        continue

                item["values"][pollen_key] = (
                    max(values)
                    if values
                    else None
                )

            result.append(item)

        return result
