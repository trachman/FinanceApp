from df import read_json 

JSON_FILE = 'Database/NasdaqFinancialStatements.json'
JSON_DATA = read_json(JSON_FILE) 
print(JSON_DATA['GOOG'])