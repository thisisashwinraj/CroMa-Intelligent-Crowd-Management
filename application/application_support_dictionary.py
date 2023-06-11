# Author: Ashwin Raj <thisisashwinraj@gmail.com>
# License: Creative Commons Attribution - NonCommercial - NoDerivs License
# Discussions-to: github.com/thisisashwinraj/CroMa-Crowd-Management-System/discussions

# By exercising the Licensed Rights (defined in LICENSE), You accept and agree
# to be bound by the terms and conditions of the Creative Commons
# Attribution-NonCommercial-NoDerivatives 4.0 International Public License
# ("Public License"). To the extent this Public License may be interpreted as
# a contract, You are granted the Licensed Rights in consideration of Your
# acceptance of the terms and conditions, and the Licensor grants You such
# rights in consideration of benefits the Licensor receives from making the
# Licensed Material available under terms and conditions described in LICENSE.

"""
This module provides the hashmaps that store information about buses, and routes 
to be used for backend computation. These dictionaries serve as a support system 
for managing & accessing data related to buses and routes within the application.

Included Hashmaps:
    [1] all_bus_stops
    [2] all_bus_id
    [3] all_routes
    [4] bus_timings

.. versionadded:: 1.3.0

Read more about the usecase of support dictionaries in :ref:`Support Dictionaries`
"""

# Hashmap storing bus stop name as keys and list of buses passing through that stop as values
all_bus_stops = {
    "Thampanoor": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
    "Venjaramoodu": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
    "Killimanoor": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
    "Jatayupara": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
    "Kottarakkara": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
    "Pandalam": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
    "Thiruvalla": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
    "Chengannur": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
    "Thampanoor": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
    "Kottayam": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
    "Pattom": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
    "Palayam": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
    "Kariavattom": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
    "Kasaragod": ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"],
}


# List of all valid bus id's assigned by the bus administrators
all_bus_id = ["KL13N", "KL08B", "KL17Q", "KL24P", "KL64L"]


# Hashmap storing Route Id as the key and list of all bus stops in that route as value
all_routes = {
    # Route 00 - Default route for inactive buses
    "Route00": [
        "Thampanoor",
        "Venjaramoodu",
        "Killimanoor",
        "Jatayupara",
        "Kottarakkara",
        "Pandalam",
        "Thiruvalla",
        "Chengannur",
        "Kottayam",
    ],
    # Route 01 - Trivandrum to Kottayam
    "Route01": [
        "Thampanoor",
        "Venjaramoodu",
        "Killimanoor",
        "Jatayupara",
        "Kottarakkara",
        "Pandalam",
        "Thiruvalla",
        "Chengannur",
        "Kottayam",
    ],
    # Route 02 - Trivandrum to Kottayam
    "Route02": [
        "Thampanoor",
        "Venjaramoodu",
        "Killimanoor",
        "Jatayupara",
        "Kottarakkara",
        "Pandalam",
        "Thiruvalla",
        "Chengannur",
        "Kottayam",
    ],
    # Route 03 - Trivandrum to Kottayam
    "Route03": [
        "Thampanoor",
        "Venjaramoodu",
        "Killimanoor",
        "Jatayupara",
        "Kottarakkara",
        "Pandalam",
        "Thiruvalla",
        "Chengannur",
        "Kottayam",
    ],
    # Route 04 - Trivandrum to Kottayam
    "Route04": [
        "Thampanoor",
        "Venjaramoodu",
        "Killimanoor",
        "Jatayupara",
        "Kottarakkara",
        "Pandalam",
        "Thiruvalla",
        "Chengannur",
        "Kottayam",
    ],
    # Route 05 - Trivandrum to Kottayam
    "Route05": [
        "Thampanoor",
        "Venjaramoodu",
        "Killimanoor",
        "Jatayupara",
        "Kottarakkara",
        "Pandalam",
        "Thiruvalla",
        "Chengannur",
        "Kottayam",
    ],
    # Route 06 - Trivandrum to Kottayam
    "Route06": [
        "Thampanoor",
        "Venjaramoodu",
        "Killimanoor",
        "Jatayupara",
        "Kottarakkara",
        "Pandalam",
        "Thiruvalla",
        "Chengannur",
        "Kottayam",
    ],
    # Route 07 - Trivandrum to Kottayam
    "Route07": [
        "Thampanoor",
        "Venjaramoodu",
        "Killimanoor",
        "Jatayupara",
        "Kottarakkara",
        "Pandalam",
        "Thiruvalla",
        "Chengannur",
        "Kottayam",
    ],
    # Route 08 - Trivandrum to Kottayam
    "Route08": [
        "Thampanoor",
        "Venjaramoodu",
        "Killimanoor",
        "Jatayupara",
        "Kottarakkara",
        "Pandalam",
        "Thiruvalla",
        "Chengannur",
        "Kottayam",
    ],
    # Route 09 - Trivandrum to Kottayam
    "Route09": [
        "Thampanoor",
        "Venjaramoodu",
        "Killimanoor",
        "Jatayupara",
        "Kottarakkara",
        "Pandalam",
        "Thiruvalla",
        "Chengannur",
        "Kottayam",
    ],
}


# Hashmap storing Route Id as key and dictionary of bus stopstiming as value
# The nested dictionary stores bus stop as key and time to reach that stop from origin as value
bus_timings = {
    "Route00": {
        "Thampanoor": 0,
        "Venjaramoodu": 6,
        "Killimanoor": 11,
        "Jatayupara": 20,
        "Kottarakkara": 31,
        "Pandalam": 39,
        "Thiruvalla": 44,
        "Chengannur": 52,
        "Kottayam": 60,
    },
    # Route 01 - Trivandrum to Kottayam
    "Route01": {
        "Thampanoor": 0,
        "Venjaramoodu": 6,
        "Killimanoor": 11,
        "Jatayupara": 20,
        "Kottarakkara": 31,
        "Pandalam": 39,
        "Thiruvalla": 44,
        "Chengannur": 52,
        "Kottayam": 60,
    },
    # Route 02 - Trivandrum to Kottayam
    "Route02": {
        "Thampanoor": 0,
        "Venjaramoodu": 6,
        "Killimanoor": 11,
        "Jatayupara": 20,
        "Kottarakkara": 31,
        "Pandalam": 39,
        "Thiruvalla": 44,
        "Chengannur": 52,
        "Kottayam": 60,
    },
    # Route 03 - Trivandrum to Kottayam
    "Route03": {
        "Thampanoor": 0,
        "Venjaramoodu": 6,
        "Killimanoor": 11,
        "Jatayupara": 20,
        "Kottarakkara": 31,
        "Pandalam": 39,
        "Thiruvalla": 44,
        "Chengannur": 52,
        "Kottayam": 60,
    },
}
