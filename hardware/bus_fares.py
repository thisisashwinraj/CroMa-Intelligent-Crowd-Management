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
This module contains the pricing parameters for decising fares.
To update the bus fares, simply  update the value of these parameters

Fare Calculation Variables:
    [1] Fixed Ticket Price
    [2] Variable Ticket Price

.. versionadded:: 1.0.1
.. versionupdated:: 1.1.0

NOTE: The fixed price and variable price changes as per the selected bus type
Read more about ticket pricing in the :ref:`Fare Calculation & Pricing Model`.
"""

# Minimum cost charged for the first three stops
FIXED_TICKET_PRICE = 10

# Succesived additinal costs charged for crossing every next three stops
VARIABLE_TICKET_PRICE = 6
