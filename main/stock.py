import json
from bsedata.bse import BSE
from typing import List, Dict, Optional
import pandas as pd

class BSEStock:
    """
    A comprehensive class for fetching and managing BSE stock data
    """
    
    def __init__(self, stock_code: str = "", name: str = ""):
        # Initialize BSE object
        self.bse = BSE()
        
        # Basic stock information
        self.stock_code = stock_code
        self.name = name
        self.security_id = ""
        self.group = ""
        self.face_value = 0.0
        
        # Price information
        self.current_price = 0.0
        self.previous_close = 0.0
        self.open_price = 0.0
        self.day_high = 0.0
        self.day_low = 0.0
        self.change = 0.0
        self.percent_change = 0.0
        
        # Volume and trading data
        self.volume = 0
        self.value = 0.0
        self.total_traded_quantity = 0
        self.total_traded_value = 0.0
        
        # 52-week data
        self.week_52_high = 0.0
        self.week_52_low = 0.0
        
        # Market cap and other metrics
        self.market_cap = 0.0
        self.book_value = 0.0
        self.dividend_yield = 0.0
        self.ttm_eps = 0.0
        self.ttm_pe = 0.0
        
        # Additional data
        self.isin_code = ""
        self.listing_date = ""
        self.industry = ""
        
        # Metadata
        self.last_updated = ""
        self.is_valid = False


    def fetch_stock_data(self, stock_code: str = None) -> bool:
        """
        Fetch comprehensive stock data from BSE
        
        Args:
            stock_code: BSE stock code (e.g., '500325' for Reliance)
            
        Returns:
            bool: True if data fetched successfully, False otherwise
        """

        try:
            code = stock_code or self.stock_code
            if not code:
                print("❌ No stock code provided")
                return False
            
            if not self.bse.verifyScripCode(code):
                print(f"❌ Invalid stock code: {code}")
                return False
            
            # Fetch stock quote
            data = self.bse.getQuote(code)
            
            if not data:
                print(f"❌ No data found for stock code: {code}")
                return False
            
            # Populate basic information
            self.stock_code = code
            self.security_id = data.get('securityID', '')
            self.name = data.get('companyName', '')
            self.group = data.get('group', '')
            self.face_value = float(data.get('faceValue', 0))
            
            # Populate price information
            self.current_price = float(data.get('currentValue', 0))
            self.previous_close = float(data.get('previousClose', 0))
            self.open_price = float(data.get('openValue', 0))
            self.day_high = float(data.get('dayHigh', 0))
            self.day_low = float(data.get('dayLow', 0))
            self.change = float(data.get('change', 0))
            self.percent_change = float(data.get('pChange', 0))
            
            # Populate volume and trading data
            self.total_traded_quantity = int(data.get('totalTradedQuantity', 0))
            self.total_traded_value = float(data.get('totalTradedValue', 0))
            
            # Populate 52-week data
            self.week_52_high = float(data.get('52weekHigh', 0))
            self.week_52_low = float(data.get('52weekLow', 0))
            
            # Additional financial metrics (if available)
            self.market_cap = float(data.get('marketCap', 0))
            self.book_value = float(data.get('bookValue', 0))
            self.dividend_yield = float(data.get('dividendYield', 0))
            self.ttm_eps = float(data.get('ttmEPS', 0))
            self.ttm_pe = float(data.get('ttmPE', 0))
            
            # Additional data
            self.isin_code = data.get('isinCode', '')
            self.industry = data.get('industry', '')
            
            # Metadata
            self.last_updated = data.get('lastUpdateTime', '')
            self.is_valid = True
            
            return True
            
        except Exception as e:
            print(f"❌ Error fetching data for {code}: {e}")
            self.is_valid = False
            return False


    def search_stock_by_name(self, company_name: str) -> Optional[str]:
        """
        Search for stock code by company name (basic implementation)
        Note: BSE API doesn't have direct search, so this is a helper method
        
        Args:
            company_name: Name of the company to search
            
        Returns:
            Optional[str]: Stock code if found, None otherwise
        """
        # Common stock codes mapping (you can expand this)

        with open("stk.json", "r") as f:
            common_stocks = json.load(f)

        
        name_lower = company_name.lower().strip()
        return common_stocks.get(name_lower)


    def to_dict(self) -> Dict:
        """
        Convert stock object to dictionary
        
        Returns:
            Dict: Dictionary representation of stock data
        """
        return {
            "stock_code": self.stock_code,
            "name": self.name,
            "security_id": self.security_id,
            "group": self.group,
            "face_value": self.face_value,
            "current_price": self.current_price,
            "previous_close": self.previous_close,
            "open_price": self.open_price,
            "day_high": self.day_high,
            "day_low": self.day_low,
            "change": self.change,
            "percent_change": self.percent_change,
            "total_traded_quantity": self.total_traded_quantity,
            "total_traded_value": self.total_traded_value,
            "week_52_high": self.week_52_high,
            "week_52_low": self.week_52_low,
            "market_cap": self.market_cap,
            "book_value": self.book_value,
            "dividend_yield": self.dividend_yield,
            "ttm_eps": self.ttm_eps,
            "ttm_pe": self.ttm_pe,
            "isin_code": self.isin_code,
            "industry": self.industry,
            "last_updated": self.last_updated,
            "is_valid": self.is_valid
        }


    def display_stock_info(self):
        """
        Display formatted stock information
        """
        if not self.is_valid:
            print("❌ No valid stock data available")
            return
        
        print("=" * 60)
        print(f"🏢 {self.name} ({self.security_id})")
        print(f"📊 Stock Code: {self.stock_code}")
        print("=" * 60)
        print(f"💰 Current Price: ₹{self.current_price:,.2f}")
        print(f"📈 Change: ₹{self.change:+,.2f} ({self.percent_change:+.2f}%)")
        print(f"🔄 Previous Close: ₹{self.previous_close:,.2f}")
        print(f"🌅 Open: ₹{self.open_price:,.2f}")
        print(f"⬆️  Day High: ₹{self.day_high:,.2f}")
        print(f"⬇️  Day Low: ₹{self.day_low:,.2f}")
        print("-" * 60)
        print(f"📊 Volume: {self.total_traded_quantity:,}")
        print(f"💵 Value: ₹{self.total_traded_value:,.2f}")
        print(f"🏔️  52W High: ₹{self.week_52_high:,.2f}")
        print(f"🏞️  52W Low: ₹{self.week_52_low:,.2f}")
        if self.ttm_pe > 0:
            print(f"📊 P/E Ratio: {self.ttm_pe:.2f}")
        if self.ttm_eps > 0:
            print(f"💹 EPS: ₹{self.ttm_eps:.2f}")
        print("=" * 60)


    @staticmethod
    def get_market_indices() -> Dict:
        """
        Get BSE market indices data
        
        Returns:
            Dict: Market indices data
        """
        try:
            bse = BSE()
            indices = bse.getIndices()
            return indices
        except Exception as e:
            print(f"❌ Error fetching indices: {e}")
            return {}


    @staticmethod
    def get_top_gainers(limit: int = 10) -> List[Dict]:
        """
        Get top gaining stocks
        
        Args:
            limit: Number of stocks to return
            
        Returns:
            List[Dict]: List of top gaining stocks
        """
        try:
            bse = BSE()
            gainers = bse.topGainers()
            return gainers[:limit]
        except Exception as e:
            print(f"❌ Error fetching top gainers: {e}")
            return []


    @staticmethod
    def get_top_losers(limit: int = 10) -> List[Dict]:
        """
        Get top losing stocks
        
        Args:
            limit: Number of stocks to return
            
        Returns:
            List[Dict]: List of top losing stocks
        """
        try:
            bse = BSE()
            losers = bse.topLosers()
            return losers[:limit]
        except Exception as e:
            print(f"❌ Error fetching top losers: {e}")
            return []


    @staticmethod
    def validate_stock_code(stock_code: str) -> bool:
        """
        Validate if a stock code exists
        
        Args:
            stock_code: BSE stock code to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            bse = BSE()
            return bse.verifyScripCode(stock_code)
        except:
            return False





# Example 1: Fetch single stock data
print("🚀 BSE Stock Data Fetcher")
print("=" * 50)


company_df = pd.read_csv("bse_companies.csv")
print(f"📊 Total Companies: {len(company_df)}")


company_name = "ABB India Limited"
print(f"🔍 Searching for stock code of '{company_name}'...")

company_code = company_df.loc[company_df['Company_Name'] == 'ABB India Limited', 'Scrip_Code'].values[0]
print(company_code)

abb = BSEStock(company_code,company_name)

abb.fetch_stock_data()




# if reliance.fetch_stock_data('500325'):  # Reliance stock code
#     reliance.display_stock_info()




# # Example 2: Fetch multiple stocks
# stock_codes = ['500325', '532540', '500209']  # Reliance, TCS, Infosys
# stock_names = ['Reliance', 'TCS', 'Infosys']
# stocks_data = []

# print("\n📊 Fetching Multiple Stocks:")
# print("=" * 50)

# for code, name in zip(stock_codes, stock_names):
#     stock = BSEStock()
#     if stock.fetch_stock_data(code):
#         print(f"✅ Fetched: {name}")
#         stocks_data.append(stock.to_dict())
#     else:
#         print(f"❌ Failed: {name}")

# # Save to JSON
# with open("bse_stocks_data.json", "w") as f:
#     json.dump(stocks_data, f, indent=4)
# print("💾 Data saved to bse_stocks_data.json")

# # Example 3: Get market indices
# print("\n📈 BSE Market Indices:")
# print("=" * 50)
# indices = BSEStock.get_market_indices()
# for name, data in list(indices.items())[:5]:
#     print(f"{name}: {data.get('currentValue', 'N/A')} ({data.get('change', 'N/A')})")

# # Example 4: Get top gainers and losers
# print("\n🏆 Top 5 Gainers:")
# print("-" * 30)
# gainers = BSEStock.get_top_gainers(5)
# for i, stock in enumerate(gainers, 1):
#     print(f"{i}. {stock.get('securityID', 'N/A')} - {stock.get('pChange', 'N/A')}%")

# print("\n📉 Top 5 Losers:")
# print("-" * 30)
# losers = BSEStock.get_top_losers(5)
# for i, stock in enumerate(losers, 1):
#     print(f"{i}. {stock.get('securityID', 'N/A')} - {stock.get('pChange', 'N/A')}%")

