import pyrebase
import busFares
import defaults
import database

defaults.selectedRoute = 0

defaults.crowdManager = []
defaults.currentPassengerCount = 0
defaults.totalTicketsPrinted = 0

defaults.collection = 0

def selectBus():

	busIdError = False

	print("Enter the bus number:")
	defaults.busId = str(input())

	if defaults.busId == "KL13N":
		defaults.selectedRoute = ["Trivandrum", "Venjaramoodu", "Killimanoor", "Vayom", "Ayur", "Kottarakara", "Adoor", "Pandalam", "Thiruvalla", "Kottayam"]
		defaults.totalSeats = 32
		defaults.busType = "Fast Passenger"
		busIdError = False

		print("You selected " + defaults.selectedRoute[-1] + " " +  defaults.busType + "(Bus Id: " + defaults.busId + ")")

	elif defaults.busId == "KL23Q":
		defaults.selectedRoute = ["Kattakad", "Trivandrum", "Venjaramoodu", "Killimanoor", "Vayom", "Ayur", "Kottarakara", "Adoor", "Ankamally", "Trissur"]
		defaults.totalSeats = 28
		defaults.busType = "Super Fast"
		busIdError = False

		print("You selected " + defaults.selectedRoute[-1] + " " +  defaults.busType + "(Bus Id: " + defaults.busId + ")")

	else:
		print("Uh-Oh! Could'nt find this bus. Try again!\n")
		busIdError = True
		
		selectBus()

	if busIdError == False:
		# Initialize the crowdManager

		for i in range(len(defaults.selectedRoute)):
			defaults.crowdManager.append(0)

	passengersInBus()


def printTicket():
	print("\nEnter the Starting Point: ")
	userStartingPoint = int(input())

	print("\nEnter the Destination: ")
	userDestination = int(input())

	print("\nEnter the no. of passengers: ")
	numberOfPassengers = int(input())

	ticketPrice = calculateTicketPrice(userStartingPoint, userDestination, numberOfPassengers)
	print("\nTotal ticket price: " + str(ticketPrice))

	# Increment crowdmanager to include passengers who onbarded at the stop
	defaults.crowdManager[userStartingPoint-1] += numberOfPassengers
	
	# Decrement crpwdmanager to remove the customers who are to deboard at the stop
	defaults.crowdManager[userDestination-1] -= numberOfPassengers
	
	defaults.totalTicketsPrinted = defaults.totalTicketsPrinted + numberOfPassengers

	updatePassengerCount()


def calculateTicketPrice(userStartingPoint, userDestination, numberOfPassengers):
	# dynamicCostMultiplier shows the no. of stops after which the ticket cost increases
	dynamicCostMultiplier = 3  #here the ticket price increase after every 3 bus stops

	# routewayStopCount is the number of stops between the starting point and the destination
	routewayStopCount = abs(userDestination - userStartingPoint)

	# divide the routewayStopCount by the dynamicCostMultiplier to get number of times the cost has to be increased
	variableTicketPriceEpochs = int(routewayStopCount / dynamicCostMultiplier)
	totalTicketPrice = (busFares.fixedTicketPrice + (variableTicketPriceEpochs * busFares.variableTicketPrice)) * numberOfPassengers

	defaults.collection = defaults.collection + totalTicketPrice
	
	return totalTicketPrice


def tripDetails():
	print("\nTRIP DETAILS\nSelected Route: " + defaults.selectedRoute[-1] + " " +  defaults.busType + "(Bus Id: " + defaults.busId + ")")
	print("Current Location: "  + defaults.selectedRoute[defaults.currentLocation-1])
	print("Total Tickets Printed: " + str(defaults.totalTicketsPrinted))

	passengersInBus()
	
	print("Seats available in Bus: " + str(defaults.availableSeatCount))


def passengersInBus():

	updatePassengerCount()

	print("Total Passengers in Bus: " + str(defaults.currentPassengerCount))


def updatePassengerCount():
	defaults.currentPassengerCount = sum(defaults.crowdManager[:defaults.currentLocation])

	defaults.availableSeatCount = defaults.totalSeats - defaults.currentPassengerCount


if __name__ == "__main__":
	defaults.currentLocation = 1

	print("\nWelcome to CroMa: The CROwd MAnagement software\n")

	# Select the BusId to configure the route and other properties 
	selectBus()

	# Create firebase real-time database with the busId as key
	database.createFirebaseRTDatabase()

	# Display MENU with conductor options
	selectedMENUOption = 0

	while(selectedMENUOption != 5):

		# Update the FireBase real-time database to reflect any changes
		database.updateFirebaseRTDatabase_KL13N()

		print("\nMENU: Select an option\n1. Print Ticket\n2. Display Trip Details\n3. Display Collections\n4. Update Location\n5. Exit")
		selectedMENUOption = int(input())

		# Print ticket for the customer
		if selectedMENUOption == 1:
			printTicket()

		# Show Trip Details
		if selectedMENUOption == 2:
			tripDetails()

		# Display total collections through ticket sale
		if selectedMENUOption == 3:
			print("Total Collections for this trip: " + str(defaults.collection))

		# Change the current location of the bus
		if selectedMENUOption == 4:
			print("\nAt present, the current location is set to " + defaults.selectedRoute[defaults.currentLocation-1] + " (Code = " + str(defaults.currentLocation) + ")")

			print("Enter the new current location: ")
			defaults.currentLocation = int(input())  # Input the location code 

			print("The current location has been updated to " + defaults.selectedRoute[defaults.currentLocation-1])

			updatePassengerCount()