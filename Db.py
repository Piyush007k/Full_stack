import sqlite3
import pandas as pd
from datetime import datetime
 
 
def get_db_conn():
    conn = sqlite3.connect('data.db')
    return conn
 
def create_organization_table(conn):
    mycursor = conn.cursor()
    mycursor.execute('''
    CREATE TABLE IF NOT EXISTS organization_table (
        Org_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Org_name TEXT NOT NULL,
        API_KEY TEXT NOT NULL
    ) ''')
    print('Created organization table')
    return mycursor
 
def create_agency_table(conn):
    mycursor = conn.cursor()
    mycursor.execute('''
    CREATE TABLE IF NOT EXISTS agency_table (
        agency_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Org_id INTEGER,
        Agency_name TEXT NOT NULL,
        Agency_email TEXT NOT NULL,
        FOREIGN KEY(Org_id) REFERENCES organization_table(Org_id)
    )''')
    print('Created agency table')
    return mycursor
 
def create_user_table(conn):
    mycursor = conn.cursor()
    mycursor.execute('''
    CREATE TABLE IF NOT EXISTS user_table (
        EMP_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Org_id INTEGER,
        Access_level TEXT NOT NULL,
        User_name TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL,
        IsAdmin TEXT NOT NULL,
        Application TEXT NOT NULL,
        FOREIGN KEY(Org_id) REFERENCES organization_table(Org_id)
    )''')
    print('Created user table')
    return mycursor

def display_agency_table(conn):
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM agency_table")
    rows = mycursor.fetchall()

    if not rows:
        print("Agency table is empty")
    else:
        print("Contents of agency_table:")
        for row in rows:
            print(row)
            
def display_user_table(conn):
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM user_table")
    rows = mycursor.fetchall()

    if not rows:
        print("User table is empty")
    else:
        print("Contents of user_table:")
        for row in rows:
            print(row)
            
def insert_organization(conn, Org_id, Org_name, API_KEY):
    mycursor = conn.cursor()
    mycursor.execute("INSERT INTO organization_table (Org_id, Org_name, API_KEY) VALUES (?, ?, ?)", (Org_id, Org_name, API_KEY))
    conn.commit()
    print("Inserted into organization_table")

def insert_agency(conn, Org_id, Agency_name, Agency_email):
    mycursor = conn.cursor()
    mycursor.execute("INSERT INTO agency_table (Org_id, Agency_name, Agency_email) VALUES (?, ?, ?)", (Org_id, Agency_name, Agency_email))
    conn.commit()
    print("Inserted into agency_table")

def insert_user(conn, Org_id, Access_level, User_name, Password, IsAdmin, Application):
    mycursor = conn.cursor()
    mycursor.execute("INSERT INTO user_table (Org_id, Access_level, User_name, Password, IsAdmin, Application) VALUES (?, ?, ?, ?, ?, ?)", (Org_id, Access_level, User_name, Password, IsAdmin, Application))
    conn.commit()
    print("Inserted into user_table")
    
def select_user_by_credentials(conn, username, password):
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM user_table WHERE User_name = ? AND Password = ?", (username, password))
    rows = mycursor.fetchall()
    return rows







conn = get_db_conn()
# create_organization_table(conn)
# create_agency_table(conn)
# create_user_table(conn)
# display_agency_table(conn)
#display_user_table(conn)
# Insert into organization_table
# insert_organization(conn, 1, "Organization 1", "qweasdfghjkl")

# insert_agency(conn, 1, "Agency 1", "email@example.com")
# insert_user(conn, 1, "user", "user1", "12345", "false", "Ranker")

matching_users = select_user_by_credentials(conn, "user1", "12345")
# print(matching_users)
# conn.close()

