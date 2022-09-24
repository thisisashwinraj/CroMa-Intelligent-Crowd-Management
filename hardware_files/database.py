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

import pyrebase
import terminal
import credentials


def log_in():
    """
    Function to authenticate users for performing CRUD operations on firebase.

    Allows user authentication by means of a pre-registered email and password.
    Only authenticated users are allowed to perform data read/write operations.
    The system will exit the execution in case a wrong email/password is input.

    Read more about authentication in CroMa in :ref:`CroMa User Authentication`

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Authenticates the user by email-password combination

    Raises:
        INVALID_EMAIL: raised if the e-mail id does not exist
        INVALID_PASSWORD: raised if the input password is wrong

    """
    # The python application's firebase real-time database's configuration
    firebase_config = {
        "apiKey": credentials.API_KEY,
        "authDomain": credentials.AUTH_DOMAIN,
        "projectId": credentials.PROJECT_ID,
        "storageBucket": credentials.STORAGE_BUCKET,
        "messagingSenderId": credentials.MESSAGING_SENDER_ID,
        "appId": credentials.APP_ID,
        "measurementId": credentials.MEASUREMENT_ID,
        "databaseURL": credentials.DATABASE_URL,
    }

    # Initialize connection with FireBase database, set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()

    try:
        terminal.input_email = str(input("Enter E-Mail: "))
        terminal.input_password = str(input("\nEnter Password: "))

        # Authenticate the user to perform CRUD operations on the database
        user = auth.sign_in_with_email_and_password(
            terminal.input_email, terminal.input_password
        )
        # RefreshToken to avoid stale tokens, idToken expires after 1 hour
        user = auth.refresh(user["refreshToken"])

    except:
        print("\nYour E-Mail Id or Password is wrong. Try Again!\n")
        raise SystemExit(0)


