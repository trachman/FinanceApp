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


# not picking up liabilities in balance sheet
# not picking up all tables in cash flows 
def get_financials(COMPANY):
	# just deal with annual for now
	financials = {
		'income-statement' : {},
		'balance-sheet' : {},
		'cash-flow' : {}
	}
	baseurl = 'https://www.marketwatch.com/investing/stock/{}/financials/'.format(COMPANY)
	statements = ('income-statement','balance-sheet','cash-flow','secfilings')
	statements = statements[:-1] # dont deal with secfilings just yet
	for statement in statements:
		if statement == statements[0]:	
			response = requests.get(baseurl)
		else:
			url = baseurl + statement	
			response = requests.get(url)
		soup = BeautifulSoup(response.content, 'html.parser')
		table = soup.find('div', {'class':'financials'})
		cells = table.find_all('div',{'class':'cell__content'})
		current_section = None
		for i, item in enumerate(cells):
			if i % 8 == 0:
				current_section = item.text
				financials[statement][current_section] = []
			if i % 8 != 0 and item.text != current_section:
				financials[statement][current_section].append(item.text)
	print_financials(financials)
	return financials

def print_financials(financials):
	for statement in financials:		  
		print(statement.upper())
		print()
		for section in financials[statement]:
			print(section, financials[statement][section])
		print()

def main():
	tesla = 'AMZN'
	get_financials(tesla)	
	print(get_current_price(tesla))

if __name__ == '__main__':
	main()
