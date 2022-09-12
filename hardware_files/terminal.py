import main

# [Pre-Defined] A list of all bus stops in a given route
global selectedRoute
# [Pre-Defined] Variable specifying the type of bus (eg: express, city etc)
global busType
# [Pre-Defined] A unique Id associate with each bus
global busId
# [Pre-Defined] Total number of seats in a bus
global totalSeats

# [Dynamic] Total no. of passengers in bus at a given time. Default value is 0
global currentPassengerCount
# [Dynamic] Free seats available in a bus in transit. Default value set to 0
global availableSeatCount
# [Dynamic] The current location of the bus. Default value set to origin
global currentLocation
# [Dynamic] Amount collected as fare during the trip. Default value set to 0
global collection
# [Dynamic] Total tickets printed throughout the trip. Default value set to 0
global totalTicketsPrinted
# [Dynamic] An array of 0s of length(selectedRoute) managing crowd information
global crowdManager
