import requests
from bs4 import BeautifulSoup
import selenium
import pandas as pd
import re
import time
import random

from df import read_json, print_dict, company_list

# USE SELENIUM FOR INTERACTIVE WEBSITES IF NEEDED
# START WITH THE NASDAQ COMPANIES

"""
TODO:

1) FINANCIAL STATEMENT DATABASE OVER LAST 5 YEARS
2) TIME SERIES DATA OF STOCK PRICES 
"""

# function made with Edward
def get_current_price(COMPANY): 
	yfurl = 'https://ca.finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch'.format(COMPANY,COMPANY) 
	response = requests.get(yfurl)
	soup = BeautifulSoup(response.content, 'html.parser')
	data = soup.find('div', {'class' : 'D(ib) Mend(20px)'})
	# format is [current trading price, dollar/pct change, last time updated]	
	try:
		result = [item.text for item in data]
		result[0] = float(result[0].replace(',',''))
		return result 
	except TypeError:
		return None

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

# fixed formatting for various years in business
def get_financials(COMPANY):
	# just deal with annual for now
	financials = {
		'income-statement' : [],
		'balance-sheet' : [],
		'cash-flow' : []
	}
	baseurl = 'https://www.marketwatch.com/investing/stock/{}/financials/'.format(COMPANY)
	statements = ('income-statement','balance-sheet','cash-flow')
	for i,statement in enumerate(statements):
		if statement == statements[0]:	
			response = requests.get(baseurl)
		else:
			url = baseurl + statement	
			response = requests.get(url)
		soup = BeautifulSoup(response.content, 'html.parser')
		tables = soup.find_all('div', {'class':'financials'})
		# iterate through each of the tables
		for j,table in enumerate(tables):
			table_dic = {}
			current_section = None
			cells = table.find_all('div',{'class':'cell__content'})
			years = table.find('thead').find_all('th')
			# retrieve the head of the table to see how many years
			if i == 0 and j == 0:
				year_arr = []
				for year in years:
					try:
						year_arr.append(int(year.text))
					except ValueError:
						continue
			len_data = len(year_arr) + 3
			for i, item in enumerate(cells):
				if item.text == ' ' or item.text == '5-year trend': 
					continue
				if i % len_data == 0:
					current_section = item.text
					table_dic[current_section] = []
					years = 1
					continue
				if item.text != current_section: 
					table_dic[current_section].append(item.text)
			financials[statement].append(table_dic)
		if len(financials[statement]) == 0: 
			return ''
	return financials

def print_financials(financials):
	for statement in financials:		  
		print(statement.upper())
		print()
		for table in financials[statement]:
			for section in table:
				print(section, table[section])
		print()

def get_market_symbols():
    # load into dataframe
	filePath = 'Resources/NasdaqListed.txt'
	with open(filePath) as file:
		data = file.readlines()
		companies = []
		for entry in data:
			splitted = entry.split('|')
			symbol = splitted[0]
			company = splitted[1].split('-')[0].strip()
			companies.append((symbol,company))	
	return companies

def format_companies(companies):
	for symbol, company in companies:
		output = get_financials(symbol)
		if output != '':
			print(symbol, company)
			print_financials(output)
			price = get_current_price(symbol)
			if price is not None:
				message = '{} has a share price of ${}. For a daily change of {}. As of {}'.format(company,price[0],price[1],price[2])
				print(message)
			else:
				print('Yahoo Finance does not have share data on this company')

def write_to_db(companies):
	FILE = 'Database/NasdaqFinancialStatements.txt'
	with open(FILE, 'w+') as file:
		for symbol, company in companies:
			financials = get_financials(symbol)
			if financials != '':
				firstline = symbol + ' ' + company + '\n\n'
				file.write(firstline)
				for statement in financials:
					file.write(statement.upper() + '\n')
					for table in financials[statement]:
						for section in table:
							line = section + ' : ' + ', '.join(table[section]) + '\n'
							file.write(line)
				file.write('\n')

# statistical success rate from full nasdaq list
# hovers around 76% listed on the nasdaq's financial statements
# over the last 5 years
# makes sense since len(JSON)/len(companies) = 0.76
def success_rate(JSON):
	companies = get_market_symbols()
	error_rates = []
	for _ in range(50):
		counter = 0
		for _ in range(500):
			c = random.choice(companies)[0]
			try:
				JSON[c]
			except KeyError:
				counter += 1
		error_rates.append(round((counter/500)*100,2))
	success_rate = 100-round(sum(error_rates)/len(error_rates),2)
	print(str(success_rate) + '% successful')
	return success_rate			

def scrape_into_txt():
	print('Retrieving Nasdaq market data...')
	companies = get_market_symbols()
	# format_companies(companies)
	start = time.time()
	print('Scraping Financial Statements of Nasdaq companies...')
	write_to_db(companies)
	end = time.time()
	seconds = end - start
	minutes = seconds * 0.0166667
	print('Scraping took {} minutes.'.format(minutes))

def main():
	# scrape_into_txt()
	JSON_FILE = 'Database/NasdaqFinancialStatements.json'
	# update read_json so the financial statements are in dataframes
	JSON = read_json(JSON_FILE) 
	print(JSON['TSLA']) # test and it works!

	# FINANCIAL DATABASE COMPLETE, WORK ON FORMAL ARCHITECTURE TMR

if __name__ == '__main__':
	main()
