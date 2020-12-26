from flask import Flask, request, jsonify
from app import Account,Position,Trade,Tracking
from app.util import get_price, generate_key,get_price_of_ticker, top_gainers,top_losers,usd_chart,crypto_stats, Logo,tracking_chart,related_Companies,Crypto,stats,stats_low,pe_ratio,day_change,stock_description,chart,ytd_change,crypto_chart
from flask_cors import CORS

Account.dbpath = 'data/ttrader.db'

api = Flask(__name__)
CORS(api)


@api.route('/api/create', methods=['POST'])
def create_account():
    data = request.get_json()
    if data:
        # email, password, balance = views.create_account()
        new_account = Account(None, data['email'], data['password'],data['first_name'],data['last_name'])
        new_account.api_key = generate_key()
        new_account.save()
        return jsonify({'status':'success', 'api_key': new_account.api_key})
    return jsonify({"error":"invalid data"})
@api.route('/')
def check():
    return jsonify({"token": user.api_key})

@api.route('/api/log', methods =['POST'])
def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        user = Account.signin(email,password)
        if user:
           
            return jsonify({"token": user.api_key})
        return jsonify({"token": ""})

@api.route('/api/price/<ticker>/<api_key>', methods=['GET'])
def lookup(ticker,api_key):
    user = Account.api_authenticate(api_key)
    if user:
        price = get_price(ticker)
        description = stock_description(ticker)
        chart_data = chart(ticker)
        logo = Logo(ticker)
        related = related_Companies(ticker)
        return jsonify({'current_price':price,"des":description,"chartData":chart_data,"logo":logo})
    return jsonify({"error":"failed"})

@api.route('/api/crypto_price/<ticker>/<api_key>', methods=['GET'])
def lookupCrypto(ticker,api_key):
    user = Account.api_authenticate(api_key)
    if user:
        price = Crypto(ticker)
        return jsonify({'crypto':price})
    return jsonify({"error":"failed"})

@api.route('/api/crypto_Chart/<ticker>/<api_key>', methods=['GET'])
def crypto_chart_data(ticker,api_key):
    user=Account.api_authenticate(api_key)
    if user:
        data = crypto_chart(ticker)
        return jsonify({"chart":data})
    return jsonify({"error":"failed"})

# @api.route('/api/recco/<ticker>/<api_key>', methods =['GET'])
# def lookup_recco(ticker,api_key):
#     user = Account.api_authenticate(api_key)
#     if user:
#         price = rec(ticker)
#         return jsonify({'current':price})
#     return jsonify({"error":"failed"})

@api.route('/api/<token>/balance', methods=['GET'])
def get_bal(token):
    
    account = Account.api_authenticate(token)
    if account:
        return jsonify({'balance': float(account.balance)})
    return jsonify({'error':'invalid key'})

# @api.route('/api/<token>/equity', methods=['GET'])
# def get_equ(token):
#     account = Account.api_authenticate(token)
#     if account:
#         position = Position.all_shares_accounts(account.pk)
#         res = Position.from_position_equity(account.pk)
#         for idx,pos in enumerate(position):
#             equ = pos[2]
#             pk = pos[3]
#             equ = 0
#             price = get_price_of_ticker(pos[1])
#             num = pos[0]
#             equ = price * int(num)
#             new_position = Position(pk,account.pk,pos[1],num,equ)
#             new_position.save()
#             total = new_position.total_equ()
#         return jsonify({'equity': total})
#     return jsonify({'error':'invalid key'})

@api.route('/api/<token>/equity', methods=['GET'])
def get_equ(token):
    account = Account.api_authenticate(token)
    if account:
        res = Position.from_position_equity(account.pk)
        total = res.total_equ(account.pk)
        return jsonify({'equity': total})
    return jsonify({'error':'invalid key'})

@api.route('/api/<api_key>/<amount>', methods=['POST'])
def deposit(api_key,amount):
    account = Account.api_authenticate(api_key)
    if account:
        account.balance += int(amount)
        account.save()
        return jsonify({"new balance": account.balance, "status": "success"})
    else:
        return jsonify({"error":"authentication error"})


