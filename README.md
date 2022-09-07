# CroMa - Crowd Management Software
CroMa is an android application that uses a python backend hardware, built on raspberry pi integrated with a firebase real-time database, and flutter framework for efficient crowd management in public transports such as buses & taxies. The hardware is effectively a handheld ticketing machine used for printing tickets, and collecting selective information about passengers. After data processings, the mobile application displays the output to the users. No LogIns required.

The project development started in April 2022 as a group project and has been licensed under the [Creative Commons Attribution - Non Commercial - No Derivs License](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/blob/main/LICENSE) (CC-BY-NC-ND). The passenger data collected, is maintained as per the Privacy Policy. The Pull Requests are maintained by a team of contributors. Learn more about CroMa software [here](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System#user-installation-and-working)

# SubDirectories and Constraints
### Software Dependencies
• **Mobile App:** Dart, Flutter, Maps SDK, Places SDK, Distance Matrix API, Directions API, Roads API, and Geocoding API
<br>
• **Ticket Machine:** Python 3.7, Firebase (Real-Time Database), RaspberryPi and ArduinoUNO | Dependencies: Pyrebase

### Files and SubDirectories
• **Mobile Application:** This directory contains the Dart code and afilliated resources for building the flutter application
<br>
• **Ticketing Machine:** This directory contains the Python3 code for designing the hand-held ticketing machine, and DB

All relevant updates, and stable versions are made available in the [~/stableVersion](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/tree/main/template_files/stable_versions) sub-directory. Some subdirectories may be sensitive for the project and may trigger review requests, when pull requests touch these files. Github handles with commit rights made available in the [~/Template Files/CODEOWNERS](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/blob/main/template_files/CODEOWNERS) are responsible for reviewing such changes

# User Installation and Working
CroMa is a firmware solution that provides commuters with real-time information about public transits(such as buses) including real-time tracking, estimated time-of-arrival and the seat occupancy. This solution is an inter-working of two major components: a handheld [ticketing machine](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/tree/main/hardware_files) and a [mobile application](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/tree/main/android). CroMa v1.0 offers support for only buses.

The hand-held ticketing machine is a micro-controller-based system used for generating billing tickets and collecting, saving, and generating daily reports and summaries. Our version of the hardware is additionally equipped with a GPS module for tracking the location of the bus. The device is to be used by conductors, and/or clippies for issuing tickets to the passengers. When new passengers board this bus, their details such as their start location, total luggage in the bus, their intended destination, & the total number of passengers is collected for issuing the tickets. These details are collected, processed and transmitted to the [FireBase RT database](https://firebase.google.com/products/realtime-database) by the hand-held ticketing machine. For passengers using a monthly, or yearly bus pass, a QR code or a unique alphanumerical code may be used to update the software.

![CroMa App](https://github.com/thisisashwinraj/CroMa-CrowdManagementSoftware/blob/main/assets/CroMaAppUI.png)

The passengers data is maintained in the FireBase Real-Time database for synchronizing this data across devices. This data is structured as a JSON tree with the data points stored as JSON objects. The parent nodes represents the Bus Id (unique to each bus) and the real-time data associated with the bus (including available seats, & current location, etc) are maintained as nested nodes. Whenever a new ticket is issued the database is updated. The algorithm ensures that the database is updated when passengers de-board the bus. The data maintained in this [FireBase RT database](https://firebase.google.com/products/realtime-database) is then made available to be fetched by the android mobile application, and the relevant machine learning models, and API's.

The android app is the end-user's application that allows the user to compare various transit options, and choose the most ideal option that fits their needs. The users, start with opening the application, and making a query, by entering their starting point, intended destination, and the type of bus (fast, SPF, express, deluxe, etc). No LogIn is required for using the android mobile app. The application looks up into the data base, and displays the location of buses in real-time within a pre set radius that passes through both their starting point and the destination entered by the user. The bus markers with red colour indicates heavy rush, while the green color indicates light occupancy. On tapping a given bus marker, the application displays more details about that bus to the users including, their estimated time of arrival, seat occupancy & ETA of buses on same route etc. Users can compare multiple options to make an informed decision.

To run the ticketing machine's sofware on a local computer, open the terminal, install [pyrebase](https://pypi.org/project/Pyrebase/), & type the command:
```
python ticketingMachine.py
```

CroMas development take place on GitHub. Please submit any bug that you may encounter to the issue tracker with a reproducible example demonstrating the problem, in accordance with the issue template, present in contributing files

```
├── assets
├── android                       // Files required for running the application on an Android
│   └── Images
├── ios                           // The files required for running the application on an iOS
├── macos
├── linux
├── lib                           // Contains main.dart which is the flutter apps entry point
│   ├── screens                      
│   └── main.dart          
├── pubspec.yaml                  // Contains the metadata, configuration specific to the app
├── web
│   └── icons
└── pubspecam.lock                // It contain the version of each dependencies and packages
```

To run the application, start debugging by clicking **Run > Start Debugging** from the main IDE window (or press F5). If you are using [VS Code](https://code.visualstudio.com/), you should see a set of Flutter specific entries in the status bar, including a [Flutter SDK](https://docs.flutter.dev/get-started/install) version and a device name (or a message displaying No Devices). The Flutter extension automatically selects the latest device connected. However, if you have multiple devices/simulators connected, click device in the status bar to see a pick-list at the top of the screen. Select the device, you want to use for running, or debugging, and finally, run this application.

# CroMa - Under the Hood

The software project aims to use human-centric technology to take public transportation & crowd manangement one step ahead. We used Rapid Application Development model (RAD) to design several firmware components developed simultaneously, as if they were smaller individual projects. These are then assembled into the main working prototype.

### Defining the Problem Statements

**Problem  Statement 1:** 
Ramesh is a busy executive who needs to reach his office on time and decide whether to take a public bus for commuting or use his personal vehicle because he stays far away from the office & want to save money
<br>
**Hypothesis:**
If Ramesh uses CroMa for tracking the public buses available at his nearest bus-stop then he can plan his shuttle accordingly, & will reach his desired location at time, without needing to travel in an alternate public transport.

![test](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/blob/main/assets/CroMa_StoryboardDark.png#gh-dark-mode-only)
![test](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/blob/main/assets/CroMa_StoryboardLight.png#gh-light-mode-only)

**Problem Statement 2:**
Vartika is a seven month pregnant women who needs to board a long distance bus with ample seats available because she is agoraphobic, and her physical conditions does'nt allow her to stand for longer duration
<br>
**Hypothesis:**
If Vartika uses CroMa, for checking the buses in her proximity with less occupancy, then she can make an intelligent choice of the bus she wants to board, & can grab a seat, without needing to worry about standing for long.

### Understanding the Algorithm that Powers CroMa
CroMa's hardware cycle starts with the bus conductor initializing a new trip in the handheld ticketing machine by entering the BusId. The machine is now configured to the route associated with that Bus Id, and reflects the pre-set values for the three passenger data variables that are: total number of available seats, the current location and total number of passengers in bus. The ticketing machine now shows options for printing the tickets, displaying trip details (used by the conductors) and showing the total fare collections during the trip. More options ill be added in  the upcoming versions.

When a new passenger boards the bus, this bus conductor issues them a ticket after collecting information about their point of origin, intended destination, and total number of co-passengers, if any. Apart from printing tickets, the proposed ticketing machine sends this data to the firebase real-time database wherein the values for the previously mentioned three parameters are updated. The location data are collected by the GPS module. For passenger using concession cards, a QR code scanner is used. This ensures the authenticity of the card holder, as well as the proper updation of the crowd data.

Under the hood, total number of current passengers (default value zero, when the bus starts the trip) is calculated by adding the number of people who onboarded the bus at a given particular bus stop, and subtracting the number of passengers who deboarded the bus at that partcular bus-stop from the total number of passengers that were present in the previous bus stop. We already know that no passenger can onboard a bus between any two consecutive bus stops, and thus accurate crowd levels will be reflected. The bus fare is calculated by adding a variable fare (depending on the distance a passenger needs to travel) to the fixed fare (minimum payable). 

While developing this software, we have assumed that the bus fares will increase by a given amount, after every third stop the passenger needs to cross to reach his destination, starting from his origin point. The transport corporation can simply revise the bus fare by changing the values of the variable part and/or the fixed part. No changes to the hardware code is required.

Users waiting for on-boarding a bus can open the CroMa application on their mobile device. They need to initialize the application by posting a query, enteringg their destination, onboarding point and the required bus type. This app then fetches the list of all nearby buses that passes through their current location, & destination from the firebase real time databse and displays it to the user. The user can select a particular bus to view more details about the bus including the available number of seats, crowd levels in the bus, timings for buses with similar route, & expected fare.

The application uses Maps SDK to display the dynamic in-app map interface. The Directions API displays the directions of buses, featuring real-time traffic information. The Distance Matrix API is used to calculate the travel time and distances between the origins and the destinations. The  Geocoding API from Maps is used to convert coordinates into addresses and addresses into coordinates. Finally the Places SDK integrates place details, search, & autocomplete.

# Contribution Guidelines
To start contributing to the project, clone the repository into your local system subdirectory using the below git code:
```
git clone https://github.com/thisisashwinraj/CroMa-CrowdManagementSoftware.git
```
Before cloning the repository, make sure to navigate to the working subdirectory of your command line interface and ensure that no folder with same name exists. Other ways to clone the repository includes using a password protected [SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent), or by using [Git CLI](https://cli.github.com/). The changes may additionally be performed by opening this repo using GitHub Desktop

### Edit the Source Code and Make Desired Changes
To be able to make changes to the source, you may need to install and use a python IDE such as [PyCharm](https://www.jetbrains.com/pycharm/download/), Microsoft [VisualStudio](https://code.visualstudio.com/), and/or any other python interpreter. You will also require a Jupyter notebook  for working with the code snippets. To work with the Flutter application, you shall have [Flutter SDK](https://docs.flutter.dev/get-started/install) installed on your local computer, and a USB cable. Ensure that you are strictly following the basic programming standards, while introducing the desired updates

Before opening a Pull Request, it is recommended to have a look at the full contributing page to make sure your code complies with all the pull request guidelines. Please ensure that you satisfy the [~/Checklist](https://github.com/thisisashwinraj/CroMa-CrowdManagementSoftware/tree/main/Template%20Files/PULL_REQUEST_TEMPLATE) before submitting your PR.

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

# License and Project Status
CroMa, & all its resources are distributed under [Creative Commons Attribution - Non Commercial - No Derivs License](https://github.com/thisisashwinraj/CroMa-CrowdManagementSoftware/blob/main/LICENSE). The app is compatible with all operating systems. The latest released stable version of CroMa is v1.0.1, and is available to be used on all local system for general use through the mobile app. All releases are logged in the [~/StableVersions]()

Upcoming updates will include new features, optimized recommendations using AI/ML and support for other transits
<br>
All contributors may reproduce and share the licensed material in whole or in part for non-commercial purposes only
