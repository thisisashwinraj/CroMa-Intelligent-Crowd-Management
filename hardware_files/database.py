import pyrebase
import defaults
import credentials

def createFirebaseRTDatabase():
  firebaseConfig = {"apiKey": credentials.API_KEY,
    "authDomain": credentials.AUTH_DOMAIN,
    "projectId": credentials.PROJECT_ID,
    "storageBucket": credentials.STORAGE_BUCKET,
    "messagingSenderId": credentials.MESSAGING_SENDER_ID,
   "appId": credentials.APP_ID,
    "measurementId": credentials.MEASUREMENT_ID,
    "databaseURL": credentials.DATABASE_URL}


  firebase = pyrebase.initialize_app(firebaseConfig)
  db = firebase.database()

  data = {"currentLocation": defaults.selectedRoute[defaults.currentLocation-1], "passengersInBus" : defaults.currentPassengerCount, "availableSeat" : defaults.availableSeatCount}

  db.child(defaults.busId).set(data)


def updateFirebaseRTDatabase_KL13N():
  firebaseConfig = {"apiKey": credentials.API_KEY,
    "authDomain": credentials.AUTH_DOMAIN,
    "projectId": credentials.PROJECT_ID,
    "storageBucket": credentials.STORAGE_BUCKET,
    "messagingSenderId": credentials.MESSAGING_SENDER_ID,
   "appId": credentials.APP_ID,
    "measurementId": credentials.MEASUREMENT_ID,
    "databaseURL": credentials.DATABASE_URL}


  firebase = pyrebase.initialize_app(firebaseConfig)
  db = firebase.database()

  db.child(defaults.busId).update({"currentLocation": defaults.selectedRoute[defaults.currentLocation-1], "passengersInBus" : defaults.currentPassengerCount, "availableSeat" : defaults.availableSeatCount})
