# Author: Ashwin Raj <thisisashwinraj@gmail.com>
# License: Creative Commons Attribution - NonCommercial - NoDerivs License
# Discussions-to: github.com/thisisashwinraj/CroMa-Crowd-Management-System/discussions

import pytest


@pytest.fixture
def busFares():
    fixedTicketPrice = 10
    variableTicketPrice = 6
    collection = 10
    totalTicketsPrinted = 5

    crowdManager = [4, 2, 3, -2, -5, -2, 0, 0, 0, 0]

    return [fixedTicketPrice, variableTicketPrice, collection, crowdManager, totalTicketsPrinted]


@pytest.mark.parametrize(
    "userStartingPoint, userDestination, numberOfPassengers, expectedOutput, expectedCollection, expectedRoutewayStopCount, expectedVariableTicketPriceEpochs, expectedTotalTicketsPrinted",
    [(1, 3, 1, 10, 20, 2, 0, 6), (2, 6, 2, 32, 42, 4, 1, 7)],
)
def test_calculateTicketPrice(
    userStartingPoint,
    userDestination,
    numberOfPassengers,
    expectedOutput,
    expectedCollection,
    expectedRoutewayStopCount,
    expectedVariableTicketPriceEpochs,
    expectedTotalTicketsPrinted,
    busFares,
):
    dynamicCostMultiplier = 3
    routewayStopCount = abs(userDestination - userStartingPoint)

    variableTicketPriceEpochs = int(routewayStopCount / dynamicCostMultiplier)

    totalTicketPrice = (
        busFares[0] +
        (variableTicketPriceEpochs * busFares[1])) * numberOfPassengers

    busFares[2] = busFares[2] + totalTicketPrice

    busFares[3][userStartingPoint - 1] += numberOfPassengers
    busFares[3][userDestination - 1] -= numberOfPassengers

    busFares[4] = busFares[4] + numberOfPassengers

    assert routewayStopCount == expectedRoutewayStopCount
    assert variableTicketPriceEpochs == expectedVariableTicketPriceEpochs
    assert totalTicketPrice == expectedOutput

    assert sum(busFares[3]) == 0
    assert busFares[2] == expectedCollection
    assert busFares[4] == expectedTotalTicketsPrinted


@pytest.fixture
def busInfo():
    crowdManager = [4, 2, 3, -2, -5, -2, 0, 0, 0, 0]
    totalSeats = 32

    return [crowdManager, totalSeats]


@pytest.mark.parametrize(
    "currentLocation, expectedCurrentPassengerCount, expectedAvailableSeatCount",
    [(3, 9, 23), (2, 6, 26)],
)
def test_updatePassengerCount(currentLocation, expectedCurrentPassengerCount,
                              expectedAvailableSeatCount, busInfo):
    currentPassengerCount = sum(busInfo[0][:currentLocation])

    availableSeatCount = busInfo[1] - currentPassengerCount

    assert currentPassengerCount == expectedCurrentPassengerCount
    assert availableSeatCount == expectedAvailableSeatCount


@pytest.mark.parametrize(
    "busId, expectedBusType, expectedSelectedRoute, expectedTotalSeats, expectedBusIdError",
    [
        (
            "KL13N",
            "Fast Passenger",
            [
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
            ],
            32,
            False,
        ),
        ("KL98WE", None, [], 0, True),
    ],
)
def test_selectBus(
    busId,
    expectedBusType,
    expectedSelectedRoute,
    expectedTotalSeats,
    expectedBusIdError,
):
    busIdError = False
    crowdManager = []

    busType = None
    selectedRoute = []
    totalSeats = 0

    if busId == "KL13N":
        selectedRoute = [
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

        totalSeats = 32
        busType = "Fast Passenger"

        busIdError = False

    elif busId == "KL24Q":
        selectedRoute = [
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

        totalSeats = 28
        busType = "Super Fast"

        busIdError = False

    elif busId == "KL94F":
        selectedRoute = [
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

        totalSeats = 28
        busType = "City Local"

        busIdError = False

    else:
        busIdError = True

    if busIdError is False:
        for i in range(len(selectedRoute)):
            crowdManager.append(0)

    assert busType == expectedBusType
    assert selectedRoute == expectedSelectedRoute
    assert totalSeats == expectedTotalSeats
    assert busIdError == expectedBusIdError
