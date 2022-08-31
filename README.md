# CroMa - Crowd Management Software
CroMa is an android application that uses a python backend hardware, built on raspberry pi integrated with a firebase real-time database, and flutter framework for efficient crowd management in public transports such as buses & taxies. The hardware is effectively a handheld ticketing machine used for printing tickets, and collecting selective information about passengers. After data processings, the mobile application displays the output to the users. No LogIns required.

The project development started in April 2022 as a group project and has been licensed under the Creative Commons Attribution - Non Commercial - No Derivs License (CC-BY-NC-ND). The passenger data collected, is maintained as per the Privacy Policy. The Pull Requests are maintained by a team of contributors. Learn more about CroMa software here

# SubDirectories and Constraints
### Software Dependencies
• **Mobile App:** Dart, Flutter, Maps SDK, Places SDK, Distance Matrix API, Directions API, Roads API, and Geocoding API
<br>
• **Ticket Machine:** Python 3.7, Firebase (Real-Time Databases), Raspberry Pi, Arduino | Dependencies: PyreBase, Pandas

### Files and SubDirectories
• **Mobile Application:** This directory contains the Dart code, and afilliated resources for building the flutter application
<br>
• **Ticketing Machine:** This directory contains the Python3 code for designing the hand-held ticketing machine, and DB

All relevant updates, and stable versions are made available in the ~/stableVersion sub-directory. Some subdirectories may be sensitive for the project and may trigger review requests, when pull requests touch these files. Github handles with commit rights made available in the ~/Template Files/CODEOWNERS are responsible for reviewing such changes

# User Installation and Working
CroMa is a hardware-driven solution that provides commuters with real time information about public transports including real-time tracking, estimated time of arrival, and seat occupancy. The solution is an inter-working of two major firmware components - a hand-held ticketing machine and the mobile application. The version v1.0.0 offers support for only public buses.

The hand-held ticketing machine is a micro-controller based system used for generating billing tickets and collecting, saving and generating daily reports and summaries. Our version of the hardware is additionally equipped with a GPS module for tracking the location of the bus. The device is to be used by the conductors, or clippies for issuing tickets to the passengers. When a new passenger boards the bus, details such as the location from where they boarded the bus, their intended destination and the number of passenger are collected for issuing a ticket. These details are collected, processed and transmitted to the FireBase real-time database by the hand-held ticketing machine. For passengers using a monthly/yearly bus pass, a QR code or a unique alphanumerical code may be used to update the software.

The passenger data is maintained in the firebase real-time database for synchronizing the application data across devices. The data is structured as a JSON tree with the data points stored as JSON objects. The parent node represents the Bus Id (unique to each bus) and the real-time data assosciated with the bus (including available seats, current location etc) are maintained as nested nodes. Whenever a new ticket is printed, the data is updated. The algorithm ensures that the database is updated when passengers deboard the bus. The data maintained in this real-time database is then made available to be fetched by the mobile application and the appropriate machine learning models.

The mobile app is the end-user application that allows the user to compare various transit options and choose the most ideal option that fits their needs. The users starts with opening the application and making a query, entering their starting point, intended destination and the type of bus (fast, superfasr, express deluxe etc). No login is required for using the application. The application looks up into the database and displays the location of buses in real-time within a given radius, that passes through both the starting point and the destination entered by the user. The red colour bus marker indicates heavy rush while the green colour indicates light occupancy. On tapping a given marker, the application displays more details about the bus to the user including the estimated time of arrival, available seat count, ETA for other buses on the same route etc. The user can compare from multiple options to make an informed decision.
