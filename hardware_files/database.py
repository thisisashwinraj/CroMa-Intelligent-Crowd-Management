# Author: Ashwin Raj <thisisashwinraj@gmail.com>
# License: Creative Commons Attribution - NonCommercial - NoDerivs License

import pyrebase
import terminal
import credentials


def createFirebaseRTDatabase():
    """
    Function to create a new child in the FireBase real-time database.
    The Bus Id is used as the database node's key value (child name).
    Initially default values are reflected as initial value by the node.

    .. versionadded:: 1.0.1

    Parameters:
        None

    Returns:
        None
        Creates a new node in the FireBase database

    Important:
        If a node with same name exists, the values of the node are reset.

    """
    # The python application's firebase real-time database's configuration
    firebaseConfig = {
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
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    # Write data to the specified child node in FireBase real-time database
    data = {
        "currentLocation":
        terminal.selectedRoute[terminal.currentLocation - 1],
        "passengersInBus": terminal.currentPassengerCount,
        "availableSeat": terminal.availableSeatCount,
    }
    db.child(terminal.busId).set(data)


def updateFirebaseRTDatabase():
    """
    Function to update values of a child node in the FireBase database.
    The Bus Id is used as the database node's key value (child name).

    .. versionadded:: 1.0.1

    Parameters:
        None

    Returns:
        None
        Updates values of the child node in the FireBase database

    """
    # The python application's firebase real-time database's configuration
    firebaseConfig = {
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
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    # Write data to the specified child node in FireBase real-time database
    db.child(terminal.busId).update({
        "currentLocation":
        terminal.selectedRoute[terminal.currentLocation - 1],
        "passengersInBus":
        terminal.currentPassengerCount,
        "availableSeat":
        terminal.availableSeatCount,
    })
