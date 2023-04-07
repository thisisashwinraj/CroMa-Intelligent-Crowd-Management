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
This module contains medthods for performing CRUD operation on firebase database.
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

.. versionadded:: 1.2.0

Read more about the database used in CroMa in the :ref:`CroMa Hardware Databases`
"""

from firebase_admin import db
import terminal


def initialize_database():
    """
    Method to initialize a fresh child node in the FireBase real-time databases.

    The Bus Id is used as the database node's key value (child name), to create
    a new node that will reflect the crowd levels, and other useful information
    pertaining to that bus in real time. Default values are initially reflected.

    .. versionadded:: 1.2.0

    Parameters:
        [str] Bus id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Creates a new node in the FireBase database, with bus id as key

    Warning:
        [node exists] If nodes with same name exists, new node values are reset.

    NOTE: User needs to be authenticated for performing the initialize operation
    """
    ref = db.reference("/")  # Create a reference to the root node of the database

    # Set the initial values for the real time-db, keeping bus_id as the key node
    ref.set(
        {
            "KL13N": {
                "available_seats": 32,
                "current_location": "Trivandrum",
                "passengers_count": 0,
            }
        }
    )


def refresh_database():
    """
    Method to refresh the values of a given child node in the Firebase database.

    The Bus Id is used as the database node's key value (child name) to refresh
    an existing node to reflect the default values and other useful information
    pertaining to that bus in real-time. Only changed values, will be refreshed.

    .. versionadded:: 1.2.0

    Parameters:
        [str] Bus id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Refreshes values of a node to its default value in the database

    NOTE: Users needs to be authenticated for performing this refresh operation
    """
    ref = db.reference("KL13N")  # Create a reference to the key node of the database

    # Refresh the values of the referenced bus_id in the firebase database
    ref.update(
        {"available_seats": 32, "current_location": "Trivandrum", "passengers_count": 0}
    )


def update_available_seats():
    """
    Method to update the current values of available seats in Firebase database.

    The Bus Id is used as the database node's key value (child name), to update
    the available seat count in the bus. Only changed values, are to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] Bus id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Refreshes the available seat in the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference("KL13N")  # Create a reference to the key node of the database

    # Refresh the values of the referenced bus_id in the firebase database
    ref.update({"available_seats": terminal.available_seat_count})


def update_current_location():
    """
    Method to update the current value of current location in Firebase database.

    The Bus Id is used as the database node's key value (child name), to update
    the current location of this bus. Only the changed values are to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] Bus id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Refresh the current location in the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference("KL13N")  # Create a reference to the key node of the database

    # Refresh the values of the referenced bus_id in the firebase database
    ref.update({"current_location": terminal.current_location})


def update_passengers_count():
    """
    Method to update the current value of passengers count in Firebase database.

    The Bus Id is used as the database node's key value (child name), to update
    the passengers count of this bus. Only the changed values are to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] Bus id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Refresh the passengers count in the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference("KL13N")  # Create a reference to the key node of the database

    # Refresh the values of the referenced bus_id in the firebase database
    ref.update({"passengers_count": terminal.total_passengers})


def retrieve_available_seats():
    """
    Method to retrieve the available seats current value from Firebase database.

    The Bus Id is used as the database nodes key value (child name) to retrieve
    the available seats of this bus. Only the changed values, are to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] Bus id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Retrieve passengerd count, from the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference("KL13N")  # Create a reference to the key node of the database

    # Create a reference to get the available seats value for the child node
    db_available_seats = ref.child("available_seats").get()

    return db_available_seats  # Return value of the referenced bus_id from the database


def retrieve_current_location():
    """
    Method to retrieve the current value of current loc from Firebase database.

    The Bus Id is used as the database nodes key value (child name) to retrieve
    the current location of the bus. Only the changed values, are to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] Bus id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Retrieve current location, from the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference("KL13N")  # Create a reference to the key node of the database

    # Create a reference to get the current location value for the child node
    db_current_location = ref.child("current_location").get()

    return (
        db_current_location  # Return value of the referenced bus_id from the database
    )


def retrieve_passengers_count():
    """
    Method to retrieve current value of passengers count from Firebase database.

    The Bus Id is used as the database nodes key value (child name) to retrieve
    the passengers count of the bus. Only the changed values, are to be updated.

    .. versionadded:: 1.2.0

    Parameters:
        [str] Bus id: Bus Id is used to initialize a child node in the database

    Returns:
        None -> Retrieve passengers count, from the real-time firebase database

    NOTE: Users needs to be authenticated, for performing this update operation
    """
    ref = db.reference("KL13N")  # Create a reference to the key node of the database

    # Create a reference to get the current location value for the child node
    db_passengers_count = ref.child("passengers_count").get()

    return (
        db_passengers_count  # Return value of the referenced bus_id from the database
    )
