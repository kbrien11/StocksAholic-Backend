import sqlite3
from time import time, strftime, localtime


class Trade:
    dbpath = "data/ttrader.db"

    def __init__(self, account_pk, ticker, num_shares,equity, trade_type ="", unix_time=""):
        self.account_pk = account_pk
        self.ticker = ticker
        self.num_shares = num_shares
        self.trade_type = trade_type
        self.unix_time = unix_time
        self.equity = round(equity,2)

    def insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """INSERT INTO trades(account_pk,
                ticker, number_shares,equity, type, unix_time)
                VALUES (?,?,?,?,?,?);"""
            values = (self.account_pk,self.ticker,self.num_shares,round(self.equity,2),
                      self.trade_type,self.unix_time)
            cursor.execute(SQL, values)

    @classmethod
    def all_for_account(cls, account_pk):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """SELECT * FROM trades WHERE account_pk=?"""
            cursor.execute(SQL, (account_pk,))
            data = cursor.fetchall()
            # trades = [cls(*row[1:]) for row in data]
            # return trades
            return data

    @classmethod
    def most_recent(cls, account_pk):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """SELECT * FROM trades WHERE account_pk=? LIMIT 5"""
            cursor.execute(SQL, (account_pk,))
            data = cursor.fetchall()
            # trades = [cls(*row[1:]) for row in data]
            # return trades
            return data

    @classmethod
    def from_account(cls, pk):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """SELECT * FROM trades WHERE account_pk=?"""
            values = (pk,)
            cursor.execute(SQL, values)
            data = cursor.fetchone()
            print("DATA: ", data)
            if data:
                return cls(data[0], data[1], data[2], data[3],data[4],data[5])
            return cls(account_pk=pk, ticker=ticker, num_shares=0,equity=0,trade_type=trade_type,unix_time=unix_time)

    # def __repr__(self):
    #     stem = "Ticker: {}\nShares: {}\nType: {}\nDate: {}\n"
    #     trade_type = "Buy" if self.trade_type == 0 else "Sell"
    #     date = strftime("%a, %d %b %Y %H:%M:%S %Z", localtime(self.trade_time))
    #     return stem.format(self.ticker, self.num_shares, trade_type, date)