def initialize_real_time_crowd_database():
    """
    Function to initialize a new child node in the FireBase real-time database.

    The Bus Id is used as the database node's key value (child name), to create
    a new node that will reflect the crowd levels, and other useful information
    pertaining to that bus in real time. Default values are initially reflected.

    Read more about CroMa's real-time crowd management in :ref:`Under the Hood`

    .. versionadded:: 1.0.1
    .. versionupdated:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Creates a new node in the FireBase database

    Important:
        If a node with same name exists, the values of the node are reset.

    NOTE: User needs to be authenticated for performing the initialize operation

    """
    # The python application's firebase real-time database's configuration
    firebase_config = {
        "apiKey": credentials.API_KEY,
        "authDomain": credentials.AUTH_DOMAIN,
        "projectId": credentials.PROJECT_ID,
        "storageBucket": credentials.STORAGE_BUCKET,
        "messagingSenderId": credentials.MESSAGING_SENDER_ID,
        "appId": credentials.APP_ID,
        "measurementId": credentials.MEASUREMENT_ID,
        "databaseURL": credentials.DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()

    # Write data to the specified child node in FireBase real-time database
    data = {
        "current_location": terminal.selected_route[terminal.current_location - 1],
        "passengersInBus": terminal.current_passenger_count,
        "availableSeat": terminal.available_seat_count,
    }

    auth = firebase.auth()

    # Authenticate the user to perform CRUD operations on the database
    user = auth.sign_in_with_email_and_password(
        terminal.input_email, terminal.input_password
    )
    # RefreshToken to avoid stale tokens, idToken expires after 1 hour
    user = auth.refresh(user["refreshToken"])

    db.child(terminal.bus_id).set(data, user["idToken"])


def update_real_time_crowd_database():
    """
    Function to update the values of a child node in the FireBase RT database.

    The Bus Id is used as the database node's key value (child name), to update
    an existing node to reflect the crowd levels, and other useful informations
    pertaining to that bus in real-time. Only changed values, are to be updated.

    Read more about CroMa's real-time crowd management in :ref:`Under the Hood`

    .. versionadded:: 1.0.1
    .. versionupdated:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Updates values of the child node in the FireBase database

    NOTE: User needs to be authenticated for performing the initialize operation

    """
    # The python application's firebase real-time database's configuration
    firebase_config = {
        "apiKey": credentials.API_KEY,
        "authDomain": credentials.AUTH_DOMAIN,
        "projectId": credentials.PROJECT_ID,
        "storageBucket": credentials.STORAGE_BUCKET,
        "messagingSenderId": credentials.MESSAGING_SENDER_ID,
        "appId": credentials.APP_ID,
        "measurementId": credentials.MEASUREMENT_ID,
        "databaseURL": credentials.DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)

    auth = firebase.auth()
    db = firebase.database()

    # Authenticate the user to perform CRUD operations on the database
    user = auth.sign_in_with_email_and_password(
        terminal.input_email, terminal.input_password
    )
    # RefreshToken to avoid stale tokens, idToken expires after 1 hour
    user = auth.refresh(user["refreshToken"])

    # Write data to the specified child node in FireBase real-time database
    db.child(terminal.bus_id).update(
        {
            "current_location": terminal.selected_route[terminal.current_location - 1],
            "passengersInBus": terminal.current_passenger_count,
            "availableSeat": terminal.available_seat_count,
        },
        user["idToken"],
    )


def fetch_route(route_id):
    """
    The function to fetch the route data for the trips from FireBase database.

    The route_id is used as the database node's key value (child name) to fetch
    the details (list of bus stops) pertaining to the route pointed by route_id.
    If the route_id is not available, the user is prompted to enter a new input.

    Read more about how the routes database functions in :ref:`Hardware Database`

    .. versionadded:: 1.1.0

    Parameters:
        [str] route_id

    Returns:
        [list] selected_route

    """
    # The python application's firebase real-time database's configuration
    firebase_config = {
        "apiKey": credentials.ROUTE_API_KEY,
        "authDomain": credentials.ROUTE_AUTH_DOMAIN,
        "projectId": credentials.ROUTE_PROJECT_ID,
        "storageBucket": credentials.ROUTE_STORAGE_BUCKET,
        "messagingSenderId": credentials.ROUTE_MESSAGING_SENDER_ID,
        "appId": credentials.ROUTE_APP_ID,
        "measurementId": credentials.ROUTE_MEASUREMENT_ID,
        "databaseURL": credentials.ROUTE_DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()

    # Fetches the list of bus stops from the route pointed by input route_id
    route = db.child(route_id).child("stops").get()
    return route.val()


def fetch_bus_type(bus_id):
    """
    The function to fetch the bus data for a given bus_id from FireBase database

    The bus_id's are used as the database node's key value(child name) to fetch
    the details (the bus type) pertaining to a given bus, pointed by the bus_id.
    If this bus_id is not available, the user is prompted to enter a new bus_id.

    Read more about how the routes database functions in :ref:`Hardware Database`

    .. versionadded:: 1.1.0

    Parameters:
        [str] bus_id

    Returns:
        [str] bus_type

    """
    # The python application's firebase real-time database's configuration
    firebase_config = {
        "apiKey": credentials.BUS_API_KEY,
        "authDomain": credentials.BUS_AUTH_DOMAIN,
        "projectId": credentials.BUS_PROJECT_ID,
        "storageBucket": credentials.BUS_STORAGE_BUCKET,
        "messagingSenderId": credentials.BUS_MESSAGING_SENDER_ID,
        "appId": credentials.BUS_APP_ID,
        "measurementId": credentials.BUS_MEASUREMENT_ID,
        "databaseURL": credentials.BUS_DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()

    # Fetch the bus_type for that bus, with the bus_id specified by the input
    bus_type = db.child(bus_id).child("type").get()
    return bus_type.val()


def fetch_total_seats(bus_id):
    """
    The function to fetch total number of seats in the bus pointed by the bus_id

    The bus_id's are used as the database node's key value(child name) to fetch
    the details (the bus type) pertaining to a given bus, pointed by the bus_id.
    If this bus_id is not available, the user is prompted to enter a new bus_id.

    Read more about how the routes database functions in :ref:`Hardware Database`

    .. versionadded:: 1.1.0

    Parameters:
        [str] bus_id

    Returns:
        [int] total_seats

    """
    # The python application's firebase real-time database's configuration
    firebase_config = {
        "apiKey": credentials.BUS_API_KEY,
        "authDomain": credentials.BUS_AUTH_DOMAIN,
        "projectId": credentials.BUS_PROJECT_ID,
        "storageBucket": credentials.BUS_STORAGE_BUCKET,
        "messagingSenderId": credentials.BUS_MESSAGING_SENDER_ID,
        "appId": credentials.BUS_APP_ID,
        "measurementId": credentials.BUS_MEASUREMENT_ID,
        "databaseURL": credentials.BUS_DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()

    # Fetch the totalSeat for the bus with the bus_id specified by the input
    total_seats = db.child(bus_id).child("total seats").get()
    return total_seats.val()


def exit_database_updation():
    """
    The function to update the trip details in the bus database & route database

    The bus_id & route_id are used as the database node's key value(child name)
    to store the details, pertaining to certain aspects of the current bus trip
    If this bus_id is not available, the user is prompted to enter a new bus_id.

    Read more about how the routes database functions in :ref:`Hardware Database`

    .. versionadded:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Updates the routeDB and BusDB with trip details

    NOTE: This feature is still in development & will be revised in later updates

    """
    # The python application's firebase real-time database's configuration
    firebase_config = {
        "apiKey": credentials.ROUTE_API_KEY,
        "authDomain": credentials.ROUTE_AUTH_DOMAIN,
        "projectId": credentials.ROUTE_PROJECT_ID,
        "storageBucket": credentials.ROUTE_STORAGE_BUCKET,
        "messagingSenderId": credentials.ROUTE_MESSAGING_SENDER_ID,
        "appId": credentials.ROUTE_APP_ID,
        "measurementId": credentials.ROUTE_MEASUREMENT_ID,
        "databaseURL": credentials.ROUTE_DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()

    try:
        # Fetch the current lifetime passenger count for the input route_id
        current_lifetime_passenger_count = (
            db.child(terminal.route_id).child("lifetime passenger count").get()
        )

        # Update lifetime passenger count for the input route_id in routeDB
        lifetime_passenger_count = (
            int(current_lifetime_passenger_count) +
            terminal.total_tickets_printed
        )

        db.child(terminal.route_id).update(
            {
                "lifetime passenger count": lifetime_passenger_count,
            }
        )

    except:
        print("\nUnable to update routes database")
        raise SystemExit(0)

    firebase_config = {
        "apiKey": credentials.BUS_API_KEY,
        "authDomain": credentials.BUS_AUTH_DOMAIN,
        "projectId": credentials.BUS_PROJECT_ID,
        "storageBucket": credentials.BUS_STORAGE_BUCKET,
        "messagingSenderId": credentials.BUS_MESSAGING_SENDER_ID,
        "appId": credentials.BUS_APP_ID,
        "measurementId": credentials.BUS_MEASUREMENT_ID,
        "databaseURL": credentials.BUS_DATABASE_URL,
    }

    # Initialize connection with FireBase database & set reference variable
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()

    try:
        # Fetch the current trip count for the input bus from the bus database
        current_trip_count = db.child(
            terminal.bus_id).child("trip count").get()

        # Update lifetime trip count for the input bus_id, in the bus database
        lifetime_trip_count = int(current_trip_count) + \
            terminal.total_tickets_printed

        db.child(terminal.bus_id).update(
            {
                "trip count": lifetime_trip_count,
            }
        )

    except:
        print("\nUnable to update bus database")
        raise SystemExit(0)
