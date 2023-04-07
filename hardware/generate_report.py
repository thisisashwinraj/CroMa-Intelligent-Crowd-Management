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
This module contains the code for generating the daily status report in PDF format.
DSR report class holds distinct methods for printing the header, basic details and
several other trip parameters, that are to be used for daily analytical activities.

Included Classes and Methdds:
    [1] DSRReport
        [a] logo_header
        [b] print_basic_details
        [c] create_table
        [d] print_table_content
        [e] print_signature_and_date

.. versionadded:: 1.2.0

Read more about the use case of CroMa reports in :ref:`CroMa Reports and Analytics`
"""
import random
from datetime import date
from fpdf import FPDF

import terminal


class DSRReport(FPDF):
    """
    Class to generate the daily status report for a bus and store it in reports dir
    The DSRReport inherits from FPDF class of the fpdf module for generating PDF's.

    Daily Status Report (DSR) is a technical document generated at the end of a bus
    trip, which contains information regarding various aspects of the last bus trip.
    DSR includes information such as total number of passengers who boarded the bus
    during the trip, the overall load factor, crowd density and other relevant data.
    This report also contains information regarding any delays, official diversions,
    or incidents that occurred during the trip. The report is generated in PDF form

    The analytics team can then use this data to analyze the data & identify trends
    or pattern that can help improve the obverall management of public transport in
    the city. This may include adjusting bus routes & schedule, improving passenger
    communication, inspecting crowd level trends and/or optimizing the bus capacity.

    .. versionadded:: 1.2.0

    NOTE: During actual trips, the DSR reports are generated and mailed to the admin
    """

    def logo_header(self):
        """
        Method to add a boundary, and print the logos on top left section of the report.

        Plain single line boundary is added on the page. Further aesthetic improvements
        can be made to the enclosing bounadry by adding images, or other graphic assets.
        Logo of the organizations are also printed on the top left section of the pages.

        .. versionadded:: 1.2.0

        Parameters:
            None -> Images are read from ~/assets directory as per admin configruations

        Returns:
            None -> A boundary is placed over the page & organization's logo is printed

        NOTE: To change the logo of organizations, replace the image file in assets dir
        """
        self.rect(5.0, 5.0, 200.0, 287.0)  # Place a rectangular boundary over the page

        self.set_xy(
            14.0, 15.0
        )  # Set the current position on the page to (idx_x, idx_y)

        # Fetch the relative image path from the assets sub-directory
        image_loc = "hardware/assets/croma_letter_head_logo.png"
        # Print the organization's logo image the specified width and height
        self.image(image_loc, link="", type="", w=1586 / 30, h=1920 / 200)

    def print_basic_details(self):
        """
        Method to print basic details like BusId, Bus Route, Driver Id and Reference No.

        Print basic details such as bus id, bus route, driver id and reference no. on a
        pdf document. The method takes zero input parameters, and operates on the class
        attributes & the terminal module variables to retrieve the required information.

        .. versionadded:: 1.2.0

        Parameters:
            [class object] self -> Values are read from the memory as per configruation

        Returns:
            None -> Print basic details such as bus id, route & driver id on a pdf file

        NOTE: The reference number is a unique 12 charecter sequence in each DSR report
        """
        # Code block to display the label for Bus Id
        self.set_xy(15.0, 40.0)  # Set x-y position for displaying the Bus Id label
        self.set_font("Arial", "B", 12)  # Set the font style for Bus Id label
        self.cell(w=10, h=10, align="C", txt="Bus Id:", border=0)  # Print the label

        # Code block to display the value for Bus Id
        self.set_xy(30.0, 40.0)  # Set x-y position for displaying the Bus Id
        self.set_font("Arial", "", 12)  # Set the font style for Bus Id
        self.cell(w=10, h=10, align="C", txt=terminal.bus_id, border=0)  # Print value

        # Code block to display the label for Bus Route
        self.set_xy(19.0, 48.0)  # Set x-y position for displaying the Bus Route label
        self.set_font("Arial", "B", 12)  # Set the font style for Bus Route label
        self.cell(w=10, h=10, align="C", txt="Bus Route:", border=0)  # Print the label

        # Code block to display the value for Bus Route
        self.set_xy(54.0, 48.0)  # Set x-y position for displaying the Bus Route
        self.set_font("Arial", "", 12)  # Set the font style for Bus Route
        self.cell(
            w=10, h=10, align="C", txt=terminal.bus_route, border=0
        )  # Print value

        # Code block to display the label for Driver Id
        self.set_xy(154.0, 48.0)  # Set x-y position for displaying the Driver Id label
        self.set_font("Arial", "B", 12)  # Set the font style for Driver Id label
        self.cell(w=10, h=10, align="C", txt="Driver Id:", border=0)  # Print the label

        # Code block to display the value for Driver Id
        self.set_xy(178.0, 48.0)  # Set x-y position for displaying the Driver Id
        self.set_font("Arial", "", 12)  # Set the font style for Driver Id
        self.cell(w=10, h=10, align="C", txt="KSR14D132A", border=0)  # Print value

        # Code block to display the label for Reference Id
        self.set_xy(
            22.9, 56.0
        )  # Set x-y position for displaying the Reference Id label
        self.set_font("Arial", "B", 12)  # Set the font style for Reference Id label
        self.cell(
            w=10, h=10, align="C", txt="Reference No.:", border=0
        )  # Print the label

        length = 3  # Define the length of the Reference Id to be generated
        alphabets = (
            "QWERTYUIOPASDFGHJKLZXCVBNM"  # String containing all upper case letters
        )
        numbers = "1234567890"  # String containing all numbers from 0 to 9

        # Generates four random strings of length 3, two with alphabets and 2 with numbers
        substring1 = "".join((random.choice(alphabets)) for _ in range(length))
        substring2 = "".join((random.choice(numbers)) for _ in range(length))

        substring3 = "".join((random.choice(alphabets)) for _ in range(length))
        substring4 = "".join((random.choice(numbers)) for _ in range(length))

        # Concatenate the randomly generated strings to generate the Reference id
        reference_id = substring1 + substring2 + substring3 + substring4

        # Code block to display the value for Reference Id
        self.set_xy(55.0, 56.0)  # Set x-y position for displaying the Reference Id
        self.set_font("Arial", "", 12)  # Set the font style for Reference Id
        self.cell(w=10, h=10, align="C", txt=reference_id, border=0)  # Print value

        # Code block to display the label for Conductor Id label
        self.set_xy(
            149.6, 56.0
        )  # Set x-y position for displaying the Conductor Id label
        self.set_font("Arial", "B", 12)  # Set the font style for Reference Id
        self.cell(w=10, h=10, align="C", txt="Conductor Id:", border=0)  # Print label

        # Code block to display the value for Conductor Id
        self.set_xy(178.0, 56.0)  # Set x-y position for displaying the Conductor Id
        self.set_font("Arial", "", 12)  # Set the font style for Conductor Id
        self.cell(w=10, h=10, align="C", txt="KSR14C213D", border=0)  # Print value

    def create_table(self):
        """
        Method to print an empty table with five columns, and one row in the DSR report.

        Prints a table on the current PDF canvas using a rectangle and 5 straight lines.
        This table has four columns & is to be used to display data in an organized way.

        .. versionadded:: 1.2.0

        Parameters:
            [class object] self -> Values are fed into the method as per configruations

        Returns:
            None -> Print table with five columns, & one row to hold data in the report

        NOTE: More rows can be added to the table by incresing the sizeof the rectangle
        """
        self.rect(13.8, 80.0, 183.0, 25.0)  # Draw rectangle that serves as table border

        # Draw the horizontal line that separates column headers from rest of the table
        self.line(13.8, 90.0, 196.8, 90.0)  # It does'nt need to be changed on expanding

        self.line(50.3, 80.0, 50.3, 105.0)  # Draw vertical lines that separates columns
        self.line(86.8, 80.0, 86.8, 105.0)  # Draw vertical lines that separates columns

        self.line(123.3, 80.0, 123.3, 105.0)  # Draw vertical line that separates column
        self.line(159.8, 80.0, 159.8, 105.0)  # Draw vertical line that separates column

    def print_table_content(self):
        """
        This method prints important trip details, such as load factor on the PDF report.

        Print the content of the table which includes Total Passenger, Collection & more.
        This method sets the font type, size, position, and alignment of the text on the
        PDF page using the set_xy() function, and the cell() functions of the FPDF class.

        .. versionadded:: 1.2.0

        Parameters:
            [class object] self -> Values are read from the memory as per configruations

        Returns:
            None -> Print important details, such as load factor & collections on a file

        NOTE: More row can be added to the table by increasing the size of the rectangle
        """
        # Code block to display the label for total passengers count
        self.set_xy(
            27.0, 80.5
        )  # Set x-y position for displaying total passengers label
        self.set_font("Arial", "B", 11)  # Set the font style for total passengers label

        self.cell(
            w=10, h=10, align="C", txt="Total Passengers", border=0
        )  # Print total passengers label

        # Code block to display the value for total passengers count
        self.set_xy(27.0, 92.5)  # Set x-y position for displaying the total passengers
        self.set_font("Arial", "", 11)  # Set the font style for total passengers

        self.cell(
            w=10, h=10, align="C", txt=str(terminal.passengers_per_trip), border=0
        )  # Print total passengers value

        # Code block to display the label for total collections
        self.set_xy(
            63.2, 80.5
        )  # Set x-y position for displaying total collections label
        self.set_font(
            "Arial", "B", 11
        )  # Set the font style for total collections label

        self.cell(
            w=10, h=10, align="C", txt="Total Collections", border=0
        )  # Print total collections label

        # Code block to display the value for total collections
        self.set_xy(63.6, 92.5)  # Set x-y position for displaying the total collections
        self.set_font("Arial", "", 11)  # Set the font style for total collections

        self.cell(
            w=10, h=10, align="C", txt=str(terminal.collection), border=0
        )  # Print total collection value

        # Code block to display the label for load factor
        self.set_xy(100.0, 80.5)  # Set x-y position for displaying load factor label
        self.set_font("Arial", "B", 11)  # Set the font style for load factor label

        self.cell(
            w=10, h=10, align="C", txt="Load Factor", border=0
        )  # Print load factor label

        # Code block to display the value for load factor
        self.set_xy(100.0, 92.5)  # Set x-y position for displaying the load factor
        self.set_font("Arial", "", 11)  # Set the font style for load factor

        self.cell(
            w=10, h=10, align="C", txt=str(round(terminal.load_factor, 2)), border=0
        )  # Print load factor value

        # Code block to display the label for max boarding
        self.set_xy(
            136.2, 80.5
        )  # Set x-y position for displaying the max boarding label
        self.set_font("Arial", "B", 11)  # Set the font style for max boarding

        self.cell(
            w=10, h=10, align="C", txt="Max Boarding", border=0
        )  # Print max boarding label

        # Code block to display the value for max boarding
        self.set_xy(136.4, 92.5)  # Set x-y position for displaying the max boarding
        self.set_font("Arial", "", 11)  # Set the font style for max boarding

        self.cell(
            w=10, h=10, align="C", txt=str(terminal.MAX_BOARDING_BUS_STOP), border=0
        )  # Print max boarding value

        # Code block to display the label for max deboarding
        self.set_xy(
            172.0, 80.5
        )  # Set x-y position for displaying the max deboarding label
        self.set_font("Arial", "B", 11)  # Set the font style for max deboarding label

        self.cell(
            w=10, h=10, align="C", txt="Max Deboarding", border=0
        )  # Print max deboarding label

        # Code block to display the value for max deboarding
        self.set_xy(172.8, 92.5)  # Set x-y position for displaying the max deboarding
        self.set_font("Arial", "", 11)  # Set the font style for max deboarding

        self.cell(
            w=10, h=10, align="C", txt=str(terminal.MAX_DEBOARDING_BUS_STOP), border=0
        )  # Print max deboarding value

    def print_signature_and_date(self):
        """
        This method attests the report with signature of the admin & adds thew timestamp

        Attest the DSR report with administrator signature and add the timestamp. Source
        image for the administrators signature is maintained in the assets sub-directory.

        .. versionadded:: 1.2.0

        Parameters:
            [class object] self -> Values are read from the system as per configruations

        Returns:
            None -> Attest the document with admin's signature and mention the timestamp

        NOTE: To change the signature of the admin, replace the image file in assets dir
        """
        self.line(
            13.8, 140.0, 63.8, 140.0
        )  # Draw a signature line in the middle section

        self.set_xy(
            18.0, 126.0
        )  # Set x-y position for displaying the admin's signature

        # Specify the location of the image file in the image_loc variable
        image_loc = "hardware/assets/signature.png"

        # Resize the image to 39.65mm wide and 24mm tall and print it on the report
        self.image(image_loc, link="", type="", w=1586 / 40, h=1920 / 80)

        self.set_xy(38.2, 142.0)  # Set x-y position for displaying the signature label
        self.set_font("Arial", "", 11)  # Set the font style for signature label

        self.cell(
            w=10, h=10, align="C", txt="KSRTC Southern Cluster Manager", border=0
        )  # Print signature label

        self.set_xy(157.6, 142.0)  # Set x-y position for displaying the timestamp label
        self.set_font("Arial", "B", 12)  # Set the font style for the date label

        self.cell(w=10, h=10, align="C", txt="Date:", border=0)  # Print date label

        today = date.today()  # Define the textual month, day and year
        todays_date_time = today.strftime(
            "%B %d, %Y"
        )  # Format today variable as a string

        self.set_xy(
            178.0, 142.0
        )  # Set x-y position for displaying the current timestamp
        self.set_font("Arial", "", 11)  # Set the font style for today's date

        self.cell(
            w=10, h=10, align="C", txt=todays_date_time, border=0
        )  # Print date value
