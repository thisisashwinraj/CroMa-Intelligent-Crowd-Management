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
This module contains the top-level environment of the user application interface.
It contains methods for printing tickets, managing passenger's data and includes
several options for performing conductor book-keeping & data-tracking operations.

Included Functions:
    [1] add_minutes_to_time
    [2] apply_style_to_sidebar_button
    [3] is_valid_email
    [4] croma_application_playground
    [5] view_bus_details
    [6] send_bug_report

.. versionupdated:: 1.3.0

Read about the functionality of this app in :ref:`CroMa - Passenger Application`
"""

import base64
import re
import pandas as pd
import streamlit as st
from PIL import Image

import time
import datetime
from datetime import datetime, timedelta

import folium
from streamlit_folium import folium_static
import googlemaps
from geopy.geocoders import Nominatim

from application import application_support_dictionary
from application.application_backend import BackendService, BusFareCalculator
from application.application_database import (
    retrieve_bus_route_id,
    retrieve_available_seats,
    retrieve_last_stop_arrival_time,
    retrieve_current_location,
)
from hardware import terminal

import firebase_admin
from firebase_admin import credentials


# Set the title and favicon for the streamlit web application
st.set_page_config(
    page_title="CroMa - User Application Simulator",
    page_icon="assets/favicon/croma-favicon.jpg",
)

try:
    if terminal.initialize_firebase_sdk_ticketing_machine < 1:
        # Increment the counter to avoid reinitializing of the firebase database
        terminal.initialize_firebase_sdk_ticketing_machine = (
            terminal.initialize_firebase_sdk_ticketing_machine + 1
        )

        # Initialize the app with a service account, granting admin privileges
        cred = credentials.Certificate("hardware/adminsdk.json")
        firebase_admin.initialize_app(
            cred, {"databaseURL": "https://technoholic-407a3.firebaseio.com/"}
        )
except:
    pass  # If the initialization process throws exception, take no action

# Remove the extra padding from the top margin of the web app
st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 1rem;
					padding-bottom: 1rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)

# Hide the streamlit menu and default footer from the app's front-end
HIDE_MENU_STYLE = """
<style>
#MainMenu  {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(HIDE_MENU_STYLE, unsafe_allow_html=True)  # Allow HTML tags in mkd

