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
It contains methods for printing tickets, managing passenger's data and includes
several options for performing conductor book-keeping & data-tracking operations.

Included Functions:
    [1] apply_style_to_sidebar_button
    [2] generate_ticket_id
    [3] calculate_time_difference
    [4] refresh_real_time_database
    [5] print_ticket
    [6] generate_dsr_report

.. versionadded:: 1.2.0
.. versionupdated:: 1.3.0

Read more about the functionality of hardware in :ref:`CroMa - Ticketing Machine`
"""

import random
import time
import streamlit as st
import pandas as pd
import re
import subprocess

import datetime
from datetime import datetime

from database import firebase_database
from database import cassandra_database

from hardware import generate_report
from hardware import send_mail
from hardware import terminal
from hardware.data import bus_fares
from hardware import application_support_dictionary

import firebase_admin
from firebase_admin import credentials


# Set the title and favicon for the streamlit web application
st.set_page_config(
    page_title="CroMa - Ticketing Machine Simulator",
    page_icon="assets/favicon/croma-favicon.jpg",
)

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

# Fixed minimum fare amount to be charged from passengers onboarding the bus
FIXED_TICKET_PRICE = bus_fares.FIXED_TICKET_PRICE
# Additional fare over and above the fixed ticket price charged based on distance
VARIABLE_TICKET_PRICE = bus_fares.VARIABLE_TICKET_PRICE

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


def apply_style_to_sidebar_button(file_name):
    """
    Function to apply CSS style specified in the parameter to the sidebar button.

    The function takes a CSS file as a parameter and applies the customized style
    to all the buttons widgets on the sidebar of the croma_hw_playground web page

    Read more in the :ref:`Styling the CroMa Web Application`.

    .. versionadded:: 1.2.0

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


def generate_ticket_id():
    """
    Function to display the bus details, route details and trip configurations.

    The ticket id is an eight charecter long string consisting of a combination
    of alphabets & numbers. This id is unique for each passenger aboard the bus

    .. versionadded:: 1.2.0

    Parameters:
        None -> Variables are read from the system memory as per configruations

    Returns:
        [str] ticket_id: 8 charecters long sequence to uniquely identify ticket

    NOTE: In the upcoming versions, this will be useful for bus-keeping records.

    """
    length = 4  # Set the length for the subsets of ticket_id
    alphabets = "QWERTYUIOPASDFGHJKLZXCVBNM"  # String containing all upper case letters
    numbers = "1234567890"  # String containing all numbers from 0 to 9

    # Generate a four charecter long random sequence of alphabets
    result1 = "".join((random.choice(alphabets)) for x in range(length))
    # Generate a four charecter long random sequence of numbers
    result2 = "".join((random.choice(numbers)) for x in range(length))

    # Coalesce the sub id's to generate an eight charecter long ticket_id
    ticket_id = result1 + result2
    return ticket_id  # Return the unique ticket id to be printed in the ticket


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


def refresh_real_time_database(bus_id, bus_stops):
    """
    Function to update the firebase database with node=bus_id with real-time values.

    Passenger count at any instance is the sum of all elements in the crowd manager.
    Available seats are calculated by subtracting passengers count from total seats.
    Load factor is calculated as the ratio of total passengers to the seat capacity.

    .. versionadded:: 1.2.0
    ..versionupdated:: 1.3.0

    Parameters:
        [str] bus_id: Bus id of the selected bus
        [list] bus_stops: The list of bus stops in the selected route

    Returns:
        None -> Values are updated in the given bus's firebase real-time database

    NOTE: At no instance can sum of the crowd manager be any value, other than zero.

    """
    # Encode the current location to it's assosciated key value
    int_current_location = bus_stops.index(current_location) + 1

    # Calculate the total number of passengers aboard the bus at the given instance
    terminal.total_passengers = sum(terminal.crowd_manager[:int_current_location])

    # Update the total passenger count in the firebase real-time database
    firebase_database.update_passengers_count(bus_id, terminal.total_passengers)

    terminal.available_seat_count = firebase_database.retrieve_available_seats(bus_id)
    # Calculate available seats by subtracting passenger count from available seats
    terminal.available_seat_count = (
        terminal.available_seat_count - terminal.passenger_count
    )

    # Update the available seat count in the firebase real-time database
    firebase_database.update_available_seats(bus_id, terminal.available_seat_count)

    # Calculate the load factor at the given instace and update the load factor list
    terminal.load_factor = terminal.total_passengers / terminal.BUS_MAX_CAPACITY
    terminal.load_factor_list.append(terminal.load_factor)


