import requests
from hashlib import sha512
import random

def get_price(ticker):
    iex_base = "https://cloud.iexapis.com/stable"
    quote_endpoint = iex_base + "/stock/{}/quote?token="
    # TODO: get token
    token = "pk_bc007805b9a3487db96520c1baac3a07"
    response = requests.get(quote_endpoint.format(ticker) + token)#.json()['latestPrice']
    data = response.json()['latestPrice']
    peRatio = response.json()['peRatio']
    company = response.json()['companyName']
    symbol = response.json()['symbol']
    market = response.json()['marketCap']
    return [company,symbol,data,peRatio,market] 

def hash_pass(password, salt="SALT"):
    new_pw = password + salt
    hashed_pw = sha512(new_pw.encode()).hexdigest()
    return hashed_pw

def generate_key(length=15):
    seed = (str(random.random()) + str(random.random())).encode()
    hashed_output = sha512(seed).hexdigest()
    return hashed_output[:length]

def get_price_of_ticker(ticker):
    iex_base = "https://cloud.iexapis.com/stable"
    quote_endpoint = iex_base + "/stock/{}/quote?token="
    # TODO: get token
    token = "pk_bc007805b9a3487db96520c1baac3a07"
    response = requests.get(quote_endpoint.format(ticker) + token)
    data = response.json()['latestPrice']
    return data

# def rec(ticker):
#     end= "https://sandbox.iexapis.com/stable/stock/{}/recommendation-trends?token=tsk_bc007805b9a3487db96520c1baac3a07"
#     response = requests.get(end.format(ticker))
#     data = response.json()
#     new_data=data['ratingBuy']
#     return new_data

def chart(ticker):
  dates = []
  prices =[]
  quote_endpoint =("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=compact&apikey=74MPQ68EA8UASL2C")
  response = requests.get(quote_endpoint.format(ticker))
  data = response.json()['Time Series (Daily)']
  for i in data:
    dates.append(i)
    prices.append(data[i]['1. open'])
  return dates,prices

def usd_chart():
  dates = []
  prices =[]
  quote_endpoint =("https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&outputsize=compact&apikey=74MPQ68EA8UASL2C")
  response = requests.get(quote_endpoint)
  data = response.json()['Time Series FX (Daily)']
  for i in data:
    dates.append(i)
    prices.append(data[i]['1. open'])
    print(dates,prices)
  return dates,prices


def crypto_chart(ticker):
  dates = []
  prices =[]
  quote_endpoint =("https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={}&market=USD&apikey=74MPQ68EA8UASL2C")
  response = requests.get(quote_endpoint.format(ticker))
  data = response.json()['Time Series (Digital Currency Daily)']
  for i in data:
    dates.append(i)
    prices.append(data[i]['1b. open (USD)'])
  return dates,prices

def crypto_stats(ticker):
  quote_endpoint =("https://www.alphavantage.co/query?function=CRYPTO_RATING&symbol={}&apikey=74MPQ68EA8UASL2C")
  response = requests.get(quote_endpoint.format(ticker))
  end = response.json()['Crypto Rating (FCAS)']
  name = end['2. name']
  rating = end['3. fcas rating']
  score = end['4. fcas score']
  market = end['6. market maturity score']
  utlity = end['7. utility score']
  return name,rating,score,market,utlity



def Crypto (ticker):
  quote_endpoint =("https://cloud.iexapis.com/stable/crypto/{}/quote?token=pk_bc007805b9a3487db96520c1baac3a07")
  response = requests.get(quote_endpoint.format(ticker))
  data = response.json()['latestPrice']
  return data

def stock_description(ticker):
  quote_endpoint =("https://cloud.iexapis.com/stable/stock/{}/company?token=pk_bc007805b9a3487db96520c1baac3a07")
  response = requests.get(quote_endpoint.format(ticker))
  desc = response.json()['description']
  ceo = response.json()['CEO']
  empl = response.json()['employees']
  industry = response.json()['industry']
  state = response.json()['state']
  city = response.json()['city']
  sector = response.json()['sector']
  return [desc,ceo,empl,industry,state,city,sector]

def stats(ticker):
  quote_endpoint ="https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_bc007805b9a3487db96520c1baac3a07"
  response = requests.get(quote_endpoint.format(ticker))
  high = response.json()['week52High']
  return high

def related_Companies(ticker):
  quote_endpoint ="https://cloud.iexapis.com/stable//stock/{}/news/last?token=pk_bc007805b9a3487db96520c1baac3a07"
  response = requests.get(quote_endpoint.format(ticker))
  related = response.json()[0]['summary']
  print(related)
  return related

def Logo(ticker):
  quote_endpoint ="https://cloud.iexapis.com/stable/stock/{}/logo?token=pk_bc007805b9a3487db96520c1baac3a07"
  response = requests.get(quote_endpoint.format(ticker))
  logo = response.json()['url']
  return logo



def stats_low(ticker):
  quote_endpoint ="https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_bc007805b9a3487db96520c1baac3a07"
  response = requests.get(quote_endpoint.format(ticker))
  low = response.json()['week52Low']
  return low

def tracking_chart(ticker):
  dates = []
  prices =[]
  quote_endpoint =("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=60min&outputsize=compact&apikey=74MPQ68EA8UASL2C")
  response = requests.get(quote_endpoint.format(ticker))
  data = response.json()['Time Series (60min)']
  for i in data:
    dates.append(i)
    prices.append(data[i]['1. open'])
  return dates[:15],prices[:15]

def chart(ticker):
  dates = []
  prices =[]
  quote_endpoint =("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=compact&apikey=74MPQ68EA8UASL2C")
  response = requests.get(quote_endpoint.format(ticker))
  data = response.json()['Time Series (Daily)']
  for i in data:
    dates.append(i)
    prices.append(data[i]['1. open'])
  return dates,prices
  
  

def pe_ratio(ticker):
  quote_endpoint ="https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_bc007805b9a3487db96520c1baac3a07"
  response = requests.get(quote_endpoint.format(ticker))
  ratio = response.json()['peRatio']
  return ratio

def ytd_change(ticker):
  quote_endpoint ="https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_bc007805b9a3487db96520c1baac3a07"
  response = requests.get(quote_endpoint.format(ticker))
  ratio = response.json()['ytdChange']
  return ratio

def top_gainers():
  end = ("https://financialmodelingprep.com/api/v3/gainers?apikey=8db666fce01a371b534ff479f0d23295")
  res = requests.get(end)
  data = res.json()
  output = []
  for i in data:
    output.append(i)
  return output[:5]

def top_losers():
  end = ("https://financialmodelingprep.com/api/v3/losers?apikey=8db666fce01a371b534ff479f0d23295")
  res = requests.get(end)
  data = res.json()
  output = []
  for i in data:
    output.append(i)
  return output[:5]
  
  

def day_change(ticker):
  quote_endpoint ="https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_bc007805b9a3487db96520c1baac3a07"
  response = requests.get(quote_endpoint.format(ticker))
  change = response.json()['change']
  
  return change

# def chart(ticker):
#   dates = []
#   open_price = []
#   end =  "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=compact&apikey=74MPQ68EA8UASL2C"
#   response = requests.get(end.format(ticker))
#   low = response.json()['Time Series (Daily)']
#   for key in low:
#     dates.append(key)
#     # example = low[key]['1. open']
#     # open_price.append(example)
#   return dates


if __name__=="__main__":
    from pprint import pprint
    pprint(get_price("ibm"))
    print(hash_pass("password"))