# Removes the default underline styling from the hyperlinks from the web app
st.markdown(
    """
    <style>
    .stMarkdown a {
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Change default font face for the web application to Google Sans
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans&display=swap');
    body {
        font-family: 'Google Sans', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add custom CSS to customize the switch button to have curved edges
st.markdown(
    """
    <style>
    .switch {
        position: relative;
        display: inline-block;
        width: 60px;
        height: 34px;
    }
    
    .switch input {
        opacity: 0;
        width: 0;
        height: 0;
    }
    
    .slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #ccc;
        transition: 0.4s;
        border-radius: 34px;
    }
    
    .slider:before {
        position: absolute;
        content: "";
        height: 26px;
        width: 26px;
        left: 4px;
        bottom: 4px;
        background-color: white;
        transition: 0.4s;
        border-radius: 50%;
    }
    
    input:checked + .slider {
        background-color: #4CAF50;
    }
    
    input:focus + .slider {
        box-shadow: 0 0 1px #4CAF50;
    }
    
    input:checked + .slider:before {
        transform: translateX(26px);
    }
    
    .slider.round {
        border-radius: 34px;
    }
    
    .slider.round:before {
        border-radius: 50%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def add_minutes_to_time(time_str, minutes):
    """
    Function to add minutes to the time argument, and return the output as time

    The minutes argument is casted using timedelta, and added with the datetime
    argument. The new time is returned as a datetime object in the HH:MM format.

    .. versionadded:: 1.3.0

    Parameters:
        [str] time_str: The time is passed as a string in HH:MM format
        [int] minutes: Minutes to be added to the time argument

    Returns:
        [str] new_time_str: Time after adding the minutes is returned as string

    NOTE: Addition is performed after converting string values to a time object.

    """
    # Converts the date string parsed in HH:MM format to a datetime object
    time_obj = datetime.strptime(time_str, "%H:%M")
    delta = timedelta(minutes=minutes)  # Converts the integer argument as minutes

    new_time_obj = time_obj + delta  # Adds the minutes to the datetime object
    new_time_str = new_time_obj.strftime("%H:%M")  # Converts datetime obj to string

    return new_time_str


def apply_style_to_sidebar_button(file_name):
    """
    Function to apply CSS style specified in the parameter to the sidebar button.

    The function takes a CSS file as a parameter and applies the customized style
    to all the buttons widgets on the sidebar of the croma_hw_playground web page

    Read more in the :ref:`Styling the CroMa Passenger Application`.

    .. versionadded:: 1.3.0

    Parameters:
        [css file] file_name: CSS file holding style to be applied on the buttons

    Returns:
        None -> Applies the style specified in the CSS file to all sidebar button
    """
    with open(file_name, encoding="utf-8") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def is_valid_email(email):
    """
    Function to check if the email id provided as the function argument is valid.

    The function takes a email address as input and checks whether it is a valid
    mail format. It uses regular expression pattern to validate the mail address.

    Read more in the :ref:`Croma - Passenger application - Backend`.

    .. versionadded:: 1.3.0

    Parameters:
        [str] email: The email address to be validated

    Returns:
        [bool] validation: True if the email address is valid, False otherwise.

    NOTE: Function validates email format but can't guarantee its deliverability.

    """
    # The pattern ensures that the email address follows the general format rules:

    # [1] Starts with alphanumeric characters, dots, underscores, percent, or plus/minus symbols.
    # [2] This is followed by the at symbol (@).
    # [3] After the at symbol, there can be one or more alphanumeric characters, dots, or hyphens.
    # [4] There should be a period (dot) followed by at least two alphabetic characters.

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def croma_application_playground():
    """
    [CroMa WebApp page 01/03] - Simulates CroMa User Application on your web browser.

    Function for displaying simulation pages for CroMa's User application. This tool
    is intended for use by the passengers to look for buses, and related information.

    The simulation page incorporates a primary record that facilitates user input of
    the user's boarding point and dropping point. This data is subsequentlt utilized
    to search for buses in route, provide information on crowd and seat availability.

    Read more in the :ref:`CroMa - Passenger application`.

    .. versionadded:: 1.3.0

    Parameters:
        None -> Variables are read in real-time from the users as per configruations

    Returns:
        None -> Values are updated inplace or within the firebase RT or SQL database

    .. See Also:
        [1] application_backend (BackendService, BusFareCalculator)
        [2] application_database
        [3] application_support_dictionary

    NOTE: Upcoming update will include using AJAX based methods to reduce load times

    """
    # Apply the CSS styles defined in the parameter file to the sidebar buttons
    apply_style_to_sidebar_button("hardware/style.css")

    # Display a horizontal rule on the sidebar to seprate different sections
    st.sidebar.markdown("---")

    # fetch the list of all bus stops in the region
    bus_stops_list = list(application_support_dictionary.all_bus_stops.keys())

    # Display selectbox for user to select the boarding point and dropping point
    input_starting_location = st.sidebar.selectbox(
        "Select starting location", bus_stops_list
    )
    input_user_destination = st.sidebar.selectbox(
        "Select destination location", bus_stops_list
    )

    # Display button to search for all the available  in the region
    find_bus_button = st.sidebar.button("Find Available Buses")

    # Search for buses only when the button is hit and valid values are entered
    if find_bus_button or input_starting_location or input_user_destination:
        # Display title on the streamlit web application
        st.markdown(
            "<H2>Showing buses to " + input_user_destination + "</H2>",
            unsafe_allow_html=True,
        )

        # Fetch th list of available buses using the function from the app backend
        list_of_available_buses = (
            BackendService.fetch_buses_to_user_destination_from_user_origin(
                input_starting_location, input_user_destination
            )
        )
        search_results_count = len(
            list_of_available_buses
        )  # Calculate the count of results

        col1, col2 = st.columns([2.9, 1])  # Divide the section into 2 columns

        with col2:
            # Display checkbox, which when checked only shows buses
            show_bus_with_seats_status = st.checkbox(
                "Show bus with seats", value=False, key="switch"
            )

        # If the checkbox is checked, show only buses with seats available
        if show_bus_with_seats_status == True:
            buses_with_seats_available = (
                []
            )  # Initialize list of bus with seats available

            # Iterate through the list of results
            for i in range(search_results_count):
                current_bus_id = list_of_available_buses[i]  # Fetch current Bus Id
                # Retrieve the count of available seats
                available_seats_in_bus = retrieve_available_seats(current_bus_id)

                # Check the available seat count in the bus
                if available_seats_in_bus > 0:
                    # If seats available, append bus id into
                    buses_with_seats_available.append(current_bus_id)

            # Only include the list of bus id's with seats available to be shown to user
            list_of_available_buses = buses_with_seats_available
            # Calculate the number of search results
            search_results_count = len(list_of_available_buses)

        with col1:
            try:
                # Fetch the traffic level between the user's boarding point and dropping point
                traffic_level = BackendService.get_traffic_level(
                    input_starting_location, input_user_destination
                )
            except:
                # In case of exceptions, keep traffic level as 2500 (moderate)
                traffic_level = 2500

            # Indicate if the traffic is heavy, Moderate or light
            if traffic_level >= 7500:
                traffic_condition = "Heavy traffic, expect delays"
            elif traffic_level <= 2500:
                traffic_condition = "Moderate traffic"
            else:
                traffic_condition = "Busier than usual"

            # Display the sub heading on the web app with related information
            if search_results_count > 1:
                st.markdown(
                    "<H5>"
                    + str(search_results_count)
                    + " buses near you • "
                    + str(traffic_condition)
                    + "</H5>",
                    unsafe_allow_html=True,
                )
            elif search_results_count == 1:
                st.markdown(
                    "<H5>"
                    + str(search_results_count)
                    + " bus near you • "
                    + str(traffic_condition)
                    + "</H5>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("<H5>No buses found near you</H5>", unsafe_allow_html=True)

        # Iterate through all the bus id's in the list of available buses
        for i in range(search_results_count):
            st.markdown(
                """
                <style>
                .custom-hr {
                    margin-top: -10px;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            # Fetch the current bus id from the list of available bues
            current_bus_id = list_of_available_buses[i]
            # Fetch bus details corresponding to the bus id from datasources (incl. firebase and SQL DB)
            (
                bus_name,
                bus_operator,
                bus_id,
                estimated_time_of_arrival_at_user_destination,
                estimated_time_of_arrival_at_user_boarding_point,
                load_factor,
                available_seats_in_bus,
                bus_type,
                bus_current_location,
            ) = BackendService.fetch_bus_details(
                current_bus_id, input_starting_location, input_user_destination
            )

            # Display a custom horizontal rule with reducecd margins
            st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)
            explore_bus_details_button_id = (
                f"button_{i}"  # Generate unique element id for each bus
            )

            # Split the frontend into three sections for displaying image, text details and buttons
            image_column, bus_name_column, bus_fare_column = st.columns([1.2, 4, 1.14])
            # Add curved boundary when displaying the image of the bus in the frontend
            st.markdown(
                """
                <style>
                .rounded-image img {
                    border-radius: 5px;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            # Select different image files based on the bus type of the current bus
            map_bus_banner_dictionary = {
                "City Fast Non-AC": "City Fast Non-AC.png",
                "Fast Double Decker": "Fast Double Decker.png",
                "Deluxe AC-Sleeper": "Deluxe AC-Sleeper.png",
                "Super Fast Non-AC": "Super Fast Non-AC.png",
                "Minnal AC-Sleeper": "Minnal AC-Sleeper.png",
            }

            # Set the path from where the image has to be fetched to be displayed on the web app
            image_path = "assets/bus_banners/" + map_bus_banner_dictionary[bus_type]

            # Open the image file from the path it is stored in as bytestream
            with open(image_path, "rb") as f:
                image_data = f.read()  # read the image file from the path
                # Base encode the image using base64 encoding
                encoded_image = base64.b64encode(image_data).decode()

            with image_column:
                # Display the image in th first column (to the extreme left)
                st.markdown(
                    f'<div class="rounded-image"><img src="data:image/png;base64,{encoded_image}"></div>',
                    unsafe_allow_html=True,
                )

            with bus_name_column:
                # Cast the name of the bus as a level three heading in doctype:HTML
                current_bus_name = "<H3>" + bus_name + "</H3>"
                # Display the name of the bus
                st.markdown(current_bus_name, unsafe_allow_html=True)

                # Display the corresponding information about the current bus
                bus_name_column_content_set_1 = (
                    "<H6>"
                    + str(bus_operator)
                    + " • "
                    + str(bus_id)
                    + " • "
                    + "Reaches "
                    + str(input_user_destination)
                    + " by "
                    + str(estimated_time_of_arrival_at_user_destination)
                    + " IST</H6>"
                )
                st.markdown(bus_name_column_content_set_1, unsafe_allow_html=True)

                # Segment the crowd level in bus corresponding to the load factor
                if load_factor < 0.5:
                    crowd_status = "Sparsely crowded"
                elif load_factor >= 0.5 and load_factor < 0.8:
                    crowd_status = "Briskly crowded"
                elif load_factor >= 0.8 and load_factor < 1.2:
                    crowd_status = "Lightly crowded"
                elif load_factor >= 1.2 and load_factor < 1.5:
                    crowd_status = "Densely crowded"
                else:
                    crowd_status = "Overcrowded"

                # Check if seats are available in the bus, Else display No
                if available_seats_in_bus <= 0:
                    available_seats_in_bus = "No"

                # Select statement depending on ETA
                if (
                    estimated_time_of_arrival_at_user_boarding_point >= 0
                    and bus_current_location != input_starting_location
                ):
                    bus_name_column_content_set_2 = (
                        "<H6>"
                        + "Arriving in "
                        + str(estimated_time_of_arrival_at_user_boarding_point)
                        + " mins • "
                        + str(crowd_status)
                        + " • "
                        + str(available_seats_in_bus)
                        + " seats available</H6>"
                    )
                elif (
                    estimated_time_of_arrival_at_user_boarding_point < 0
                    and bus_current_location != input_starting_location
                ):
                    bus_name_column_content_set_2 = (
                        "<H6>"
                        + "Arriving in few secs • "
                        + str(crowd_status)
                        + " • "
                        + str(available_seats_in_bus)
                        + " seats available</H6>"
                    )
                else:
                    bus_name_column_content_set_2 = (
                        "<H6>"
                        + "Arrived at "
                        + input_starting_location
                        + " • "
                        + str(crowd_status)
                        + " • "
                        + str(available_seats_in_bus)
                        + " seats available</H6>"
                    )

                # Display the estimated time of arrival, seat count and other details
                st.markdown(bus_name_column_content_set_2, unsafe_allow_html=True)

            with bus_fare_column:
                # Fetch the route id assignjed to the bus
                selected_bus_route_id = retrieve_bus_route_id(bus_id)

                # Calculate the fare from the user's boarding point to dropping point
                bus_fare = BusFareCalculator.bus_fare_calculator(
                    input_starting_location,
                    input_user_destination,
                    bus_type,
                    selected_bus_route_id,
                )

                # Display the bus fare after right aligning to fit the interface
                display_bus_fare = (
                    "<div style='text-align: right;'><H3>Rs "
                    + str(bus_fare)
                    + "</H3></div>"
                )
                st.markdown(display_bus_fare, unsafe_allow_html=True)

                st.text("")
                # Display the button to track the current location of the bus
                display_map_button = st.button(
                    "Track on Map", key=explore_bus_details_button_id
                )

            if display_map_button:
                # Retrieve the current location of the bus
                bus_current_location = retrieve_current_location(bus_id)
                # Display the map using folium on the web application's frontend
                map = BackendService.display_bus_on_map(bus_current_location)
                folium_static(map)

    else:
        # Display prompt to select a boarding point and a dropping point
        st.markdown(
            "<H2>Select a starting point and a destination</H2>", unsafe_allow_html=True
        )


def view_bus_details():
    """
    [CroMa WebApp page 02/03] - Simulates CroMa bus details page on your web browser.

    Function for displaying simulation pages for CroMa's Bus Details page. This tool
    is intended for use by the passenger to look for the details of the selected bus.

    The simulation page incorporates a primary record that facilitates user input of
    the Bus Id. The data is subsequently utilized to fetch the necessary information

    Read more in the :ref:`CroMa - Passenger application`.

    .. versionadded:: 1.3.0

    Parameters:
        None -> Variables are read in real-time from the users as per configruations

    Returns:
        None -> Values are updated inplace or within the firebase RT or SQL database

    .. See Also:
        [1] application_backend (BackendService, BusFareCalculator)
        [2] application_database
        [3] application_support_dictionary

    NOTE: Upcoming update will include using AJAX based methods to reduce load times

    """
    # Apply the CSS styles defined in the parameter file to the sidebar buttons
    apply_style_to_sidebar_button("hardware/style.css")

    # Display a horizontal rule on the sidebar to seprate different sections
    st.sidebar.markdown("---")

    # Enter the bus id of which the details will be displayed
    user_input_bus_id = st.sidebar.selectbox("Enter Bus Id", application_support_dictionary.all_bus_id)

    # Display button to show bus details
    show_bus_details_button = st.sidebar.button("Show Bus Details")

    # Display details only when input bus id is provided by the user
    if user_input_bus_id or show_bus_details_button:
        # Fetch the necessary attributes assosciated with the input bus id
        (
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
        ) = BackendService.fetch_bus_attributes(user_input_bus_id)
        # Display the name of the bus
        st.markdown("<H2>" + bus_name + "</H2>", unsafe_allow_html=True)

        # Segment the first section to three columns with different width size
        col1, col2, col3 = st.columns([1.3, 1.48, 1.9])

        # Corresponding to the load factor, select the bus_crowd status
        if load_factor < 0.5:
            bus_crowd_status = (
                "Not crowded"  # Displayed when almost all seats are available
            )
        elif load_factor >= 0.5 and load_factor < 0.8:
            bus_crowd_status = (
                "Briskly crowded"  # Displayed when there are few people aboard bus
            )
        elif load_factor >= 0.8 and load_factor < 1.2:
            bus_crowd_status = (
                "Lightly crowded"  # Displayed when the bus is lightly filled
            )
        elif load_factor >= 1.2 and load_factor < 1.5:
            bus_crowd_status = "Densely crowded"  # Displayed when bus is full with few passengers standing
        else:
            bus_crowd_status = (
                "Overcrowded"  # Displayed when many passengers are standing
            )

        with col1:
            # Display the crowd status of the bus
            st.markdown(
                "<H5>👨‍👩‍👦 " + bus_crowd_status + "</H5>", unsafe_allow_html=True
            )

        with col2:
            # Display the total delay in the bus's schedule
            if total_delay_in_current_journey > 0:
                st.markdown(
                    "<H5>🕔 Delayed by " + str(total_delay_in_current_journey) + " min</H5>",
                    unsafe_allow_html=True,
                )
            elif total_delay_in_current_journey == 0:
                st.markdown(
                    "<H5>🕔 Bus is on schedule</H5>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<H5>🕔 Early by " + str(abs(total_delay_in_current_journey)) + " min</H5>",
                    unsafe_allow_html=True,
                )

        with col3:
            # Check if there are seats available in the bus
            if available_seats_in_bus < 0:
                # If firebase db holds value less than 0, set the seat count as 0
                available_seats_in_bus_str = 0
            else:
                # Otherwise, keep the count unchanged
                available_seats_in_bus_str = available_seats_in_bus

            # Display the accurate number of available seat count in bus
            st.markdown(
                "<H5>💺 "
                + str(available_seats_in_bus_str)
                + " seats available"
                + "</H5>",
                unsafe_allow_html=True,
            )

        # Customize the top and bottom margin of the horizontal rule
        st.markdown(
            """
            <style>
            .custom-hr {
                margin-top: -10px;
                margin-bottom: -10px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        # Display a custom sized horizontal rule on the main section of the web app
        st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(
            [1, 5, 1]
        )  # Divide the section into three segments

        with col1:
            # Display the starting location of the bus (depends on the assigned route id)
            st.markdown(bus_starting_location, unsafe_allow_html=True)

        with col3:
            # Display the terminal location of the bus (depends on the assigned route id)
            st.markdown(
                """
                <div style="text-align: right;">"""
                + bus_terminal_location
                + """</div>
            """,
                unsafe_allow_html=True,
            )

        # Display the progress bar indicating the percentage of journey completed by the bus
        my_bar = st.progress(int(percentage_journey_completed))

        # Fetch the list of bus stops in the route assigned to the bus id
        stops_in_route = application_support_dictionary.bus_timings.get(bus_route_id)
        # Fetch the pre-determined duration for the bus to reach the previous stop
        time_from_origin_to_reach_bus_last_loc = stops_in_route[bus_current_location]

        # Calculate the time in mins to reach the previous stop
        time_in_mins_to_reach_last_stop = (
            total_delay_in_current_journey + time_from_origin_to_reach_bus_last_loc
        )
        current_time = datetime.now().time()  # determine the current time

        # Fetch the time of arrival of the bus at the previous stop
        time_of_arrival_at_last_stop = retrieve_last_stop_arrival_time(
            user_input_bus_id
        )
        # Parse the datetime object in string frormat
        time_of_arrival_at_last_stop_str = time_of_arrival_at_last_stop.strftime(
            "%H:%M"
        )

        # Calculate the time in mins to reach the next stop, strating from current location of the bus
        time_in_mins_to_reach_next_stop_from_current_stop = (
            stops_in_route[bus_next_location]
            - stops_in_route[bus_current_location]
        )
        # Determine the estimated time of arrival at the next stop
        time_of_arrival_at_next_stop_str = add_minutes_to_time(
            time_of_arrival_at_last_stop_str,
            time_in_mins_to_reach_next_stop_from_current_stop,
        )

        # Display the details corresponding to the current location and the estimated time
        st.write(
            "Bus reached "
            + bus_current_location
            + " at "
            + time_of_arrival_at_last_stop_str
            + " (Updated few secs ago). Next stop is "
            + bus_next_location
            + ". Est. arrival at "
            + str(time_of_arrival_at_next_stop_str)
        )

        # Display status message corresponding to the total delay in the bus journey
        if total_delay_in_current_journey <= 5:
            st.success(
                "This bus is running on time. Please scroll down below to check the complete route guide for this bus."
            )
        elif total_delay_in_current_journey > 5 and total_delay_in_current_journey < 15:
            st.warning(
                "This bus is slightly delayed. Please scroll down below to check the complete route guide for this bus."
            )
        else:
            st.error(
                "Bus is substantialy delayed. Please scroll down below to check the complete route guide for this bus."
            )

        # Display information pertaining to the bus operator and other related information
        st.write(
            "This bus is owned and operated by "
            + bus_operator
            + ". All complaints shall be registered at helpdesk@ksrtc.kerala.gov"
            + " For pre-booking tickets, please visit the official website. For details related to bus timings, visit official site"
        )

        # Customize the top and bottom margin of the horizontal rule
        st.markdown(
            """
            <style>
            .custom-hr2 {
                margin-top: -5px;
                margin-bottom: -5px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<hr class="custom-hr2">', unsafe_allow_html=True
        )  # Display the horizontal rule

        # Display the section heading for Fare calculator
        st.markdown("<H5>Fare Calculator</H5>", unsafe_allow_html=True)

        # Segment th seection into three columns of variable width size
        col_boarding_point, col_dropping_point, col_calculate_button = st.columns(
            [3, 3, 1]
        )
        with col_boarding_point:
            # Select the user's boarding point
            user_input_starting_location_calculate_fare = st.selectbox(
                "Select boarding point",
                ["Select boarding point"] + all_bus_stops_list,
                label_visibility="collapsed",
            )
        with col_dropping_point:
            # Select the user's deboarding point
            user_input_destination_location_calculate_fare = st.selectbox(
                "Select dropping point",
                ["Select dropping point"] + all_bus_stops_list,
                label_visibility="collapsed",
            )

        with col_calculate_button:
            calculate_bus_fare_button = st.button(
                "Calculate"
            )  # Display the button to calculate the fare

        if calculate_bus_fare_button:
            # If both inputs are provided, calculate the total fare payable
            if (
                user_input_starting_location_calculate_fare != "Select boarding point"
                and user_input_destination_location_calculate_fare
                != "Select dropping point"
            ):
                # Fetch the code to calculate the bus fare
                calculated_fare = BusFareCalculator.bus_fare_calculator(
                    user_input_starting_location_calculate_fare,
                    user_input_destination_location_calculate_fare,
                    bus_type,
                    bus_route_id,
                )

                # Display a success status message with total payable fare
                fare_alert = st.success(
                    "The total bus fare from "
                    + user_input_starting_location_calculate_fare
                    + " to "
                    + user_input_destination_location_calculate_fare
                    + " is Rs."
                    + str(calculated_fare),
                    icon="✅",
                )

                time.sleep(3)  # Hold the execution for the next three seconds
                fare_alert.empty()  # Remove the fare alert from the front end of the web app

            elif user_input_starting_location_calculate_fare == "Select boarding point":
                # Display warning message prompting to enter the boarding point
                fare_alert = st.warning("Please enter your boarding point", icon="⚠️")

                time.sleep(3)  # Hold the execution for the next three seconds
                fare_alert.empty()  # Remove the fare alert from the front end of the web app

            elif (
                user_input_destination_location_calculate_fare
                == "Select dropping point"
            ):
                # Display warning message prompting to enter the dropping point
                fare_alert = st.warning("Please enter your dropping point", icon="⚠️")

                time.sleep(3)  # Hold the execution for the next three seconds
                fare_alert.empty()  # Remove the fare alert from the front end of the web app

            else:
                # Display alert indicating there has been some exception in the fare calculation
                fare_alert = st.error(
                    "Oops! We are facing some trouble. Please try again later", icon="🚨"
                )

                time.sleep(3)  # Hold the execution for the next three seconds
                fare_alert.empty()  # Remove the fare alert from the front end of the web app

        # Customize the top and bottom margin of the horizontal rule
        st.markdown(
            """
            <style>
            .custom-hr3 {
                margin-top: -05px;
                margin-bottom: -10px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            '<hr class="custom-hr3">', unsafe_allow_html=True
        )  # Display the horizontal rule

        # Display the section heading for More Information
        st.markdown("<H5>More Information</H5>", unsafe_allow_html=True)

        # initialize the route guide as an empty string
        route_guide_string = ""

        # Create an expander to hold the bus route guide
        with st.expander("Bus Route Guide"):
            # Iterate through all the bus stops in the bus stops list
            for i in range(len(all_bus_stops_list)):
                # Display names of each stop followed by arrow indicating direction of travel
                if (
                    all_bus_stops_list.index(all_bus_stops_list[i])
                    == len(all_bus_stops_list) - 1
                ):
                    route_guide_string = route_guide_string + all_bus_stops_list[i]
                else:
                    route_guide_string = (
                        route_guide_string + all_bus_stops_list[i] + " -> "
                    )

            st.write(
                route_guide_string
            )  # Display the route guide string in the expander

        # Display an expaner to show the current location of the bus
        with st.expander("Track Live Location"):
            # Retrieve the current location of the bus
            bus_current_location = retrieve_current_location(user_input_bus_id)

            # Display the bus's current location on folium map
            map = BackendService.display_bus_on_map(bus_current_location)
            folium_static(map)


def send_bug_report():
    """
    [CroMa WebApp page 03/03] - Sends email containing information about bug reports

    Fuction for sending a bug report mail from the specified sender email address to
    the team. The mail is structured with options to include one or more attachments.

    The send_bug_report() function sends an email containing bug reports submitted by
    users. This function takes in the user's name, e-mail id, and the bug description
    as the input parameters. It then composes an email message using the user's input,
    & sends it to the CroMa team. If sent successfully it'd returns a success message.

    Read more in the :ref:`CroMa - Bug Reports`.

    .. versionadded:: 1.2.0

    Parameters:
        None -> Variables are read in real-time from the users as per configruations

    Returns:
        None -> The bug report is mailed to the support team with any/all attachment

    Warnings:
        invalid_email_address: True if a user enters an invalid email id (ref: mail)

    Alerts:
        bug_report_sent_alert: Alert the users that the bug report has been e-mailed

    NOTE: Upcoming updates will include method to generate bug reports in PDF format
    """
    # Display a markdown title for the bug report  with a bug emoji
    br_full_name_warning = False
    br_email_id_warning = False

    st.markdown("# :ladybug: Send Bug Report")

    # Display a message to users who wish to report a bug
    st.markdown(
        "<p align = 'justify'>If you believe that you have discovered any "
        + "vulnerability in Jasper, please fill in thr form below with a thorough "
        + "explanation of the vulnerability. We will revert back to you after due "
        + "diligence of your bug report</p>",
        unsafe_allow_html=True,
    )
    # Create two columns to hold text input fields
    col1, col2 = st.columns(2)

    # Define context managers to set the current column for the following input fields
    with col1:
        # Create a text input field in the first column to read user's full name
        br_full_name = st.text_input("Full Name:")

    # Check if the length of the full name field is more than one
    if len(br_full_name) < 1:
        st.warning("Full Name is a required field", icon="⚠️")
        br_full_name_warning = True

    # Otherwise don't flag this parameter
    else:
        br_full_name_warning = False

    with col2:
        # Create a text input field in the second column to read user's email id
        br_email_id = st.text_input("E-Mail Id:")

    # Check if the length of the email id field is more than one
    if len(br_email_id) < 1:
        st.warning("E-Mail Id is a required field", icon="⚠️")
        br_email_id_warning = True
    # Otherwise don't flag this parameter

    else:
        br_email_id_warning = False

    # Check if the email id entered is a valid email id
    if br_email_id_warning == False and is_valid_email(br_email_id) == False:
        # If not, display a warning message
        st.warning("Please enter a valid email id", icon="⚠️")
        br_email_id_warning = True
    # Otherwise don't flag this parameter
    else:
        br_email_id_warning = False

    # Create two columns to hold input dropdown fields
    col3, col4 = st.columns(2)

    # Define context managers to set the current column for selectbox input field
    with col3:
        # Create a selectbox input field in the third column to read the bug location
        br_bug_in_page = st.selectbox(
            "Which page is the bug in?", croma_applications_page_list
        )

    # Tuple of strings that represent different types of bugs for users to select from
    bug_types = (
        "General Bug/Error",
        "Access Token/API Key Disclosure",
        "Memory Corruption",
        "Database Injection",
        "Code Execution",
        "Denial of Service",
        "Privacy/Authorization",
    )

    # Define context managers to set the current column for selectbox input field
    with col4:
        # Create a selectbox input field in the fourth column to read the bug type
        br_bug_type = st.selectbox("What type of bug is it?", bug_types)

    # Create a text area where users can describe the bug and steps to reproduce it
    br_bug_description = st.text_area(
        "Describe the issue in detail (include steps to reproduce the issue):"
    )

    # Widget to upload relevant attachments, such as screenshots, charts, and reports.
    # The file uploader widget is set to accept multiple files (limit: 200mb per file)
    br_uploaded_files = st.file_uploader(
        "Include any relevant attachments such as screenshots, or reports:",
        accept_multiple_files=True,
    )

    # Checkbox that user must check to indicate that they accept terms & conditions
    bug_report_terms_and_conditions = st.checkbox(
        "I accept the terms and conditions and I consent to be contacted in future by "
        + "the CroMa support team"
    )

    # If any flag is raised corresponding to invalid inputs, set the isDisabled flag
    isDisabled = (
        br_email_id_warning
        or br_full_name_warning
        or (not bug_report_terms_and_conditions)
    )

    # Create a button that the users can click to send the bug reports to the CroMa team
    # Disabled argument enables the button only if the user has checked the T&C checkbox
    if st.button("Send Bug Report", disabled=isDisabled):
        # Call send_bug_report_mail method of the BugReportMail object to send the mail
        BugReportMail.send_bug_report_mail(
            br_full_name,
            br_email_id,
            br_bug_in_page,
            br_bug_type,
            br_bug_description,
            br_uploaded_files,
        )

        # Displays a success message to user indicating that their report has been sent
        bug_report_sent_alert = st.success("Your bug report has been sent!", icon="✅")

        time.sleep(3)  # Hold the execution for the next three seconds
        bug_report_sent_alert.empty()  #  Clear the bug_report_sent_alert from the frontend

    # Create an expander to display the FAQs regarding bug reports in the sidebar
    faq_expander = st.sidebar.expander("Frequently Asked Questions", True)

    # Display the various frequently asked questions in the sidebar expander
    faq_expander.write(
        "Q: Do you offer any kind of bug bounty?\nA: No, we do not offer any bug bounties."
    )  # FAQ Question 1
    faq_expander.write(
        "Q: How long does it takes to hear back?\nA: You'll hear back from us within 3 days."
    )  # FAQ Question 2
    faq_expander.write(
        "Q: Can we share our reports with others?\nA: We expect you don't share any report."
    )  # FAQ Question 3

    # Add some empty lines to the sidebar to place the button on the bottom section
    for _ in range(16):
        st.sidebar.write("\n\n")

    # Apply the CSS styles defined in the parameter file to the sidebar buttons
    apply_style_to_sidebar_button("hardware/style.css")

    # Create a button to redirect to CroMa's social media handles
    # NOTE: Streamlit is still implementing redirection features. This is only a workaround.
    if st.sidebar.button("Join our Community Handle"):
        # Open a new window/tab on user's default web browser
        javascript = "window.open('https://www.streamlit.io/')"

        # Trigger the JavaScript code when it fails to load an image
        html = f"img src onerror={javascript}"

        div = Div(text=html)  # Create a bokeh div with HTML
        st.bokeh_chart(
            div
        )  # Display the div object as a Bokeh chart in the Streamlit app

        # On succesfully opening the tab, display a success message
        st.sidebar.success("Redirecting you to community handle")


# Create a dictionary of different pages of thew web app, along with their corresponding functions
croma_applications_page_list = {
    "User Application": croma_application_playground,
    "View Bus Info": view_bus_details,
    "Send Bug Report": send_bug_report,
}

# Create a dropdown menu for selecting a page from the croma_applications_page_list, passing the dictionary key
selected_page = st.sidebar.selectbox(
    "Navigate Within Pages:", croma_applications_page_list.keys()
)

croma_applications_page_list[
    selected_page
]()  # Call function corresponding to the page keeping key as an index
