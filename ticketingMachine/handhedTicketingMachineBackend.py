import pyrebase

selectedRoute = 0

fixedTicketPrice = 10
variableTicketPrice = 6

totalTicketsPrinted = 0

crowdManager = []
currentPassengerCount = 0

collection = 0

def selectBus():
	global selectedRoute
	global busType
	global busId
	global totalSeats

	busIdError = False

	print("Enter the bus number:")
	busId = str(input())

	if busId == "KL13N":
		selectedRoute = ["Trivandrum", "Venjaramoodu", "Killimanoor", "Vayom", "Ayur", "Kottarakara", "Adoor", "Pandalam", "Thiruvalla", "Kottayam"]
		totalSeats = 32
		busType = "Fast Passenger"
		busIdError = False

		print("You selected " + selectedRoute[-1] + " " +  busType + "(Bus Id: " + busId + ")")

	elif busId == "KL23Q":
		selectedRoute = ["Kattakad", "Trivandrum", "Venjaramoodu", "Killimanoor", "Vayom", "Ayur", "Kottarakara", "Adoor", "Ankamally", "Trissur"]
		totalSeats = 28
		busType = "Super Fast"
		busIdError = False

		print("You selected " + selectedRoute[-1] + " " +  busType + "(Bus Id: " + busId + ")")

	else:
		print("Uh-Oh! Could'nt find this bus. Try again!\n")
		busIdError = True
		selectBus()

	if busIdError == False:
		# Initialize the crowdManager
		global crowdManager

		for i in range(len(selectedRoute)):
			crowdManager.append(0)
		#print(crowdManager)
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
	crowdManager[userStartingPoint-1] += numberOfPassengers
	# Decrement crpwdmanager to remove the customers who are to deboard at the stop
	crowdManager[userDestination-1] -= numberOfPassengers
	'''
	print("\n")
	print(crowdManager)
	print("\n")
	'''
	global totalTicketsPrinted
	totalTicketsPrinted = totalTicketsPrinted + numberOfPassengers

	updatePassengerCount()


def calculateTicketPrice(userStartingPoint, userDestination, numberOfPassengers):
	# dynamicCostMultiplier shows the no. of stops after which the ticket cost increases
	dynamicCostMultiplier = 3  #here the ticket price increase after every 3 bus stops

	# routewayStopCount is the number of stops between the starting point and the destination
	routewayStopCount = abs(userDestination - userStartingPoint)

	# divide the routewayStopCount by the dynamicCostMultiplier to get number of times the cost has to be increased
	variableTicketPriceEpochs = int(routewayStopCount / dynamicCostMultiplier)
	totalTicketPrice = (fixedTicketPrice + (variableTicketPriceEpochs * variableTicketPrice)) * numberOfPassengers

	global collection
	collection = collection + totalTicketPrice
	
	return totalTicketPrice


def tripDetails():
	print("\nTRIP DETAILS\nSelected Route: " + selectedRoute[-1] + " " +  busType + "(Bus Id: " + busId + ")")
	print("Current Location: "  + selectedRoute[currentLocation-1])
	print("Total Tickets Printed: " + str(totalTicketsPrinted))

	passengersInBus()
	
	print("Seats available in Bus: " + str(availableSeatCount))


def passengersInBus():
	#currentPassengerCount = sum(crowdManager[:currentLocation])
	updatePassengerCount()

	print("Total Passengers in Bus: " + str(currentPassengerCount))

	'''
	global availableSeatCount
	availableSeatCount = totalSeats - currentPassengerCount
	'''


def updatePassengerCount():
	global currentPassengerCount
	currentPassengerCount = sum(crowdManager[:currentLocation])

	global availableSeatCount
	availableSeatCount = totalSeats - currentPassengerCount


def sendDataToFirebase():
	firebaseConfig = {"apiKey": "AIzaSyCY6jTxpTWnGIS46sK1XnwilvceAuaeUKE",
	  "authDomain": "croma-ed592.firebaseapp.com",
	  "projectId": "croma-ed592",
	  "storageBucket": "croma-ed592.appspot.com",
	  "messagingSenderId": "85756972861",
	  "appId": "1:85756972861:web:bb73b935a71f90ee603f54",
	  "measurementId": "G-ZXEDMDDFMT",
	  "databaseURL": "https://croma-ed592-default-rtdb.firebaseio.com/"}


	firebase = pyrebase.initialize_app(firebaseConfig)
	db = firebase.database()

	data = {"currentLocation": currentLocation, "passengersInBus" : currentPassengerCount, "availableSeat" : availableSeatCount}
		
	#db.push(data)

	from datetime import datetime

	now = datetime.now()
	timestamp = int(datetime.timestamp(now))

	db.child(timestamp).set(data)



if __name__ == "__main__":
	global currentLocation

	currentLocation = 1

	print("\nWelcome to CroMa: The CROwd MAnagement software\n")

	# Display all routes
	selectBus()

	# Display MENU with conductor options
	selectedMENUOption = 0

	while(selectedMENUOption != 5):

		#333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333

		#333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333

		sendDataToFirebase()

		print("\nMENU: Select an option\n1. Print Ticket\n2. Display Trip Details\n3. Display Collections\n4. Update Location\n5. Exit")
		selectedMENUOption = int(input())

		# Print ticket for the customer
		if selectedMENUOption == 1:
			printTicket()
		# Show Trip Details
		if selectedMENUOption == 2:
			tripDetails()

		if selectedMENUOption == 3:
			print("Total Collections for this trip: " + str(collection))

		if selectedMENUOption == 4:
			#selectedRouteBusStopsList = routeDictionary[selectedRoute]
			# print(selectedRouteBusStopsList) #Shows list of stations in route

			print("\nAt pesent, the current location is set to " + selectedRoute[currentLocation-1] + " (Code = " + str(currentLocation) + ")")

			print("Enter the new current location: ")
			currentLocation = int(input())

			print("The current location has been updated to " + selectedRoute[currentLocation-1])

			updatePassengerCount()