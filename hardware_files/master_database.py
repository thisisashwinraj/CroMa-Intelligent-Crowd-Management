import pyrebase
import master_credentials
import master_terminal


def master_route_create():
    firebaseConfig = {
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
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    # Write data to the specified child node in FireBase real-time database
    data = {
        "stops": master_terminal.bus_stops,
        "distance": master_terminal.route_distance,
        "fuel required": master_terminal.route_required_fuel,
        "travel duration": master_terminal.route_duration,
        "route start date": master_terminal.route_start_date,
        "lifetime passenger count": 0,
    }

    db.child(master_terminal.route_id).set(data)


def master_bus_create():
    firebaseConfig = {
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
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

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

    db.child(master_terminal.bus_id).set(data)


def master_route_update():
    firebaseConfig = {
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
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    # Write data to the specified child node in FireBase real-time database
    data = {
        "stops": master_terminal.bus_stops,
        "distance": master_terminal.route_distance,
        "fuel required": master_terminal.route_required_fuel,
        "travel duration": master_terminal.route_duration,
        "route start date": master_terminal.route_start_date,
        "lifetime passenger count": 0,
    }

    db.child(master_terminal.route_id).update(data)


def master_bus_update():
    firebaseConfig = {
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
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

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

    db.child(master_terminal.bus_id).update(data)


def master_route_delete():
    firebaseConfig = {
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
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    db.child(master_terminal.route_id).remove()


def master_bus_delete():
    firebaseConfig = {
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
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    db.child(master_terminal.bus_id).remove()
