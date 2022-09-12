import pyrebase
import terminal
import credentials


def createFirebaseRTDatabase():
    firebaseConfig = {
        "apiKey": credentials.API_KEY,
        "authDomain": credentials.AUTH_DOMAIN,
        "projectId": credentials.PROJECT_ID,
        "storageBucket": credentials.STORAGE_BUCKET,
        "messagingSenderId": credentials.MESSAGING_SENDER_ID,
        "appId": credentials.APP_ID,
        "measurementId": credentials.MEASUREMENT_ID,
        "databaseURL": credentials.DATABASE_URL}

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    data = {"currentLocation": terminal.selectedRoute[terminal.currentLocation-1], "passengersInBus": terminal.currentPassengerCount, "availableSeat": terminal.availableSeatCount}
    db.child(terminal.busId).set(data)


def updateFirebaseRTDatabase():
    firebaseConfig = {
        "apiKey": credentials.API_KEY,
        "authDomain": credentials.AUTH_DOMAIN,
        "projectId": credentials.PROJECT_ID,
        "storageBucket": credentials.STORAGE_BUCKET,
        "messagingSenderId": credentials.MESSAGING_SENDER_ID,
        "appId": credentials.APP_ID,
        "measurementId": credentials.MEASUREMENT_ID,
        "databaseURL": credentials.DATABASE_URL}

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    db.child(terminal.busId).update({"currentLocation": terminal.selectedRoute[terminal.currentLocation-1], "passengersInBus": terminal.currentPassengerCount, "availableSeat": terminal.availableSeatCount})
