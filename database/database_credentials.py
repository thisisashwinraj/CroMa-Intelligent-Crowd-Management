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
This module provides the user credentials for accessing the cassandra keyspace &
tables. These credentials are necessary for authenticating the admin user(s) and
for establishing a secure connection to the Azure CosmosDB for storing user data.

Included Credentials:
    [1] CASSANDRA_CROMA_USERNAME
    [2] CASSANDRA_CROMA_PASSWORD

.. versionadded:: 1.3.0

Read about the functionalities of the necessary APIs in :ref:`Databases in CroMa`
"""

import streamlit

# Username of the account accessing CassandraDB
CASSANDRA_CROMA_USERNAME = streamlit.secrets["CASSANDRA_CROMA_USERNAME"]
# Password of the account accessing CassandraDB
CASSANDRA_CROMA_PASSWORD = streamlit.secrets["CASSANDRA_CROMA_PASSWORD"]
