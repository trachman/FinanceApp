import requests
from bs4 import BeautifulSoup
import selenium

# USE SELENIUM FOR INTERACTIVE WEBSITES IF NEEDED

def get_current_price(COMPANY): 
	yfurl = 'https://ca.finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch'.format(COMPANY,COMPANY) 
	response = requests.get(yfurl)
	soup = BeautifulSoup(response.content, 'html.parser')
	data = soup.find('div', {'class' : 'D(ib) Mend(20px)'})
	# format is [current trading price, dollar/pct change, last time updated]	
	return [item.text for item in data] 

def get_income_statements(COMPANY):
	url = 'https://finance.yahoo.com/quote/{}/financials/'.format(COMPANY)
	response = requests.get(url)
	soup = BeautifulSoup(response.content,'html.parser')
	data = soup.find('div',{'class' : 'D(tbrg)'})
	spans = data.find_all('span')
	result = {}
	for i, item in enumerate(spans):
		print(item.text,i)

def helperfunc:
	pass

def get_financials(COMPANY):
	# just deal with annual for now
	baseurl = 'https://www.marketwatch.com/investing/stock/{}/financials/'.format(COMPANY)
	statements = ('income statement','balance-sheet','cash-flow','secfilings')
	statements = statements[:-1] # dont deal with secfilings just yet
	for statement in statements:
		if statement == statements[0]:
			print(statement)
			print(baseurl)
			response = requests.get(baseurl)
			soup = BeautifulSoup(response.content, 'html.parser')
			table = soup.find('div', {'class':'financials'})
			print(table)
		else:
			url = baseurl + statement
			print(statement)
			print(url)
			response = requests.get(url)
			soup = BeautifulSoup(response.content, 'html.parser')
			table = soup.find('div', {'class':'financials'})
			print(table)
		print()

def main():
	# form = get_current_price('TSLA')
	# get_income_statements('AMZN')
	tesla = 'TSLA'
	get_financials(tesla)

if __name__ == '__main__':
	main()
