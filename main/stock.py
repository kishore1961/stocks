import requests


class Stock:

    url = "https://api.tickertape.in/screener/query"

    headers = {
    'user-agent':
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

    def __init__(self,name: str="",exchange: str = ""):
        self.name = name
        self.sector = ""
        self.symbol = ""
        self.exchange = exchange
        self.market_cap = 0.0
        self.price = 0.0
        self.pe_ratio = 0.0
        self.dividend_yield = 0.0
        self.beta = 0.0
        self.volume = 0
        self.avg_volume = 0
        self.open = 0.0
        self.close = 0.0
        self.high = 0.0
        self.low = 0.0
        self.year_high = 0.0
        self.year_low = 0.0


    def get_market_cap(self,company_name_or_ticker):

        payload = {
            "match": {},
            "sortOrder": -1,
            "project": ["subindustry", "mrktCapf", "lastPrice", "apef"],
            "offset": 0,
            "sids": []
        }

        response = requests.post(url=Stock.url, json=payload, headers=Stock.headers).json()
        
        print(response)

        for result in response['data']['results']:
            info = result['stock']['info']
            ratios = result['stock']['advancedRatios']

            name = info.get('name', '').lower()
            ticker = info.get('ticker', '').lower()
            input_lower = company_name_or_ticker.lower()

            if input_lower in name or input_lower == ticker:
                marketcap = ratios.get('mrktCapf')
                return float(marketcap) if marketcap else None

        return None  # If company not found

    
reliance = Stock("RELIANCE")
reliance.market_cap = reliance.get_market_cap(reliance.name)

print(reliance.market_cap)  # Try 'RELIANCE', 'Reliance Industries', etc.

# market cap data 2050710.9029563603

