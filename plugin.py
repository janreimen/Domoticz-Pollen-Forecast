# -*- coding: utf-8 -*-
#
# Domoticz Pollen Forecast Plugin
#
# Version: 0.2.1-beta
# Authors: 4D, blooesky, janreimen
#
# Data source: Open-Meteo Air Quality API / CAMS European Air Quality Forecast
# No external Python packages required.
#

"""
<plugin key="PollenForecast"
        name="Pollen Forecast"
        author="4D, blooesky, janreimen"
        version="0.2.1-beta"
        externallink="https://github.com/janreimen/Domoticz-Pollen-Forecast">

    <description>
        <h2>Pollen Forecast</h2>
        <p>
            Modular pollen forecast from the Open-Meteo Air Quality API
            using the CAMS European Air Quality Forecast.
        </p>
        <p>
            Provides individual pollen levels, an optional selected-allergen
            aggregate and a global pollen situation for today and tomorrow.
        </p>
        <p>
            Supports 22 languages: English, Lëtzebuergesch, Deutsch, Français,
            Nederlands, Español, Português, Română, Italiano, Polski, Čeština,
            Български, Magyar, Svenska, Slovenčina, Hrvatski, Slovenščina,
            Srpski, Suomi, Norsk, Dansk and Ελληνικά.
        </p>
    </description>

    <params>
        <param field="Mode1"
               label="Location (longitude,latitude)"
               width="220px"
               required="false"
               default="">
            <description>
                Optional. Enter longitude,latitude to override the Domoticz system location.
                Leave empty to use the latitude and longitude configured in Domoticz.
            </description>
        </param>

        <param field="Mode2"
               label="Language"
               width="180px"
               required="true"
               default="en">
            <options>
                <option label="English" value="en" default="true"/>
                <option label="Lëtzebuergesch" value="lb"/>
                <option label="Deutsch" value="de"/>
                <option label="Français" value="fr"/>
                <option label="Nederlands" value="nl"/>
                <option label="Español" value="es"/>
                <option label="Português" value="pt"/>
                <option label="Română" value="ro"/>
                <option label="Italiano" value="it"/>
                <option label="Polski" value="pl"/>
                <option label="Čeština" value="cs"/>
                <option label="Български" value="bg"/>
                <option label="Magyar" value="hu"/>
                <option label="Svenska" value="sv"/>
                <option label="Slovenčina" value="sk"/>
                <option label="Hrvatski" value="hr"/>
                <option label="Slovenščina" value="sl"/>
                <option label="Srpski" value="sr"/>
                <option label="Suomi" value="fi"/>
                <option label="Norsk" value="no"/>
                <option label="Dansk" value="da"/>
                <option label="Ελληνικά" value="el"/>
            </options>
        </param>

        <param field="Mode3"
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

        <param field="Mode4"
               label="Allergens"
               width="260px"
               required="false"
               default="">
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

VERSION = "0.2.1-beta"


class BasePlugin:
    def __init__(self):
        self.config = None
        self.api = None
        self.devices = None
        self.last_update = 0.0

    def log(self, message):
        if self.config and self.config.debug:
            Domoticz.Log("PollenForecast: {}".format(message))

    def error(self, message):
        Domoticz.Error("PollenForecast: {}".format(message))

    def onStart(self):
        self.config = PluginConfig.from_domoticz(Parameters, Settings)

        if not self.config.valid_location:
            self.error("Invalid location; configure Mode1 as longitude,latitude or leave it empty to use Domoticz coordinates.")
            Domoticz.Heartbeat(30)
            return

        self.api = PollenApi(
            latitude=self.config.latitude,
            longitude=self.config.longitude,
            debug=self.config.debug,
            log_fn=self.log,
        )

        self.devices = PollenDevices(
            devices=Devices,
            language=self.config.language,
            selected_allergens=self.config.allergens,
            debug=self.config.debug,
            log_fn=self.log,
        )
        self.devices.create()

        Domoticz.Heartbeat(30)
        self.log("Starting version {}".format(VERSION))
        self.log("Location: longitude={:.6f}, latitude={:.6f} (source: {})".format(self.config.longitude, self.config.latitude, self.config.location_source))
        self.log("Language: {}".format(self.config.language))
        self.log("Refresh interval: {} minutes".format(self.config.refresh_minutes))
        self.log("Selected allergens: {}".format(", ".join(self.config.allergens)))
        self.update()

    def onStop(self):
        self.log("Plugin stopped")

    def onHeartbeat(self):
        if self.config is None or not self.config.valid_location:
            return
        if time.time() - self.last_update >= self.config.refresh_minutes * 60:
            self.update()

    def update(self):
        if self.api is None or self.devices is None:
            return
        self.log("Updating pollen forecast")
        try:
            data = self.api.fetch()
            days = self.api.build_daily_data(data)
            if len(days) < 2:
                raise ValueError("API response does not contain today and tomorrow")
            self.devices.update_days(days)
            self.last_update = time.time()
            self.log("Pollen forecast updated successfully ({} forecast days received)".format(len(days)))
        except Exception as exc:
            self.error("Update failed: {}".format(exc))
            self.last_update = time.time()


_plugin = BasePlugin()


def onStart():
    _plugin.onStart()


def onStop():
    _plugin.onStop()


def onHeartbeat():
    _plugin.onHeartbeat()
