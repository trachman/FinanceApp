import os
import requests

"""
PLAN:

FIND SOURCE OF DATA FOR STOCK PRICES 

stooq.com its lit -> got 5 minute info for etfs, stocks

move to ALPHA VANTAGE when the database if fully fledged

STRUCTURE OF DATA
https://stooq.com/db/h/

EG:

DATABASE
	TRACKED TICKER SYMBOLS | MARKET | SECURITY TYPE -> all in JSON
	MARKETS
		NASDAQ
			FINANCIAL STATEMENTS
			ETF
			STOCK
				AAPL
				GOOG
				ETC.
		NYSE
			FINANCIAL STATEMENTS
			ETF
			STOCK
		TSX
			FINANCIAL STATEMENTS
			ETF
			STOCK
"""


def get_intra_day_data():
	# convert to json data
	historical = {}
	for i in range(1,3):
		HISTORICAL_FILE = 'Database/StockPrices/5min/us/nasdaqstocks/' + str(i) + '/'
		companies = os.listdir(HISTORICAL_FILE)
		for company in companies:
			FILE = HISTORICAL_FILE + company
			with open(FILE,'r') as file:
				data = file.readlines()
				company = company.split('.')[0].upper()
				historical[company] = data

	# clean apples data
	for company in historical:
		intra_day_data = historical[company]
		for i, datapoint in enumerate(intra_day_data):
			datapoint = datapoint[:-2].split(',')
			datapoint[0] = datapoint[0].split('.')[0]
			datapoint.pop()
			for j in range(len(datapoint)):
				try:
					datapoint[j] = float(datapoint[j])
				except:
					continue
			intra_day_data[i] = datapoint
		historical[company] = intra_day_data

	# DATA FORMAT -> symbol, interval (seconds), date, time, open, high, low, close, volume
	format = ['symbol','interval','date','time','open','high','low','close','volume']
	result = {}
	for company in historical:
		result[company] = []
		for datapoint in historical[company]:
			JSON = {}
			for i, point in enumerate(datapoint):
				JSON[format[i]] = point
			result[company].append(JSON)
		for i, line in enumerate(result[company]):
			try:
				result[company][i]['interval'] = int(line['interval'])
				result[company][i]['date'] = int(line['date'])
				result[company][i]['time'] = int(line['time'])
				result[company][i]['volume'] = int(line['volume'])
			except ValueError:
				continue
	return result

def write_to_db(historical_data):
	for company in historical_data:
		for line in historical_data[company]:
			print(line)
	# now write to files
	
"""
GOING TO HAVE TO UPDATE THIS MANUALLY FOR THE TIME BEING
TRY TO DEVELOP A FUNCTION TO AUTOMATICALLY APPEND THE UPDATED 
DATA TO THE DATABASE

LAST UPDATED: JANUARY 29, 2021
"""

# historical_data = get_intra_day_data()
# write_to_db(historical_data)

# they have two years of intraday data on stocks

""" ALPHA VANTAGE """ 
# key = '5UKYNVII43CDI9G0'
# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&outputsize=full&apikey={}'.format(key)
# response = requests.get(url)
# print(response.content.decode())
# ALPHA VANTAGE IS THE ANSWER FOR PAYING FOR CHEAP WITH GOOD DATA
""" ALPHA VANTAGE CODE ENDS """

def nasdaq_tickers():
	f = 'Database/StockPrices/5min/us/nasdaqstocks/'
	companies = []
	for i in range(1,3): companies += os.listdir(f+str(i))
	tickers = [ company.split('.')[0].upper() for company in companies]
	return tickers

def nyse_tickers():
	f = 'Database/StockPrices/5min/us/nysestocks/'
	companies = []
	for i in range(1,4): companies += os.listdir(f+str(i))
	tickers = [ company.split('.')[0].upper() for company in companies]
	return tickers

na_tickers = nasdaq_tickers()
ny_tickers = nyse_tickers()

print(len(na_tickers))
print(len(ny_tickers))


# all the tickers are different which is cool
# maybe check for differences between tickers and other data sites

