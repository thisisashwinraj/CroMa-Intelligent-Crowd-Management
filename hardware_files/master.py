import master_database
import master_terminal


def createNewRoute():
    loopEnd = False

    print("\nEnter the route id: ")
    master_terminal.route_id = str(input())

    print(
        "\nEnter the bus stops in correct order:\n(Enter DONE after entering all stops)"
    )
    next_stop = 1
    master_terminal.bus_stops = []

    while loopEnd is False:
        next_stop = input()

        if next_stop != "DONE":
            master_terminal.bus_stops.append(next_stop)
        else:
            loopEnd = True

    print("\nEnter the total distance of this route, in km: ")
    master_terminal.route_distance = int(input())

    print("\nEnter the approximate fuel required for the trip, in litres: ")
    master_terminal.route_required_fuel = int(input())

    print("\nEnter the travel time required, in minutes:")
    master_terminal.route_duration = int(input())

    print("\nEnter todays date (DD\MM\YYYY):")
    master_terminal.route_start_date = str(input())

    master_database.master_route_create()

    print(
        "\nDetails for the route id "
        + master_terminal.route_id
        + " have been recorded\n"
    )


def createNewBus():
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


def updateRoute():
    print("\nEnter the route id to be updated: ")
    loopEnd = False
    master_terminal.route_id = str(input())

    print(
        "\nEnter the bus stops in correct order:\n(Enter DONE after entering all stops)"
    )
    next_stop = 1
    master_terminal.bus_stops = []

    while loopEnd is False:
        next_stop = input()

        if next_stop != "DONE":
            master_terminal.bus_stops.append(next_stop)
        else:
            loopEnd = True

    print("\nEnter the total distance of this route, in km: ")
    master_terminal.route_distance = int(input())

    print("\nEnter the approximate fuel required for the trip, in litres: ")
    master_terminal.route_required_fuel = int(input())

    print("\nEnter the travel time required, in minutes:")
    master_terminal.route_duration = int(input())

    print("\nEnter todays date (DD\MM\YYYY):")
    master_terminal.route_start_date = str(input())

    master_database.master_route_update()

    print(
        "\nDetails for the route id "
        + master_terminal.route_id
        + " have been updated\n"
    )


def updateBus():
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


def deleteRoute():
    print("\nEnter the route id to be deleted: ")
    master_terminal.route_id = str(input())

    master_database.master_route_delete()

    print("\nThe Route " + master_terminal.route_id + " have been deleted\n")


def deleteBus():
    print("\nEnter the bus id to be deleted: ")
    bus_id = str(input())

    master_database.master_bus_delete()

    print("\nThe Bus " + master_terminal.bus_id + " have been deleted\n")


if __name__ == "__main__":
    error = None
    storedUsername = "Admin"
    storedPassword = "xKSRTC4%6"

    print("\nEnter your username:")
    username = str(input())

    if username != storedUsername:
        print("\nUh-Oh Could find this Username! Try again!")
        error = 502  # Bad Gateway
        exit()  # Not working

    print("\nEnter your password:")
    password = str(input())

    if password != storedPassword:
        print("\nUh-Oh Wrong Password! Try again!")
        error = 502  # Bad Gateway
        exit()  # Not working

    if not error:
        selectedMasterOption = 0

        while selectedMasterOption != 7:

            print(
                "MENU: Enter option:\n1. Add New Route\n2. Add New BusID\n3. Update Route\n4. Update BusID\n5. Delete Route\n6. Delete BusID\n7. Exit"
            )
            selectedMasterOption = int(input())

            # add a new route
            if selectedMasterOption == 1:
                createNewRoute()

            # add a new busid
            elif selectedMasterOption == 2:
                createNewBus()

            elif selectedMasterOption == 3:
                updateRoute()

            elif selectedMasterOption == 4:
                updateBus()

            elif selectedMasterOption == 5:
                deleteRoute()

            elif selectedMasterOption == 6:
                deleteBus()

            else:
                print("Enter a valid choice")
