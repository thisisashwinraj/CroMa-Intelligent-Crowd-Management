![CroMa Readme Banner](https://github.com/thisisashwinraj/croma-intelligent-crowd-management/blob/main/assets/CroMa_Banner_Light.png#gh-light-mode-only)
![CroMa Readme Banner](https://github.com/thisisashwinraj/croma-intelligent-crowd-management/blob/main/assets/CroMa_Banner_Dark.png#gh-dark-mode-only)

<p align='justify'>CroMa is an android application that uses a python backend hardware, built on raspberry pi integrated with a firebase real-time database and flutter framework for efficient crowd management in public transports such as buses & taxies. The hardware is effectively a handheld ticketing machine used for printing tickets, and collecting selective information about passengers. After data processing, the mobile application displays the output to the users. No Login is required</p>

The project development started in April 2022 as a group project and has been licensed under the [Creative Commons Attribution - Non Commercial - No Derivs License](https://github.com/thisisashwinraj/croma-intelligent-crowd-management/blob/main/LICENSE) (CC-BY-NC-ND). The passenger data collected, is maintained as per the Privacy Policy. The pull requests are maintained by a team of [contributors](https://github.com/thisisashwinraj/croma-intelligent-crowd-management#all-contributors). Learn more about CroMa software [here](https://github.com/thisisashwinraj/croma-intelligent-crowd-management#user-installation-and-working)

# SubDirectories and Constraints
### Software Dependencies
• **Mobile App:** Dart, [Flutter](https://docs.flutter.dev/get-started/install), Maps SDK, Places SDK, Distance Matrix API, Directions API, Roads API, and Geocoding API
<br>
• **Ticket Machine:** [Python 3.7](https://www.python.org/downloads/release/python-370/), Firebase (Real-Time Database), RaspberryPi and [ArduinoUNO](https://docs.arduino.cc/hardware/uno-rev3) | Dependencies: [Pyrebase](https://pypi.org/project/Pyrebase/)

### Files and SubDirectories
• **Mobile Application:** This directory contains the Dart code and afilliated resources for building the flutter application
<br>
• **Ticketing Machine:** This directory contains the Python3 code for designing the hand-held ticketing machine, and DB

<p align = "justify">
All relevant updates, and stable versions are made available in the <a href="https://github.com/thisisashwinraj/croma-intelligent-crowd-management/tree/main/template_files/stable_versions">~/stableVersion</a> sub-directory. Some subdirectories may be sensitive for the project and may trigger review requests, when pull requests touch these files. Github handles with commit rights made available in the <a href="https://github.com/thisisashwinraj/croma-intelligent-crowd-management/blob/main/template_files/CODEOWNERS">~/Template Files/CODEOWNERS</a> are responsible for reviewing such changes
</p>

# User Installation and Working
<p align = "justify">
CroMa is a firmware solution that provides commuters with real-time information about public transits(such as buses) including real-time tracking, estimated time-of-arrival and the seat occupancy. This solution is an interworking of two major components: a <a href="https://github.com/thisisashwinraj/croma-intelligent-crowd-management/tree/main/hardware_files">handheld ticketing machine</a>, and a <a href="https://github.com/thisisashwinraj/croma-intelligent-crowd-management/tree/main/android">mobile application</a>. CroMa v1.0 offers support for only buses
</p>
<p align = "justify">
The hand-held ticketing machine is a micro-controller-based system used for generating billing tickets and collecting, saving, and generating daily reports and summaries. Our version of the hardware is additionally equipped with a GPS module for tracking the location of the bus. The device is to be used by conductors, and/or clippies for issuing tickets to the passengers. When new passengers board this bus, their details such as their start location, total luggage in the bus, their intended destination, & the total number of passengers is collected for issuing the tickets. These details are collected, processed and transmitted to the <a herf="https://firebase.google.com/products/realtime-database">FireBase RT database</a> by the hand-held ticketing machine. For passengers using a monthly, or yearly bus pass, a QR code or a unique alpha-numerical code may be used to update the software
</p>

![CroMa App](https://github.com/thisisashwinraj/croma-intelligent-crowd-management/blob/main/assets/CroMaAppUI.png)

<p align = "justify">
The passengers data is maintained in the FireBase Real-Time database for synchronizing this data across devices. This data is structured as a JSON tree with the data points stored as JSON objects. The parent nodes represents the Bus Id (unique to each bus) and the real-time data associated with the bus (including available seats, & current location, etc) are maintained as nested nodes. Whenever a new ticket is issued the database is updated. The algorithm ensures that the database is updated when passengers de-board the bus. The data maintained in this <a href="https://firebase.google.com/products/realtime-database">FireBase RT database</a> is then made available to be fetched by the android mobile application, and the relevant machine learning models, and API's.
</p>

<p align = "justify">
The android app is the end-user's application that allows the user to compare various transit options, and choose the most ideal option that fits their needs. The users, start with opening the application, and making a query, by entering their starting point, intended destination, and the type of bus (fast, SPF, express, deluxe, etc). No LogIn is required for using the android mobile app. The application looks up into the data base, and displays the location of buses in real-time within a pre set radius that passes through both their starting point and the destination entered by the user. The bus markers with red colour indicates heavy rush, while the green color indicates light occupancy. On tapping a given bus marker, the application displays more details about that bus to the users including, their estimated time of arrival, seat occupancy & ETA of buses on same route etc. Users can compare multiple options to make an informed decision
</p>

To run the ticketing machine's sofware on a local computer, open the terminal, install [pyrebase](https://pypi.org/project/Pyrebase/), & type the command:
```
python hardware/ticketingMachine.py
```

CroMas development take place on [GitHub](https://github.com/thisisashwinraj/croma-intelligent-crowd-management). Please submit any bug that you may encounter to the issue tracker with a reproducible example demonstrating the problem, in accordance with the issue template, present in contributing files

```
├── .github
├── android                          // Files required for running the application on an Android
│   ├── android                      
│   └── ios
├── assets                           // The files required for running the application on an iOS
├── asv_bench
├── database
├── example                          // Contains eamples and use cases for the hardware & mobile
├── hardware
│   ├── main.py                      
│   └── master                       // Contains the code for operators, including master access
├── sphinx
├── templates
├── test                             // Contain sthe code for unit testing the app, and hardware
│   ├── app                      
│   └── hardware
├── versions                         // Contains the ziped versions of all major stable releases          
└── .mailmap
```

<p align='justify'>To run the application, start debugging by clicking <B>Run > Start Debugging</B> from the main IDE window (or press F5). If you are using <a href='https://code.visualstudio.com/'>VS Code</a>, you should see a set of Flutter-specific entries in the status bar, including a <a href='https://docs.flutter.dev/get-started/install'>Flutter SDK</a> version and a device name (or a message displaying No Devices). The Flutter extension automatically selects the latest device connected. However, if you have multiple devices/simulators connected, click device in the status bar to see a pick list at the top of the screen. Select the devices you want to use for running/debugging & then run the command</p>

# CroMa - Under the Hood

<p align='justify'>The software project aims to use human-centric technology to take public transportation & crowd manangement one step ahead. We used <a href='https://en.wikipedia.org/wiki/Rapid_application_development'>Rapid Application Development model (RAD)</a> to design several firmware components developed simultaneously as if they were smaller individual projects. These are then assembled into the main working prototype.</p>

### Defining the Problem Statements
<p align='justify'><B>Problem  Statement 1:</B> Ramesh is a busy executive who needs to reach his office on time and decide whether to take a public bus for commuting, or use his personal vehicle as he stays very far away from the office, & want to save money<BR><B>Hypothesis:</B> If Ramesh uses CroMa for tracking the public buses available at his nearest bus-stop then he can plan his shuttle accordingly, & will reach his desired location at time, without needing to travel in an alternate public transport</p>

<p align='justify'><B>Problem Statement 2:</B> Vartika is a seven month pregnant women who needs to board a long distance bus with ample seats available because she is agoraphobic, and her physical conditions does'nt allow her to stand for longer duration<BR><B>Hypothesis:</B> If Vartika uses CroMa, for checking the buses in her proximity with less occupancy, then she can make an intelligent choice of the bus she wants to board, & can grab a seat, without needing to worry about standing for long.</p>

### The Logic that Powers the System
<p align="justify">The system's hardware cycle starts with the bus conductor initializing a new trip on the handheld ticketing machine by entering the Bus ID. The machine is then configured with the routes associated with that Bus ID and reflects the pre-set values for necessary passenger data variables, including the total number of available seats, the current location, and the total number of passengers on the bus. The ticketing machine will now display the options for printing tickets, managing journey details (for use by conductors) and displaying total fare collections during this trip</p>

<p align='justify'>When a new passenger boards the bus, the bus conductor issues them a ticket after collecting information about their point of origin, intended destination, and the number of co-passengers, if any. In addition to simply printing tickets, the proposed ticketing machine sends this data to the Firebase real-time database, where the values for these three parameters are updated. Bus location data are collected by the GPS module. For passengers using concession cards, the QR code scanner is used to verify the authenticity of the cardholder and the proper updation of crowd data</p>

<p align='justify'>The application calculates the crowd on a bus in real time using a global list variable called terminal.crowd_manager. This list represents the bus stops along a route (and is thus initialized with the same length as the number of bus stops in the route), with each element set to zero, indicating no passengers at the start. When a ticket is issued, the print_ticket function increments the corresponding boarding point element in terminal.crowd_manager by the number of passengers boarding. It then decrements the alighting point element by the same number, reflecting passenger deboarding. The refresh_real_time_database function calculates the total number of passengers on the bus by summing the values in terminal.crowd_manager up to the bus's current stop. This information, along with available seat count and load factor, is then updated in the Firebase real-time database, ensuring that the user app displays accurate real-time crowd load information. The total bus fare is calculated by adding the variable fare to the fixed fare</p>

<p align='justify'>While developing this software, we have assumed that the bus fares will increase by a given amount, after every third stop the passenger needs to cross to reach his destination, starting from their origin point. The transport corporation can simply revise the bus fare by changing the values of the variable part or the fixed part. No code changes required.</p>

<p align='justify'>Passengers waiting to board the bus can open the user application. They need to initialize the application by entering their destination, boarding point, and the required bus type. The app then retrieves a list of nearby buses that pass through their current location and destination from the Firebase Realtime Database and displays it to the user. The user can select a bus to view more information, including the number of available seats, crowd levels, timings for other buses travelling on the same routes, and fares. Users can also view the current location of the buses on the map</p>
  
# Contribution Guidelines
To start contributing to the project, clone the repository into your local system subdirectory using the below git code:
```
git clone https://github.com/thisisashwinraj/croma-intelligent-crowd-management.git
```
Before cloning the repository, make sure to navigate to the working subdirectory of your command line interface and ensure that no folder with same name exists. Other ways to clone the repository includes using a password protected [SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent), or by using [Git CLI](https://cli.github.com/). The changes may additionally be performed by opening this repo using [GitHub Desktop](https://desktop.github.com/)

### Edit the Source Code and Make Desired Changes
<p align="justify">To be able to make changes to the source, you may need to install and use a python IDE such as <a href="https://www.jetbrains.com/pycharm/download/">PyCharm</a>, Microsoft <a href="https://code.visualstudio.com/">VisualStudio</a>, and/or any other python interpreter. You will also require a Jupyter notebook  for working with the code snippets. To work with the Flutter application, you shall have <a href="https://docs.flutter.dev/get-started/install">Flutter SDK</a> installed on your local computer, and a USB cable. Ensure that you are strictly following the PEP-8 programming standards, while introducing the desired updates.</p>

Before opening a Pull Request, it is recommended to have a look at the full contributing page to make sure your code complies with all the pull request guidelines. Please ensure that you satisfy the [~/Checklist](https://github.com/thisisashwinraj/croma-intelligent-crowd-management/tree/main/Template%20Files/PULL_REQUEST_TEMPLATE) before submitting your PR.

Navigate to this subdirectory, & check status of all files that were altered (red) by running the below code in Git Bash:
```
git status
```
Stage all your files that are to be pushed into your pull request. This can be done in two ways - stage all or some files:
```
git add .            // adds every single file that shows up red when running git status
```
```
git add <filename>   // type in the particular file that you would like to add to the PR
```

Commit all the changes that you've made and describe in brief the changes that you have made using this command:
```
git commit -m "<commit_message>"
```
Push all of your updated work into this GitHub repo in the form of a Pull Request by running the following command:
```
git push origin main
```
All pull requests are reviewed on a monthly rolling basis. Your understanding is appreciated during the review process

# Data Security and Privacy
Safegaurding your data starts with understanding how CroMa collects, and processes your personal info. The in-hand ticketing machine only collects data pertaining to the user's starting location, destination, and the total number of co-passengers. When this data is shared, all that CroMa records is that a few passengers bought ticket(s) and onboarded the bus, but it doesn't know who they exactly are. CroMa does not collect your personal data in any form. Similarly on the mobile app's side, it does'nt require users to log-in to the application. They can simply startoff without signing up.

The Firebase database are secured by means of firebase rules. The Firebase rules ensure that only authenticated users are allowed to manipulate the data. This includes real time passenger data collected by a given bus during its journey

# License and Project Status
CroMa & all its resources are distributed under [Creative Commons Attribution - Non Commercial - No Derivs License](https://github.com/thisisashwinraj/croma-intelligent-crowd-management/blob/main/LICENSE). The app is compatible with all operating systems. The latest released stable version of CroMa is v1.0.1, and is available to be used on all local system for general use through the mobile app. All releases are logged in the [~/StableVersions]()

Upcoming updates will include new features, optimized recommendations using AI/ML and support for other transits
<br>
All contributors may reproduce and share the licensed material in whole or in part for non-commercial purposes only

