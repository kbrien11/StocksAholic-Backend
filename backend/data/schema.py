import sqlite3
import os

DIR = os.path.dirname(__file__)
DBNAME = "ttrader.db"
DBPATH = os.path.join(DIR, DBNAME)


def schema(dbpath):
    with sqlite3.connect(dbpath) as connection:
        cursor = connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS accounts;")

        SQL = """CREATE TABLE accounts (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(128),
                password_hash VARCHAR(32),
                first_name VARCHAR(32),
                last_name VARCHAR(32),
                api_key VARCHAR(15),
                balance INTEGER,
                equity INTEGER,
                ticker VARCHAR(6),
                number_shares INTEGER,
                FOREIGN KEY(equity) REFERENCES positions(equity)
                
            );"""

        cursor.execute(SQL)

        cursor.execute("DROP TABLE IF EXISTS positions;")

        SQL = """CREATE TABLE positions (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                account_pk INTEGER,
                ticker VARCHAR(6),
                number_shares INTEGER,
                equity INTEGER,
                FOREIGN KEY (account_pk) REFERENCES accounts(pk)
            );"""

        cursor.execute(SQL)

        cursor.execute("DROP TABLE IF EXISTS trades;")

        SQL = """CREATE TABLE trades (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                account_pk INTEGER,
                ticker VARCHAR(6),
                number_shares INTEGER,
                equity INTEGER,
                type Varchar(6),
                unix_time TEXT,
                FOREIGN KEY (account_pk) REFERENCES accounts(pk)
            );"""

        cursor.execute(SQL)

        cursor.execute("DROP TABLE IF EXISTS tracking;")

        SQL = """CREATE TABLE tracking (
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                account_pk INTEGER,
                ticker VARCHAR(6),
                tracking BOOL,
                FOREIGN KEY (account_pk) REFERENCES accounts(pk)
            );"""

        cursor.execute(SQL)


if __name__ == "__main__":
    schema("ttrader.db")
