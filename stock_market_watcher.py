
import requests


url = 'http://google.com'
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo'
url = 'http://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=VIX&interval=60min&apikey=BUEP4L39E4POL2KK'
url = 'https://ws-api.iextrading.com/1.0/?symbols=FB'
url = 'https://www.alphavantage.co/query?apikey=BUEP4L39E4POL2KK&function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT'
url = 'https://api.iextrading.com/1.0/stock/VIX/stats'
url = 'https://api.iextrading.com/1.0/stock/BMY/stats'
r = requests.get(url,verify=False)
print r.text
