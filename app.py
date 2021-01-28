import requests
from bs4 import BeautifulSoup
import selenium
import pandas as pd
import re

# USE SELENIUM FOR INTERACTIVE WEBSITES IF NEEDED
# START WITH THE FORTUNE 500 COMPANIES

"""
TODO:

1) FINANCIAL STATEMENT DATABASE OVER LAST 5 YEARS
2) TIME SERIES DATA OF STOCK PRICES 
"""
 
def get_current_price(COMPANY): 
	yfurl = 'https://ca.finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch'.format(COMPANY,COMPANY) 
	response = requests.get(yfurl)
	soup = BeautifulSoup(response.content, 'html.parser')
	data = soup.find('div', {'class' : 'D(ib) Mend(20px)'})
	# format is [current trading price, dollar/pct change, last time updated]	
	return [item.text for item in data]  

"""
1) INCOME STATEMENT IS ONE LARGE TABLE

2) BALANCE SHEET IS MADE UP OF 2 TABLES
	- ASSETS
	- LIABILITIES AND SHAREHOLDER EQUITY 

3) CASH FLOWS IS MADE UP OF 3 TABLES
	- OPERATING ACTIVITIES
	- INVESTING ACTIVITIES
	- FINANCING ACTIVITIES

TODO: PORT FINANCIAL DICTIONARY INTO A DATAFRAME 
"""

def get_financials(COMPANY):
	# just deal with annual for now
	financials = {
		'income-statement' : [],
		'balance-sheet' : [],
		'cash-flow' : []
	}
	baseurl = 'https://www.marketwatch.com/investing/stock/{}/financials/'.format(COMPANY)
	statements = ('income-statement','balance-sheet','cash-flow')
	for statement in statements:
		if statement == statements[0]:	
			response = requests.get(baseurl)
		else:
			url = baseurl + statement	
			response = requests.get(url)
		soup = BeautifulSoup(response.content, 'html.parser')
		tables = soup.find_all('div', {'class':'financials'})
		# iterate through each of the tables
		for table in tables:
			table_dic = {}
			current_section = None
			cells = table.find_all('div',{'class':'cell__content'})
			for i, item in enumerate(cells):
				if item.text == ' ' or item.text == '5-year trend': continue
				if i % 8 == 0:
					current_section = item.text
					table_dic[current_section] = []
					continue
				if item.text != current_section: table_dic[current_section].append(item.text)
			financials[statement].append(table_dic)
	print_financials(financials)
	return financials

def print_financials(financials):
	for statement in financials:		  
		print(statement.upper())
		print()
		for table in financials[statement]:
			for section in table:
				print(section, table[section])
		print()

def main():
	tesla = 'MSFT'
	get_financials(tesla)	
	print(get_current_price(tesla))

if __name__ == '__main__':
	main()
