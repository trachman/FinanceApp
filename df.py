import pandas as pd 
import json

# use regex eventually it is far more efficient
def to_dict(FILE):
    with open(FILE,'r') as file:
        data = file.readlines()
        companies = {}
        current_company, current_statement = None, None
        for line in data:
                line = repr(line)[:-3].split(':')
                if len(line) == 1 and repr(line[0]) not in (repr("'INCOME-STATEMENT"),repr("'BALANCE-SHEET"),repr("'CASH-FLOW")): 
                    if repr(line[0]) == repr("'"): continue
                    current_company = repr(line[0]).replace("'",'').split(' ')[0].replace('"','')
                    companies[current_company] = {}
                    continue
                if repr(line[0]) in (repr("'INCOME-STATEMENT"),repr("'BALANCE-SHEET"),repr("'CASH-FLOW")):
                    current_statement = line[0].replace("'",'')
                    companies[current_company][current_statement] = {}
                    continue
                else:
                    line = [ item.strip().replace("'",'') for item in line ]
                    section = line[0].replace('"','')
                    data = line[1].split(', ')
                    companies[current_company][current_statement][section] = data
    return companies

def print_dict(companies):
    for company in companies:
        print(company)
        for statement in companies[company]:
            print(statement)
            for key, value in companies[company][statement].items():
                print(key, value)

def to_json(companies,FILE):
    with open(FILE, 'w') as file: 
        json.dump(companies, file)

def read_json(FILE):
    with open(FILE,'r') as file:
        data = file.readlines()
        data = json.loads(data[0])
    return data

# retrieves companies as a list 
def company_list(JSON):
    return list(JSON.keys())

# FILE = 'Database/NasdaqFinancialStatements.txt'
# JSON_FILE = 'Database/NasdaqFinancialStatements.json'
# companies = to_dict(FILE)
# to_json(companies, JSON_FILE)
# companies = read_json(JSON_FILE)
