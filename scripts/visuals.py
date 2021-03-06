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

def PEratio(company, COMPANY_DICT):
    EPS = JSON_DATA[company]['INCOME-STATEMENT']['EPS (Basic)']
    last_index = len(EPS)-1
    try:
        price = get_current_price(company)[0]
        earnings = float(EPS[last_index])
        print(company, COMPANY_DICT[company],'PE RATIO:', round(price/earnings,2))
    except TypeError:
        pass
    except ZeroDivisionError:
        pass

# helper function so we know the names of the symbols
def company_dict():
    FILE = 'Resources/NasdaqListed.txt'
    with open(FILE,'r') as file:
        data = file.readlines()
    result = {}
    for i in range(len(data)):
        data[i] = data[i][:-2].split('|')[:2]
        data[i][1] = data[i][1].split(' - ')[0]
        result[data[i][0]] = data[i][1]
    return result

c = 'AMZN'
print(c)
for statement in JSON_DATA[c]:
    print()
    print(statement)
    for item in JSON_DATA[c][statement]:
        print(item, JSON_DATA[c][statement][item])
    print()
# COMPANY_DICT = company_dict()
# print(COMPANY_DICT['GOOG'])
# for company in JSON_DATA:
#     PEratio(company, COMPANY_DICT)