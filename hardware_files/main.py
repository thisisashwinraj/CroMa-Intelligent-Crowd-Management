# Author: Ashwin Raj <thisisashwinraj@gmail.com>
# License: Creative Commons Attribution - Non Commercial - No Derivs License

import busFares
import database
import terminal

terminal.collection = 0
terminal.crowdManager = []
terminal.currentPassengerCount = 0
terminal.selectedRoute = 0
terminal.totalTicketsPrinted = 0


def updatePassengerCount():
    """
    Function to update the passenger count in bus.
    Passenger count at any instance is the sum of all elements in the crowd manager.
    Available seat count is calculated by subtracting passenger count from total seats.

    .. versionadded:: 1.0.1

    Parameters:
        None

    Returns:
        None
        Values are updated in-place

    """
    terminal.currentPassengerCount = sum(
        terminal.crowdManager[: terminal.currentLocation]
    )

    # Calculate available seat by subtracting passenger count from total seats
    terminal.availableSeatCount = terminal.totalSeats - terminal.currentPassengerCount


def passengersInBus():
    """
    Function to print current passenger count in bus.
    Calculate the passenger count using updatePassengerCount().

    .. versionadded:: 1.0.1

    Parameters:
        None

    Returns:
        None
        Prints a string with current passenger count

    .. See Also:
        updatePassengerCount()

    """
    updatePassengerCount()

    print("Total Passengers in Bus: " + str(terminal.currentPassengerCount))


def selectBus():
    """
    Function to initialize the in-hand ticketing machine.
    Reads bus id to configure the trip details in the machine.

    Read more in the :ref:`User Installation and Working`.

    .. versionadded:: 1.0.1

    Parameters:
        None

    Returns:
        None
        Values are update in-place.
        Prints basic trip details.

    .. See Also:
        selectBus()
        passengersInBus()

    """
    # The value is flagged as 'True' if the input busId is not available
    # In such cases it will re-run the function to request another input
    busIdError = False

    print("Enter the bus number:")
    terminal.busId = str(input())

    # Note: This method will be depreceated after setting an SQL database

    # Configurations for Bus Id - KL13N
    if terminal.busId == "KL13N":
        # List of all stops in this route. Update to fetch from Routes DB
        terminal.selectedRoute = [
            "Trivandrum",
            "Venjaramoodu",
            "Killimanoor",
            "Vayom",
            "Ayur",
            "Kottarakara",
            "Adoor",
            "Pandalam",
            "Thiruvalla",
            "Kottayam",
        ]

        # Defines bus type & total capacity. Update to fetch from Buses DB
        terminal.totalSeats = 32
        terminal.busType = "Fast Passenger"

        # Unflag this variable to show succesful configuration of the unit
        busIdError = False

        print(
            "You selected "
            + terminal.selectedRoute[-1]
            + " "
            + terminal.busType
            + "(Bus Id: "
            + terminal.busId
            + ")"
        )

    # Configurations for Bus Id - KL23Q
    elif terminal.busId == "KL24Q":
        # List of all stops in this route. Update to fetch from Routes DB
        terminal.selectedRoute = [
            "Kattakad",
            "Trivandrum",
            "Venjaramoodu",
            "Killimanoor",
            "Vayom",
            "Ayur",
            "Kottarakara",
            "Adoor",
            "Ankamally",
            "Trissur",
        ]

        # Defines bus type & total capacity. Update to fetch from Buses DB
        terminal.totalSeats = 28
        terminal.busType = "Super Fast"

        # Unflag this variable to show succesful configuration of the unit
        busIdError = False

        print(
            "You selected "
            + terminal.selectedRoute[-1]
            + " "
            + terminal.busType
            + "(Bus Id: "
            + terminal.busId
            + ")"
        )

    # Configurations for Bus Id - KL23Q
    elif terminal.busId == "KL94F":
        # List of all stops in this route. Update to fetch from Routes DB
        terminal.selectedRoute = [
            "Eastfort",
            "Palayam",
            "PMG",
            "Ulloor",
            "Sreekaryam",
            "Chavdimukku",
            "Pongamoodu",
            "Kariavattom",
            "Kazhakootam",
            "Technopark",
        ]

        # Defines bus type & total capacity. Update to fetch from Buses DB
        terminal.totalSeats = 28
        terminal.busType = "City Local"

        # Unflag this variable to show succesful configuration of the unit
        busIdError = False

        print(
            "You selected "
            + terminal.selectedRoute[-1]
            + " "
            + terminal.busType
            + "(Bus Id: "
            + terminal.busId
            + ")"
        )

    else:
        # ToDo: Fix error - Displays multiple output lines when wrong input
        # for BusId is entered multiple times by the user. GitHub issue #01

        print("Uh-Oh! Could'nt find this bus. Try again!\n")

        # Flag the var to re-enter the BusId before proceeding to next step
        busIdError = True

        selectBus()

    if busIdError is False:
        # Initialize crowd manager, and set values at all positions to zero
        for i in range(len(terminal.selectedRoute)):
            terminal.crowdManager.append(0)  # Successive vals denotes stops

    passengersInBus()  # Display current passenger count as initial message