def print_ticket(
    user_starting_point,
    user_destination,
    passenger_count,
    bus_id,
    bus_stops,
    is_subsidy,
):
    """
    Function to print ticket based on inputs from the user.

    The total fare is calculated based on the passenger's onboarding location, their
    destination and co-passengers count. The function supports both single and round
    trip fare calculation. Multiple KPI's are also updated for admin level analytics

    Read more in the :ref:`Fare calculation`.

    .. versionadded:: 1.2.0
    ..versionupdated:: 1.3.0

    Parameters:
        [int] user_starting_point: The onboarding location of the passenger
        [int] user_destination: The destination location of the passenger
        [int] passenger_count: The total number of co-passengers boarding together
        [str] bus_id: Bus id of the selected bus
        [list] bus_stops: The list of bus stops in the selected route
        [bool] is_subsidy: Indicates whether user has an active subsidy

    Returns:
        [int] total_ticket_fare: The total bus fare, inclusive of all co-passengers

    .. See Also:
        refresh_real_time_database()

    NOTE: The upcoming update will include saving the printed tickets into a folder

    """
    terminal.passenger_count = passenger_count  # Set passenger count

    # Check if passengers are offered any subsidy, if yes don't charge any fare
    if is_subsidy == True:
        total_ticket_fare = 0

    else:
        # dynamic_cost_multiplier shows no. of stops after which costs increases
        dynamic_cost_multiplier = 3  # The cost is set to increase after 3 stops
        # routeway_stop_count gives no. of stops between origin, and destination
        routeway_stop_count = abs(user_destination - user_starting_point)
        # divide routeway_stop_count / dynamic_cost_multiplier to get cost epoch
        variable_ticket_price_epochs = int(
            routeway_stop_count / dynamic_cost_multiplier
        )  # Variable price increases by an amount for every fixed number of stops

        # Total fare is calculated by adding variable price to the fixed price
        total_ticket_fare = (
            FIXED_TICKET_PRICE + (variable_ticket_price_epochs * VARIABLE_TICKET_PRICE)
        ) * terminal.passenger_count

    # Update the total fare collections by calculating value of each ticket
    terminal.collection = terminal.collection + total_ticket_fare

    # Increment crowd manager to include passengers who onboarded at the stop
    terminal.crowd_manager[user_starting_point - 1] += terminal.passenger_count
    # Decrement crowd manager to remove passengers who deboarded at the stop
    terminal.crowd_manager[user_destination - 1] -= terminal.passenger_count

    # Update the total_tickets_printed to reflect total number of tickets printed
    terminal.total_tickets_printed = terminal.total_tickets_printed + 1

    # Update the boarding tracker and the deboarding tracker with passenger count
    terminal.boarding_tracker[user_starting_point - 1] += terminal.passenger_count
    terminal.deboarding_tracker[user_destination - 1] += terminal.passenger_count

    # Update the value of crowd manager each time new tickets are printed
    terminal.passengers_per_trip = (
        terminal.passengers_per_trip + terminal.passenger_count
    )

    # Revise the firebase datbase to reflect real time values for the parameters
    refresh_real_time_database(bus_id, bus_stops)
    terminal.passenger_count = 0  # Refresh passenger_count's value in terminal

    return total_ticket_fare  # Return the payable ticket fare for the passenger


