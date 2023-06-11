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
The module contains the backend methods that powers user application's interface. 
It contains method for processing real-time value, calculating fares, displaying 
maps and performing other computations that are required for the app to function.

Included Functions:
    [1] BackendService (class)
        [i] fetch_buses_to_user_destination_from_user_origin
        [ii] display_bus_on_map
        [iii] calculate_time_difference
        [iv] fetch_bus_details
        [v] get_traffic_level
        [vi] fetch_bus_attributes

    [2] BusFareCalculator (class)
        [i] bus_fare_calculator

.. versionupdated:: 1.3.0

Read about the working of the app's backend in :ref:`CroMa - Application backend`
"""

import pandas as pd
from application import application_support_dictionary
from application.application_database import (
    retrieve_bus_total_delay,
    retrieve_current_bus_status,
    retrieve_last_stop_arrival_time,
    retrieve_bus_total_delay,
    retrieve_bus_route_id,
    retrieve_bus_data_from_sql_database,
    retrieve_current_location,
    retrieve_available_seats,
    retrieve_passengers_count,
)

import firebase_admin
from firebase_admin import credentials

import datetime
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim

import openrouteservice as ors
from application import application_credentials


class BackendService:
    """
    Class to perform the backend computation necessary for the application to work.

    Major backend service methods packed within the class includes one for fetching
    list of buses to a partcular stop, displaying interactive map, fetching traffic
    levels in route, & calculating the time difference between multiple time stamps.

    This class can be considered as the heart of the firmware as the passenger apps
    uses processed data, to display accurate information to passenger using the app.

    .. versionadded:: 1.3.0

    NOTE: During actual trips, the DSR reports are generated and mailed to the admin
    """

    def fetch_buses_to_user_destination_from_user_origin(
        boarding_point, dropping_point
    ):
        """
        Method to fetch list of buses that pass through users origin and destination.

        This method takes 2 locations as arguments and returns the list of all buses
        that passes through both these locations. The method uses a combination of a
        series of support dictionaries, firebase real time database and SQL database.

        .. versionadded:: 1.3.0

        Parameters:
            [str] boarding_point: Bus stop from which the passenger boards the bus
            [str] dropping_point: Bus stop at which the passenger deboards the bus

        Returns:
            [list] available_buses_to_destination: list of buses through both stops

        NOTE: The user's boarding point must not be the same as their dropping point.

        """
        # Fetch the list of buses that pass through user's boarding point
        buses_passing_through_boarding_point = (
            application_support_dictionary.all_bus_stops[boarding_point]
        )

        # Initialize an empty list to store the list of available buses
        available_buses_to_destination = []

        # Iterate through all buses passing through the boarding point
        for bus_id in buses_passing_through_boarding_point:
            # retrueve the current bus status
            current_bus_status = retrieve_current_bus_status(bus_id)

            # Continue the operation only if the bus is active at the moment
            if current_bus_status == "Active":
                # Fetch the route id assigned to the bus
                selected_bus_route_id = retrieve_bus_route_id(bus_id)

                # Fetch the list of bus stops corresponding to this route id
                all_stops_of_bus = application_support_dictionary.all_routes[
                    selected_bus_route_id
                ]

                # Retrieve the current location of the bus
                current_bus_location = retrieve_current_location(bus_id)
                # Find the numerical index corresponding to this location
                int_current_bus_location = (
                    all_stops_of_bus.index(current_bus_location) + 1
                )

                # Check if the user's dropping point is present in the bus's route map
                if dropping_point not in all_stops_of_bus[int_current_bus_location:]:
                    break  # stop computing if it's not present

                # Find the numerical index corresponding to the user's boarding point
                index_of_user_boarding_point = all_stops_of_bus.index(boarding_point)

                # Check if the bus is currently within three stops from the user's boarding point
                if index_of_user_boarding_point < 3:
                    lookup_three_bus_stops = all_stops_of_bus[
                        : index_of_user_boarding_point + 1
                    ]
                else:
                    lookup_three_bus_stops = all_stops_of_bus[
                        index_of_user_boarding_point
                        - 3 : index_of_user_boarding_point
                        + 1
                    ]

                # If within three stops, add the bus id of that bus to the list
                if current_bus_location in lookup_three_bus_stops:
                    available_buses_to_destination.append(bus_id)

        return available_buses_to_destination  # Return the list of all available buses

    def display_bus_on_map(city):
        """
        # Method to display a map with marker on the location passed as the argument

        This method takes a city name as argument and dislays a map using the folium
        package, with a pointer at the location read as the argument for this method

        .. versionadded:: 1.3.0

        Parameters:
            [str] city: name of the city where the marker is to be placed

        Returns:
            [folium.folium.map] map: Map with the marker indicating current location

        NOTE: City is geocoded to get the latitude & longitude for displaying marker

        """
        # Use geocoding to get the coordinates of the city
        geolocator = Nominatim(user_agent="my-app")
        location = geolocator.geocode(city)
        # Fetch the latitude and longitude of the current location
        lat, lon = location.latitude, location.longitude

        # Create a map object using the python folium package
        map = folium.Map(location=[lat, lon], zoom_start=17)

        # Add a marker to the map
        folium.Marker(location=[lat, lon], popup=city).add_to(map)

        return map  # Return the folium.folium.map object

    def calculate_time_difference(time1, time2):
        """
        Function to calculate difference between times and return output as minutes

        Two arguments representing time in HH:MM format, type-casted as strings are
        passed into the function. Difference is calculated after converting to mins.

        .. versionadded:: 1.3.0

        Parameters:
            [str] time1: The subtrahend string value of the time var, in HH:MM format
            [str] time2: The minuend value of time casted as string in HH:MM format

        Returns:
            [int] difference_minutes: The total difference in time returned as mins

        NOTE: Time difference is returned as mins. Using seconds increases accuracy.

        """
        # Split the subtrahend and minuend into hours and minutes & map as integers
        hours1, minutes1 = map(int, time1.split(":"))
        hours2, minutes2 = map(int, time2.split(":"))

        # Convert the time values for both operands into minutes for calculation
        total_minutes1 = hours1 * 60 + minutes1
        total_minutes2 = hours2 * 60 + minutes2

        difference_minutes = total_minutes2 - total_minutes1  # Calculate difference

        # Return the calculated time difference as minutes
        return difference_minutes

    def fetch_bus_details(bus_id, boarding_point, dropping_point):
        """
        Method to fetch necessary bus details, to be used in the web app's frontend

        The method takes bus id, boarding point and dropping point as the arguments
        and performs complex processings and computations to retrieve parameters to
        be used for displaying information on the frontend of the users application.

        .. versionadded:: 1.3.0

        Parameters:
            [str] bus_id: The id tagged to a particular bus
            [str] boarding_point: Bus stop from which the passenger boards the bus
            [str] deboarding_point: Bus stop at which a passenger deboards the bus

        Returns:
            [str] bus_name: Name of the bus
            [str] bus_operator: Organization that operates and controls the bus
            [str] bus_id: Unique id for the bus
            [str] estimated_time_of_arrival_at_user_destination: ETA at destination
            [int] minutes_required_to_reach_user_boarding_point_from_bus_current_loc: mins to reach boarding point
            [float] load_factor: A mathematical variable indicating crowd level in the bus
            [int] available_seats_in_bus: Seats available in the bus
            [str] bus_type: The type of the bus, as defined by the bus operator
            [str] bus_current_location: Current location of the bus

        NOTE: Time difference is returned as mins. Using seconds increases accuracy.

        """
        # Retrieve the route id assigned to the particular bus
        bus_route_id = retrieve_bus_route_id(bus_id)
        # Fetch the last stop in the bus's route
        bus_last_stop = application_support_dictionary.all_routes[bus_route_id][-1]

        # Fetch the operator and type of the bus
        bus_operator, bus_type = retrieve_bus_data_from_sql_database(bus_id)
        # Lexically fix the bus type before showing to the end user
        bus_type_shortened = " ".join(bus_type.split()[:-1])

        # Generate the bus name by suffixing the bus type to the last stop
        bus_name = bus_last_stop + " " + bus_type_shortened

        # Fetch the current location of the bus
        bus_current_location = retrieve_current_location(bus_id)
        # Fetch the list of all bus stops in the route
        stops_in_route = application_support_dictionary.bus_timings.get(bus_route_id)

        # Fetch the time required for the bus to reach bus's current location
        time_from_origin_to_reach_bus_current_loc = stops_in_route[bus_current_location]
        # Fetch the time required for the bus to reach the user's destination
        time_from_origin_to_reach_user_destination = stops_in_route[dropping_point]

        # Calculate the mins required to reach the user's destination from bus's current location
        minutes_required_to_reach_user_destination_from_bus_current_loc = (
            time_from_origin_to_reach_user_destination
            - time_from_origin_to_reach_bus_current_loc
            + retrieve_bus_total_delay(bus_id)
        )

        # Determine the current time
        current_time = datetime.datetime.now().time()
        # calculate the estimated time of arrival of the bus at user destination
        eta_user_destination = datetime.datetime.combine(
            datetime.date.today(), current_time
        ) + datetime.timedelta(
            minutes=int(minutes_required_to_reach_user_destination_from_bus_current_loc)
        )

        # Parse the datetime string into HH:MM format
        estimated_time_of_arrival_at_user_destination = eta_user_destination.strftime(
            "%H:%M"
        )

        # Fetch the estimated time required to reach the user's boarding point from the origin
        time_from_origin_to_reach_user_boarding_point = stops_in_route[boarding_point]
        # Retrieve the arrival time of the bus at the last stop
        arrival_time_at_last_stop = retrieve_last_stop_arrival_time(bus_id)
        # Calculate the time in minutes sibnce the bus left the last stop
        minutes_since_bus_left_last_stop = BackendService.calculate_time_difference(
            arrival_time_at_last_stop.strftime("%H:%M"),
            datetime.datetime.now().strftime("%H:%M"),
        )
        # Calculate the time in minurtes required for the bus to reach the user's boarding point
        minutes_required_to_reach_user_boarding_point_from_bus_current_loc = (
            time_from_origin_to_reach_user_boarding_point
            - time_from_origin_to_reach_bus_current_loc
            - minutes_since_bus_left_last_stop
            + retrieve_bus_total_delay(bus_id)
        )

        # Retrieve the total number of seats available in the bus
        available_seats_in_bus = retrieve_available_seats(bus_id)
        # Retrieve the total number of passengers aboard the bus
        total_passengers_in_bus = retrieve_passengers_count(bus_id)

        # Calculate the total number of seats in the bus
        total_seats_in_bus = total_passengers_in_bus + available_seats_in_bus
        # Calculate the load factor of the bus at the given time instance
        load_factor = total_passengers_in_bus / total_seats_in_bus

        return (
            bus_name,
            bus_operator,
            bus_id,
            estimated_time_of_arrival_at_user_destination,
            minutes_required_to_reach_user_boarding_point_from_bus_current_loc,
            load_factor,
            available_seats_in_bus,
            bus_type,
            bus_current_location,
        )

    def get_traffic_level(origin, destination):
        """
        Method to fetch the traffic level between two locations using ORS API data

        The method takes two locations and fetches the traffic level between these
        location using the data from openrouteservice api with driving-car profile

        .. versionadded:: 1.3.0

        Parameters:
            [str] origin: Bus stop from which the passenger boards the bus
            [str] destination: Bus stop at which a passenger deboards the bus

        Returns:
            [int] traffic_level: Traffic level between the origin, and destination

        NOTE: The output is highly susceptible to changes made to the ORS API data

        """
        # Fetch the API key for accessing the Open Route Service API
        api_key = application_credentials.OPENROUTESERVICE_API_KEY
        client = ors.Client(key=api_key)  # Set up the client

        # Determine co-ordinates fro the origin
        origin_coords = client.pelias_search(text=origin)["features"][0]["geometry"][
            "coordinates"
        ]
        # Determine co-ordinates fro the destination
        destination_coords = client.pelias_search(text=destination)["features"][0][
            "geometry"
        ]["coordinates"]

        # Fetch the response from the API
        response = client.directions(
            coordinates=[origin_coords, destination_coords],
            profile="driving-car",
            units="km",
            instructions=True,
            options={"avoid_features": ["tollways"]},
        )

        # Retrieve the duration_no_traffic parameter
        duration_no_traffic = response["routes"][0]["summary"]["duration"]
        # Simulate traffic condition by considering historical average
        historical_traffic_factor = (
            1.2  # Adjust this factor based on your estimation of traffic conditions
        )

        # Calculate the duration with traffic
        duration_with_traffic = duration_no_traffic * historical_traffic_factor
        # Calculate the traffic level by subtracting duration_no_traffic from duration_with_traffic
        traffic_level = duration_with_traffic - duration_no_traffic

        return traffic_level

    def fetch_bus_attributes(bus_id):
        """
        Method to fetch necessary bus attributes, to be used to get bus information

        This method takes bus id as the argument to perform complex processings and
        computations to retrieve core parameters, corresponding to a particular bus

        .. versionadded:: 1.3.0

        Parameters:
            [str] bus_id: The id tagged to a particular bus

        Returns:
            [str] bus_name: Name of the bus
            [str] bus_operator: Organization that operates and controls the bus
            [str] bus_type: Type of the bus as defined by the operator
            [str] bus_route_id: Unique id assosciated to a route
            [int] available_seats_in_bus: No. of seats available in the bus
            [list] all_bus_stops_list: List of all stops in a route
            [str] bus_starting_location: Starting location of the bus
            [str] bus_terminal_location: Terminal of the bus
            [int] total_delay_in_current_journey: Total delay in schedule in minutes
            [str] bus_current_location: Current location of the bus
            [str] bus_next_location: Upcoming stop of the bus
            [int] total_passengers_in_bus: Total number of passengers in the bus
            [float] load_factor: Mathematical variable indicating crowd level
            [int] percentage_journey_completed: Percentage of the route already traversed

        NOTE: Time difference is returned as mins. Using seconds increases accuracy.

        """
        # Fetch the route id corresponding to the bus
        bus_route_id = retrieve_bus_route_id(bus_id)
        # Bus terminal location
        bus_last_stop = application_support_dictionary.all_routes[bus_route_id][-1]

        # Retrieve the bus operator and the bus type as define by the operator
        bus_operator, bus_type = retrieve_bus_data_from_sql_database(bus_id)
        # Shorten the bus type before showing to the end users
        bus_type_shortened = " ".join(bus_type.split()[:-1])

        # Generate the name of the bus by preixing the bus terminal to the bus type
        bus_name = bus_last_stop + " " + bus_type_shortened

        # Fetch the list of all bus stops in the route
        all_bus_stops_list = application_support_dictionary.all_routes[bus_route_id]

        # Fetch the starting location of the from firebase database
        bus_starting_location = all_bus_stops_list[0]
        # Fetch the terminal location of the bus from firebase database
        bus_terminal_location = all_bus_stops_list[-1]
        # Fetch the current location of the bus from firebase database
        bus_current_location = retrieve_current_location(bus_id)
        # Fetch the upcoming bus stop for the bus
        bus_next_location = all_bus_stops_list[
            all_bus_stops_list.index(bus_current_location) + 1
        ]

        # Calculate the total delay in the bus's journey at the time instance
        total_delay_in_current_journey = retrieve_bus_total_delay(bus_id)

        # Retrieve the total number of passengers in the bus
        total_passengers_in_bus = retrieve_passengers_count(bus_id)
        # Retrieve the count of available seats in the bus
        available_seats_in_bus = retrieve_available_seats(bus_id)
        # Calculate the total number of seats available in the bus
        total_seats_in_bus = total_passengers_in_bus + available_seats_in_bus

        # Calculate the load factor of the bus
        load_factor = total_passengers_in_bus / total_seats_in_bus

        # Calculate the percentage of journey already traversed by the bus
        percentage_journey_completed = (
            (all_bus_stops_list.index(bus_current_location) + 1)
            / len(all_bus_stops_list)
        ) * 100

        return (
            bus_name,
            bus_operator,
            bus_type,
            bus_route_id,
            available_seats_in_bus,
            all_bus_stops_list,
            bus_starting_location,
            bus_terminal_location,
            total_delay_in_current_journey,
            bus_current_location,
            bus_next_location,
            total_passengers_in_bus,
            load_factor,
            percentage_journey_completed,
        )


# print(BackendService.get_traffic_level("Burari", "Shalimar Bagh"))


class BusFareCalculator:
    """
    Class to calculate the total bus fares payable by the passengers aboard the bus.

    This class contains the method, that reads necessary arguments to calculate the
    total fare payable by passenger(s) aboard a bus, depending on custom parameters

    .. versionadded:: 1.3.0

    NOTE: During actual trips, the DSR reports are generated and mailed to the admin

    """

    def bus_fare_calculator(user_starting_point, user_destination, bus_type, route_id):
        """
        Function to print ticket based on inputs from the user.

        The total fare is calculated based on the passenger's onboarding location, their
        destination and co-passengers count. The function supports both single and round
        trip fare calculation. Multiple KPI's are also updated for admin level analytics

        Read more in the :ref:`Fare calculation`.

        ..versionupdated:: 1.3.0

        Parameters:
            [str] user_starting_point: The onboarding location of the passenger
            [str] user_destination: The destination location of the passenger
            [str] bus_type: The type of bus as defined by the operator
            [str] route_id: Route Id corresponding to the selected bus

        Returns:
            [int] total_ticket_fare: The total bus fare, inclusive of all charges

        """
        # dynamic_cost_multiplier shows no. of stops after which costs increases
        dynamic_cost_multiplier = 3  # The cost is set to increase after 3 stops

        # List of all stops in the selected route id
        stops_list = list(application_support_dictionary.all_routes[route_id])

        # The index values corresponding to the coarding and deboarding points
        user_starting_point = stops_list.index(user_starting_point)
        user_destination = stops_list.index(user_destination)

        # routeway_stop_count gives no. of stops between origin, and destination
        routeway_stop_count = abs(user_destination - user_starting_point)

        # divide routeway_stop_count / dynamic_cost_multiplier to get variable cost epoch
        variable_ticket_price_epochs = int(
            routeway_stop_count / dynamic_cost_multiplier
        )

        # Dictionary of fixed ticket price corresponding to the bus type
        fixed_ticket_price_dictionary = {
            "City Fast Non-AC": 10,
            "Fast Double Decker": 16,
            "Deluxe AC-Sleeper": 32,
            "Super Fast Non-AC": 24,
            "Minnal AC-Sleeper": 40,
        }

        # Set the fixed ticket price based on the bus type
        FIXED_TICKET_PRICE = fixed_ticket_price_dictionary[bus_type]

        # Dictionary of variable ticket price corresponding to the bus type
        variable_ticket_price_dictionary = {
            "City Fast Non-AC": 6,
            "Fast Double Decker": 12,
            "Deluxe AC-Sleeper": 16,
            "Super Fast Non-AC": 14,
            "Minnal AC-Sleeper": 20,
        }

        # Set the variable ticket price based on the bus type
        VARIABLE_TICKET_PRICE = variable_ticket_price_dictionary[bus_type]

        # Calculate the total ticket fare for the trip
        total_ticket_fare = FIXED_TICKET_PRICE + (
            variable_ticket_price_epochs * VARIABLE_TICKET_PRICE
        )

        return total_ticket_fare  # Return the total ticket fare
