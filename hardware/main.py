
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
This module contains the top-level environment of the hardware ticketing-machine.
It contains functions for printing tickets, managing passenger data and includes
several options for performing conductor book-keeping & data-tracking operations.

Included Functions:
    [1] update_passenger_count
    [2] passengers_in_bus
    [3] select_bus
    [4] print_ticket
    [5] calculate_ticket_price
    [6] trip_details

.. versionadded:: 1.0.1
.. versionupdated:: 1.1.0

Read more about the working of the hardware in the :ref:`CroMa Hardware Design`
"""

import terminal
import database
import bus_fares
import mathematica


terminal.collection = 0
terminal.crowd_manager = []
terminal.current_passenger_count = 0
terminal.selected_route = 0
terminal.total_tickets_printed = 0


def update_passenger_count():
    """
    Function to update the real-time passenger count in the bus.

    Passenger count at any instance is the sum of all elements in the crowd manager.
    Available seats are calculated by subtracting passengers count from total seats.
    At no instance can the sum of the entire crowd manager be a value, other than 0.

    .. versionadded:: 1.0.1

    Parameters:
        None

    Returns:
        None
        Values are updated in-place

    """
    terminal.current_passenger_count = sum(
        terminal.crowd_manager[: terminal.current_location]
    )

    # Calculate available seat by subtracting passenger count from total seats
    terminal.available_seat_count = (
        terminal.total_seats - terminal.current_passenger_count
    )


def passengers_in_bus():
    """
    Function to print the total current passenger count in the bus.

    Calculates the passengers count using update_passenger_count().
    After calculating the bus fare, displays this value to the user.

    .. versionadded:: 1.0.1

    Parameters:
        None

    Returns:
        None
        Prints a string with current passenger count

    .. See Also:
        update_passenger_count()

    """
    update_passenger_count()  # Update the database to reflect real-time values

    print("Total Passengers in Bus: " + str(terminal.current_passenger_count))


def select_bus():
    """
    Function to initialize the in-hand ticketing machine and configure trip

    Reads the route id and the bus id, to configure the trip details in the
    handheld-ticketing machine. In case no match is found for either of the
    two parameters in the database, a new input is requested unless manualy
    stopped. Once configure with valid inputs, crowd manager is initialized

    Read more in the :ref:`User Installation and Working`.

    .. versionadded:: 1.0.1
    .. versionupdated:: 1.1.0

    Parameters:
        None

    Warnings:
        route_id shall be available in the database
        bus_id shall be available in the database

    Returns:
        None
        Values are update in-place.
        Prints basic trip details.

    .. See Also:
        select_bus()
        passengers_in_bus()

    """
    # route_id_error is flagged True, if the input route_id is not available
    # If True, then loop will run again to request a new route_id from user

    bus_id_error = True
    route_id_error = True

    while route_id_error is True:
        route_id_error = False

        print("Enter the route id:")
        terminal.route_id = str(input())

        # Fetch the stops list from the database corresponding to route_id
        terminal.selected_route = database.fetch_route(terminal.route_id)

        # Raise a warning message if the entered route_id is not available
        if terminal.selected_route is None:
            route_id_error = True
            print(
                "Uh-Oh! Could not find the route " + terminal.route_id + ". Try Again!"
            )

        # If found display the list of all bus stops in the selected_route
        else:
            print("Selected route: ")
            print(terminal.selected_route)

    # bus_id_error is flagged as 'True' if the input bus_id is not available
    # If True, the loop will run again to request a fresh bus_id from user

    while bus_id_error is True:
        bus_id_error = False

        print("Enter the bus id:")
        terminal.bus_id = str(input())

        # Fetch the bus_type & total_seats corresponding to the input bus_id
        terminal.bus_type = database.fetch_bus_type(terminal.bus_id)
        terminal.total_seats = database.fetch_total_seats(terminal.bus_id)

        # Raise warning message if the input bus_id is not available in DB
        if (terminal.bus_type is None) or (terminal.total_seats is None):
            bus_id_error = True
            print("Uh-Oh! Could not find the bus " +
                  terminal.bus_id + ". Try Again!")

        # If found display the bus_type & total_seats for the bus with bus_id
        else:
            print(
                "Bus type: "
                + str(terminal.bus_type)
                + "\nTotal seats in bus: "
                + str(terminal.total_seats)
            )

    # Initialize the crowd manager and set values at all position to zero
    for _ in range(len(terminal.selected_route)):
        terminal.crowd_manager.append(0)  # Successive value denotes stops

    passengers_in_bus()  # Display current passenger count as first message


def print_ticket():
    """
    Function to print ticket based on inputs from the user.

    Reads user's origin, destination and co-passenger count to calculate the
    total busfare to be charged. The input values are then checked for their
    validity, and are then fed as arguments to the fare calculation function
    The crowd manager list is then updated, every time new ticket is printed

    Read more in the :ref:`User Installation and Working`.

    .. versionadded:: 1.0.1
    .. versionupdated:: 1.1.0

    Parameters:
        None

    Returns:
        None
        Prints the ticket price

    Warning:
        User's destination cannot be before or same as the strating point
        Number of passengers cannot be zero or a negative number

    .. See Also:
        calculate_ticket_price()
        update_passenger_count()

    """
    # valid_input is flagged False, if the starting point is not available
    # If False, then loop will run again to request a fresh starting point

    valid_user_starting_point = False

    while valid_user_starting_point is False:
        valid_user_starting_point = True

        print("\nEnter the Starting Point: ")
        user_starting_point = int(input())

        # Check if the input value for the user's starting point is legal
        if (user_starting_point <= 0) or (
            user_starting_point > len(terminal.selected_route)
        ):
            print("\nEnter a Valid Input")

            # Request a new input if input user_starting_point isn't valid
            valid_user_starting_point = False

    # valid_input is flagged False if destination's value is not available
    # If False, loop will run again to request fresh input for destination

    valid_user_destination = False

    while valid_user_destination is False:
        valid_user_destination = True

        print("\nEnter the Destination: ")
        user_destination = int(input())

        # Check if the input value for the user_destination is legal value
        if (user_destination <= 0) or (user_destination > len(terminal.selected_route)):
            print("\nEnter a Valid Input")

            # If the user_destination isn't valid, request for a new input
            valid_user_destination = False

    # valid_input is flagged False if wrong number_of_passengers is entered
    # If False, the loop will run again to request new number_of_passengers

    valid_number_of_passengers = False

    while valid_number_of_passengers is False:
        valid_number_of_passengers = True

        print("\nEnter the no. of co-passengers: ")
        number_of_passengers = int(input())

        # Check if the input value for the number of passengers is legal
        if number_of_passengers < 1:
            print("Number of passengers can not be less than 1")
            valid_number_of_passengers = False

    calculated_fare = calculate_ticket_price(
        user_starting_point, user_destination, number_of_passengers
    )

    print("\nTotal ticket price: " + str(calculated_fare))

    # Increment crowd_manager to include passenger who onboard at the stop
    terminal.crowd_manager[user_starting_point - 1] += number_of_passengers

    # Decrement crowd_manager to remove passengers who deboard at the stop
    terminal.crowd_manager[user_destination - 1] -= number_of_passengers

    terminal.total_tickets_printed = (
        terminal.total_tickets_printed + number_of_passengers
    )

    # Update the value of crowd manager each time new tickets are printed
    update_passenger_count()


def calculate_ticket_price(user_starting_point, user_destination, number_of_passengers):
    """
    Function to print ticket based on inputs from the user.

    Uses user's origin, destination, and co-passengers count to calculate the
    total bus fare to be charged. The fare is calculated by adding a variable
    charge to the mandatory fixed charge. The program is designed to increase
    the variable charges every time after crossing three succesive bus stops.

    Read more in the :ref:`User Installation and Working`.

    .. versionadded:: 1.0.1

    Parameters:
        user_starting_point (int): The onboarding point of the user
        user_destination (int): The destination point of the user
        number_of_passengers (int): Total number of co-passengers

    Returns:
        total_ticket_price (int): Total bus fare

    .. See Also:
        calculate_ticket_price()
        update_passenger_count()

    NOTE: Additional charges (eg: Luggages), may be added as per requirements

    """
    # dynamic_cost_multiplier shows no. of stops after which costs increases
    dynamic_cost_multiplier = 3  # the cost is set to increase after 3 stops

    # routeway_stop_count gives no. of stops between origin, and destination
    routeway_stop_count = abs(user_destination - user_starting_point)

    # divide routeway_stop_count / dynamic_cost_multiplier to get cost epoch
    variable_ticket_price_epochs = int(
        routeway_stop_count / dynamic_cost_multiplier)

    # Total fare is calculated by adding variable price to the fixed price
    # Variable price increases by an amt after every given number of stops
    # NOTE: To change pricing, navigate to bus_fares and update the values

    total_ticket_price = (
        bus_fares.FIXED_TICKET_PRICE
        + (variable_ticket_price_epochs * bus_fares.VARIABLE_TICKET_PRICE)
    ) * number_of_passengers

    # update the total collections by adding the value of the ticket price
    terminal.collection = terminal.collection + total_ticket_price

    return int(total_ticket_price)


def trip_details():
    """
    Function to display the bus details, route details and trip configurations.

    Displays route info, tickets printed, available seats, and passenger count.
    These details are updated in real-time, before being displayed to the user.

    Note: In the upcoming versions this will include useful buskeeping records.

    .. versionadded:: 1.0.1

    Parameters:
        None

    Returns:
        None
        Prints all trip details

    .. See Also:
        passengers_in_bus()

    """
    print(
        "\nTRIP DETAILS\nSelected Route: "
        + terminal.selected_route[-1]
        + " "
        + terminal.bus_type
        + "(Bus Id: "
        + terminal.bus_id
        + ")"
    )

    # Display the current_location and the total number of tickets printed
    print("Current Location: " +
          terminal.selected_route[terminal.current_location - 1])
    print("Total Tickets Printed: " + str(terminal.total_tickets_printed))

    # Update passenger count, and print total number of passengers onboard
    passengers_in_bus()

    print("Seats available in Bus: " + str(terminal.available_seat_count))


if __name__ == "__main__":
#    This is the top-level environment of the program.
#    It is the entry point of the program, and contains the boot code.
#
#    .. versionadded:: 1.0.1
#    .. versionupdated:: 1.1.0
#
#    See Also:
#        .. [1]  database.py :: connects to the FireBase real-time database
#        .. [2]  terminal.py :: defines variables used throughout the program
#
#    Example:
#        >>> Enter E-Mail:
#        testCroMa@gmail.com
#
#        >>> Enter Password:
#        **********
#
#        Welcome to CroMa: The Crowd Management Software
#
#        >>> Enter the route id:
#        TVM_KYM_01
#
#        >>> Enter the bus id:
#        KL13N
#
#        >>> MENU: Select an option
#            1. Print Ticket
#            2. Display Trip Details
#            3. Display Collections
#            4. Update Location
#            5. Exit
#        1
#
#        >>> Enter the Starting Point:
#        1
#
#        >>> Enter the Destination:
#        5
#
#        >>> Enter the no. of co-passengers:
#        2
#
#        Total ticket price: 32

    database.log_in()  # Authenticate users to allow read, write operation

    terminal.current_location = 1 # Set the starting loc to first bus stop

    print("\nWelcome to CroMa: The Crowd Management Software\n")

    # Enter the bus_id & route_id to configure the route, and the bus info
    select_bus()

    # Create a Real-Time DataBase node in FireBase, with Bus Id as the key
    database.initialize_real_time_crowd_database()

    SELECTED_MENU_OPTION = 0

    # Display the MENU with options to print ticket, and perform other ops
    while SELECTED_MENU_OPTION != 565496723:

        # Update the FireBase real-time databases to reflect fresh changes
        database.update_real_time_crowd_database()

        print(
            "\nMENU: Select an option\n\
            1. Print Ticket\n\
            2. Display Trip Details\n\
            3. Display Collections\n\
            4. Update Location\n\
            5. Exit"
        )

        SELECTED_MENU_OPTION = int(input())  # Perform the task asis input

        # Print new ticket for the passenger whenever someone onboards bus
        if SELECTED_MENU_OPTION == 1:
            print_ticket()

        # Show trip details including route info, available seat count etc
        if SELECTED_MENU_OPTION == 2:
            trip_details()

        # Display total collection through ticket sale since start of trip
        if SELECTED_MENU_OPTION == 3:
            print("\nTotal Collections for this trip: " + str(terminal.collection))

        # Change the current location of the bus to the new input location
        if SELECTED_MENU_OPTION == 4:
            print(
                "\nAt present, the current location is "
                + terminal.selected_route[terminal.current_location - 1]
                + " (Code = "
                + str(terminal.current_location)
                + ")"
            )

            # Note: The current and new location are read as integer values
            print("\nEnter your new location: ")
            terminal.current_location = int(input())  # Input location code

            print(
                "\nThe current location has been updated to "
                + terminal.selected_route[terminal.current_location - 1]
            )

            # Update crowd manager value every time new tickets are printed
            update_passenger_count()

        if SELECTED_MENU_OPTION == 5:
            print("\nDo you want to exit [Y/N]: ")
            END_TRIP = str(input())

            # Confirm if user want to exit the program and terminate system
            if END_TRIP in ('Y', 'y'):
                database.exit_database_updation()

                print("\nThank you for using CroMa.\n")
                break