def generate_dsr_report(bus_id, route_id):
    """
    Function to generate the daily status report for the current trip of the bus.

    The daily status report consolidates the information pertaining to the entire
    trip into a single document. This document can then be sent to the admin team
    or analytics team for exploratory data analytics (EDA) and business analytics

    Read more in the :ref:`CroMa Daily Status Report`.

    .. versionadded:: 1.2.0
    ..versionupdated:: 1.3.0

    Parameters:
        [str] bus_id: Bus id of the elected bus
        [str] route_id: Route Id assigned to the bus

    Returns:
        None -> DSR Report is generated and saved within the reports subdirectory

    NOTE: DSR report may contain sensitive data regarding the trip, bus and other
    custom variable and it is recommended to encrypt/password protect this report
    """
    # Create an object dsr_report_pdf of the DSRReport class and create a new page
    dsr_report_pdf = generate_report.DSRReport(orientation="P", unit="mm", format="A4")
    dsr_report_pdf.add_page()

    # Run off the header section and print the basic details about the trip
    dsr_report_pdf.logo_header()
    dsr_report_pdf.print_basic_details(bus_id, route_id)

    # Preprint the data frame table and enter the values corresponding to the headers
    dsr_report_pdf.create_table()
    dsr_report_pdf.print_table_content()

    # Print the date and emboss the signature of the cluster manager/administrator
    dsr_report_pdf.print_signature_and_date()

    # Save the DSR report to the reports directory in the portable document format
    terminal.report_location = "hardware/reports/DSR_Report.pdf"
    dsr_report_pdf.output(terminal.report_location, "F")


# Apply the CSS styles defined in the parameter file to the sidebar buttons
apply_style_to_sidebar_button("hardware/style.css")

# Select the Bus Id to initialize the ticketing machine
bus_id = st.sidebar.selectbox(
    "Enter the Bus Id", ["Select Bus Id"] + application_support_dictionary.all_bus_id
)
# Enter the route Id to fetch the route related information
route_id = st.sidebar.selectbox(
    "Select the route",
    ["Select Route Id"] + list(application_support_dictionary.all_routes.keys()),
)

# Run only when both bus id and route id have been selected
if (
    terminal.initialize_firebase_sdk_ticketing_machine < 1
    and route_id != "Select Route Id"
    and bus_id != "Select Bus Id"
):
    try:
        # Initialize the app with a service account, granting admin privileges
        cred = credentials.Certificate("hardware/adminsdk.json")
        firebase_admin.initialize_app(
            cred, {"databaseURL": "https://technoholic-407a3.firebaseio.com/"}
        )

        # Initialize the database with default values to clear any inconsistency
        firebase_database.initialize_database(bus_id, route_id)
        # Increment counter to ensure the db isn't initialized again during trip
        terminal.initialize_firebase_sdk_ticketing_machine = (
            terminal.initialize_firebase_sdk_ticketing_machine + 1
        )

    except:
        pass  # Don't take any action if firebase authorization throws exception

