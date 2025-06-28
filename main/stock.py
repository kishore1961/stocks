import requests
from pprint import pprint


class Stock:

    url = "https://api.tickertape.in/screener/query"

    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    def __init__(self, name: str = "", exchange: str = ""):
        self.name = name
        self.symbol = ""
        self.exchange = exchange
        self.sector = ""
        self.subindustry = ""

        # Financial attributes
        self.market_cap = 0.0
        self.price = 0.0
        self.prev_close = 0.0
        self.day_high = 0.0
        self.day_low = 0.0
        self.volume = 0
        self.avg_volume = 0
        self.pe_ratio = 0.0
        self.pb_ratio = 0.0
        self.apef = 0.0
        self.eps = 0.0
        self.div_yield = 0.0
        self.roe = 0.0
        self.roce = 0.0
        self.de_ratio = 0.0
        self.opm = 0.0
        self.npm = 0.0
        self.ev_ebitda = 0.0
        self.peg = 0.0
        self.price_to_sales = 0.0
        self.beta = 0.0
        self.volatility = 0.0

        # Returns
        self.returns = {}

    def fetch_stock_data(self, company_name_or_ticker):
        payload = {
            "match": {},
            "sortOrder": -1,
            "project": [
                "ticker", "name", "sector", "subindustry", "sid",
                "lastPrice", "prevClose", "dayHigh", "dayLow", "volume", "avgVolume",
                "priceToBook", "mrktCapf", "apef", "pe", "pb", "eps", "divYield",
                "revenueGrowth3Y", "profitGrowth3Y", "roe", "roce", "deRatio",
                "opm", "npm", "evEbitda", "peg", "priceToSales", "beta", "volatility",
                "1DReturn", "5DReturn", "1MReturn", "3MReturn", "6MReturn",
                "1YReturn", "3YReturn", "5YReturn"
            ],
            "offset": 0,
            "sids": [],
            "count": 1
        }

        response = requests.post(url=Stock.url, json=payload, headers=Stock.headers).json()

        for result in response['data']['results']:
            info = result['stock']['info']
            ratios = result['stock']['advancedRatios']

            name = info.get('name', '').lower()
            ticker = info.get('ticker', '').lower()
            input_lower = company_name_or_ticker.lower()

            if input_lower in name or input_lower == ticker:
                self.name = info.get('name', '')
                self.symbol = info.get('ticker', '')
                self.sector = info.get('sector', '')
                self.subindustry = ratios.get('subindustry', '')

                self.price = ratios.get('lastPrice', 0.0)
                self.prev_close = ratios.get('prevClose', 0.0)
                self.day_high = ratios.get('dayHigh', 0.0)
                self.day_low = ratios.get('dayLow', 0.0)
                self.volume = ratios.get('volume', 0)
                self.avg_volume = ratios.get('avgVolume', 0)
                self.market_cap = ratios.get('mrktCapf', 0.0)
                self.pe_ratio = ratios.get('pe', 0.0)
                self.pb_ratio = ratios.get('pb', 0.0)
                self.apef = ratios.get('apef', 0.0)
                self.eps = ratios.get('eps', 0.0)
                self.div_yield = ratios.get('divYield', 0.0)
                self.roe = ratios.get('roe', 0.0)
                self.roce = ratios.get('roce', 0.0)
                self.de_ratio = ratios.get('deRatio', 0.0)
                self.opm = ratios.get('opm', 0.0)
                self.npm = ratios.get('npm', 0.0)
                self.ev_ebitda = ratios.get('evEbitda', 0.0)
                self.peg = ratios.get('peg', 0.0)
                self.price_to_sales = ratios.get('priceToSales', 0.0)
                self.beta = ratios.get('beta', 0.0)
                self.volatility = ratios.get('volatility', 0.0)

                self.returns = {
                    "1D": ratios.get('1DReturn'),
                    "5D": ratios.get('5DReturn'),
                    "1M": ratios.get('1MReturn'),
                    "3M": ratios.get('3MReturn'),
                    "6M": ratios.get('6MReturn'),
                    "1Y": ratios.get('1YReturn'),
                    "3Y": ratios.get('3YReturn'),
                    "5Y": ratios.get('5YReturn'),
                }

                return True  # success

        return False  # company not found

    def display(self):
        print(f"\n📈 Stock: {self.name} ({self.symbol})")
        print(f"Sector: {self.sector} | Subindustry: {self.subindustry}")
        print(f"Price: ₹{self.price} | Market Cap: ₹{self.market_cap:,.2f}")
        print(f"PE Ratio: {self.pe_ratio} | PB Ratio: {self.pb_ratio} | APEF: {self.apef}")
        print(f"Dividend Yield: {self.div_yield}% | EPS: {self.eps}")
        print(f"ROE: {self.roe}% | ROCE: {self.roce}% | D/E Ratio: {self.de_ratio}")
        print(f"OPM: {self.opm}% | NPM: {self.npm}% | EV/EBITDA: {self.ev_ebitda}")
        print(f"PEG: {self.peg} | Price/Sales: {self.price_to_sales}")
        print(f"Beta: {self.beta} | Volatility: {self.volatility}")
        print("Returns (%):")
        for k, v in self.returns.items():
            print(f"  {k}: {v}")
        print()


# ✅ Usage
reliance = Stock()
if reliance.fetch_stock_data("RELIANCE"):
    reliance.display()
else:
    print("Company not found.")
