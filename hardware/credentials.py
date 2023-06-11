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
This module provides the user's email credentials required for sending the mails
via SMTP. These credentials are necessary for authenticating the hardware user &
for establishing a secure TLS connection to the SMTP server for sending the mail.

Included Credentials:
    [1] SENDER_EMAIL_ID
    [2] CONDUCTOR_PASSWORD

.. versionadded:: 1.2.0

Read more about the functionality of the SMTP mails in :ref:`Daily Status Report`
"""

import streamlit

# E-mail id of the sender, from which the mail will be sent
SENDER_EMAIL_ID = streamlit.secrets["CONDUCTOR_EMAIL_ID"]
# App password for gmail for authorizing the user in SMTP session
CONDUCTOR_PASSWORD = streamlit.secrets["CONDUCTOR_PASSWORD"]