@api.route('/api/<api_key>/positions',methods=['GET'])
def get_positions(api_key):
    account = Account.api_authenticate(api_key)
    if account:
        res = Position.all_shares_accounts(account.pk)
        for pos in res:
            equ = pos[2]
            pk = pos[3]
            ticker = pos[0]
            number_shares = pos[1]
            equ = 0
            equ = get_price_of_ticker(ticker) * int(number_shares)
            New_positions = Position(pk,account.pk,ticker,number_shares,equ)
            New_positions.save()
        return jsonify({"Positions":account.get_my_positions(),"Positions_for_graph":New_positions.positions_for_graph(account.pk)})
        
    return jsonify({'error':'invalid key'})

@api.route('/api/num/<api_key>/<ticker>', methods = ['GET'])
def get_num_shares(api_key,ticker):
    user = Account.api_authenticate(api_key)
    if user:
        total_shares = Position.one_from_account(user.pk,ticker)
        
        return jsonify({"total":total_shares})
    return jsonify({'error':'invalid key'})

@api.route('/api/total_shares/<api_key>', methods = ['GET'])
def get_shares(api_key):
    user = Account.api_authenticate(api_key)
    if user:
        total = Position.total_shares(user.pk)
        return jsonify({"total":total})
    return jsonify({'error':'invalid key'})


@api.route('/api/<api_key>/other_positions',methods=['GET'])
def get_pos(api_key):
    account = Account.api_authenticate(api_key)
    if account:
        return jsonify({"Posit":account.get_shares_positions()})
    return jsonify({'error':'invalid key'})

@api.route('/api/<api_key>/usd_chart',methods=['GET'])
def usd_daily_chart(api_key):
    account = Account.api_authenticate(api_key)
    if account:
        return jsonify({"USD":usd_chart()})
    return jsonify({'error':'invalid key'})



@api.route('/api/<api_key>/trades',methods=['GET'])
def get_trades(api_key):
    account = Account.api_authenticate(api_key)
    if account:
        return jsonify({"trades":account.get_my_trades()})
    return jsonify({'error':'invalid key'})

@api.route('/api/<api_key>/recent',methods = ['GET'])
def recent(api_key):
    user = Account.api_authenticate(api_key)
    if user:
        return jsonify({"trades":user.get_limit_trades()})
    return jsonify({'error':'invalid key'})

# @api.route('/api/<api_key>/trades/<ticker>',methods=['GET'])
# def get_specific_trade(api_key,ticker):
#     account = Account.api_authenticate(api_key)
#     if account:

#         return jsonify({"Trades":account.get_my_trades()})
#     return jsonify({'error':'invalid key'})





@api.route('/api/<api_key>/buy', methods=['POST'])
def buy(api_key):
    data=request.get_json()
    account = Account.api_authenticate(api_key)
    if account:
        ticker = request.get_json()['ticker']
        amount = request.get_json()['amount']
        Deposit = request.get_json()['type']
        current_price = get_price_of_ticker(ticker) * int(amount)
        if account.balance < current_price:
            return jsonify({"Insufficient_funds":"Insufficient_funds"})
        account.balance -= current_price
        account.equity += current_price
        current_position = Position.from_account(account.pk, ticker)
        current_position.equity+=current_price
        current_position.number_shares += int(amount)
        current_position.save()
        time=data.get('unix_time')
        new_trade = Trade(account.pk, ticker, amount,current_position.equity, Deposit, time)
        new_trade.equity = current_price
        new_trade.insert()
        account.save()
        return jsonify({"ticker":ticker,"amount":amount})
    return jsonify({'error':'invalid key'})


