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
    [1] bus_fares (supporting function)
    [2] test_calculate_ticket_price
    [3] bus_info (supporting function)
    [4] test_update_passenger_count

.. versionadded:: 1.0.1
.. versionupdated:: 1.1.0

Read more about the working of the hardware in the :ref:`CroMa Hardware Design`
"""

import pytest  # pylint: disable=import-error


@pytest.fixture
def bus_fares():
    """
    Supporting function for the bus fare calculation algorithm.

    The crowd manager is initialized with ambigous input values that may rise
    during actual bus trip. Each instance of fare calculation is to be tested.
    NOTE: At no point the sum of crowd manager can be a value other than zero.

    .. versionadded:: 1.0.1

    Parameters:
        None

    Returns:
        fixed_ticket_price (int)
        variable_ticket_price (int)
        collection (int)
        crowd_manager (list)
        total_tickets_printed (int)
    """
    fixed_ticket_price = 10
    variable_ticket_price = 6
    collection = 10
    total_tickets_printed = 5

    crowd_manager = [4, 2, 3, -2, -5, -2, 0, 0, 0, 0]

    return [
        fixed_ticket_price,
        variable_ticket_price,
        collection,
        crowd_manager,
        total_tickets_printed,
    ]


@pytest.mark.parametrize(
    "user_starting_point, user_destination, number_of_passengers,\
         expected_output, expected_collection, expected_routeway_stop_count,\
              expected_variable_ticket_price_epochs, expected_total_tickets_printed",
    [(1, 3, 1, 10, 20, 2, 0, 6), (2, 6, 2, 32, 42, 4, 1, 7)],
)

# pylint: disable=too-many-arguments
def test_calculate_ticket_price(
    user_starting_point,
    user_destination,
    number_of_passengers,
    expected_output,
    expected_collection,
    expected_routeway_stop_count,
    expected_variable_ticket_price_epochs,
    expected_total_tickets_printed,
    bus_fares, # pylint: disable=redefined-outer-name
):
    """
    Test if the bus fare calculation algorithm is working correctly.

    The crowd manager is initialized with ambigous input values that may rise
    during actual bus trip. Each instance of fare calculation is to be tested.
    NOTE: At no point the sum of crowd manager can be a value other than zero.

    .. versionadded:: 1.0.1

    Parameters:
        user_starting_point (int)
        user_destination (int)
        number_of_passengers (int)
        expected_output (int)
        expected_collection (int)
        expected_routeway_stop_count (int)
        expected_variable_ticket_price_epochs (int)
        expected_total_tickets_printed (int)
        bus_fares (int)

    Returns:
        None
    """
    dynamic_cost_multiplier = 3
    routeway_stop_count = abs(user_destination - user_starting_point)

    variable_ticket_price_epochs = int(
        routeway_stop_count / dynamic_cost_multiplier)

    total_ticket_price = (
        bus_fares[0] + (variable_ticket_price_epochs * bus_fares[1])
    ) * number_of_passengers

    bus_fares[2] = bus_fares[2] + total_ticket_price

    bus_fares[3][user_starting_point - 1] += number_of_passengers
    bus_fares[3][user_destination - 1] -= number_of_passengers

    bus_fares[4] = bus_fares[4] + number_of_passengers

    assert routeway_stop_count == expected_routeway_stop_count
    assert variable_ticket_price_epochs == expected_variable_ticket_price_epochs
    assert total_ticket_price == expected_output

    assert sum(bus_fares[3]) == 0
    assert bus_fares[2] == expected_collection
    assert bus_fares[4] == expected_total_tickets_printed


@pytest.fixture
def bus_info():
    """
    Supporting function for the update passenger count method

    Whenever a fresh operation is performed on the hardware ticketing machine,
    some of the values need to be updated, to reflect the appropriate changes
    NOTE: At no point the sum of crowd manager can be a value other than zero.

    .. versionadded:: 1.0.1

    Parameters:
        None

    Returns:
        crowd_manager (list)
        total_seats (int)
    """
    crowd_manager = [4, 2, 3, -2, -5, -2, 0, 0, 0, 0]
    total_seats = 32

    return [crowd_manager, total_seats]


@pytest.mark.parametrize(
    "current_location, expected_current_passenger_count, expected_available_seat_count",
    [(3, 9, 23), (2, 6, 26)],
)
def test_update_passenger_count(
    current_location,
    expected_current_passenger_count, # pylint: disable=redefined-outer-name
    expected_available_seat_count,
    bus_info, # pylint: disable=redefined-outer-name
):
    """
    Test if the update passenger count method is functioning correctly.

    Whenever a fresh operation is performed on the hardware ticketing machine,
    some of the values need to be updated, to reflect the appropriate changes
    NOTE: At no point the sum of crowd manager can be a value other than zero.

    .. versionadded:: 1.0.1

    Parameters:
        current_location (int)
        expected_current_passenger_count (int)
        expected_available_seat_count (int)
        bus_info (int)

    Returns:
        None
    """
    current_passenger_count = sum(bus_info[0][:current_location])

    available_seat_count = bus_info[1] - current_passenger_count

    assert current_passenger_count == expected_current_passenger_count
    assert available_seat_count == expected_available_seat_count
