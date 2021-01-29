from df import read_json 
from app import get_current_price

JSON_FILE = 'Database/NasdaqFinancialStatements.json'
JSON_DATA = read_json(JSON_FILE) 

def negative_income_deltas():
    for company in JSON_DATA:
        try:
            years = JSON_DATA[company]['INCOME-STATEMENT']['Item']
            revenue = JSON_DATA[company]['INCOME-STATEMENT']['Sales/Revenue']
        except KeyError:
            years = JSON_DATA[company]['INCOME-STATEMENT']['Item']
            revenue = JSON_DATA[company]['INCOME-STATEMENT']['Interest Income']
        # percentage changes
        negative = False
        for i in range(len(revenue)):
            if i > 0 and revenue[i-1] != 0:
                difference = revenue[i] - revenue[i-1]
                delta = round((difference/revenue[i-1]) * 100,2)
                if delta < 0:
                    negative = True
                    print(company, delta, years[i])
        if negative:
            print(get_current_price(company))
            print()

# def positive_only():
#     for company in JSON_DATA:
#         try:
#             years = JSON_DATA[company]['INCOME-STATEMENT']['Item']
#             revenue = JSON_DATA[company]['INCOME-STATEMENT']['Sales/Revenue']
#         except KeyError:
#             years = JSON_DATA[company]['INCOME-STATEMENT']['Item']
#             revenue = JSON_DATA[company]['INCOME-STATEMENT']['Interest Income']
#         # percentage changes
#         negative = False
#         for i in range(len(revenue)):
#             if i > 0 and revenue[i-1] != 0:
#                 difference = revenue[i] - revenue[i-1]
#                 delta = round((difference/revenue[i-1]) * 100,2)
#                 if delta < 0:
#                     negative = True
#                     print(company, delta, years[i])
#         if negative:
#             print(get_current_price(company))
#             print()    


def PEratio():
    for company in JSON_DATA:
        EPS = JSON_DATA[company]['INCOME-STATEMENT']['EPS (Basic)']
        last_index = len(EPS)-1
        try:
            price = get_current_price(company)[0]
            earnings = float(EPS[last_index])
            print(company, 'PE RATIO:', round(price/earnings,2))
        except TypeError:
            continue
        except ZeroDivisionError:
            continue
        # except ValueError:
        #     # this is when they couldnt conver price to float
        #     # fix get price to return float
        #     continue

PEratio()