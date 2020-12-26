import sqlite3
from .position import Position
from .trade import Trade
from .util import hash_pass, get_price, generate_key
import time

class Account:
    dbpath = "data/ttrader.db"

    def __init__(self, pk, email, password,first_name,last_name, api_key='', balance=0,equity=0):
        self.pk = pk
        self.email = email
        self.password = hash_pass(password)
        self.first_name = first_name
        self.last_name = last_name
        self.api_key = api_key
        self.balance = balance
        self.equity = round(equity,2)

    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """INSERT INTO accounts(
                email, password_hash,first_name,last_name, api_key, balance,equity) 
                VALUES (?,?,?,?,?,?,?);"""

            values = (self.email, self.password,self.first_name,self.last_name,self.api_key, self.balance,round(self.equity,2))
            cursor.execute(SQL, values)

    def _update(self):
         with sqlite3.connect(self.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """UPDATE accounts SET balance=?,equity=? WHERE (pk=?);"""
            values = (self.balance,round(self.equity,2), self.pk)
            cursor.execute(SQL, values)

    def update_equ(self):
         with sqlite3.connect(self.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """UPDATE accounts SET equity=? WHERE (pk=?);"""
            values = (round(self.equity,2), self.pk)
            cursor.execute(SQL, values)

    def save(self):
        if self.pk:
            self._update()
        else:
            self._insert()

    def buy(self, ticker, amount):
        current_price = get_price(ticker) * amount
        if self.balance < current_price:
            raise ValueError
        self.balance -= current_price
        current_position = Position.one_from_account(self.pk, ticker)
        current_position.num_shares += amount
        current_position.save()
        new_trade = Trade(self.pk, ticker, amount, 0)
        new_trade.insert()
        self.save()

    def sell(self, ticker, amount):
        current_position = Position.one_from_account(self.pk, ticker)
        if current_position.num_shares < amount:
            raise ValueError
        transaction_price = get_price(ticker) * amount
        self.balance += transaction_price
        current_position.num_shares -= amount
        current_position.save()
        new_trade = Trade(self.pk, ticker, amount, 1)
        new_trade.insert()
        self.save()



    def get_my_trades(self):
        my_trades = Trade.all_for_account(self.pk)
        return my_trades

    def get_limit_trades(self):
        my_trades = Trade.most_recent(self.pk)
        return my_trades

    def get_my_positions(self):
        my_positions = Position.all_for_account(self.pk)
        return my_positions

    def get_other_positions(self):
        my_pos = Position.all_for_accounts(self.pk)
        return my_pos

    def get_shares_positions(self):
        my_pos = Position.all_shares_accounts(self.pk)
        return my_pos

    def get_equity(self,equity):
        my_equity = Position.all_for_accounts(self.pk,self.equity)
        return my_equity

    @classmethod
    def signin(cls, email, password):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """SELECT * FROM accounts WHERE email=? AND password_hash=?;"""
            cursor.execute(SQL, (email,hash_pass(password)))
            row = cursor.fetchone()
            if row:
                return cls(row[0], row[1], row[2], row[3], row[4],row[5],row[6],row[7])
            return None

    @classmethod
    def api_authenticate(cls, api_key):
        with sqlite3.connect(cls.dbpath) as conn:
            cursor = conn.cursor()
            SQL = """SELECT * FROM accounts WHERE api_key=?;"""
            cursor.execute(SQL, (api_key,))
            row = cursor.fetchone()
            if row:
                return cls(row[0], row[1], row[2], row[3], row[4],row[5],row[6],row[7])
            return None

    def __repr__(self):
        stem = "<Account for {}, balance={}>"
        return stem.format(self.email, self.balance)
    