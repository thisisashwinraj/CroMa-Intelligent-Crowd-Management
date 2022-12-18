![CroMa Banner](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/blob/main/assets/CroMa_Banner_Light.png#gh-light-mode-only)
![CroMa Banner](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/blob/main/assets/CroMa_Banner_Dark.png#gh-dark-mode-only)

CroMa is an android application that uses a python backend hardware, built on raspberry pi integrated with a firebase real-time database and flutter framework for efficient crowd management in public transports such as buses & taxies. The hardware is effectively a handheld ticketing machine used for printing tickets, and collecting selective information about passengers. After data processing, the mobile application displays the output to the users. No LogIn's required.

The project development started in April 2022 as a group project and has been licensed under the [Creative Commons Attribution - Non Commercial - No Derivs License](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/blob/main/LICENSE) (CC-BY-NC-ND). The passenger data collected, is maintained as per the Privacy Policy. The pull requests are maintained by a team of [contributors](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System#all-contributors). Learn more about CroMa software [here](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System#user-installation-and-working)

# SubDirectories and Constraints
### Software Dependencies
• **Mobile App:** Dart, [Flutter](https://docs.flutter.dev/get-started/install), Maps SDK, Places SDK, Distance Matrix API, Directions API, Roads API, and Geocoding API
<br>
• **Ticket Machine:** [Python 3.7](https://www.python.org/downloads/release/python-370/), Firebase (Real-Time Database), RaspberryPi and [ArduinoUNO](https://docs.arduino.cc/hardware/uno-rev3) | Dependencies: [Pyrebase](https://pypi.org/project/Pyrebase/)

### Files and SubDirectories
• **Mobile Application:** This directory contains the Dart code and afilliated resources for building the flutter application
<br>
• **Ticketing Machine:** This directory contains the Python3 code for designing the hand-held ticketing machine, and DB

All relevant updates, and stable versions are made available in the [~/stableVersion](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/tree/main/template_files/stable_versions) sub-directory. Some subdirectories may be sensitive for the project and may trigger review requests, when pull requests touch these files. Github handles with commit rights made available in the [~/Template Files/CODEOWNERS](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/blob/main/template_files/CODEOWNERS) are responsible for reviewing such changes

# User Installation and Working
CroMa is a firmware solution that provides commuters with real-time information about public transits(such as buses) including real-time tracking, estimated time-of-arrival and the seat occupancy. This solution is an interworking of two major components: a [handheld ticketing machine](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/tree/main/hardware_files) and a [mobile application](https://github.com/thisisashwinraj/CroMa-Crowd-Management-System/tree/main/android). CroMa v1.0 offers support for only buses.

The hand-held ticketing machine is a micro-controller-based system used for generating billing tickets and collecting, saving, and generating daily reports and summaries. Our version of the hardware is additionally equipped with a GPS module for tracking the location of the bus. The device is to be used by conductors, and/or clippies for issuing tickets to the passengers. When new passengers board this bus, their details such as their start location, total luggage in the bus, their intended destination, & the total number of passengers is collected for issuing the tickets. These details are collected, processed and transmitted to the [FireBase RT database](https://firebase.google.com/products/realtime-database) by the hand-held ticketing machine. For passengers using a monthly, or yearly bus pass, a QR code or a unique alphanumerical code may be used to update the software.

![CroMa App](https://github.com/thisisashwinraj/CroMa-CrowdManagementSoftware/blob/main/assets/CroMaAppUI.png)

The passengers data is maintained in the FireBase Real-Time database for synchronizing this data across devices. This data is structured as a JSON tree with the data points stored as JSON objects. The parent nodes represents the Bus Id (unique to each bus) and the real-time data associated with the bus (including available seats, & current location, etc) are maintained as nested nodes. Whenever a new ticket is issued the database is updated. The algorithm ensures that the database is updated when passengers de-board the bus. The data maintained in this [FireBase RT database](https://firebase.google.com/products/realtime-database) is then made available to be fetched by the android mobile application, and the relevant machine learning models, and API's.

<p align = "justify">
The android app is the end-user's application that allows the user to compare various transit options, and choose the most ideal option that fits their needs. The users, start with opening the application, and making a query, by entering their starting point, intended destination, and the type of bus (fast, SPF, express, deluxe, etc). No LogIn is required for using the android mobile app. The application looks up into the data base, and displays the location of buses in real-time within a pre set radius that passes through both their starting point and the destination entered by the user. The bus markers with red colour indicates heavy rush, while the green color indicates light occupancy. On tapping a given bus marker, the application displays more details about that bus to the users including, their estimated time of arrival, seat occupancy & ETA of buses on same route etc. Users can compare multiple options to make an informed decision
</p>

To run the ticketing machine's sofware on a local computer, open the terminal, install [pyrebase](https://pypi.org/project/Pyrebase/), & type the command:
```
python ticketingMachine.py
```

CroMas development take place on GitHub. Please submit any bug that you may encounter to the issue tracker with a reproducible example demonstrating the problem, in accordance with the issue template, present in contributing files

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

To run the application, start debugging by clicking **Run > Start Debugging** from the main IDE window (or press F5). If you are using [VS Code](https://code.visualstudio.com/), you should see a set of Flutter specific entries in the status bar, including a [Flutter SDK](https://docs.flutter.dev/get-started/install) version and a device name (or a message displaying No Devices). The Flutter extension automatically selects the latest device connected. However, if you have multiple devices/simulators connected, click device in the status bar to see a pick-list at the top of the screen. Select the device, you want to use for running, or debugging, and finally, run this application.

# CroMa - Under the Hood

The software project aims to use human-centric technology to take public transportation & crowd manangement one step ahead. We used [Rapid Application Development model](https://en.wikipedia.org/wiki/Rapid_application_development) (RAD) to design several firmware components developed simultaneously as if they were smaller individual projects. These are then assembled into the main working prototype.

### Defining the Problem Statements

**Problem  Statement 1:** 
Ramesh is a busy executive who needs to reach his office on time and decide whether to take a public bus for commuting or use his personal vehicle as he stays very far away from the office & want to save money
<br>
**Hypothesis:**
If Ramesh uses CroMa for tracking the public buses available at his nearest bus-stop then he can plan his shuttle accordingly & will reach his desired location at time, without needing to travel in an alternate public transport.

**Problem Statement 2:**
Vartika is a seven month pregnant women who needs to board a long distance bus with ample seats available because she is agoraphobic, and her physical conditions does'nt allow her to stand for longer duration
<br>
**Hypothesis:**
If Vartika uses CroMa, for checking the buses in her proximity with less occupancy, then she can make an intelligent choice of the bus she wants to board, & can grab a seat, without needing to worry about standing for long.

### The Logic that Powers the System
<p align="justify">
The system's hardware cycle starts with the bus conductor initializing a new trip in the handheld ticketing machine by entering the Bus Id. This machine is now configured to the routes associated with that Bus Id, and reflects the pre-set values for necessary passenger data variables, that are: total number of available seats, the current location, and total number of passengers in bus. The ticketing machine now shows options for printing the tickets, displaying trip details (used by conductors), and showing the total fare collections, during the trip. More options will be added in the future.

When new passenger boards this bus, the bus conductor issues them a bus ticket after collecting informations about their point of origin, intended destination & the total number of copassengers, if any. Apart from printing tickets, the proposed ticketing machine sends this data to the FireBase real-time database, wherein, the values for the previously mentioned three parameters are updated. Bus's location data are collected by the GPS module. For passengers using concession cards, a QR code scanner is used. This ensures authenticity of the card holder, & proper updation of data.

Under the hood, total number of current passengers (default value zero, when the bus starts the trip) is calculated by adding total number of people who onboarded the bus at a given particular bus stop and subtracting the number of passengers who deboarded the bus at that partcular busstop from the total number of passengers that were present in the previous bus stop. We already know that no passenger can onboard the bus between any two consecutive bus stops, and thus accurate crowd level will be reflected. The bus fare is calculated by adding a variable fare (depending on the distance the passenger needs to travel to reach their destination) to the fixed fare (minimum payable amount)

While developing this software, we have assumed that the bus fares will increase by a given amount, after every third stop the passenger needs to cross to reach his destination, starting from their origin point. The transport corporation can simply revise the bus fare by changing the values of the variable part or the fixed part. No code changes required

The passengers waiting for onboarding the bus can open the CroMa application on their mobile device. They need to initialize this application by posting a query, entering their destination, on-boarding point, and the required bus type. This app then fetches the list of all near-by buses, that passes through their current location and destination from the firebase real time databse, and displays it to the user. The user can select a given bus to view more information about that bus including the available number of seats, crowd levels in that bus, timings for buses with similar routes & fare.

The application uses Maps SDK to display the dynamic in-app map interface. The Directions API displays information on directions of buses, featuring real-time traffic information. The Distance Matrix API are used to calculate the travel time and distances between the origins, and the destinations. The  Geocoding APIs from Maps SDK is used to convert coordinates into addresses & addresses into coordinates. Places SDK integrates place details, search & autocomplete.
<p align = "justify">
  
# Contribution Guidelines
To start contributing to the project, clone the repository into your local system subdirectory using the below git code:
```
git clone https://github.com/thisisashwinraj/CroMa-Crowd-Management-System.git
```
Before cloning the repository, make sure to navigate to the working subdirectory of your command line interface and ensure that no folder with same name exists. Other ways to clone the repository includes using a password protected [SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent), or by using [Git CLI](https://cli.github.com/). The changes may additionally be performed by opening this repo using [GitHub Desktop](https://desktop.github.com/)

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

### All Contributors
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://www.linkedin.com/in/thisisashwinraj/"><img src="https://avatars.githubusercontent.com/u/62590141?v=4" width="100px;" alt=""/><br /><sub><b>Ashwin Raj</b></sub></a><br /><a href="#" title="Hardware Team">:computer:</a></td>
      <td align="center"><a href="https://www.google.com"><img src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmTj-nbO8zR4gGO-k8PPMaJk84plUgJCwiuJe3MoNM8l0SqzVtNpkh1sMXNxyZzVYKmfudguLe8=w1366-h597" width="100px;" alt=""/><br /><sub><b>Anjali PA</b></sub></a><br /><a href="#" title="Database Team">:computer:</a></td>
      <td align="center"><a href="https://www.linkedin.com/in/vishnu-rk-a8b4b81b5/"><img src="https://media-exp1.licdn.com/dms/image/C4E03AQEcTmDwrsLCCw/profile-displayphoto-shrink_800_800/0/1650949192384?e=1669852800&v=beta&t=KqteebIKCRemO5ErX0zGaqZt-ilx50iSY56snUDqrkk" width="100px;" alt=""/><br /><sub><b>Vishnu RK</b></sub></a><br /><a href="#" title="Mobile Team">:computer:</a></td>
      <td align="center"><a href="https://www.linkedin.com/in/asiya-r-ashkar-b2a053226/"><img src="https://ernglobal.org/wp-content/uploads/2017/10/default-user-image.png" width="100px;" alt=""/><br /><sub><b>Asiya R Ashkar</b></sub></a><br /><a href="#" title="Hardware Team">:computer:</a></td>
      <td align="center"><a href="https://www.linkedin.com/in/hariharan-g-8b3071230/"><img src="https://media-exp1.licdn.com/dms/image/C4D03AQE0YFMeWQsNhQ/profile-displayphoto-shrink_800_800/0/1642942804514?e=1669852800&v=beta&t=V4seEtab_bRJaHH7TKP8MSPXNiWpsrMJ3-4jpFA48QU" width="100px;" alt=""/><br /><sub><b>Hariharan G</b></sub></a><br /><a href="#" title="Database Team">:computer:</a></td>
      <td align="center"><a href="https://www.linkedin.com/in/devi-a-855b431b4/"><img src="https://lh3.googleusercontent.com/drive-viewer/AJc5JmSnPSxBCQHfrYmBlNMp22x5LVVQGxUMitJ3qXtKn4GquO67cP164skL7Ye4_FkI4iILsDZ4jAQ=w1366-h597" width="100px;" alt=""/><br /><sub><b>Devi A</b></sub></a><br /><a href="#" title="Mobile Team">:computer:</a></td>
      <td align="center"><a href="https://www.google.com"><img src="https://ernglobal.org/wp-content/uploads/2017/10/default-user-image.png" width="100px;" alt=""/><br /><sub><b>Vishnu Vinod</b></sub></a><br /><a href="#" title="Database Team">:computer:</a></td>
    </tr>
  </tbody>
</table>

# Data Security and Privacy
Safegaurding your data starts with understanding how CroMa collects, and processes your personal info. The in-hand ticketing machine only collects data pertaining to the user's starting location, destination, and the total number of co-passengers. When this data is shared, all that CroMa records is that a few passengers bought ticket(s) and onboarded the bus, but it doesn't know who they exactly are. CroMa does not collect your personal data in any form. Similarly on the mobile app's side, it does'nt require users to log-in to the application. They can simply startoff without signing up.

The Firebase database are secured by means of firebase rules. The Firebase rules ensure that only authenticated users are allowed to manipulate the data. This includes real time passenger data collected by a given bus during its journey

# License and Project Status
CroMa & all its resources are distributed under [Creative Commons Attribution - Non Commercial - No Derivs License](https://github.com/thisisashwinraj/CroMa-CrowdManagementSoftware/blob/main/LICENSE). The app is compatible with all operating systems. The latest released stable version of CroMa is v1.0.1, and is available to be used on all local system for general use through the mobile app. All releases are logged in the [~/StableVersions]()

Upcoming updates will include new features, optimized recommendations using AI/ML and support for other transits
<br>
All contributors may reproduce and share the licensed material in whole or in part for non-commercial purposes only

