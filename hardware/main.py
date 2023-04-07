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
    [1] refresh_real_time_database
    [2] print_ticket
    [3] generate_ticket_id
    [4] generate_dsr_report

.. versionadded:: 1.2.0

Read more about the functionality of the hardware in :ref:`CroMa Hardware Design`
"""

import random
import time
import streamlit as st
import pandas as pd

import terminal
import generate_report
import send_mail

import firebase_admin
from firebase_admin import credentials
from streamlit_star_rating import st_star_rating
from bokeh.models.widgets import Div

import database


# Minimum fare charged per ticket from a passenger boarding the bus
FIXED_TICKET_PRICE = 10
# Additional fare over and above the fixed ticket price based on distance
VARIABLE_TICKET_PRICE = 6

# Fetch the firebase service account key JSON file
cred = credentials.Certificate("hardware/adminsdk.json")
terminal.count = terminal.count + 1

# Initialize the app with a service account, granting admin privileges
if terminal.count <= 1:
    firebase_admin.initialize_app(
        cred, {"databaseURL": "https://technoholic-407a3.firebaseio.com/"}
    )

# Set the title and favicon for the streamlit web application
st.set_page_config(
    page_title="CroMa - Ticketing Machine",
    page_icon="hardware/assets/croma-favicon.png",
)

# Hide the streamlit menu and default footer from the app's front-end
HIDE_MENU_STYLE = """
<style>
#MainMenu  {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(HIDE_MENU_STYLE, unsafe_allow_html=True)  # Allow HTML tags in mkd

# Read the details of bus stops from the data folder for the selected route
bus_stops = pd.read_csv("hardware/data/bus_stops.csv")


def refresh_real_time_database():
    """
    Function to update the firebase database with node=bus_id with real-time values.

    Passenger count at any instance is the sum of all elements in the crowd manager.
    Available seats are calculated by subtracting passengers count from total seats.
    Load factor is calculated as the ratio of total passengers to the seat capacity.

    .. versionadded:: 1.2.0

    Parameters:
        None -> Variables are read in real-time from the users as per configruations

    Returns:
        None -> Values are updated in the gicen bus's firebase real-time database

    NOTE:
        At no instance can the sum of the crowd manager be a value, other than zero.

    """
    # Encode the current location to it's assosciated key value
    int_current_location = bus_stops.loc[
        bus_stops["Name"] == terminal.current_location, "Number"
    ].item()

    # Calculate the total number of passengers aboard the bus at the given instance
    terminal.total_passengers = sum(terminal.crowd_manager[:int_current_location])

    # Update the total passenger count in the firebase real-time database
    database.update_passengers_count()

    terminal.available_seat_count = database.retrieve_available_seats()
    # Calculate available seats by subtracting passenger count from available seats
    terminal.available_seat_count = (
        terminal.available_seat_count - terminal.passenger_count
    )

    # Update the available seat count in the firebase real-time database
    database.update_available_seats()

    # Calculate the load factor at the given instace and update the load factor list
    terminal.load_factor = terminal.total_passengers / terminal.BUS_MAX_CAPACITY
    terminal.load_factor_list.append(terminal.load_factor)


def print_ticket(user_starting_point, user_destination, passenger_count):
    """
    Function to print ticket based on inputs from the user.

    The total fare is calculated based on the passenger's onboarding location, their
    destination and co-passengers count. The function supports both single and round
    trip fare calculation. Multiple KPI's are also updated for admin level analytics

    Read more in the :ref:`User Installation and Working`.

    .. versionadded:: 1.2.0

    Parameters:
        [int] user_starting_point: The onboarding location of the passenger
        [int] user_destination: The destination location of the passenger
        [int] passenger_count: The total number of co-passengers boarding together

    Returns:
        [int] total_ticket_fare: The total bus fare, inclusive of all co-passengers

    .. See Also:
        refresh_real_time_database()

    NOTE: The upcoming update will include saving the printed tickets into a folder

    """
    terminal.passenger_count = passenger_count  # Set passenger count

    # dynamic_cost_multiplier shows no. of stops after which costs increases
    dynamic_cost_multiplier = 3  # the cost is set to increase after 3 stops

    # routeway_stop_count gives no. of stops between origin, and destination
    routeway_stop_count = abs(user_destination - user_starting_point)

    # divide routeway_stop_count / dynamic_cost_multiplier to get cost epoch
    variable_ticket_price_epochs = int(routeway_stop_count / dynamic_cost_multiplier)

    # Total fare is calculated by adding variable price to the fixed price
    # Variable price increases by an amount for every fixed number of stops
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
    refresh_real_time_database()
    terminal.passenger_count = 0  # Refresh passenger_count's value in terminal

    return total_ticket_fare  # Return the payable ticket fare for the passenger


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


