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
This module contains the functions used for performing CRUD operation on DB.
It also contains functions for user authentication & selective data fetching.

Included Functions:
    [1] log_in
    [2] initialize_real_time_crowd_database
    [3] update_real_time_crowd_database
    [4] fetch_route
    [5] fetch_bus_type
    [6] fetch_total_seats

.. versionadded:: 1.0.1
.. versionupdated:: 1.1.0

NOTE: Firebase authentication uses e-mail/password for authentication of users
Read more about the database used in CroMa in the :ref:`CroMa Hardware Database`
"""

# pylint: disable=unsubscriptable-object

import pyrebase # pylint: disable=import-error
import master_terminal
import master_credentials # pylint: disable=import-error


def master_route_create():
    """
    Function to create a new child node in the routes firebase real-time database.

    To create a new route in the database, start with entering the route id followed
    by each  parameter of the database as prompted. If the route id is already used,
    the existing values will be updated with the fresh data. Requires authentication.

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Values are updated in the routes database

    NOTE: User needs to be authenticated for performing the route_create operation

    """
    firebase_config = {
        "apiKey": master_credentials.ROUTE_API_KEY,
        "authDomain": master_credentials.ROUTE_AUTH_DOMAIN,
        "projectId": master_credentials.ROUTE_PROJECT_ID,
        "storageBucket": master_credentials.ROUTE_STORAGE_BUCKET,
        "messagingSenderId": master_credentials.ROUTE_MESSAGING_SENDER_ID,
        "appId": master_credentials.ROUTE_APP_ID,
        "measurementId": master_credentials.ROUTE_MEASUREMENT_ID,
        "databaseURL": master_credentials.ROUTE_DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    _db = firebase.database()

    # Write data to the specified child node in FireBase real-time database
    data = {
        "stops": master_terminal.bus_stops,
        "distance": master_terminal.route_distance,
        "fuel required": master_terminal.route_required_fuel,
        "travel duration": master_terminal.route_duration,
        "route start date": master_terminal.route_start_date,
        "lifetime passenger count": 0,
    }

    _db.child(master_terminal.route_id).set(data)


def master_bus_create():
    """
    Function to create a new child node in the buses firebase real-time database.

    To create a new bus in the database, start with entering the bus id followed by
    each parameter of the bus database as prompted. If the bus id is already in use,
    the existing values will be updated with the new value. Requires authentication.

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Values are updated in the buses database

    NOTE: User needs to be authenticated for performing the bus_create operation
    """
    firebase_config = {
        "apiKey": master_credentials.BUS_API_KEY,
        "authDomain": master_credentials.BUS_AUTH_DOMAIN,
        "projectId": master_credentials.BUS_PROJECT_ID,
        "storageBucket": master_credentials.BUS_STORAGE_BUCKET,
        "messagingSenderId": master_credentials.BUS_MESSAGING_SENDER_ID,
        "appId": master_credentials.BUS_APP_ID,
        "measurementId": master_credentials.BUS_MEASUREMENT_ID,
        "databaseURL": master_credentials.BUS_DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    _db = firebase.database()

    # Write data to the specified child node in FireBase real-time database
    data = {
        "total seats": master_terminal.bus_seats,
        "type": master_terminal.bus_type,
        "manufacturer": master_terminal.bus_manufacturer,
        "year of manufacture": master_terminal.bus_manufacture_year,
        "year of purchase": master_terminal.bus_purchase_year,
        "fuel type": master_terminal.bus_fuel,
        "fuel capacity": master_terminal.bus_fuel_capacity,
        "trip count": 0,
        "maintenance day": master_terminal.bus_maintenance_date,
    }

    _db.child(master_terminal.bus_id).set(data)


def master_route_update():
    """
    Function to update a route node in the routes firebase real-time database.

    To update the route in the database, start with entering the route id followed
    by each parameter of the database, as prompted. Support for selective updation
    is not available. Operators needs to be authenticated for performing updations.

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Values are updated in the routes database

    NOTE: User needs to be authenticated for performing the route_update operation
    """
    firebase_config = {
        "apiKey": master_credentials.ROUTE_API_KEY,
        "authDomain": master_credentials.ROUTE_AUTH_DOMAIN,
        "projectId": master_credentials.ROUTE_PROJECT_ID,
        "storageBucket": master_credentials.ROUTE_STORAGE_BUCKET,
        "messagingSenderId": master_credentials.ROUTE_MESSAGING_SENDER_ID,
        "appId": master_credentials.ROUTE_APP_ID,
        "measurementId": master_credentials.ROUTE_MEASUREMENT_ID,
        "databaseURL": master_credentials.ROUTE_DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    _db = firebase.database()

    # Write data to the specified child node in FireBase real-time database
    data = {
        "stops": master_terminal.bus_stops,
        "distance": master_terminal.route_distance,
        "fuel required": master_terminal.route_required_fuel,
        "travel duration": master_terminal.route_duration,
        "route start date": master_terminal.route_start_date,
        "lifetime passenger count": 0,
    }

    _db.child(master_terminal.route_id).update(data)


def master_bus_update():
    """
    Function to update a bus node in the buses firebase real-time database.

    To update the records in the database, start with entering the bus id followed
    by each parameter of the database, as prompted. Support for selective updation
    is not available. Operators needs to be authenticated for performing updations.

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Values are updated in the buses database

    NOTE: User needs to be authenticated for performing the bus_update operation
    """
    firebase_config = {
        "apiKey": master_credentials.BUS_API_KEY,
        "authDomain": master_credentials.BUS_AUTH_DOMAIN,
        "projectId": master_credentials.BUS_PROJECT_ID,
        "storageBucket": master_credentials.BUS_STORAGE_BUCKET,
        "messagingSenderId": master_credentials.BUS_MESSAGING_SENDER_ID,
        "appId": master_credentials.BUS_APP_ID,
        "measurementId": master_credentials.BUS_MEASUREMENT_ID,
        "databaseURL": master_credentials.BUS_DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    _db = firebase.database()

    # Write data to the specified child node in FireBase real-time database
    data = {
        "total seats": master_terminal.bus_seats,
        "type": master_terminal.bus_type,
        "manufacturer": master_terminal.bus_manufacturer,
        "year of manufacture": master_terminal.bus_manufacture_year,
        "year of purchase": master_terminal.bus_purchase_year,
        "fuel type": master_terminal.bus_fuel,
        "fuel capacity": master_terminal.bus_fuel_capacity,
        "trip count": 0,
        "maintenance day": master_terminal.bus_maintenance_date,
    }

    _db.child(master_terminal.bus_id).update(data)


def master_route_delete():
    """
    Function to delete a route node from the routes firebase real-time database.

    To delete a route from the database, start with entering the route id followed
    by confirming it. Operators needs to be authenticated for performing deletions.
    WARNING: The action is permanent i.e once deleted the records are lost forever.

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Route records are deleted from the routes database

    NOTE: User needs to be authenticated for performing the route_delete operation
    """
    firebase_config = {
        "apiKey": master_credentials.ROUTE_API_KEY,
        "authDomain": master_credentials.ROUTE_AUTH_DOMAIN,
        "projectId": master_credentials.ROUTE_PROJECT_ID,
        "storageBucket": master_credentials.ROUTE_STORAGE_BUCKET,
        "messagingSenderId": master_credentials.ROUTE_MESSAGING_SENDER_ID,
        "appId": master_credentials.ROUTE_APP_ID,
        "measurementId": master_credentials.ROUTE_MEASUREMENT_ID,
        "databaseURL": master_credentials.ROUTE_DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    _db = firebase.database()

    _db.child(master_terminal.route_id).remove()


def master_bus_delete():
    """
    Function to delete a bus node from the buses firebase real-time database.

    To delete a bus from the RT database start with entering the bus's id followed
    by confirming it. Operators needs to be authenticated for performing deletions.
    WARNING: The action is permanent i.e once deleted the records are lost forever.

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Route records are deleted from the buses database

    NOTE: User needs to be authenticated for performing the bus_delete operation
    """
    firebase_config = {
        "apiKey": master_credentials.BUS_API_KEY,
        "authDomain": master_credentials.BUS_AUTH_DOMAIN,
        "projectId": master_credentials.BUS_PROJECT_ID,
        "storageBucket": master_credentials.BUS_STORAGE_BUCKET,
        "messagingSenderId": master_credentials.BUS_MESSAGING_SENDER_ID,
        "appId": master_credentials.BUS_APP_ID,
        "measurementId": master_credentials.BUS_MEASUREMENT_ID,
        "databaseURL": master_credentials.BUS_DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    _db = firebase.database()

    _db.child(master_terminal.bus_id).remove()

def bus_fare_updation():
    """
    Function to delete a bus node from the buses firebase real-time database.

    To update fares for a given bus, start with entering the bus type, followed by
    confirming it. The operator needs to be authenticated for performing updations.
    WARNING: Both fixed and variable part must be updated while updating the fares.

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Bus fares are updated in the firebase database

    NOTE: User needs to be authenticated for performing the bus fare updation
    """
    firebase_config = {
        "apiKey": master_credentials.ROUTE_API_KEY,
        "authDomain": master_credentials.ROUTE_AUTH_DOMAIN,
        "projectId": master_credentials.ROUTE_PROJECT_ID,
        "storageBucket": master_credentials.ROUTE_STORAGE_BUCKET,
        "messagingSenderId": master_credentials.ROUTE_MESSAGING_SENDER_ID,
        "appId": master_credentials.ROUTE_APP_ID,
        "measurementId": master_credentials.ROUTE_MEASUREMENT_ID,
        "databaseURL": master_credentials.ROUTE_DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    _db = firebase.database()

    print("\nEnter the type of bus: ")
    bus_type = str(input())

    print("\nEnter fixed fare: ")
    fixed_fare = int(input())
    print("\nEnter variable fare: ")
    variable_fare = int(input())

    # Write data to the specified child node in FireBase real-time database
    data = {
        "FIXED_TICKET_PRICE": fixed_fare,
        "VARIABLE_TICKET_PRICE": variable_fare,
    }

    _db.child("BUS_FARES").child(bus_type).set(data)
