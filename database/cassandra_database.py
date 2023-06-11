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
The module contains methods for performing CRUD operations on Cassandra database.
It also holds provisions for authenticatinng the users & selective data updation.

Included Functions:
    [1] store_newsletter_subscriber_data_cassandra

.. versionadded:: 1.3.0

Read more about Cassandra database used in CroMa in the :ref:`CroMa Cassandra DB`
"""

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from ssl import PROTOCOL_TLSv1_2, SSLContext, CERT_NONE
import uuid

import database.database_credentials as database_credentials


def store_newsletter_subscriber_data_cassandra(email):
    """
    Function to store the email id of user who subscribed to receive newsletter.

    This method takes an email as the argument and stores it into the cassandra
    database's newsletter_subscribers table alongside a UUID as the primary key

    .. versionadded:: 1.2.0

    Parameters:
        [str] email: E-Mail Id of the user who subscribed to receive newsletter

    Returns:
        [str] status_message: Returns SUCCESS when query succeeds, else FAILED

    NOTE: User shall be authenticated for performing the data storage operation
    """
    try:
        # Set up authentication credentials from the credentials manager
        cassandra_username = database_credentials.CASSANDRA_CROMA_USERNAME
        cassandra_password = database_credentials.CASSANDRA_CROMA_PASSWORD

        # Create and configure SSL context for connecting to Cassandra using TLSv1.2 protocol
        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = CERT_NONE

        # Establish connection to the Cassandra cluster by providing the necessary details
        auth_provider = PlainTextAuthProvider(
            username=cassandra_username, password=cassandra_password
        )
        cluster = Cluster(
            ["croma-cassandra-db.cassandra.cosmos.azure.com"],
            port=10350,
            auth_provider=auth_provider,
            ssl_context=ssl_context,
        )
        session = cluster.connect()

        # Set keyspace croma as the active keyspace for subsequent database operations.
        session.execute("USE croma")

        email_id = (
            uuid.uuid4()
        )  # Generate a universally unique identifier to serve as primary key

        # Insert the email into the 'newsletter_subscriber_emails' table
        insert_query = session.prepare(
            "INSERT INTO newsletter_subscribers (id, email) VALUES (?, ?)"
        )
        session.execute(insert_query, (email_id, email))

        return (
            "SUCCESS"  # Return success message if the operation is executed succesfully
        )

    except:
        return "FAILED"  # Otherwise, return a failed message indicating an exception in the query
