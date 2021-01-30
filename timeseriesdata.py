import os

"""
PLAN:

FIND SOURCE OF DATA FOR STOCK PRICES 

stooq.com its lit -> got 5 minute info for etfs, stocks

STRUCTURE OF DATA

DATABASE
    MARKET
        SECURITY TYPE
            COMPANIES

https://stooq.com/db/h/

EG:

DATABASE
    TRACKED TICKER SYMBOLS | MARKET | SECURITY TYPE
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

historical_data = get_intra_day_data()
write_to_db(historical_data)