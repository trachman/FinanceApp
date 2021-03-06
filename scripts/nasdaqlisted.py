import requests

def update_nasdaq_companies():
    url = 'http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt'
    response = requests.get(url)
    companies = response.content.decode()
    data = repr(companies).split(r'\r\n')
    data = data[:-2] # pop the last 2 lines
    FILE = 'Resources/NasdaqListed.txt'
    with open(FILE,'w+') as file:
        for line in data:
            file.write(line + '\n')

update_nasdaq_companies()