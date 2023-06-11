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
    [1] retrieve_current_bus_status
    [2] retrieve_bus_route_id
    [3] retrieve_current_location
    [4] retrieve_bus_data_from_sql_database
    [5] retrieve_available_seats
    [6] retrieve_passengers_count
    [7] retrieve_bus_total_delay
    [8] retrieve_last_stop_arrival_time

.. versionadded:: 1.2.0
.. versionupdate:: 1.3.0

Read more about the database used in CroMa in the :ref:`CroMa Hardware Databases`
"""

import sqlite3
import datetime
from datetime import datetime
from firebase_admin import db


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

    # Create a reference to get the current bus status for the child node
    db_current_bus_status = ref.child("current_bus_status").get()

    return (
        db_current_bus_status  # Return value of the referenced bus_id from the database
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

    # Create a reference to get the route id for the child node
    db_current_route_id = ref.child("current_route_id").get()

    return (
        db_current_route_id  # Return value of the referenced bus_id from the database
    )


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


def retrieve_bus_data_from_sql_database(bus_id):
    """
    Method to retrieve select data corresponding to a bus from the SQL database.

    The Bus Id is used as the database nodes key value (child name) to retrieve
    the corresponding data of the bus. Only the changed value, is to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] bus_id: Bus Id is used to uniquely identify the buses in SQL DBMS

    Returns:
        None -> Retrieve the bus operator, & the bus type from the SQL database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    conn = sqlite3.connect("croma_playground.db")
    cursor = conn.cursor()  # Connect to the SQL database

    # Retrieve specific values from the table
    select_query = """
        SELECT BusOperator, BusType
        FROM Bus
        WHERE BusId = ?
    """
    cursor.execute(select_query, (bus_id,))
    result = cursor.fetchone()

    # Close the database connection
    return result


def retrieve_available_seats(bus_id):
    """
    Method to retrieve the available seats current value from Firebase database.

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

    # Create a reference to get the  passenger count value for the child node
    db_passengers_count = ref.child("passengers_count").get()

    return (
        db_passengers_count  # Return value of the referenced bus_id from the database
    )


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

    # Create a reference to get the delay in minutes for the child node
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

    # Create a reference to get the last stop arrival time for the child node
    db_last_stop_arrival_time = ref.child("last_stop_arrival_time").get()

    # Convert the datetime string into datetime object
    return datetime.strptime(db_last_stop_arrival_time, "%Y-%m-%d %H:%M:%S")
