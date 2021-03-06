import yfinance as yf

data = yf.download( tickers='MSFT AAPL',  # i am appending something
					start='2021-01-01', 
					end='2021-02-24', 
					interval='2m' )
for date, row in data.iterrows(): # can go as far back as 730 days 
    print(date, row)

'''
1m -> 30 days
2m -> 60 days 
5m -> 60 days 
15m -> 60 days
30m -> 60 days
60m -> 730 days
90m -> 60 days
1h -> 730 days
1d ->
5d -> 
1wk ->
1mo -> 
3mo ->
'''
# - AAPL: 1m data not available for startTime=1548997200 and endTime=1549515600. The requested range must be within the last 30 days. 

# def organize_data(data, granularity=False):
# 	# save data into a dictionary 
# 	if granularity:
# 		company_information = {}
# 		i, length = 0, len(data.index)
# 	else:
# 		company_information = {}
# 		i, length = 0, len(data.index)
# 		for date, row in data.iterrows():
# 			if granularity:
# 				date = str(date)
# 			else:
# 				date = str(date).split(' ')[0]
# 			information = row.iteritems()
# 			for item in information:
# 				symbol, key, value = item[0][0], item[0][1], item[1]
# 				if symbol not in company_information:
# 					company_information[symbol] = { date : {} }
# 				else:
# 					if date not in company_information[symbol]:
# 						company_information[symbol][date] = { key : value }
# 					else:
# 						company_information[symbol][date][key] = value
# 			i += 1
# 	return company_information

# test = organize_data(data)
# print(test)
