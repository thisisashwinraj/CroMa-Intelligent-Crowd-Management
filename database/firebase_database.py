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
This module contains methods for performing CRUD operations on firebase database.
It also contains methods for authenticatinng the users & selective data fetching.
NOTE: Firebase authentication uses app mail/password for authenticating the user.

Included Functions:
    [1] initialize_database
    [2] refresh_database
    [3] update_available_seats
    [4] update_current_location
    [5] update_passengers_count
    [6] retrieve_available_seats
    [7] retrieve_current_location
    [8] retrieve_passengers_count
    [9] update_last_stop_arrival_time
    [10] update_current_bus_status
    [11] update_current_route_id
    [12] retrieve_bus_total_delay
    [13] retrieve_last_stop_arrival_time
    [14] retrieve_current_bus_status
    [15] retrieve_bus_route_id
    [16] update_bus_total_delay

.. versionadded:: 1.2.0
.. versionupdated:: 1.3.0

Read more about the database used in CroMa in the :ref:`CroMa Hardware Databases`
"""

from firebase_admin import db
import datetime
from datetime import datetime


def initialize_database(bus_id="KL13N", input_route_id="Route00"):
    """
    Method to initialize a fresh child node in the FireBase real-time databases.

    The Bus Id is used as the database node's key value (child name), to create
    a new node that will reflect the crowd levels, and other useful information
    pertaining to that bus in real time. Default values are initially reflected.

    .. versionadded:: 1.2.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database
        [str] input_route_id: Unique Route Id assigned to the bus for this trip

    Returns:
        None -> Creates/Updates a node in the FireBase db with the bus id as key

    Warning:
        [node exists] If nodes with same name exists, new node values are reset.

    NOTE: User needs to be authenticated for performing the initialize operation
    """
    ref = db.reference("/")  # Create a reference to the root node of the database

    # Set the initial values for the real time-db, keeping bus_id as the key node
    ref.update(
        {
            bus_id: {
                "available_seats": 32,
                "current_location": "Thampanoor",
                "passengers_count": 0,
                "current_bus_status": "Active",
                "current_route_id": input_route_id,
                "delay_in_mins": 0,
                "last_stop_arrival_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        }
    )


def refresh_database(bus_id):
    """
    Method to refresh the values of a given child node in the Firebase database.

    The Bus Id is used as the database node's key value (child name) to refresh
    an existing node to reflect the default values and other useful information
    pertaining to that bus in real-time. Only changed values, will be refreshed.

    .. versionadded:: 1.2.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Refreshes values of a node to its default value in the database

    NOTE: Users needs to be authenticated for performing this refresh operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Refresh the values of the referenced bus_id in the firebase database
    ref.update(
        {
            "available_seats": 32,
            "current_location": "Thampanoor",
            "passengers_count": 0,
            "current_bus_status": "Inactive",
            "current_route_id": "Route00",
            "delay_in_mins": 0,
        }
    )


def update_available_seats(bus_id, available_seat_count):
    """
    Method to update the current values of available seats in Firebase database.

    The Bus Id is used as the database node's key value (child name), to update
    the available seat count in the bus. Only changed values, are to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Updates available seat count in the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Refresh the values of the referenced bus_id in the firebase database
    ref.update({"available_seats": available_seat_count})


def update_current_location(bus_id, new_location):
    """
    Method to update the present value of current location in Firebase database.

    The Bus Id is used as the database node's key value (child name), to update
    the current location of this bus. Only the changed values are to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Updates the current location in the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Refresh the values of the referenced bus_id in the firebase database
    ref.update({"current_location": new_location})


def update_passengers_count(bus_id, total_passengers):
    """
    Method to update the present value of passengers count in Firebase database.

    The Bus Id is used as the database node's key value (child name), to update
    the passengers count of this bus. Only the changed values are to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database
        [int] total_passengers: The total count of passenger to be updated with

    Returns:
        None -> Update the passengers count in the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Refresh the values of the referenced bus_id in the firebase database
    ref.update({"passengers_count": total_passengers})


def retrieve_available_seats(bus_id):
    """
    Method to retrieve the total count of available seats in Firebase database.

    The Bus Id is used as the database nodes key value (child name) to retrieve
    the available seats of this bus. Only the changed values, are to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Retrieve passengerd count, from the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Create a reference to get the available seats value for the child node
    db_available_seats = ref.child("available_seats").get()

    return db_available_seats  # Return value of the referenced bus_id from the database


