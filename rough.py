import requests

def get_market_cap(company_name_or_ticker):
    url = 'https://api.tickertape.in/screener/query'

    payload = {
        "sortBy": "mrktCapf",
        "match": {},
        "sortOrder": -1,
        "project": ["subindustry", "mrktCapf", "lastPrice", "apef"],
        "offset": 0,
        "count": 500,
        "sids": []
    }

    headers = {
        'user-agent':
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    response = requests.post(url=url, json=payload, headers=headers).json()

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

# Example usage:
print(get_market_cap("RELIANCE"))  # Try 'RELIANCE', 'Reliance Industries', etc.

# market cap data 2050710.9029563603

