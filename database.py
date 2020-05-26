'''
python3 database.py -f ./services.sqlite3 -s 'Jira' -v 8.5.1 -d jira.example.com -u https://jira.example.com/

sqlite> .open services.sqlite3
sqlite> select * from services;
'''

import sqlite3
import argparse
import sys
import datetime
import time

def get_timestamp():
    ts = time.time()
    dt = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    return dt

def create_connection(database):
    conn = None
    try:
        conn = sqlite3.connect(database)
        return conn
    except Exception as e:
        print(e)

    return conn

def create_table(conn, sqlite_create_table):
    try:
        c = conn.cursor()
        c.execute(sqlite_create_table)
    except Exception as e:
        print(e)

def insert_data(conn, service, version, domain, url, credentials):
    try:
        crsr = conn.cursor()
        crsr.execute('INSERT INTO SERVICES (id, service, version, domain, url, credentials, discovered) VALUES(NULL,?,?,?,?,?,?)', (service, version, domain, url, credentials, get_timestamp()))
        conn.commit()
        conn.close()
    except Exception as e:
        print('Database update failed')
        print(e)

def main():

    parser = argparse.ArgumentParser(description='Store services found in Bug Bounties to sqlite3 database for future reference in case of a CVE/Exploit.')

    parser.add_argument('-f', type=str, help='sqlite file to process', dest='fsqlite')
    parser.add_argument('-s', type=str, help='Service', dest='service', default='')
    parser.add_argument('-v', type=str, help='Service Version', dest='version', default='')
    parser.add_argument('-d', type=str, help='Service Domain', dest='domain', default='')
    parser.add_argument('-u', type=str, help='Service URL', dest='url', default='')
    parser.add_argument('-c', type=str, help='Service Credentials if found', dest='credentials', default='')

    args = parser.parse_args()

    database = args.fsqlite
    service = args.service
    version = args.version
    domain = args.domain
    url = args.url
    credentials = args.credentials

    sqlite_create_table = """ CREATE TABLE IF NOT EXISTS SERVICES (
                                id integer PRIMARY KEY,
                                service text NOT NULL,
                                version text NOT NULL,
                                domain text NOT NULL,
                                url text NOT NULL,
                                credentials text,
                                discovered timestamp
                              ); """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sqlite_create_table)
        insert_data(conn, service, version, domain, url, credentials)
    else:
        print("Error cannot create database connection")


if __name__ == '__main__':
    main()
