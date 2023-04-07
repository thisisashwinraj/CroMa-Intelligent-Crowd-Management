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
This module contains the global variables that are used across hardware-files.
Variables may be used by a single module or by multiple module simultaneously.

Categories of Variables:
    [1] Dynamic - These variables store data that changes in real-time
    [2] User Input - These variables store the input read from users
    [3] Database Fetched - These variables reflect values read from database.
    [4] Alert - Warning to raise system flag alerts during execution
    [5] Calculated - Value is calculated at runtime during execution

.. versionadded:: 1.2.0

NOTE: At runtime values of all of these variables are set to system defaults.
"""
# pylint: disable=invalid-name

# [Database Fetched] Variable specifying bus type (eg:express, city etc)
bus_type = None

# [User Input] E-Mail for user authentication by firebase real-time database
input_email = None
# [User Input] Password assosciated with firebase email id authentication
input_password = None
# [User Input] Unique Id associated with each route, fetches info from routesDB
route_id = None

# [Dynamic] The current location of the bus. Default value set to origin at runtime
current_location = None
# [Dynamic] Free seats available in a bus in transit. Default value set to 0
available_seat_count = 0
# [Dynamic] Total no. of passengers in bus at a given time. Default value is 0
total_passengers = 0

# [User-Input] Unique Id associate with each bus, fetches info from busDB
bus_id = "KL13N"
# [Database Fetched] A list of all bus stops in a given route
bus_route = "Trivandrum to Kottayam"

# [Calculated] Ration of total passengers in the bus to its maximum capacity
load_factor = 0
# [Calculated] List of load factors after each ticket is printed
load_factor_list = []
# [Database Fetched] Total capcity of the bus
BUS_MAX_CAPACITY = 32

# [Calculated] Bus stop from where the maximum passengers boarded the bus
MAX_BOARDING_BUS_STOP = " "
# [Calculated] Bus stop where the maximum passengers deboarded the bus
MAX_DEBOARDING_BUS_STOP = " "
# [User Input] Number of passengers boarding the bus at each stop
boarding_tracker = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# [User Input] Number of passengers deboarding the bus at each stop
deboarding_tracker = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# [Calculated] Value to disable firebase re-initialization
count = 0
# [User Input] Directory location where the DSR report is saved
report_location = " "

# [Dynamic] Amount collected as fare during the trip. Default value set to 0
collection = 0
# [Dynamic] An array of 0s of length(selected_route) managing crowd information
crowd_manager = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# [Dynamic] Total number of co-passengers while printing the ticket
passenger_count = 0
# [User Input] Numerical encoded form of the selected route
selected_route = 0
# [Dynamic] Total tickets printed throughout the trip. Default value set to 0
total_tickets_printed = 0
# [Alert] General warning flag for alerting the user
warning_flag = False
# [Alert] Warning to alert the user if the origin and destination are the same
same_starting_and_destination_location_warning_flag = False
# [Alert] Warning to alert the user if the destination has already been crossed
wrong_destination_warning_flag = False
# [Calculated] Total number of passengers who boarded the bus throughout the journey
total_trip_passenger_count = 0
# [Calculated] Total number of passengers who boarded the bus throughout the journey
passengers_per_trip = 0
# [Calculated] Number of passengers who boarded the bus at a particular time
current_passenger_count = None

# [User Input] The email address to which the mail is to be delivered
RECEIVER_EMAIL_ID = " "

# [User Input] Full name to be printed in the bug report
br_full_name = " "
# [User Input] E-mail id to be printed in the bug report
br_email_id = " "
# [User Input] Page with bug to be printed in the bug report
br_bug_in_page = " "
# [User Input] Bug type to be printed in the bug report
br_bug_type = " "
# [User Input] Bug description to be printed in the bug report
br_bug_description = " "
# [User Input] Byte code of the file to be attached in the bug report
br_uploaded_files = None
# [User Input] Body of the mail to be printed in the bug report
br_mail_body = " "
