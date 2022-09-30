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
This module contains top-level environment of master software, for bus operators.
It contains functions for creating new routes, updating existing routes, editing
the firebase storage database & other supporting functions for the bus operators.

Included Functions:
    [1] create_route
    [2] create_bus
    [3] update_route
    [4] update_bus
    [5] delete_route
    [6] delete_bus

.. versionadded:: 1.1.0

Read more about working of the operator app in the :ref:`CroMa Operator Firmware`
"""

import master_database
import master_terminal


def create_route():
    """
    Function to create a new route in the firebase routes database.

    To create a new route in the database, start with entering the route id followed
    by each  parameter of the database as prompted. If the route id is already used,
    the existing values will be updated with the fresh data. Requires authentication.

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Values are updated in the routes database

    .. See Also:
        master_route_create()

    """
    loop_end = False

    print("\nEnter the route id: ")
    master_terminal.route_id = str(input())

    print(
        "\nEnter the bus stops in correct order:\
        \n(Enter DONE after entering all stops)"
    )
    next_stop = 1
    master_terminal.bus_stops = []

    while loop_end is False:
        next_stop = input()

        if next_stop != "DONE":
            master_terminal.bus_stops.append(next_stop)
        else:
            loop_end = True

    print("\nEnter the total distance of this route, in km: ")
    master_terminal.route_distance = int(input())

    print("\nEnter the approximate fuel required for the trip, in litres: ")
    master_terminal.route_required_fuel = int(input())

    print("\nEnter the travel time required, in minutes:")
    master_terminal.route_duration = int(input())

    print(
        "\nEnter todays date (DD\MM\YYYY):" # pylint: disable=anomalous-backslash-in-string
    )
    master_terminal.route_start_date = str(input())

    master_database.master_route_create()

    print(
        "\nDetails for the route id "
        + master_terminal.route_id
        + " have been recorded\n"
    )


def create_new_bus():
    """
    Function to create a new bus in the firebase buses database.

    To create a new bus in the database, start with entering the bus id followed by
    each parameter of the bus database as prompted. If the bus id is already in use,
    the existing values will be updated with the new value. Requires authentication.

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Values are updated in the buses database

    .. See Also:
        master_bus_create()

    """
    print("\nEnter the bus id: ")
    master_terminal.bus_id = str(input())
    print("\nEnter the total number of seats: ")
    master_terminal.bus_seats = int(input())
    print("\nEnter the type of bus: ")
    master_terminal.bus_type = str(input())

    print("\nEnter the bus manufacturer's name: ")
    master_terminal.bus_manufacturer = str(input())
    print("\nEnter the year of manufacture of bus: ")
    master_terminal.bus_manufacture_year = int(input())
    print("\nEnter the year of purchase of bus: ")
    master_terminal.bus_purchase_year = int(input())

    print("\nEnter the fuel type of bus: ")
    master_terminal.bus_fuel = str(input())
    print("\nEnter the fuel tank capacity of bus: ")
    master_terminal.bus_fuel_capacity = int(input())
    print("\nEnter the date of maintenance: ")
    master_terminal.bus_maintenance_date = str(input())

    master_database.master_bus_create()

    print("\nDetails for the busid " +
          master_terminal.bus_id + " have been recorded\n")


def update_route():
    """
    Function to update route records in the firebase routes database.

    To update the route in the database, start with entering the route id followed
    by each parameter of the database, as prompted. Support for selective updation
    is not available. Operators needs to be authenticated for performing updations.

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Values are updated in the routes database

    .. See Also:
        master_route_update()

    """
    print("\nEnter the route id to be updated: ")
    loop_end = False
    master_terminal.route_id = str(input())

    print(
        "\nEnter the bus stops in correct order:\n(Enter DONE after entering all stops)"
    )
    next_stop = 1
    master_terminal.bus_stops = []

    while loop_end is False:
        next_stop = input()

        if next_stop != "DONE":
            master_terminal.bus_stops.append(next_stop)
        else:
            loop_end = True

    print("\nEnter the total distance of this route, in km: ")
    master_terminal.route_distance = int(input())

    print("\nEnter the approximate fuel required for the trip, in litres: ")
    master_terminal.route_required_fuel = int(input())

    print("\nEnter the travel time required, in minutes:")
    master_terminal.route_duration = int(input())

    print(
        "\nEnter todays date (DD\MM\YYYY):" # pylint: disable=anomalous-backslash-in-string
    )
    master_terminal.route_start_date = str(input())

    master_database.master_route_update()

    print(
        "\nDetails for the route id "
        + master_terminal.route_id
        + " have been updated\n"
    )


def update_bus():
    """
    Function to update bus records in the firebase buses database.

    To update the records in the database, start with entering the bus id followed
    by each parameter of the database, as prompted. Support for selective updation
    is not available. Operators needs to be authenticated for performing updations.

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Values are updated in the buses database

    .. See Also:
        master_bus_update()

    """
    print("\nEnter the bus id to be updated: ")
    master_terminal.bus_id = str(input())
    print("\nEnter the total number of seats: ")
    master_terminal.bus_seats = int(input())
    print("\nEnter the type of bus: ")
    master_terminal.bus_type = str(input())

    print("\nEnter the bus manufacturer's name: ")
    master_terminal.bus_manufacturer = str(input())
    print("\nEnter the year of manufacture of bus: ")
    master_terminal.bus_manufacture_year = int(input())
    print("\nEnter the year of purchase of bus: ")
    master_terminal.bus_purchase_year = int(input())

    print("\nEnter the fuel type of bus: ")
    master_terminal.bus_fuel = str(input())
    print("\nEnter the fuel tank capacity of bus: ")
    master_terminal.bus_fuel_capacity = int(input())
    print("\nEnter the date of maintenance: ")
    master_terminal.bus_maintenance_date = str(input())

    master_database.master_bus_update()

    print("\nDetails for the busid " +
          master_terminal.bus_id + " have been updated\n")


def delete_route():
    """
    Function to delete all records for routes in the firebase routes database.

    To delete a route from the database, start with entering the route id followed
    by confirming it. Operators needs to be authenticated for performing deletions.
    WARNING: The action is permanent i.e once deleted the records are lost forever.

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Route records are deleted from the routes database

    .. See Also:
        master_route_delete()

    """
    print("\nEnter the route id to be deleted: ")
    master_terminal.route_id = str(input())

    master_database.master_route_delete()

    print("\nThe Route " + master_terminal.route_id + " has been deleted\n")


def delete_bus():
    """
    Function to delete all records for routes in the firebase routes database.

    To delete bus record from database, start with entering the bus id followed by
    confirming that. Operators needs to be authenticated, for performing deletions.
    Warning: The action is permanent i.e once deleted the records are lost forever.

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Bus records are deleted from the buses database

    .. See Also:
        master_bus_delete()

    """
    print("\nEnter the bus id to be deleted: ")
    master_terminal.bus_id = str(input())

    master_database.master_bus_delete()

    print("\nThe Bus " + master_terminal.bus_id + " has been deleted\n")


if __name__ == "__main__":
#    >>> Enter your username:
#    Admin@ksrtc.com
#
#    >>> Enter your password:
#    ********
#
#    >>> MENU: Enter option:
#            1. Add New Route
#            2. Add New BusID
#            3. Update Route
#            4. Update BusID
#            5. Delete Route
#            6. Delete BusID
#            7. Exit
#    5
#
#    >>>  Enter the route id to be deleted:
#    TVM_KYM_01
#
#    The Route TVM_KYM_01 has been deleted.

    ERROR = None

    AUTH_USERNAME = "Admin@ksrtc.com"
    AUTH_PASSWORD = "xKSRTC4%6"

    print("\nEnter your username:")
    USERNAME = str(input())

    if USERNAME != AUTH_USERNAME:
        print("\nUh-Oh Could find this Username! Try again!")

        ERROR = 502  # Bad Gateway
        SystemExit(0)

    print("\nEnter your password:")
    PASSWORD = str(input())

    if PASSWORD != AUTH_PASSWORD:
        print("\nUh-Oh Wrong Password! Try again!")

        ERROR = 502  # Bad Gateway
        SystemExit(0)

    if not ERROR:
        SELECTED_OPTION = 0

        while SELECTED_OPTION != 7:

            print(
                "MENU: Enter option:\
                \n1. Add New Route\
                \n2. Add New BusID\
                \n3. Update Route\
                \n4. Update BusID\
                \n5. Delete Route\
                \n6. Delete BusID\
                \n7. Exit\n"
            )
            SELECTED_OPTION = int(input())

            # add a new route
            if SELECTED_OPTION == 1:
                create_route()

            # add a new busid
            elif SELECTED_OPTION == 2:
                create_new_bus()

            elif SELECTED_OPTION == 3:
                update_route()

            elif SELECTED_OPTION == 4:
                update_bus()

            elif SELECTED_OPTION == 5:
                delete_route()

            elif SELECTED_OPTION == 6:
                delete_bus()

            else:
                print("Enter a valid choice")
