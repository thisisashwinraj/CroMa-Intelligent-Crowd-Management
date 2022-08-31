# CroMa - Crowd Management Software
CroMa is an android application that uses a python backend hardware, built on raspberry pi integrated with a firebase real-time database, and flutter framework for efficient crowd management in public transports such as buses & taxies. The hardware is effectively a handheld ticketing machine used for printing tickets, and collecting selective information about passengers. After data processings, the mobile application displays the output to the users. No LogIns required.

The project development started in April 2022 as a group project and has been licensed under the Creative Commons Attribution - Non Commercial - No Derivs License (CC-BY-NC-ND). The passenger data collected, is maintained as per the Privacy Policy. The Pull Requests are maintained by a team of contributors. Learn more about CroMa software here

# SubDirectories and Constraints
### Software Dependencies
• **Mobile App:** Dart, Flutter, Maps SDK, Places SDK, Distance Matrix API, Directions API, Roads API, and Geocoding API
<br>
• **Ticket Machine:** Python 3.7, Firebase (Real-Time Databases), RaspberryPi and ArduinoUNO| Dependencies: Pyrebase

### Files and SubDirectories
• **Mobile Application:** This directory contains the Dart code and afilliated resources for building the flutter application
<br>
• **Ticketing Machine:** This directory contains the Python3 code for designing the hand-held ticketing machine, and DB

All relevant updates, and stable versions are made available in the ~/stableVersion sub-directory. Some subdirectories may be sensitive for the project and may trigger review requests, when pull requests touch these files. Github handles with commit rights made available in the ~/Template Files/CODEOWNERS are responsible for reviewing such changes

# User Installation and Working
CroMa is a firmware solution that provides commuters with real-time information about public transits(such as buses) including real-time tracking, estimated time-of-arrival and the seat occupancy. This solution is an inter-working of two major components: a handheld ticketing machine and a mobile application. CroMa v1.0 offers support for only buses.

The hand-held ticketing machine is a micro-controller-based system used for generating billing tickets and collecting, saving, and generating daily reports and summaries. Our version of the hardware is additionally equipped with a GPS module for tracking the location of the bus. The device is to be used by conductors, and/or clippies for issuing tickets to the passengers. When new passengers board this bus, their details such as their start location, total luggage in the bus, their intended destination, & the total number of passengers is collected for issuing the tickets. These details are collected, processed and transmitted to the FireBase RT database by the hand-held ticketing machine. For passengers using a monthly, or yearly bus pass, a QR code or a unique alphanumerical code may be used to update the software.

The passengers data is maintained in the FireBase Real-Time database for synchronizing this data across devices. This data is structured as a JSON tree with the data points stored as JSON objects. The parent nodes represents the Bus Id (unique to each bus) and the real-time data associated with the bus (including available seats, & current location, etc) are maintained as nested nodes. Whenever a new ticket is issued the database is updated. The algorithm ensures that the database is updated when passengers de-board the bus. The data maintained in this FireBase RT database is then made available to be fetched by the android mobile application, and the relevant machine learning models, and API's.

The android app is the end-user's application that allows the user to compare various transit options, and choose the most ideal option that fits their needs. The users start with opening the application, and making a query, by entering their starting point, intended destination, and the type of bus (fast, SPF, express, deluxe, etc). No LogIn is required for using the android mobile app. The application looks up into the database, and displays the location of buses in real-time within a preset radius, that passes through both the starting point, and the destination entered by the user. The bus marker with red color indicates heavy rush while the green color indicates light occupancy. On tapping a given bus marker, the application displays more details about that bus to the users including, the estimated time of arrival, available seats, ETA of buses on same route etc. The user can compare multiple options to make an informed decision.
