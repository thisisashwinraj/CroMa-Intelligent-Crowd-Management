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
This module contains the variables used across the hardware-files.
Variables may be used by a single module or by multiple modules simultaneously.

Categories of Variables:
    [1] Buses - Variables used to  store data corresponding to buses database
    [2] Routes - Variables used to  store data corresponding to buses database

.. versionupdated:: 1.1.0

NOTE: By default the values of all of these variables are set to None
"""

# pylint: disable=C0103

# [Routes Database] Variable specifying the route id
route_id = None
# [Routes Database] Variable specifying the list of all bus stops
bus_stops = None
# [Routes Database] Variable specifying the total distance of the route
route_distance = None
# [Routes Database] Variable specifying the expected fuel required
route_required_fuel = None
# [Routes Database] Variable specifying the expected duration  of the journey
route_duration = None
# [Routes Database] Variable specifying the date of creation of the route
route_start_date = None

# [Buses Database] Variable specifying the bus id
bus_id = None
# [Buses Database] Variable specifying total seats in the bus
bus_seats = None
# [Buses Database] Variable specifying the bus type (eg.: fast, Deluxe etc.)
bus_type = None
# [Buses Database] Variable specifying the bus manufacturer's name
bus_manufacturer = None
# [Buses Database] Variable specifying the year of manufacture of the bus
bus_manufacture_year = None
# [Buses Database] Variable specifying the purchase year of the bus
bus_purchase_year = None
# [Buses Database] Variable specifying the type  of fuel used in the bus
bus_fuel = None
# [Buses Database] Variable specifying the fuel capacity of the bus
bus_fuel_capacity = None
# [Buses Database] Variable specifying the next maintenance date of the bus
bus_maintenance_date = None
