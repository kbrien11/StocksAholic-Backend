import sqlite3


class Tracking:
    dbname = "data/ttrader.db"

    def __init__(self, pk, account_pk, ticker, tracking =1):
        self.pk = pk
        self.account_pk = account_pk
        self.ticker = ticker
        self.tracking = tracking

    def save(self):
        if self.pk:
            self._update()
        else:
            self._insert()


    def _insert(self):
        with sqlite3.connect(self.dbname) as conn:
            cursor = conn.cursor()
            SQL = """INSERT INTO tracking 
                    (account_pk, ticker, tracking)
                    VALUES (?,?,?);"""
            values = (self.account_pk, self.ticker, self.tracking)
            cursor.execute(SQL, values)

    def _update(self):
         with sqlite3.connect(self.dbname) as conn:
            cursor = conn.cursor()
            SQL = """UPDATE tracking SET tracking=1
                    WHERE (account_pk=? AND ticker=?);"""
            values = (self.tracking, self.account_pk, self.ticker)
            cursor.execute(SQL, values)

    @classmethod
    def all_for_account(cls, pk):
        with sqlite3.connect(cls.dbname) as conn:
            cursor = conn.cursor()
            SQL = """SELECT ticker FROM tracking WHERE account_pk=?"""
            cursor.execute(SQL, (pk,))
            data = cursor.fetchall()
            return data

    @classmethod
    def pk_authenticate(cls, pk):
        with sqlite3.connect(cls.dbname) as conn:
            cursor = conn.cursor()
            SQL = """SELECT * FROM accounts WHERE pk=?;"""
            cursor.execute(SQL, (pk,))
            row = cursor.fetchone()
            if row:
                return cls(row[0], row[1], row[2], row[3])
            return None