def retrieve_current_location(bus_id):
    """
    Method to retrieve the current value of current loc from Firebase database.

    The Bus Id is used as the database nodes key value (child name) to retrieve
    the current location of the bus. Only the changed values, are to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Retrieve current location, from the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Create a reference to get the current location value for the child node
    db_current_location = ref.child("current_location").get()

    return (
        db_current_location  # Return value of the referenced bus_id from the database
    )


def retrieve_passengers_count(bus_id):
    """
    Method to retrieve current value of passengers count from Firebase database.

    The Bus Id is used as the database nodes key value (child name) to retrieve
    the passengers count of the bus. Only the changed values, are to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Retrieve passengers count, from the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Create a reference to get the current location value for the child node
    db_passengers_count = ref.child("passengers_count").get()

    return (
        db_passengers_count  # Return value of the referenced bus_id from the database
    )


def update_last_stop_arrival_time(bus_id, last_stop_arrival_time):
    """
    Method to update the value of last stop's arrival time in Firebase database.

    The Bus Id is used as the database node's key value (child name), to update
    the last stop arrival time of bus. Only the changed values are to be updated.

    .. versionadded:: 1.3.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database
        [datetime] last_stop_arrival_time: Time at which bus reached last stop

    Returns:
        None -> Update last stop's arrival time, in real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    last_stop_arrival_time = last_stop_arrival_time.strftime("%Y-%m-%d %H:%M:%S")

    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Update the values of the referenced bus_id in the firebase database
    ref.update({"last_stop_arrival_time": last_stop_arrival_time})


def update_current_bus_status(bus_id, bus_status):
    """
    Method to update the value of last stop's arrival time in Firebase database.

    The Bus Id is used as the database node's key value (child name), to update
    the last stop arrival time of bus. Only the changed values are to be updated.

    .. versionadded:: 1.3.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database
        [datetime] last_stop_arrival_time: Time at which bus reached last stop

    Returns:
        None -> Update last stop's arrival time, in real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Update the values of the referenced bus_id in the firebase database
    ref.update({"current_bus_status": bus_status})


def update_current_route_id(bus_id, route_id):
    """
    Method to update the value of the bus current route id in Firebase database.

    The Bus Id is used as the database node's key value (child name), to update
    the value of the route id of bus. Only the changed values are to be updated.

    .. versionadded:: 1.3.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database
        [str] route_id: The unique route id assigned to the bus for single trip

    Returns:
        None -> Update the value of the route id in real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Update the values of the referenced bus_id in the firebase database
    ref.update({"current_route_id": route_id})


def retrieve_bus_total_delay(bus_id):
    """
    Method to retrieve the total delay in current journey from Firebase database.

    The Bus Id is used as the database nodes key value (child name) to retrieve
    the total delay in the journey of the bus. Only changed values, are updated.

    .. versionadded:: 1.3.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Retrieve bus's total delay from the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Create a reference to get the current location value for the child node
    db_passengers_count = ref.child("delay_in_mins").get()

    return (
        db_passengers_count  # Return value of the referenced bus_id from the database
    )


def retrieve_last_stop_arrival_time(bus_id):
    """
    Method to retrieve the arrival time at the last stop from Firebase database.

    The Bus Id is used as the database nodes key value (child name) to retrieve
    bus's arrival time at last stop. Only the changed values, are to be updated.

    .. versionadded:: 1.3.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Retrieve the last stop arrival time from the real-time database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Create a reference to get the current location value for the child node
    db_last_stop_arrival_time = ref.child("last_stop_arrival_time").get()

    return datetime.strptime(db_last_stop_arrival_time, "%Y-%m-%d %H:%M:%S")


def retrieve_current_bus_status(bus_id):
    """
    Method to retrieve current value of passengers count from Firebase database.

    The Bus Id is used as the database nodes key value (child name) to retrieve
    the passengers count of the bus. Only the changed values, are to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Retrieve passengers count, from the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Create a reference to get the current location value for the child node
    db_passengers_count = ref.child("passengers_count").get()

    return (
        db_passengers_count  # Return value of the referenced bus_id from the database
    )


def retrieve_bus_route_id(bus_id):
    """
    Method to retrieve current value of the bus route id from Firebase database.

    The Bus Id is used as the database nodes key value (child name) to retrieve
    the specific route id of that bus. Only the changed value, is to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Retrieve the bus route id, from the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Create a reference to get the current location value for the child node
    db_current_route_id = ref.child("current_route_id").get()

    return (
        db_current_route_id  # Return value of the referenced bus_id from the database
    )


def update_bus_total_delay(bus_id, delay_in_mins):
    """
    Method to update the value of the bus's total delay in the Firebase database.

    The Bus Id is used as the database node's key value (child name), to update
    the value of total delay in trip. Only the changed values are to be updated.

    .. versionadded:: 1.3.0

    Parameters:
        [str] bus_id: Bus Id is used to initialize a child node in the database
        [int] delay_in_mins: Total delay in minutes to be updated in firebase db

    Returns:
        None -> Update the value of total delay in mins in real-time firebase db

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference(bus_id)  # Create a reference to the key node of the database

    # Refresh the values of the referenced bus_id in the firebase database
    ref.update({"delay_in_mins": delay_in_mins})
