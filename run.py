from app import run
from app import Account
# from app import Position
# from app import Trade

Account.dbpath = "data/ttrader.db"
# Trade.dbpath = "data/ttrader.db"
# Position.dbpath = "data/ttrader.db"

run()