def generate_dsr_report():
    """
    Function to generate the daily status report for the current trip of the bus.

    The daily status report consolidates the information pertaining to the entire
    trip into a single document. This document can then be sent to the admin team
    or analytics team for exploratory data analytics (EDA) and business analytics

    Read more in the :ref:`CroMa Daily Status Report`.

    .. versionadded:: 1.2.0

    Parameters:
        None -> Variables are read in real-time from users as per configruations

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
    dsr_report_pdf.print_basic_details()

    # Preprint the data frame table and enter the values corresponding to the headers
    dsr_report_pdf.create_table()
    dsr_report_pdf.print_table_content()

    # Print the date and emboss the signature of the cluster manager/administrator
    dsr_report_pdf.print_signature_and_date()

    # Save the DSR report to the reports directory in the portable document format
    terminal.report_location = "hardware/reports/DSR_Report.pdf"
    dsr_report_pdf.output(terminal.report_location, "F")


def croma_hw_playground():  # pylint: disable=too-many-locals,too-many-statements
    """
    [CroMa WebApp page 01/03] - Simulate CroMa ticketing machine on your web browser

    Function for displaying simulation page for CroMa's ticketing machine. This tool
    is intended for use by the bus conductor to issue tickets to passengers on-board

    The simulation page incorporates a primary record that facilitates user input of
    major trip details such as the origin, destination, and the number of passengers.
    This data is subsequently utilized to execute multiple tasks, including printing
    tickets, real-time updates to the firebase database, and analytical computations.

    The sidebar of the webapp offers a concise view of bus related parameters stored
    in the firebase real-time database, which can be accessed & monitored on the fly.

    Read more in the :ref:`CroMa Playground`.

    .. versionadded:: 1.2.0

    Parameters:
        None -> Variables are read in real-time from the users as per configruations

    Returns:
        None -> Values are updated inplace or within the firebase real-time database

    Warnings:
        same_starting_and_destination_location: True if start & destination are same
        destination_behind_current_location: True if selected destination is crossed

    Alerts:
        ticket_printed_alert: Alert the user that the ticket has succesfully printed
        location_updated_alert: Alert the user that location has updated succesfully
        trip_terminated_alert: Alert users that the current trip has been terminated
        dsr_report_generated_alert: Alert the user that the DSR report has generated
        dsr_mail_sent_alert: Alert users that DSR report has been mailed succesfully

    .. See Also:
        apply_style_to_sidebar_button()

    NOTE: The upcoming update will include saving the printed tickets into a folder
    """
    # Update terminal attributes with values retrieved from the firebase database
    terminal.current_location = database.retrieve_current_location()
    terminal.available_seat_count = database.retrieve_available_seats()
    terminal.total_passengers = database.retrieve_passengers_count()

    # Display title on the streamlit web application
    st.title(":oncoming_bus: Ticketing Machine Playground")

    # Display dropdowns for selecting the starting and destination locations
    # NOTE: The list of bus_stops may vary depending on the selected bus route
    starting_location = st.selectbox(
        "Select the Starting Location:", bus_stops["Name"].values
    )
    destination_location = st.selectbox(
        "Select Destination Location:", bus_stops["Name"].values
    )

    # Check if the starting location and destination locations are the same
    if starting_location == destination_location:
        # Display warning and set same_starting_and_destination_location to True
        st.warning("Starting location can not be same as destination", icon="⚠️")
        terminal.same_starting_and_destination_location = True

    # Set same_starting_and_destination_location attribute to False if not same
    else:
        terminal.same_starting_and_destination_location = False

    # Fetch the numerical value corresponding to the current location of the bus
    bus_current_location = bus_stops.loc[
        bus_stops["Name"] == terminal.current_location, "Number"
    ].item()

    # Fetch the numerical value corresponding to the user-provided origin
    user_starting_point = bus_stops.loc[
        bus_stops["Name"] == starting_location, "Number"
    ].item()
    # Fetch the numerical value corresponding to the user-provided destination
    user_destination = bus_stops.loc[
        bus_stops["Name"] == destination_location, "Number"
    ].item()

    # Determine if the bus has already passed the user-provided destination
    if bus_current_location > user_destination:
        # Set the warning & flag indicating destination to be behind current location
        st.warning("The bus has already crossed the selected destination", icon="⚠️")
        terminal.destination_behind_current_location = True

    # Set the destination_behind_current_location attribute to False if not behind
    else:
        terminal.destination_behind_current_location = False

    # Define user input field for passenger count, with limits and default value
    passenger_count = st.number_input(
        "Enter Number of Passengers:", min_value=1, max_value=10, value=1
    )
    int_passenger_count = int(passenger_count)  # Cast passenger_count to integer

    # Define is_disabled boolean based on terminal location relative to bus route
    # Returns True if any warning is flagged, else returns False
    is_disabled = (
        terminal.destination_behind_current_location
        or terminal.same_starting_and_destination_location
    )

    # Prompt the user to print tickets if no warning flags are marked True
    if st.button("Print Ticket", disabled=is_disabled):
        # Call the print_ticket function to return the bus fare as per input
        ticket_price = print_ticket(
            user_starting_point, user_destination, int_passenger_count
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

    # Display a dropdown on the sidebar for selecting the current location
    new_location = st.sidebar.selectbox(
        "Select Current Location:", bus_stops["Name"].values
    )

    # Update the current_location when the Update Location button is clicked
    if st.sidebar.button("Update Location"):
        # Set the new location on the current location terminal object
        terminal.current_location = new_location

        # Display success message indicating the current location has been upodated
        location_updated_alert = st.sidebar.success(
            ":white_check_mark: Location Updated"
        )
        # Update the current location in the firebase real-time database
        database.update_current_location()

        time.sleep(3)  # Wait for three seconds
        location_updated_alert.empty()  # Clear the location_updated_alert

        # Retrive the current passenger count from the firebase real-time database
        quondam_passenger_count = database.retrieve_passengers_count()
        # Get number correponding to current location from the bus_stops dataframe
        int_current_location = bus_stops.loc[
            bus_stops["Name"] == terminal.current_location, "Number"
        ].item()

        # Calculate total passengers aboard the bus at the current location
        terminal.total_passengers = sum(terminal.crowd_manager[:int_current_location])
        database.update_passengers_count()  # Update the passenger count in the database

        # Retrieve the number of currently available seats from the database
        terminal.available_seat_count = database.retrieve_available_seats()

        # Calculate available seat by subtracting passenger count from available seats
        terminal.available_seat_count = (
            terminal.available_seat_count
            + quondam_passenger_count
            - terminal.total_passengers
        )

        # Update the available seat count in the firebase real-time database
        database.update_available_seats()

    st.sidebar.markdown("""---""")  # Add a horizontal line to the web app's sidebar

    # Create an expander to display the real-time databse values in the sidebar
    expander = st.sidebar.expander("Backend Details")

    # Add some empty lines to the sidebar to place the button on the bottom section
    for _ in range(16):
        st.sidebar.write("")

    # Apply the CSS styles defined in the parameter file to the sidebar buttons
    apply_style_to_sidebar_button("hardware/style.css")

    # Execute the following code when End Trip and Refresh Database button is clicked
    if st.sidebar.button("End Trip and Refresh Database"):
        # Display an info message indicating that the current trip has been terminated
        trip_terminated_alert = st.sidebar.info(
            "Current trip has been terminated", icon="ℹ️"
        )

        time.sleep(3)  # Wait for three seconds
        trip_terminated_alert.empty()  # Clear the trip_terminated_alert

        # Compute and update the overall load factor for the current trip
        terminal.load_factor = sum(terminal.load_factor_list) / len(
            terminal.load_factor_list
        )

        # Inspect the boarding_tracker to find the stop with maximum onboards
        max_boarding = int(
            terminal.boarding_tracker.index(max(terminal.boarding_tracker)) + 1
        )
        # Save the bus stop's name from where maximum passengers onbaorded
        terminal.MAX_BOARDING_BUS_STOP = bus_stops.loc[
            bus_stops["Number"] == max_boarding, "Name"
        ].item()

        # Inspect the deboarding_tracker to find the stop with maximum deboards
        max_deboarding = int(
            terminal.deboarding_tracker.index(max(terminal.deboarding_tracker)) + 1
        )
        # Save the bus stop's name where maximum number of passengers debaorded
        terminal.MAX_DEBOARDING_BUS_STOP = bus_stops.loc[
            bus_stops["Number"] == max_deboarding, "Name"
        ].item()

        # Generate the Daily Status Report (DSR) and displays a success alert
        generate_dsr_report()
        dsr_report_generated_alert = st.sidebar.success(
            "DSR Report has been generated", icon="ℹ️"
        )

        time.sleep(3)  # Pause execution for three seconds
        dsr_report_generated_alert.empty()  # Clear the dsr_report_generated_alert

        # Create a mail object consonant to the DSRMail class
        mail = send_mail.DSRMail()

        # Send an email containing the DSR and display an info alert in the sidebar
        mail.send_dsr_mail()
        dsr_mail_sent_alert = st.sidebar.info("DSR Report has been emailed", icon="ℹ️")

        time.sleep(3)  # Wait for three seconds
        dsr_mail_sent_alert.empty()  # Clear the dsr_mail_sent_alert

        database.refresh_database()  # Refresh the database with the default values
        terminal.collection = terminal.load_factor = 0  # Reset colection & load_factor
        terminal.crowd_manager = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Retrive the default current location from the firebase real-time database
        terminal.current_location = database.retrieve_current_location()
        # Retrive the default available seat count from the firebase real-time database
        terminal.available_seat_count = database.retrieve_available_seats()
        # Retrive the default total passenger from the firebase real-time database
        terminal.total_passengers = database.retrieve_passengers_count()

        terminal.count = 10  # Set the count value to any value higher than 1

    # Display the total number of passengers at that instance in the expander
    expander.markdown(
        "**:male-office-worker: Passenger Count:**"
        + " "
        + str(terminal.total_passengers)
    )

    # Display the bus's current location at the given instance in the expander
    expander.markdown(
        "**:world_map: Current Location:**" + " " + str(terminal.current_location)
    )

    # Display the total collection at the given instance in the expander
    expander.markdown(
        "**:moneybag: Total Collections:** Rs." + " " + str(terminal.collection)
    )

    # Display the available seat count at the given instance in the expander
    expander.markdown(
        "**:seat: Seats Available:**" + " " + str(terminal.available_seat_count)
    )

    # Display the selected route of the bus in the expander
    expander.markdown(
        "**:bus: Selected Route:**"
        + " "
        + str(bus_stops.loc[bus_stops["Number"] == 1, "Code"].item())
        + " - "
        + str(bus_stops.loc[bus_stops["Number"] == 10, "Code"].item())
    )


def about_croma():
    """
    [CroMa WebApp page 03/03] - Sends email containing information about bug reports

    Function for documenting the purpose and use cases of CroMa hardware setup using
    various widgets & elements. Main page describes in detail about the HW operation

    The page includes several function to learn more about CroMas hardware setup. It
    includes an expander widget on the sidebar, which expands to show a form to send
    message to CroMa's dev team. Additionally the function adds an area for the user
    to rate their experience whilst using CroMa sandbox, with a 5-star rating widget.

    Read more in the :ref:`CroMa Playground - About Section`.

    .. versionadded:: 1.2.0

    Parameters:
        None -> Variables are read in real-time from the users as per configruations

    Returns:
        None -> The star ratings & email id's for newsletter are recorded in backend

    Warnings:
        invalid_email_address: True if a user enters an invalid email id (ref: mail)

    Alerts:
        newsletter_subscribed_alert: Alert users that they subscribed to newsletters
        contact_dev_team_alert: Alert users that message has been sent to dev team
        star_rating_alert: Alert the user that their star ratings have been recorded

    NOTE: Upcoming updates will include method to save the star recordings in our DB
    """
    # Display a markdown title for the about section with an emoji
    st.markdown("# :dart: About CroMa - Crowd Mgmt Tool")

    # Display a paragraph with basic information about CroMa and it's features
    st.markdown(
        "<p align = 'justify'>CroMa is a firmware solution that provides real-time "
        + "information pertaining to the crowd levels in public buses. It includes features such "
        + "as real-time tracking, estimated time-of-arrival, and seat occupancy. This solution "
        + "comprises of three major components: a ticketing machine, real-time database and a "
        + "mobile app</p>",
        unsafe_allow_html=True,
    )

    # Display paragraph with information about ticketing machine and real-time database
    st.markdown(
        "<p align = 'justify'>The hand-held ticketing machine is a micro-controller-based system "
        + "that generates billing tickets, collects and saves data, and generates daily reports "
        + "and summaries. The hardware is equipped with a GPS module for tracking the location of "
        + "the bus. The device is intended for use by conductors and clippies to issue tickets to "
        + "passengers. When new passengers board a bus, their details, including their start "
        + "location, total luggage in the bus, intended destination, and total number of "
        + "passengers, are collected for issuing tickets. The hand-held ticketing machine "
        + "collects, processes, and transmits this data to the FireBase RT databases</p>",
        unsafe_allow_html=True,
    )

    # Display another paragraph with information about CroMa's database structure and rules
    st.markdown(
        "<p align = 'justify'>A QR code or unique alphanumerical code may be used to update the "
        + "software for passengers using a monthly or yearly bus pass. The data is maintained in "
        + "the FireBase Real-Time database, which synchronizes the data across devices. The data "
        + "is structured as a JSON tree, with data points stored as JSON objects. The parent "
        + "nodes represent the Bus Id (unique to each bus), and the real-time data associated "
        + "with the bus, including available seats and current location, are maintained as nested "
        + "nodes. The database is updated whenever new tickets are issued or when passengers "
        + "boards or de-board the bus",
        unsafe_allow_html=True,
    )

    # Add an input box for the user to enter their email ID
    st.sidebar.text_input("Enter your Email Id")

    # Apply the CSS styles defined in the parameter file to the sidebar buttons
    apply_style_to_sidebar_button("hardware/style.css")

    # Add a button for the user to subscribe to the newsletter
    newsletter_mailing_list_user_email_id = st.sidebar.button(
        "Subscribe to our Newsletter"
    )

    if newsletter_mailing_list_user_email_id:
        # Display a success message when user subscribes to receive our newsletters
        newsletter_subscribed_alert = st.sidebar.success(
            "You have subscribed to newsletter", icon="✅"
        )

        time.sleep(3)  # Hold the execution for the next three seconds
        newsletter_subscribed_alert.empty()  # Clear the star_rating_alert from the UI

    st.sidebar.markdown("""---""")  # Add a horizontal line to the web app's sidebar

    # Create an expander widget for Contact the CroMa Team section
    contact_dev_team_expander = st.sidebar.expander("Contact the CroMa Team")

    # Add text input fields for the user to enter their name, email, and message
    contact_dev_team_expander.text_input("Enter your Full Name:")
    contact_dev_team_expander.text_input("Enter your E-Mail Id:")
    contact_dev_team_expander.text_area("Enter your Message:")

    # Add a button to allow the user to send their message
    send_message_to_dev_team_button = contact_dev_team_expander.button("Send Message")

    if send_message_to_dev_team_button:
        # Display a success message when user sends a message to CroMa's dev team
        contact_dev_team_alert = contact_dev_team_expander.success(
            "Your message has been sent", icon="✅"
        )

        time.sleep(3)  # Hold the execution for the next three seconds
        contact_dev_team_alert.empty()  # Clear the star_rating_alert from the UI

    # Add 13 new lines to create space between sections in the sidebar
    for _ in range(13):
        st.sidebar.write("\n\n")

    # Add a section to rate the user's experience with CroMa using st_star_rating
    with st.sidebar:
        st.write("Found CroMa helpful? Rate your experience:")
        # Add a 5-star rating widget to allow the user to rate their experience
        star_rating = st_star_rating("", 5, 3, 54)

        # Check if star rating has been altered by the user
        if star_rating != 3:
            # Display a success message when a new star rating has been given
            star_rating_alert = st.success(
                "Thanks for sharing your experience", icon="✅"
            )

            time.sleep(3)  # Hold the execution for the next three seconds
            star_rating_alert.empty()  # Clear the star_rating_alert from the UI


def send_bug_report():
    """
    [CroMa WebApp page 03/03] - Sends email containing information about bug reports

    Fuction for sending a bug report mail from the specified sender email address to
    the team. The mail is structured with options to include one or more attachments.

    The send_bug_report() function sends an email containing bug reports submitted by
    users. This function takes in the user's name, e-mail id, and the bug description
    etc as input parameters. It then composes an email message using the user's input,
    & sends it to the CroMa team. If sent successfully it'd returns a success message.

    Read more in the :ref:`CroMa Playground - Bug Reports Section`.

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
    st.markdown("# :ladybug: Send Bug Report")

    # Display a message to users who wish to report a bug
    st.markdown(
        "<p align = 'justify'>If you believe that you have discovered any "
        + "vulnerability in CroMa, please fill in the form below with a thorough "
        + "explanation of the vulnerability. We will revert back to you after due "
        + "diligence of your bug report</p>",
        unsafe_allow_html=True,
    )
    # Create two columns to hold text input fields
    col1, col2 = st.columns(2)

    # Define context managers to set the current column for the following input fields
    with col1:
        # Create a text input field in the first column to read user's full name
        terminal.br_full_name = st.text_input("Full Name:")
    with col2:
        # Create a text input field in the second column to read user's email id
        terminal.br_email_id = st.text_input("E-Mail Id:")

    # Create two columns to hold input dropdown fields
    col3, col4 = st.columns(2)

    # Define context managers to set the current column for selectbox input field
    with col3:
        # Create a selectbox input field in the third column to read the bug location
        terminal.br_bug_in_page = st.selectbox(
            "Which page is the bug in?", croma_page_list
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
        terminal.br_bug_type = st.selectbox("What type of bug is it?", bug_types)

    # Create a text area where users can describe the bug and steps to reproduce it
    terminal.br_bug_description = st.text_area(
        "Describe the issue in detail (include steps to reproduce the issue):"
    )

    # Widget to upload relevant attachments, such as screenshots, charts, and reports.
    # The file uploader widget is set to accept multiple files (limit: 200mb per file)
    terminal.br_uploaded_files = st.file_uploader(
        "Include any relevant attachments such as screenshots, or reports:",
        accept_multiple_files=True,
    )

    # Checkbox that user must check to indicate that they accept terms & conditions
    bug_report_terms_and_conditions = st.checkbox(
        "I accept the terms and conditions and I consent to be contacted in future by " 
        + "the CroMa support team"
    )

    # Create a button that the users can click to send the bug reports to the CroMa team
    # Disabled argument enables the button only if the user has checked the T&C checkbox
    if st.button("Send Bug Report", disabled=not bug_report_terms_and_conditions):
        # Create an instance of a BugReportMail object from the send_mail module
        bug_report = send_mail.BugReportMail

        # Call send_bug_report_mail method of the BugReportMail object to send the mail
        bug_report.send_bug_report_mail()

        # Displays a success message to user indicating that their report has been sent
        bug_report_sent_alert = st.success("Your bug report has been sent!")

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

        # On rsuccesfully opening the tab, display a success message
        st.sidebar.success("Redirecting you to community handle")


# Create a dictionary of different pages of thew web app, along with their corresponding functions
croma_page_list = {
    "Hardware Sandbox": croma_hw_playground,
    "About CroMa": about_croma,
    "Send Bug Report": send_bug_report,
}

# Create a dropdown menu for selecting a page from the croma_page_list, passing the dictionary key
selected_page = st.sidebar.selectbox("Navigate Within Pages:", croma_page_list.keys())

croma_page_list[
    selected_page
]()  # Call function corresponding to the page keeping key as an index