def printTicket():
    """
    Function to print ticket based on inputs from the user.
    Reads user's origin, destination and co-passenger count.

    Read more in the :ref:`User Installation and Working`.

    .. versionadded:: 1.0.1

    Parameters:
        None

    Returns:
        None
        Prints the ticket price

    .. See Also:
        calculateTicketPrice()
        updatePassengerCount()

    """
    print("\nEnter the Starting Point: ")
    userStartingPoint = int(input())

    print("\nEnter the Destination: ")
    userDestination = int(input())

    # Note: The starting point, and destination are read as integer numbers
    # This will be replaced with unique stop codes in the upcoming releases

    print("\nEnter the no. of co-passengers: ")
    numberOfPassengers = int(input())

    ticketPrice = calculateTicketPrice(
        userStartingPoint, userDestination, numberOfPassengers
    )

    print("\nTotal ticket price: " + str(ticketPrice))

    # Increment crowdmanager to include passengers who onbarded at the stop
    terminal.crowdManager[userStartingPoint - 1] += numberOfPassengers

    # Decrement crowdmanager to remove passengers who deboarded at the stop
    terminal.crowdManager[userDestination - 1] -= numberOfPassengers

    terminal.totalTicketsPrinted = terminal.totalTicketsPrinted + numberOfPassengers

    # Update the values of crowd manager every time new tickets are printed
    updatePassengerCount()


def calculateTicketPrice(userStartingPoint, userDestination, numberOfPassengers):
    """
    Function to print ticket based on inputs from the user.
    Reads user's origin, destination and co-passenger count.

    Read more in the :ref:`User Installation and Working`.

    .. versionadded:: 1.0.1

    Parameters:
        userStartingPoint, userDestination, numberOfPassengers

    Returns:
        Total ticket price

    .. See Also:
        calculateTicketPrice()
        updatePassengerCount()

    """
    # dynamicCostMultiplier shows no. of stops after which costs increases
    dynamicCostMultiplier = 3  # the cost is set to increase after 3 stops

    # routewayStopCount gives no. of stops between origin, and destination
    routewayStopCount = abs(userDestination - userStartingPoint)

    # divide routewayStopCount by dynamicCostMultiplier to get cost epochs
    variableTicketPriceEpochs = int(routewayStopCount / dynamicCostMultiplier)
    totalTicketPrice = (
        busFares.fixedTicketPrice
        + (variableTicketPriceEpochs * busFares.variableTicketPrice)
    ) * numberOfPassengers

    # update the total collections by adding the value of the ticket price
    terminal.collection = terminal.collection + totalTicketPrice

    return float(totalTicketPrice)


def tripDetails():
    """
    Function to print the trip details configured during boot.
    Displays route info, tickets printed, available seats and passenger count.

    .. versionadded:: 1.0.1

    Parameters:
        None

    Returns:
        None
        Prints all trip details

    .. See Also:
        passengersInBus()

    """
    print(
        "\nTRIP DETAILS\nSelected Route: "
        + terminal.selectedRoute[-1]
        + " "
        + terminal.busType
        + "(Bus Id: "
        + terminal.busId
        + ")"
    )
    print("Current Location: " + terminal.selectedRoute[terminal.currentLocation - 1])
    print("Total Tickets Printed: " + str(terminal.totalTicketsPrinted))

    # Update passenger count, and print total number of passengers onboard
    passengersInBus()

    print("Seats available in Bus: " + str(terminal.availableSeatCount))


if __name__ == "__main__":
    """
    This is the top-level environment of the program.
    It acts as the entry point of the program, and contains the boot code.

    .. versionadded:: 1.0.1

    See Also:
        .. [1]  database.py :: connects to the FireBase real-time database
        .. [2]  terminal.py :: defines variables used throughout the program

    Example:
        >>> Enter the bus number:
        KL13N

        >>> MENU: Select an option
            1. Print Ticket
            2. Display Trip Details
            3. Display Collections
            4. Update Location
            5. Exit
        1

        >>> Enter the Starting Point:
        1

        >>> Enter the Destination:
        5

        >>> Enter the no. of co-passengers:
        2

        Total ticket price: 32.0

    """
    terminal.currentLocation = 1

    print("\nWelcome to CroMa: The CROwd MAnagement software\n")

    # Enter the Bus Id to configure the route, and the related information
    selectBus()

    # Create a Real-Time DataBase node in FireBase, with Bus Id as the key
    database.createFirebaseRTDatabase()

    selectedMENUOption = 0

    # Display the MENU with options to print ticket, and perform other ops
    while selectedMENUOption != 5:

        # Update the FireBase real-time databases to reflect fresh changes
        database.updateFirebaseRTDatabase()

        print(
            "\nMENU: Select an option\n1. Print Ticket\n2. Display Trip Details\n3. Display Collections\n4. Update Location\n5. Exit"
        )
        selectedMENUOption = int(input())

        # Print new ticket for the passenger whenever someone onboards bus
        if selectedMENUOption == 1:
            printTicket()

        # Show trip details including route info, available seat count etc
        if selectedMENUOption == 2:
            tripDetails()

        # Display total collection through ticket sale since start of trip
        if selectedMENUOption == 3:
            print("Total Collections for this trip: " + str(terminal.collection))

        # Change the current location of the bus to the new input location
        if selectedMENUOption == 4:
            print(
                "\nAt present, the current location is set to "
                + terminal.selectedRoute[terminal.currentLocation - 1]
                + " (Code = "
                + str(terminal.currentLocation)
                + ")"
            )

            # Note: The current and new location are read as integer values
            # This will be replaced with stop codes in the upcoming release

            print("Enter the new current location: ")
            terminal.currentLocation = int(input())  # Input location code

            print(
                "The current location has been updated to "
                + terminal.selectedRoute[terminal.currentLocation - 1]
            )

            # Update crowd manager value every time new tickets are printed
            updatePassengerCount()