# Display the ticketing machine interface only if bus id & route id are selected
if route_id != "Select Route Id" and bus_id != "Select Bus Id":
    # Fetch the list of bus stops in the selected route
    bus_stops = application_support_dictionary.all_routes[route_id]

    # """ NEEDS TO CHECK IF UPDATION CAN BE AVOIDED AGAINST DB INITALIZATION """
    # Initialize the firebase database with current route id and bus status
    firebase_database.update_current_route_id(bus_id, route_id)
    firebase_database.update_current_bus_status(bus_id, "Active")

    # Update necessary attributes with values retrieved from firebase database
    current_location = firebase_database.retrieve_current_location(bus_id)
    available_seat_count = firebase_database.retrieve_available_seats(bus_id)
    total_passengers = firebase_database.retrieve_passengers_count(bus_id)

    # Display title on the streamlit web application
    st.title(":oncoming_bus: Ticketing Machine Playground")

    # Display dropdowns for selecting the starting and destination locations
    starting_location = st.selectbox("Select the Starting Location:", bus_stops)
    destination_location = st.selectbox("Select Destination Location:", bus_stops)

    # Check if the starting location and destination locations are the same
    if starting_location == destination_location:
        # Display warning and set same_starting_and_destination_location to True
        st.warning("Starting location can not be same as destination", icon="⚠️")
        flag_bus_user_location_mismatch = True

    # Check if the current location is behind user's boarding point
    elif current_location < starting_location:
        # Display warning and set same_starting_and_destination_location to True
        st.warning(
            "The boarding point cannot be ahead of bus's current location", icon="⚠️"
        )
        flag_bus_user_location_mismatch = True

    # Set same_starting_and_destination_location flag to False if not same
    else:
        flag_bus_user_location_mismatch = False

    # Fetch numerical value corresponding to the current location
    bus_current_location = bus_stops.index(current_location) + 1
    # Fetch numerical value corresponding to user's boarding point
    user_starting_point = bus_stops.index(starting_location) + 1
    # Fetch numerical value corresponding to user's dropping point
    user_destination = bus_stops.index(destination_location) + 1

    # Determine if the bus has already passed the user-provided destination
    if bus_current_location > user_destination:
        # Set the warning & flag indicating destination to be behind current location
        st.warning("The bus has already crossed the selected destination", icon="⚠️")
        flag_destination_behind_current_location = True

    # Set the destination_behind_current_location attribute to False if not behind
    else:
        flag_destination_behind_current_location = False

    if user_starting_point > user_destination:
        # Set the warning & flag indicating destination to be behind current location
        st.warning("The destination cannot be behind the boarding point", icon="⚠️")
        flag_destination_behind_boarding_point = True

    # Set the destination_behind_current_location attribute to False if not behind
    else:
        flag_destination_behind_boarding_point = False

    # Define user input field for passenger count, with limits and default value
    passenger_count = st.number_input(
        "Enter Number of Passengers:", min_value=1, max_value=10, value=1
    )
    int_passenger_count = int(passenger_count)  # Cast passenger_count to integer

    # Display checkbox to indicate if the ticket is to be offered under free subsidy
    subsidy_checkbox = st.checkbox(
        "Check if passenger is a subsidy card holder. Tickets without a fare shall be issued to such passengers "
    )

    # Define is_disabled based on location relative to bus route
    is_disabled = (
        flag_destination_behind_current_location
        or flag_bus_user_location_mismatch
        or flag_destination_behind_boarding_point
    )  # Returns True if any warning is flagged, else returns False

    # Prompt the user to print tickets if no warning flags are marked True
    col_button_print_ticket, col_button_end_trip_and_refresh_database = st.columns(
        [1, 4]
    )

    # Display button to generate a new ticket
    with col_button_print_ticket:
        button_print_ticket = st.button("Generate Ticket", disabled=is_disabled)

    if button_print_ticket:
        # Call the print_ticket function to return the bus fare as per input
        ticket_price = print_ticket(
            user_starting_point,
            user_destination,
            int_passenger_count,
            bus_id,
            bus_stops,
            subsidy_checkbox,
        )

        ticket_id = generate_ticket_id()  # Generate a unique ticket id

        # Display a success status message connoting a ticket to be printed
        if int_passenger_count > 1:
            ticket_printed_alert = st.success(
                "**TICKET BOOKED** | Ticket No.: "
                + ticket_id
                + "  \n"
                + str(int_passenger_count)
                + " tickets booked from "
                + starting_location
                + " to "
                + destination_location
                + " | "
                + "Net Payable = "
                + str(ticket_price)
            )

        # Display a success status message connoting multiple tickets to be printed
        else:
            ticket_printed_alert = st.success(
                "**TICKET BOOKED** | Ticket No.: "
                + ticket_id
                + "  \n"
                + str(int_passenger_count)
                + " ticket booked from "
                + starting_location
                + " to "
                + destination_location
                + " | "
                + "Net Payable = "
                + str(ticket_price)
            )

        # Display the success status message for five seconds before clearing it
        time.sleep(5)
        ticket_printed_alert.empty()

    # Display a horizontal rule on the sidebar to seprate different sections
    st.sidebar.markdown("---", unsafe_allow_html=True)

    # Display dropdown for selecting the new current location
    new_location = st.sidebar.selectbox("Select Current Location:", bus_stops)

    # Update the current_location when the Update Location button is clicked
    if st.sidebar.button("Update Location"):
        # Set the new location on the current location terminal object
        stops_in_route = application_support_dictionary.bus_timings.get(route_id)
        # Fetch pre-determined time to reach bus's last location from the origin
        expected_time_from_origin_to_reach_bus_last_loc = stops_in_route[
            current_location
        ]

        # Fetch the time of arrival of the bus at the last stop from firebase db
        last_stop_arrival_time = firebase_database.retrieve_last_stop_arrival_time(
            bus_id
        )

        current_location = new_location  # Set new location as current location
        current_stop_arrival_time = datetime.now()  # Determine the current datetime

        # Calculate the time in mins to reach the next bus stop from last bus stop
        mins_to_reach_new_location_from_last_location = calculate_time_difference(
            current_stop_arrival_time.strftime("%H:%M"),
            last_stop_arrival_time.strftime("%H:%M"),
        )

        # Fetch pre-determined time to reach bus's current location from the origin
        expected_time_from_origin_to_reach_bus_current_loc = stops_in_route[
            current_location
        ]
        # Calculate expected time in mins to reach current location from last stop
        expected_mins_to_reach_new_loc_from_last_loc = (
            expected_time_from_origin_to_reach_bus_current_loc
            - expected_time_from_origin_to_reach_bus_last_loc
        )

        # Calculate total delay in journey, negative delay indicates arrival before time
        delay = (
            mins_to_reach_new_location_from_last_location
            - expected_mins_to_reach_new_loc_from_last_loc
            + firebase_database.retrieve_bus_total_delay(bus_id)
        )

        # Update the total delay and last stop arrival time in firebase database
        firebase_database.update_bus_total_delay(bus_id, delay)
        firebase_database.update_last_stop_arrival_time(
            bus_id, current_stop_arrival_time
        )

        # Update the current location in the firebase real-time database
        firebase_database.update_current_location(bus_id, new_location)

        # Display success message indicating the current location has been upodated
        location_updated_alert = st.sidebar.success(
            ":white_check_mark: Location Updated"
        )

        time.sleep(3)  # Wait for three seconds
        location_updated_alert.empty()  # Clear the location_updated_alert

        # Retrive the current passenger count from the firebase real-time database
        quondam_passenger_count = firebase_database.retrieve_passengers_count(bus_id)
        # Get number correponding to current location from the bus_stops dataframe
        int_current_location = bus_stops.index(current_location) + 1

        # Calculate total passengers aboard the bus at the current location
        total_passengers = sum(terminal.crowd_manager[:int_current_location])

        firebase_database.update_passengers_count(
            bus_id, total_passengers
        )  # Update the passenger count in the database

        # Retrieve the number of currently available seats from the database
        available_seat_count = firebase_database.retrieve_available_seats(bus_id)

        # Calculate available seat by subtracting passenger count from available seats
        available_seat_count = (
            available_seat_count + quondam_passenger_count - total_passengers
        )

        # Update the available seat count in the firebase real-time database
        firebase_database.update_available_seats(bus_id, available_seat_count)

    st.sidebar.markdown("---", unsafe_allow_html=True)  # Display horizontal rule

    # Create an expander to preview the real-time databse values in the sidebar
    expander = st.sidebar.expander("Database Preview")

    # Execute the following code when End Trip and Refresh Database button is clicked
    with col_button_end_trip_and_refresh_database:
        button_end_trip_and_refresh_database = st.button(
            "End Trip and Refresh Database"
        )

    if button_end_trip_and_refresh_database:
        # Display an info message indicating that the current trip has been terminated
        trip_terminated_alert = st.info("Current trip has been terminated", icon="ℹ️")

        # Compute and update the overall load factor for the current trip
        try:
            terminal.load_factor = sum(terminal.load_factor_list) / len(
                terminal.load_factor_list
            )
        except:
            terminal.load_factor = 0  # Set load factor as 0 on ZeroDivisionException

        # Inspect the boarding_tracker to find the stop with maximum onboards
        if sum(terminal.boarding_tracker) == 0:
            terminal.MAX_BOARDING_BUS_STOP = "Unavailable"  # Set as unavailable
        else:
            max_boarding = int(
                terminal.boarding_tracker.index(max(terminal.boarding_tracker))
            )
            # Save the bus stop's name from where maximum passengers onbaorded
            terminal.MAX_BOARDING_BUS_STOP = bus_stops[max_boarding]

        # Inspect the deboarding_tracker to find the stop with maximum deboards
        if sum(terminal.deboarding_tracker) == 0:
            terminal.MAX_DEBOARDING_BUS_STOP = "Unavailable"  # Set as unavailable
        else:
            max_deboarding = int(
                terminal.deboarding_tracker.index(max(terminal.deboarding_tracker))
            )
            # Save the bus stop's name where maximum number of passengers debaorded
            terminal.MAX_DEBOARDING_BUS_STOP = bus_stops[max_deboarding]

        # Generate the Daily Status Report (DSR) and displays a success alert
        generate_dsr_report(bus_id, route_id)
        trip_terminated_alert.empty()  # Clear the trip_terminated_alert

        # Display an alert when the DSR report is generated
        dsr_report_generated_alert = st.success(
            "DSR Report has been generated", icon="ℹ️"
        )
        # Create mail object consonant to the DSRMail class in hardware sub-directory
        mail = send_mail.DSRMail()

        # Send an email containing DSR and display info message on sidebar
        mail.send_dsr_mail(bus_id)
        dsr_report_generated_alert.empty()  # Clear dsr_report_generated_alert

        # Dislay info message when email with attachment has been delivered
        dsr_mail_sent_alert = st.info("DSR Report has been emailed", icon="ℹ️")

        time.sleep(3)  # Wait for three seconds
        dsr_mail_sent_alert.empty()  # Clear the dsr_mail_sent_alert

        firebase_database.refresh_database(
            bus_id
        )  # Refresh the database with the default values

        terminal.collection = terminal.load_factor = 0  # Reset colection & load_factor

        # Reset crowd manager, boarding tracker and deboarding tracker to defaults
        terminal.crowd_manager = (
            terminal.boarding_tracker
        ) = terminal.deboarding_tracker = [0] * 20

        # Retrive the default current location from the firebase real-time database
        current_location = firebase_database.retrieve_current_location(bus_id)
        # Retrive the default available seat count from the firebase real-time database
        available_seat_count = firebase_database.retrieve_available_seats(bus_id)
        # Retrive the default total passenger from the firebase real-time database
        total_passengers = firebase_database.retrieve_passengers_count(bus_id)

        terminal.initialize_firebase_sdk_ticketing_machine = (
            2  # Set the count value to any value higher than 1
        )

    # Display the total number of passengers at that instance in the expander
    expander.markdown(
        "**:male-office-worker: Passenger Count:**" + " " + str(total_passengers)
    )

    # Display the bus's current location at the given instance in the expander
    expander.markdown("**:world_map: Current Location:**" + " " + str(current_location))

    # Display the total collection at the given instance in the expander
    expander.markdown(
        "**:moneybag: Total Collections:** Rs." + " " + str(terminal.collection)
    )

    # Display the available seat count at the given instance in the expander
    expander.markdown("**:seat: Seats Available:**" + " " + str(available_seat_count))

    # Display the selected route of the bus in the expander
    expander.markdown(
        "**:bus: Route:**" + " " + str(bus_stops[0]) + " - " + str(bus_stops[-1])
    )

    # Display the button to launch the user application's demo
    if st.sidebar.button("Launch User Application Demo"):
        subprocess.Popen(["streamlit", "run", "application_main.py"])  # Launch user app

