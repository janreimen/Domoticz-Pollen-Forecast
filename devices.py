# -*- coding: utf-8 -*-
"""Domoticz device handling for the Pollen Forecast plugin."""

import math

import Domoticz

from pollen import KNOWN_POLLEN, get_definition, level_for, pollen_key_for_allergen
from translations import get_translation


class PollenDevices:
    DAYS = ("today", "tomorrow")
    SELECTED_UNIT_START = 100
    GLOBAL_UNIT_START = 110

    def __init__(self, devices, language, selected_allergens, debug=False, log_fn=None):
        self.devices = devices
        self.language = language
        self.translation = get_translation(language)
        self.selected_allergens = tuple(selected_allergens)
        self.debug = debug
        self.log_fn = log_fn

    def log(self, message):
        if self.debug and self.log_fn:
            self.log_fn("Devices: {}".format(message))

    def create(self):
        # Keep the complete fixed unit map internally, but only create
        # individual pollen devices selected by the user.
        for allergen in self.selected_allergens:
            pollen_key = pollen_key_for_allergen(allergen)
            for day in self.DAYS:
                self._create_if_missing(
                    self._unit_for(pollen_key, day),
                    self._device_name(pollen_key, day),
                )
        if len(self.selected_allergens) > 1:
            self._create_if_missing(100, self._aggregate_device_name("selected_pollen", "today"))
            self._create_if_missing(101, self._aggregate_device_name("selected_pollen", "tomorrow"))
        self._create_if_missing(110, self._aggregate_device_name("global_situation", "today"))
        self._create_if_missing(111, self._aggregate_device_name("global_situation", "tomorrow"))

    def _create_if_missing(self, unit, name):
        if unit in self.devices:
            return
        Domoticz.Device(Name=name, Unit=unit, TypeName="Alert", Used=1).Create()
        self.log("Created device {}: {}".format(unit, name))

    def update_days(self, days):
        if len(days) < 2:
            raise ValueError("Need today and tomorrow forecast data")
        self.update_day(days[0], "today")
        self.update_day(days[1], "tomorrow")

    def update_day(self, day, day_name):
        if day_name not in self.DAYS:
            raise ValueError("Unsupported forecast day: {}".format(day_name))
        # Calculate all supported pollen levels because the global
        # situation is independent of the user's allergen selection.
        levels = {}
        for pollen_key in self._pollen_keys():
            concentration = day["values"].get(pollen_key)
            levels[pollen_key] = level_for(pollen_key, concentration)

        # Only update individual devices selected by the user. Their unit
        # numbers remain fixed according to the complete internal map.
        for allergen in self.selected_allergens:
            pollen_key = pollen_key_for_allergen(allergen)
            self._update(
                self._unit_for(pollen_key, day_name),
                levels[pollen_key],
                self._level_text(levels[pollen_key]),
            )

        available = [level for level in levels.values() if level > 0]
        global_level = max(available) if available else 0
        self._update(
            self._aggregate_unit("global_situation", day_name),
            global_level,
            self._level_text(global_level),
        )
        if len(self.selected_allergens) > 1:
            selected_levels = [levels.get(pollen_key_for_allergen(a), 0) for a in self.selected_allergens]
            selected_level = self._average_level(selected_levels)
            self._update(
                self._aggregate_unit("selected_pollen", day_name),
                selected_level,
                self._level_text(selected_level),
            )

    @staticmethod
    def _pollen_keys():
        return tuple(KNOWN_POLLEN.keys())

    def _device_name(self, pollen_key, day_name):
        pollen_label = self.translation["pollen"].get(pollen_key, get_definition(pollen_key).key)
        suffix = self.translation[day_name]
        return "{} {}".format(pollen_label, suffix)

    def _aggregate_device_name(self, key, day_name):
        return "{} {}".format(self.translation[key], self.translation[day_name])

    def _unit_for(self, pollen_key, day_name):
        index = self._pollen_keys().index(pollen_key)
        return index * 2 + self.DAYS.index(day_name) + 1

    def _aggregate_unit(self, key, day_name):
        base = self.SELECTED_UNIT_START if key == "selected_pollen" else self.GLOBAL_UNIT_START
        return base + self.DAYS.index(day_name)

    def _level_text(self, level):
        return self.translation["levels"].get(level, self.translation["no_data"])

    @staticmethod
    def _average_level(levels):
        if not levels:
            return 0
        return int(math.floor((sum(levels) / float(len(levels))) + 0.5))

    def _update(self, unit, nvalue, svalue):
        if unit not in self.devices:
            return
        device = self.devices[unit]
        if device.nValue != nvalue or device.sValue != svalue:
            device.Update(nValue=nvalue, sValue=svalue)
