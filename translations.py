# -*- coding: utf-8 -*-
"""
Translations for the Pollen Forecast plugin.
"""


TRANSLATIONS = {

    "en": {

        "device_alert_today": "Pollen Alert Today",
        "device_alert_tomorrow": "Pollen Alert Tomorrow",
        "device_today": "Pollen Today",
        "device_tomorrow": "Pollen Tomorrow",

        "unknown_pollen": "Unknown pollen",
        "no_data": "No data",

        "levels": {
            0: "No data",
            1: "None",
            2: "Low",
            3: "Medium",
            4: "High",
        },

        "pollen": {
            "alder_pollen": "Alder",
            "birch_pollen": "Birch",
            "grass_pollen": "Grass",
            "mugwort_pollen": "Mugwort",
            "olive_pollen": "Olive",
            "ragweed_pollen": "Ragweed",
        },
    },

    "lb": {

        "device_alert_today": "Pollen Alarm haut",
        "device_alert_tomorrow": "Pollen Alarm muer",
        "device_today": "Pollen haut",
        "device_tomorrow": "Pollen muer",

        "unknown_pollen": "Onbekannte Pollen",
        "no_data": "Keng Donnéeën",

        "levels": {
            0: "Keng Donnéeën",
            1: "Keng",
            2: "Niddereg",
            3: "Mëttel",
            4: "Héich",
        },

        "pollen": {
            "alder_pollen": "Erle",
            "birch_pollen": "Birk",
            "grass_pollen": "Gras",
            "mugwort_pollen": "Beifouss",
            "olive_pollen": "Oliven",
            "ragweed_pollen": "Ambrosia",
        },
    },

    "de": {

        "device_alert_today": "Pollenwarnung heute",
        "device_alert_tomorrow": "Pollenwarnung morgen",
        "device_today": "Pollen heute",
        "device_tomorrow": "Pollen morgen",

        "unknown_pollen": "Unbekannter Pollen",
        "no_data": "Keine Daten",

        "levels": {
            0: "Keine Daten",
            1: "Keine",
            2: "Niedrig",
            3: "Mittel",
            4: "Hoch",
        },

        "pollen": {
            "alder_pollen": "Erle",
            "birch_pollen": "Birke",
            "grass_pollen": "Gräser",
            "mugwort_pollen": "Beifuß",
            "olive_pollen": "Olive",
            "ragweed_pollen": "Ambrosia",
        },
    },

    "fr": {

        "device_alert_today": "Alerte pollen aujourd'hui",
        "device_alert_tomorrow": "Alerte pollen demain",
        "device_today": "Pollen aujourd'hui",
        "device_tomorrow": "Pollen demain",

        "unknown_pollen": "Pollen inconnu",
        "no_data": "Aucune donnée",

        "levels": {
            0: "Aucune donnée",
            1: "Aucun",
            2: "Faible",
            3: "Moyen",
            4: "Élevé",
        },

        "pollen": {
            "alder_pollen": "Aulne",
            "birch_pollen": "Bouleau",
            "grass_pollen": "Graminées",
            "mugwort_pollen": "Armoise",
            "olive_pollen": "Olivier",
            "ragweed_pollen": "Ambroisie",
        },
    },

    "nl": {

        "device_alert_today": "Pollenwaarschuwing vandaag",
        "device_alert_tomorrow": "Pollenwaarschuwing morgen",
        "device_today": "Pollen vandaag",
        "device_tomorrow": "Pollen morgen",

        "unknown_pollen": "Onbekend pollen",
        "no_data": "Geen gegevens",

        "levels": {
            0: "Geen gegevens",
            1: "Geen",
            2: "Laag",
            3: "Gemiddeld",
            4: "Hoog",
        },

        "pollen": {
            "alder_pollen": "Els",
            "birch_pollen": "Berk",
            "grass_pollen": "Grassen",
            "mugwort_pollen": "Bijvoet",
            "olive_pollen": "Olijf",
            "ragweed_pollen": "Ambrosia",
        },
    },
}


def get_translation(
    language,
):

    return TRANSLATIONS.get(
        language,
        TRANSLATIONS["en"],
    )
