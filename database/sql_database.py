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
This module contains methods for performing CRUD operations on the SQL databases.
It also holds provisions for authenticatinng the users & selective data fetching.

Included Functions:
    [1] retrieve_bus_data_from_sql_database
    [2] create_new_table
    [3] insert_bus_data
    [4] display_full_table
    [5] delete_bus_table

.. versionadded:: 1.3.0

Read more about the SQL databases used in CroMa in the :ref:`CroMa SQL Databases`
"""

import sqlite3
import datetime
from datetime import datetime


def retrieve_bus_data_from_sql_database(bus_id):
    """
    Function to retrieve the bus operator, & the bus type from the SQL database.

    The Bus Id is used as the database's primary key (unique value) to retrieve
    the bus operator, & bus type. None is returned in case when no key is found.

    .. versionadded:: 1.3.0

    Parameters:
        [str] bus_id: Bus Id is used to search the SQL DB for the required data

    Returns:
        [str] bus_operator: Organization's name responsible for managing the bus
        [str] bus_type: The type of the public bus as is defined by bus operator

    """
    # Set up connection to the SQL database
    conn = sqlite3.connect("croma_playground.db")
    cursor = conn.cursor()

    # Retrieve specific values from the table
    select_query = """
        SELECT BusOperator, BusType
        FROM Bus
        WHERE BusId = ?
    """
    # Execute the SQL query on the specified table
    cursor.execute(select_query, (bus_id,))
    result = cursor.fetchone()  # Fetch the records with the value

    # Close the database connection
    conn.close()
    return result  # Return the output as comma seprated values


def create_new_table(table_name):
    """
    Function to create a new table in the SQL database, with name passed in arg.

    This function creates new table in the croma_playground database as per the
    conditions laid out in the SQL query. This is for use by the CroMa dev team.

    .. versionadded:: 1.3.0

    Parameters:
        [str] table_name: Name of the table to be created

    Returns:
        None -> Creates a table with specified fields & stores it in the SQL DB

    """
    # Set up connection to the SQL database
    conn = sqlite3.connect("croma_playground.db")
    cursor = conn.cursor()

    # Create the table
    create_table_query = """
        CREATE TABLE IF NOT EXISTS ? (
            BusId TEXT PRIMARY KEY,
            BusOperator TEXT,
            BusType TEXT
        )
    """
    # Execute the SQL query on the specified table
    cursor.execute(create_table_query, (table_name,))
    conn.close()  # Close the connection to the SQL database


def insert_bus_data(table_name, new_bus_details):
    """
    Function to insert a set of new records into the table, in the SQL database.

    This function inserts multiple records into croma_playground database as per
    conditions laid out in this SQL query. This is for use by the CroMa dev team.

    .. versionadded:: 1.3.0

    Parameters:
        [str] table_name: Name of the table in which the data is to be inserted
        [str] new_bus_details: New details to be inserted into croma's database

    Returns:
        None -> Inserts multiple records into the specified table present in DB

    """
    # Set up connection to the SQL database
    conn = sqlite3.connect("croma_playground.db")
    cursor = conn.cursor()

    # Insert new records into the SQL Bus table
    insert_query = (
        "INSERT INTO " + table_name + " (BusId, BusOperator, BusType) VALUES (?, ?, ?)"
    )
    """
    insert_query = '''
        INSERT INTO Bus (BusId, BusOperator, BusType)
        VALUES (?, ?, ?)
    '''
    """
    # Add all new records into the specified table within the SQL database
    cursor.executemany(insert_query, new_bus_details)

    # Commit the changes to the database
    conn.commit()
    conn.close()  # Close the connection to the SQL database


def display_full_table(table_name):
    """
    Function to display all the records present in the table of the SQL database.

    This function displays all records of the table corresponding to the argument
    name, if present in CroMa database. Otherwise, it does not display any output.

    .. versionadded:: 1.3.0

    Parameters:
        [str] table_name: Name of the table which is to be displayed

    Returns:
        [str] rows -> Displays all records present in this table with name as arg

    """
    # Set up the connection to the SQL database
    conn = sqlite3.connect("croma_playground.db")
    cursor = conn.cursor()

    # Query to display all records of the table
    select_query = """
        SELECT * FROM ?
    """
    cursor.execute(select_query, (table_name,))  # Execute the SQL query

    # Fetch all rows from the result set
    rows = cursor.fetchall()
    conn.close()  # Close the connection to the database

    return rows  # Returns all records stored in the SQL table


def delete_bus_table(table_name):
    """
    Function to delete an entire table from the SQL database.

    This function deletes all records and the table corresponding to the argument
    name, if present in CroMa database. Otherwise, it does not perform any action.

    .. versionadded:: 1.3.0

    Parameters:
        [str] table_name: Name of the table which is to be deleted

    Returns:
        None -> The table, if exists is dropped entirely from the SQL database

    """
    # Set up the connection to the SQL database
    conn = sqlite3.connect("croma_playground.db")
    cursor = conn.cursor()

    # Delete the table, if it exists in the database
    delete_table_query = """
        DROP TABLE IF EXISTS ?
    """
    cursor.execute(delete_table_query, (table_name,))

    # Commit the changes to the database
    conn.commit()

    conn.close()  # Close the connection to the SQL database
