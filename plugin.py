# -*- coding: utf-8 -*-
#
# Domoticz Pollen Forecast Plugin
#
# Version: 0.2.0-alpha
# Author: 4D, janreimen
#
# Data source:
#   Open-Meteo Air Quality API
#   CAMS European Air Quality Forecast
#
# No external Python packages required.
#

"""
<plugin key="PollenForecast"
        name="Pollen Forecast"
        author="4D, janreimen"
        version="0.2.0-alpha"
        externallink="https://github.com/janreimen/Domoticz-Pollen-Forecast">

    <description>
        <h2>Pollen Forecast</h2>

        <p>
            Pollen forecast from the Open-Meteo Air Quality API
            using the CAMS European Air Quality Forecast.
        </p>

        <p>
            Supports English, Lëtzebuergesch, Deutsch, Français and Nederlands.
        </p>

        <p>
            Creates pollen alert and detail devices for today and tomorrow.
        </p>
    </description>

    <params>

        <param field="Mode1"
               label="Latitude"
               width="120px"
               required="true"
               default=""/>

        <param field="Mode2"
               label="Longitude"
               width="120px"
               required="true"
               default=""/>

        <param field="Mode3"
               label="Language"
               width="160px"
               required="true"
               default="en">

            <options>
                <option label="English" value="en" default="true"/>
                <option label="Lëtzebuergesch" value="lb"/>
                <option label="Deutsch" value="de"/>
                <option label="Français" value="fr"/>
                <option label="Nederlands" value="nl"/>
            </options>

        </param>

        <param field="Mode4"
               label="Refresh interval"
               width="180px"
               required="true"
               default="60">

            <options>
                <option label="30 minutes" value="30"/>
                <option label="60 minutes" value="60" default="true"/>
                <option label="3 hours" value="180"/>
                <option label="6 hours" value="360"/>
            </options>

        </param>

        <param field="Mode5"
               label="Debug"
               width="100px"
               required="true"
               default="0">

            <options>
                <option label="Off" value="0" default="true"/>
                <option label="On" value="1"/>
            </options>

        </param>

    </params>

</plugin>
"""

import time

import Domoticz

from api import PollenApi
from config import PluginConfig
from devices import PollenDevices


VERSION = "0.2.0-alpha"


class BasePlugin:

    def __init__(self):
        self.config = None
        self.api = None
        self.devices = None

        self.last_update = 0.0
        self.heartbeat_counter = 0

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def log(self, message):
        if self.config and self.config.debug:
            Domoticz.Log(
                "PollenForecast: {}".format(message)
            )

    def error(self, message):
        Domoticz.Error(
            "PollenForecast: {}".format(message)
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def onStart(self):

        self.config = PluginConfig.from_domoticz(
            Parameters
        )

        self.api = PollenApi(
            latitude=self.config.latitude,
            longitude=self.config.longitude,
            debug=self.config.debug,
            log_fn=self.log,
        )

        self.devices = PollenDevices(
            devices=Devices,
            language=self.config.language,
            debug=self.config.debug,
            log_fn=self.log,
        )

        self.devices.create()

        Domoticz.Heartbeat(30)

        self.log(
            "Starting version {}".format(
                VERSION
            )
        )

        self.log(
            "Location: {:.6f}, {:.6f}".format(
                self.config.latitude,
                self.config.longitude,
            )
        )

        self.log(
            "Language: {}".format(
                self.config.language
            )
        )

        self.log(
            "Refresh interval: {} minutes".format(
                self.config.refresh_minutes
            )
        )

        self.update()

    def onStop(self):

        self.log("Plugin stopped")

    def onHeartbeat(self):

        self.heartbeat_counter += 1

        if self.config is None:
            return

        if (
            time.time() - self.last_update
            >= self.config.refresh_minutes * 60
        ):
            self.update()

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self):

        self.log("Updating pollen forecast")

        try:

            data = self.api.fetch()

            days = self.api.build_daily_data(
                data
            )

            if len(days) < 2:
                raise ValueError(
                    "API response does not contain "
                    "today and tomorrow"
                )

            self.devices.update_day(
                alert_unit=1,
                text_unit=3,
                day=days[0],
            )

            self.devices.update_day(
                alert_unit=2,
                text_unit=4,
                day=days[1],
            )

            self.last_update = time.time()

            self.log(
                "Pollen forecast updated successfully "
                "({} forecast days received)".format(
                    len(days)
                )
            )

        except Exception as exc:

            self.error(
                "Update failed: {}".format(exc)
            )

            # Do not retry every 30 seconds after
            # a network/API failure.
            self.last_update = time.time()


_plugin = BasePlugin()


def onStart():
    _plugin.onStart()


def onStop():
    _plugin.onStop()


def onHeartbeat():
    _plugin.onHeartbeat()
