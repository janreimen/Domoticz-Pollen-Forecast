# -*- coding: utf-8 -*-
"""
Translations for the Pollen Forecast plugin.
"""


TRANSLATIONS = {

    "en": {
        "today": "Today",
        "tomorrow": "Tomorrow",

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
        "today": "Haut",
        "tomorrow": "Muer",

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
        "today": "Heute",
        "tomorrow": "Morgen",

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
        "today": "aujourd'hui",
        "tomorrow": "demain",

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
        "today": "vandaag",
        "tomorrow": "morgen",

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
