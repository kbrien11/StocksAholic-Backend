import sqlite3
from .util import get_price_of_ticker


class Position:
    dbname = "data/ttrader.db"

    def __init__(self, pk, account_pk, ticker, number_shares,equity =0):
        self.pk = pk
        self.account_pk = account_pk
        self.ticker = ticker
        self.number_shares = number_shares
        self.equity = round(equity,2)

    def save(self):
        if self.pk:
            self._update()
        else:
            self._insert()

        

    def _insert(self):
        with sqlite3.connect(self.dbname) as conn:
            cursor = conn.cursor()
            SQL = """INSERT INTO positions 
                    (account_pk, ticker, number_shares,equity)
                    VALUES (?,?,?,?);"""
            values = (self.account_pk, self.ticker, self.number_shares,self.equity)
            cursor.execute(SQL, values)

    def _update(self):
         with sqlite3.connect(self.dbname) as conn:
            cursor = conn.cursor()
            SQL = """UPDATE positions SET number_shares=?, equity =?
                    WHERE (account_pk=? AND ticker=?);"""
            values = (self.number_shares,self.equity, self.account_pk, self.ticker)
            cursor.execute(SQL, values)

    
    def equity_update(self,ticker,account_pk,equity):
        with sqlite3.connect(self.dbname) as conn:
            cursor = conn.cursor()
            SQL = """UPDATE positions SET equity =?
                    WHERE (account_pk=? AND ticker=?);"""
            values = (self.equity,self.account_pk,self.ticker)
            cursor.execute(SQL, values)

    @classmethod
    def all_for_account(cls, pk):
        with sqlite3.connect(cls.dbname) as conn:
            cursor = conn.cursor()
            SQL = """SELECT ticker, number_shares,equity FROM positions WHERE account_pk=? AND number_shares >0 ORDER BY equity DESC LIMIT 5"""
            cursor.execute(SQL, (pk,))
            data = cursor.fetchall()
            return data
            

    @classmethod
    def all_for_accounts(cls, pk):
        with sqlite3.connect(cls.dbname) as conn:
            cursor = conn.cursor()
            SQL = """SELECT ticker FROM positions WHERE account_pk=?"""
            cursor.execute(SQL, (pk,))
            data = cursor.fetchall()
            return data

    @classmethod
    def all_shares_accounts(cls, pk):
        with sqlite3.connect(cls.dbname) as conn:
            cursor = conn.cursor()
            SQL = """SELECT  ticker,number_shares,equity,pk FROM positions WHERE account_pk=? ORDER BY equity DESC LIMIT 5"""
            cursor.execute(SQL, (pk,))
            data = cursor.fetchall()
            return data

    @classmethod
    def positions_for_graph(cls, pk):
        with sqlite3.connect(cls.dbname) as conn:
            cursor = conn.cursor()
            SQL = """SELECT  ticker,number_shares,equity,pk FROM positions WHERE account_pk=?"""
            cursor.execute(SQL, (pk,))
            data = cursor.fetchall()
            return data

    @classmethod
    def one_from_account(cls, pk,ticker):
        with sqlite3.connect(cls.dbname) as conn:
            cursor = conn.cursor()
            SQL = """SELECT number_shares FROM positions WHERE account_pk=? AND ticker =?"""
            values = (pk,ticker)
            cursor.execute(SQL, values)
            data = cursor.fetchall()
            if data:
                return data
            return 0

    @classmethod
    def total_equ(cls,pk):
        with sqlite3.connect(cls.dbname) as conn:
            cursor = conn.cursor()
            SQL = """SELECT SUM(equity) FROM positions WHERE account_pk = ?"""
            values = (pk,)
            cursor.execute(SQL,values)
            data = cursor.fetchall()
            if data:
                return data
            return cls(pk=None, account_pk=pk, ticker=ticker, number_shares=0,equity=0)

    @classmethod
    def from_account(cls, pk, ticker):
        with sqlite3.connect(cls.dbname) as conn:
            cursor = conn.cursor()
            SQL = """SELECT ticker,number_shares,equity FROM positions WHERE account_pk=? AND ticker=?"""
            values = (pk, ticker)
            cursor.execute(SQL, values)
            data = cursor.fetchall()
            print("DATA: ", data)
            if data:
                return data
            return cls(pk=None, account_pk=pk, ticker=ticker, number_shares=0,equity=0)

    @classmethod
    def from_position_equity(cls, pk):
        with sqlite3.connect(cls.dbname) as conn:
            cursor = conn.cursor()
            SQL = """SELECT * FROM positions WHERE account_pk=?"""
            values = (pk,)
            cursor.execute(SQL, values)
            data = cursor.fetchone()
            print("DATA: ", data)
            if data:
                return cls(data[0], data[1], data[2], data[3],data[4])
            return cls(pk=None, account_pk=pk, ticker=ticker, number_shares=0,equity=0)

    @classmethod
    def total_shares(cls, pk):
        with sqlite3.connect(cls.dbname) as conn:
            cursor = conn.cursor()
            SQL = """SELECT number_shares FROM positions WHERE account_pk=?"""
            values = (pk,)
            cursor.execute(SQL, values)
            data = cursor.fetchall()
            if data:
                return (data)
            return 0
                
            # #     print("DATA: ", data)
                
            #               return cls(data[0], data[1], data[2], data[3],data[4])
            # return cls(pk=None, account_pk=pk, ticker=ticker, num_shares=0,equity=0)
