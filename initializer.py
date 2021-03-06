import yfinance as yf
import json
import datetime
import pandas as pd
import os
import time
from requests.exceptions import ConnectionError
from json.decoder import JSONDecodeError
from pandas.errors import InvalidIndexError

class TimeSeriesInitializer(object):
	def __init__(self):
		print('Welcome to the database intializer!')
		print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
		print()
		
		print('Ensuring the database is ready to be setup...')
		self.set_up_db()
		print('Database is setup.')

		print()
		print('Collecting tickers...')
		print()
		
		# collect all the tracked tickers
		tickers = self.get_tickers()

		# branch off to other features here
		# granularity_options = ( '1m','2m','5m','15m',
		# 						'30m','60m','90m', '1d',
		# 						'5d','1wk','1mo','3mo' )
		
		# temporary
		granularity_options = ('5d','1wk','1mo','3mo')
	
		for granularity in granularity_options:
			# figure out how far to go back
			print()
			print('Starting collection of {} granularity data'.format(granularity))
			print()
			granularity_families = [ ('1m'),
									('2m','5m','15m','30m','90m'),
									('60m') ]	
			granularity_type = None
			for option in granularity_families:
				if granularity in option: 
					granularity_type = option
					break
			
			if granularity_type is not None:
				distance_allowed = {
					('1m') : 29, # 30 but 29 to be safe
					('2m','5m','15m','30m','90m') : 59, # 60 
					('60m') : 729, # 730
				}
				distance_back = distance_allowed[granularity_type]
				date_periods = self.get_date_periods(distance_back)
				self.initialize_db( tickers,
									granularity = granularity,
									date_periods = date_periods )
			else:
				self.initialize_db( tickers, 
									granularity = granularity )	
		return 
	
	def initialize_db(	self, tickers, 
						granularity=None, 
						date_periods=None ):
		print()
		print('Retrieving tickers...') 
		print()
		tickers_list = [ *tickers ]
		chunks = self.make_chunks(tickers_list)
		for chunk_num, chunk in enumerate(chunks):
			print()
			print('Retrieving chunk {} of {}'.format(chunk_num+1, len(chunks)))
			print()
			ticker_string = ' '.join(chunk)
			if date_periods is None:
				try:
					data = yf.download( tickers = ticker_string,
										period = 'max',
										interval = granularity,
										group_by = 'ticker',
										auto_adjust = True,
										prepost = True,
										threads = False,
										proxy = None )
				except (ConnectionError, JSONDecodeError, RuntimeError, InvalidIndexError) as e:
					print()
					print(e)
					print()
					time.sleep(120)
					data = yf.download( tickers = ticker_string,
										period = 'max',
										interval = granularity,
										group_by = 'ticker',
										auto_adjust = True,
										prepost = True,
										threads = False,
										proxy = None )
				print()
				company_information = self.organize_data(data)
			else:
				for i in range(1, len(date_periods)):
					start_date = str(date_periods[i-1])
					end_date = str(date_periods[i])
					print('Date Range:', str(start_date), str(end_date))
					try:
						data = yf.download( tickers=ticker_string,
											start=start_date,
											end=end_date,
											interval=granularity,
											group_by='ticker',
											auto_adjust=True,
											prepost=True,
											threads=False,
											proxy=None )
					except (ConnectionError, JSONDecodeError, RuntimeError, InvalidIndexError) as e:
						print()
						print(e)
						print()
						time.sleep(120)
						data = yf.download( tickers=ticker_string,
											start=start_date,
											end=end_date,
											interval=granularity,
											group_by='ticker',
											auto_adjust=True,
											prepost=True,
											threads=False,
											proxy=None )
					if i == 1: all_data = data
					else:
						frames = [all_data,data]
						all_data = pd.concat(frames)
				print()
				company_information = self.organize_data(data, granularity=True)
			self.write_to_json(company_information, granularity)
			print('Chunk {} collection complete.'.format(chunk_num+1))
			print()

		print()
		print('All chunks accounted for.')
		print('Database initialization complete.')
		print()
		return 

	# HELPER METHODS
	
	# retrieves the tickers from tickers.json file
	def get_tickers(self):
		file_location = 'Database/DailyData/tickers.json' 
		with open(file_location, 'r') as file:
			json_string = file.read()
			tickers = json.loads(json_string)
		return tickers

	# makes chunks for 1m data since max 1w chunks
	def make_chunks(self, tickers_list):	
		chunks = []
		chunk_length = 250 
		print('Making chunks...')
		holder, length = 0, len(tickers_list)
		while holder < length:
			if length - holder <= chunk_length: chunks.append(tickers_list[holder:length])
			else: chunks.append(tickers_list[holder:holder+chunk_length])
			holder += chunk_length
		return chunks

	# writes the dictionary into company_information
	def organize_data(self, data, granularity=False):
		company_information = {}
		i, length = 0, len(data.index)
		for date, row in data.iterrows():
			if granularity:	date = str(date)
			else: date = str(date).split(' ')[0]
			information = row.iteritems()
			for item in information:
				symbol, key, value = item[0][0], item[0][1], item[1]
				if symbol not in company_information:
					company_information[symbol] = { date : {} }
				else:
					if date not in company_information[symbol]:
						company_information[symbol][date] = { key : value }
					else:
						company_information[symbol][date][key] = value
			i += 1
			self.print_progress_bar(i, length, suffix=date.split(' ')[0], prefix='Organizing... ')
		print("\033[A" +  ' '*150+ "\033[A")
		return company_information

	# writes the company_information dictionary to json 
	def write_to_json(self, company_information, folder):	
		i, length = 0, len(company_information)
		for company in company_information:
			file_location = 'Database/TimeSeriesData/{}/{}.json'.format(folder, company)
			info = json.dumps(company_information[company])
			with open(file_location, 'w+') as file:
				file.write(info)
			i += 1
			self.print_progress_bar(i, length, suffix=company, prefix='Writing data to files... ')
		print("\033[A" +  ' '*150+ "\033[A")
		return 

	# retrieves the date periods we need for collection
	def get_date_periods(self, distance_back):	
		today = datetime.date.today()
		delta = datetime.timedelta(days=(distance_back-1))
		current_date = today - delta
		if distance_back < 30:
			delta = datetime.timedelta(days=7)
			date_periods = []
			while today > current_date:
				date_periods.append(current_date)
				current_date = current_date + delta
			date_periods.append(today)
		else: 
			date_periods = (current_date, today)
		return date_periods

	# organizes the file structure on first launch
	def set_up_db(self):
		folders = ('1m','2m','5m','15m','30m','60m','90m','1d','5d','1wk','1mo','3mo')
		if os.path.exists('Database'):
			if os.path.exists('Database/TimeSeriesData'):
				for folder in folders:
					if os.path.exists('Database/TimeSeriesData/{}'.format(folder)):
						continue
					else:
						os.makedirs('Database/TimeSeriesData/{}'.format(folder))
			else:
				for folder in folders:
					os.makedirs('Database/TimeSeriesData/{}'.format(folder))
		else:
			for folder in folders:
				os.makedirs('Database/TimeSeriesData/{}'.format(folder))			
		return 
		
	# don't need to touch this function	
	def print_progress_bar( self, iteration, total, 
							prefix = '', suffix = ': ', 
							decimals = 1, length = 50, 
							fill = '█', printEnd = '\r' ):
		percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
		filledLength = int( length*iteration//total)
		bar = fill * filledLength + '-' * (length - filledLength)
		print(f'\r{prefix} |{bar}| {percent}% {suffix}    ', end = printEnd)
		if iteration == total: 
			print()
		return 

if __name__ == '__main__':
	start = time.time()
	init = TimeSeriesInitializer()
	elapsed = time.time() - start
	print('Initialization took {} seconds to run'.format(elapsed//60))