else:
    # Display a markdown title for the about section with an emoji
    st.markdown("## Say Hello to CroMa :dart:")

    # Display a paragraph with basic information about CroMa and it's features
    st.markdown(
        "<p align = 'justify'>CroMa is a firmware solution that brings you real-time information "
        + "about public buses, including tracking, arrival times, crowd leves and seat availability. "
        + "It's uses combination of a handheld ticketing machine and a user-friendly mobile app. With "
        + "CroMa, you can compare multiple transit options and make an informed decision. With CroMa, "
        + "simply say say good bye to uncertainties & enjoy a smoother commuting experience</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p align = 'justify'>Started in April 2022 as a capstone project, this development is now "
        + "licensed under CC-BY-NC-ND. Rest assured, no personal data is collected and several stringent "
        + "security policies are in place to protect all data</p>",
        unsafe_allow_html=True,
    )

    # Display a markdown title for the about section with an emoji
    st.markdown("## How CroMa Works? :bus:")

    # Display paragraph with information about ticketing machine and real-time database
    st.markdown(
        "<p align = 'justify'>A handheld ticketing machine, powered by a micro-controller, generates "
        + "tickets, collects the necessary data, and generates reports. Conductors "
        + "use this device to issue tickets and gather passenger details like boarding point and "
        + "dropping point. All the data is seamlessly transmitted to a Firebase real-time database</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p align = 'justify'>In the database, passenger information is stored as a JSON tree, with "
        + "each bus having its own unique ID. Data such as available seats and current location are updated "
        + "in real-time. Whenever a new ticket is issued or a passenger disembark, data is automatically "
        + "updated. SQL database is used to fetch the pre-fixed data</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p align = 'justify'>CroMa passenger application is the go-to tool for transit planning. User's "
        + "can simply enter their boarding point and destination. The app instantly retrieves real-time buses "
        + "within the user's specified radius. Simply select a bus to view "
        + "more details like its ETA, seat availability, and much more. "
        + "No login is required!</p>",
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("---")

    # Add an input box for the user to enter their email ID
    newsletter_subscriber_email = st.sidebar.text_input(
        "Subscribe to receive our newsletter", placeholder="Enter your Email Id"
    )

    if (
        is_valid_email(newsletter_subscriber_email) is False
        and len(newsletter_subscriber_email) > 0
    ):
        st.sidebar.warning("Please enter a valid e-mail id", icon="⚠️")

    # Apply the CSS styles defined in the parameter file to the sidebar buttons
    apply_style_to_sidebar_button("hardware/style.css")

    # Add a button for the user to subscribe to the newsletter
    newsletter_mailing_list_user_email_id = st.sidebar.button(
        "Subscribe to our Newsletter",
        disabled=not (is_valid_email(newsletter_subscriber_email)),
    )

    if newsletter_mailing_list_user_email_id:
        store_subscriber_email = (
            cassandra_database.store_newsletter_subscriber_data_cassandra(
                newsletter_subscriber_email
            )
        )

        if store_subscriber_email == "SUCCESS":
            # Display a success message when user subscribes to receive our newsletters
            newsletter_subscribed_alert = st.sidebar.success(
                "You have subscribed to newsletter", icon="✅"
            )

            time.sleep(3)  # Hold the execution for the next three seconds
            newsletter_subscribed_alert.empty()  # Clear the newsletter_subscribed_alert from the UI
        else:
            # Display a success message when user subscribes to receive our newsletters
            newsletter_subscribed_alert = st.sidebar.error(
                "Could not connect to the database", icon="🚨"
            )

            time.sleep(3)  # Hold the execution for the next three seconds
            newsletter_subscribed_alert.empty()  # Clear the newsletter_subscribed_alert from the UI

    # Display the button to launch the user application's demo
    for _ in range(7):
        st.sidebar.write(" ")

    if st.sidebar.button("Launch User Application Demo"):
        subprocess.Popen(["streamlit", "run", "application_main.py"])  # Launch user app
