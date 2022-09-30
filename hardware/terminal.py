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
    [1] Dynamic - These variables store data that changes in real-time
    [2] User Input - These variables store the input read from users
    [3] Database Fetched - These variables reflect values read from database.

.. versionadded:: 1.0.1
.. versionupdated:: 1.1.0

NOTE: By default the values of all of these variables is set to None
"""

# pylint: disable=C0103

# [Database Fetched] Variable specifying bus type (eg:express, city etc)
bus_type = None
# [Database Fetched] A list of all bus stops in a given route
selected_route = None
# [Database Fetched] Total number of seats in a bus
total_seats = None

# [User-Input] Unique Id associate with each bus, fetches info from busDB
bus_id = None
# [User-Input] E-Mail for user authentication by firebase real-time database
input_email = None
# [User-Input] Password assosciated with firebase email id authentication
input_password = None
# [User-Input] Unique Id associated with each route, fetches info from routesDB
route_id = None

# [Dynamic] Free seats available in a bus in transit. Default value set to 0
available_seat_count = None
# [Dynamic] Amount collected as fare during the trip. Default value set to 0
collection = None
# [Dynamic] An array of 0s of length(selected_route) managing crowd information
crowd_manager = None
# [Dynamic] The current location of the bus. Default value set to origin
current_location = None
# [Dynamic] Total no. of passengers in bus at a given time. Default value is 0
current_passenger_count = None
# [Dynamic] Total tickets printed throughout the trip. Default value set to 0
total_tickets_printed = None