@api.route('/api/<api_key>/sell', methods=['POST'])
def sell(api_key):
    data=request.get_json()
    account = Account.api_authenticate(api_key)
    if account:
        ticker = request.get_json()['ticker']
        amount = request.get_json()['amount']
        Withdrawal = request.get_json()['type']
        current_position = Position.from_account(account.pk, ticker)
        if current_position.num_shares < int(amount):
             return jsonify({"Insufficient_funds":"Insufficient_funds"})
        transaction_price = get_price_of_ticker(ticker) * int(amount)
        account.balance += (transaction_price)
        account.equity -= transaction_price
        current_position.equity -= (transaction_price)
        current_position.num_shares -= int(amount)
        current_position.save()
        time=data.get('unix_time')
        new_trade = Trade(account.pk, ticker, amount,current_position.equity, Withdrawal,time)
        new_trade.equity = transaction_price
        new_trade.insert()
        account.save()
        return jsonify({"ticker":ticker,"amount":amount})
    return jsonify({'error':'invalid key'})

@api.route('/api/track/<ticker>/<api_key>', methods =['POST'])
def track(ticker,api_key):
    data = request.get_json()
    ticker = data.get('ticker')
    account = Account.api_authenticate(api_key)
    if account:
        new_track = Tracking(None,account.pk,ticker)
        new_track.save()
        return jsonify({"tracking": ticker})
    return jsonify({"error":"no track added"})

@api.route('/api/gettracking/<api_key>', methods =['GET'])
def get_tracking(api_key):
    account = Account.api_authenticate(api_key)
    if account:
        tracks = Tracking.all_for_account(account.pk)
        return jsonify({"tracking": tracks,"token":account.api_key})
    return jsonify({"error":"failed"})
    
@api.route('/api/prices/<ticker>/<api_key>', methods=['GET'])
def look_price(api_key,ticker):
    user = Account.api_authenticate(api_key)
    if user:
        new_user = Tracking.pk_authenticate(user.pk)
        price = get_price_of_ticker(ticker)
        change = day_change(ticker)
        # tracker = tracking_chart(ticker)
        return jsonify({'current_price':price,'change':change})
    return jsonify({"error":"failed"})

@api.route('/api/tracking_chart/<ticker>/<api_key>', methods=['GET'])
def tracker_chart(api_key,ticker):
    user = Account.api_authenticate(api_key)
    if user:
        new_user = Tracking.pk_authenticate(user.pk)
      
        tracker = tracking_chart(ticker)
        return jsonify({"tracker":tracker})
    return jsonify({"error":"failed"})

@api.route('/api/top_gainers/<token>',methods = ['GET'])
def gainers(token):
    user = Account.api_authenticate(token)
    if user:
        gainers = top_gainers()
        return jsonify({"gainers":gainers})
    return jsonify({"error":"failed"})

@api.route('/api/top_losers/<token>',methods = ['GET'])
def losers(token):
    user = Account.api_authenticate(token)
    if user:
        losers = top_losers()
        return jsonify({"losers":losers})
    return jsonify({"error":"failed"})

@api.route('/api/crypto_stats/<ticker>/<token>',methods = ['GET'])
def crypto_stats_rating(ticker,token):
    user = Account.api_authenticate(token)
    if user:
        crypto = crypto_stats(ticker)
        return jsonify({"crypto":crypto})
    return jsonify({"error":"failed"})

@api.route('/api/logo/<ticker>',methods=['GET'])     
def get_logo(ticker):
    logo = Logo(ticker)
    return jsonify({"logo":logo})





if __name__=="__main__":
    api.run(debug=True)

"""
GET /api/price/<ticker> : look up a price
GET /api/<api_key>/balance : look up a user's balance
GET /api/<api_key>/positions : look up a user's stock positions
GET /api/<api_key>/trades : look up a user's trade history
GET /api/<api_key>/trades/<ticker> : look up a user's trade history for a specific stock
POST /api/<api_key>/deposit : deposit money into an account by sending json data of the form '{"amount": 3.50}'
POST /api/<api_key>/sell : issue a sell order by sending json data of the form '{"ticker": "aapl", "volume": 5}'
POST /api/<api_key>/buy : issue a buy order by sending json data of the form '{"ticker": "tsla", "volume": 2}'
"""
