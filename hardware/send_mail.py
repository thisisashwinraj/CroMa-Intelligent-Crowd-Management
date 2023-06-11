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
This module contains the code for sending emails with attachments using the SMTP
protocol. It can be used to send both plain text mails, and rich text HTML mails
after changing payload to encoded format. This module uses smtp.gmail.com server 
at port 587 for sending the mails with MIMEBase payloads, and base64 attachments

Included Functions:
    [1] DSR_Mail
        [a] send_dsr_mail
    [2] BugReportMail
        [a] send_bug_report_mail

.. versionadded:: 1.2.0

Read more about the usecase of mail triggering in :ref:`Bus Reports and E-mails`
"""

import smtplib
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from email import encoders
from email.mime.application import MIMEApplication

from hardware import terminal
from hardware import credentials  # pylint: disable=import-error


class DSRMail:  # pylint: disable=too-few-public-methods
    """
    Class to send a DSR (Daily Status Report) email with an attachment to the admin.

    Daily Status Report (DSR) is a technical document generated at the end of a bus
    trip, which contains information regarding various aspects of the last bus trip.
    DSR includes information such as total number of passengers who boarded the bus
    during the trip, the overall load factor, crowd density and other relevant data.
    This report also contains information regarding any delays, official diversions,
    or incidents that occurred during the trip. The report is generated in PDF form

    The mail is sent to the receiver's email id (in this case, the admin or cluster
    manager) using the smtp.gmail.com server at port 587 alongside all the payloads.

    .. versionadded:: 1.2.0
    .. versionupdated:: 1.3.0

    NOTE: During actual trips, the DSR reports are generated and mailed to the admin
    """

    # Set the receiver e-mail id as the administrator's e-mail id
    terminal.RECEIVER_EMAIL_ID = "rajashwin812@gmail.com"

    def send_dsr_mail(self, bus_id):
        """
        Method to send a DSR (Daily Status Report) mail with an attachment to the admin

        Sends an email from the support team's mail id to the administrators mail using
        the smtp.gmail.com server at port 587 along with a PDF attachment, as a payload.

        .. versionadded:: 1.2.0
        .. versionupdated:: 1.3.0

        Parameters:
            None -> All variables are read from the system memory as per configruations

        Returns:
            None -> Sends an email with atttachment to the receivers mail id using SMTP

        NOTE: Credentials file holding the app key should be maintained in a secure env
        """
        email = MIMEMultipart()  # Create an instance of MIMEMultipart

        # Store the senders email address in the To field
        email["From"] = credentials.SENDER_EMAIL_ID
        # Store the receivers email address in the from field
        email["To"] = terminal.RECEIVER_EMAIL_ID

        today = datetime.now()  # Fetch todays timestamp with date and time
        todays_date_time = today.strftime(
            "%d/%m/%Y %H:%M:%S"
        )  # Cast the date as string

        # Store the subject of the email with timestamp in the mail's subject field
        email["Subject"] = bus_id + " DSR Report " + str(todays_date_time)

        # Store the body of the mail in the function variable named body
        body = (
            "Hello,\n\nPlease find attached the DSR Report for Bus Id: "
            + bus_id
            + "'s journey as on "
            + todays_date_time
            + ".\n\nThanks,\nCroMa Support Team"
        )

        email.attach(MIMEText(body, "plain"))  # Attach the body with the email instance

        filename = "DSR_Report.pdf"  # open the file to be sent in the filename variable
        attachment = open(
            "hardware/reports/DSR_Report.pdf", "rb"
        )  # pylint: disable=consider-using-with

        # Create an instance of MIMEBase and named as payload
        payload = MIMEBase("application", "octet-stream")
        payload.set_payload((attachment).read())  # Change the payload into encoded form

        encoders.encode_base64(payload)  # Encode the payload into base-64 form
        payload.add_header(
            "Content-Disposition", "attachment; filename= %s" % filename
        )  # pylint: disable=consider-using-f-string

        email.attach(payload)  # Attach the instance 'payload' to the instance 'email'

        smtp_session = smtplib.SMTP("smtp.gmail.com", 587)  # Create an SMTP session
        smtp_session.starttls()  # Encrypt the connection using transport layer security

        # Authenticate the sender before sending the email to the receiver
        smtp_session.login(credentials.SENDER_EMAIL_ID, credentials.CONDUCTOR_PASSWORD)

        text = (
            email.as_string()
        )  # Converts the Multipart mail into a string & send the mail
        smtp_session.sendmail(
            credentials.SENDER_EMAIL_ID, terminal.RECEIVER_EMAIL_ID, text
        )  # Perform entire mail transaction

        smtp_session.quit()  # Terminate the SMTP session after sending the mail


class BugReportMail:  # pylint: disable=too-few-public-methods
    """
    Class to send bug report emails with form info and file attachments to the admin

    The bug report typically includes information about the error including steps to
    reproduce the issue, the expected behavior, and the actual behavior observed. It
    also includes details about the user's environment such as the operating systems,
    software version and hardware details. These reports help developers to identify
    & fix the reported issue - improving the software's functionality, & performance

    The mail is sent to the receiver's email id (in this case, the admins or cluster
    managers) using the smtp.gmail.com server at port 587 alongside all the payloads.

    .. versionadded:: 1.2.0

    NOTE: Credentials file holding the app keys should be maintained in a secure env
    """

    # Set the receiver e-mail id as the admin's e-mail id
    terminal.RECEIVER_EMAIL_ID = "rajashwin812@gmail.com"

    def send_bug_report_mail(attachment=None):  # pylint: disable=no-self-argument
        """
        Method to send a mail with a bug report, reported by a user to CroMa's dev team

        Sends an email from the support team's mail id to the dev team's email id using
        the smtp.gmail.com server at port 587 along with a PDF attachment, as a payload.

        .. versionadded:: 1.2.0

        Parameters:
            [file] attachment: A pdf file or an image file to be attached to the e-mail
            None -> All variables are read from the system memory as per configruations

        Returns:
            None -> Sends an email with atttachment to the receivers mail id using SMTP

        NOTE: Credentials file holding the app key should be maintained in a secure env
        """
        message = MIMEMultipart()  # Create an instance of MIMEMultipart

        message[
            "To"
        ] = terminal.RECEIVER_EMAIL_ID  #  Store the receivers mail id in the To field
        message[
            "From"
        ] = credentials.SENDER_EMAIL_ID  # Store the senders mail id in the From field
        message[
            "Subject"
        ] = "Bug Report"  # Store the subject of the mail in the subject field

        terminal.br_mail_body = (
            "Hello,\n\nA new bug report has been raised for CroMa "
            + "Hardware Playground. Please find the details as mentioned below.\n\nFull Name: "
            + terminal.br_full_name
            + "\n\nE-Mail Id: "
            + terminal.br_email_id
            + "\n\nPage with Bug: "
            + terminal.br_bug_in_page
            + "\n\nType of Bug: "
            + terminal.br_bug_type
            + "\n\nDescription: "
            + terminal.br_bug_description
            + "\n\nRegards,\nCroMa Support Team"
        )  # Store the body of the mail in the function variable named br_mail_body

        message.attach(
            MIMEText(terminal.br_mail_body, "plain", "utf-8")
        )  # Attach body with email instance

        # Check if a file is provided as an attachment to be sent across
        if attachment:
            att = MIMEApplication(
                attachment.read()  # pylint: disable=no-member
            )  # Read the attachment using read method
            att.add_header(
                "Content-Disposition",
                "attachment",
                filename=attachment.name,  # pylint: disable=no-member
            )
            message.attach(att)  # Attach the file to the email

        server = smtplib.SMTP(
            "smtp.gmail.com", 587
        )  # Create an SMTP session at Port 587
        server.starttls()  # Encrypt the connection using transport layer security
        server.ehlo()  # Hostname to send for this command defaults to the FQDN of the local host.

        # Authenticate the sender before sending the email to the receiver
        server.login(credentials.SENDER_EMAIL_ID, credentials.CONDUCTOR_PASSWORD)
        text = (
            message.as_string()
        )  # Converts the Multipart mail into a string & send the mail

        # Perform entire mail transaction
        server.sendmail(credentials.SENDER_EMAIL_ID, terminal.RECEIVER_EMAIL_ID, text)
        server.quit()  # Terminate the SMTP session after sending the mail
