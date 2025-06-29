from bsedata.bse import BSE
import pandas as pd
import json
from datetime import datetime
import time

class Stock:
    def __init__(self):
        """Initialize BSE data extractor using only bsedata library"""
        try:
            self.bse = BSE()
            print("✓ BSE data library initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing BSE library: {e}")
            raise
    
    def get_quote(self, scrip_code):
        """Get quote data for a company"""
        try:
            quote = self.bse.getQuote(scrip_code)
            return quote
        except Exception as e:
            print(f"Error getting quote for {scrip_code}: {e}")
            return None
    
    def get_top_gainers(self):
        """Get top gainers"""
        try:
            gainers = self.bse.topGainers()
            return gainers
        except Exception as e:
            print(f"Error getting top gainers: {e}")
            return None
    
    def get_top_losers(self):
        """Get top losers"""
        try:
            losers = self.bse.topLosers()
            return losers
        except Exception as e:
            print(f"Error getting top losers: {e}")
            return None
    
    def get_category_data(self, category="A"):
        """Get category-wise stock data"""
        try:
            if category == "A":
                return self.bse.getScripCodes()
            # Note: bsedata library has limited category functions
            return None
        except Exception as e:
            print(f"Error getting category data: {e}")
            return None
    
    def search_scrip(self, company_name):
        """Search for scrip code by company name (limited functionality)"""
        try:
            # This is a basic implementation - bsedata doesn't have built-in search
            scrip_codes = self.bse.getScripCodes()
            if scrip_codes:
                # Simple search in available data
                matches = []
                for code, name in scrip_codes.items():
                    if company_name.lower() in name.lower():
                        matches.append((code, name))
                return matches
            return None
        except Exception as e:
            print(f"Error searching scrip: {e}")
            return None
    
    def get_comprehensive_data(self, scrip_code):
        """Get all available data for a company using bsedata library"""
        print(f"Fetching data for scrip code: {scrip_code}")
        print("=" * 50)
        
        company_data = {
            'scrip_code': scrip_code,
            'fetch_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'quote_data': None,
            'market_data': {
                'top_gainers': None,
                'top_losers': None
            }
        }
        
        # 1. Get Quote Data
        print("1. Fetching quote data...")
        company_data['quote_data'] = self.get_quote(scrip_code)
        if company_data['quote_data']:
            print("   ✓ Quote data retrieved")
        else:
            print("   ✗ Quote data failed")
        
        time.sleep(0.5)
        
        # 2. Get Market Data (for context)
        print("2. Fetching market data...")
        company_data['market_data']['top_gainers'] = self.get_top_gainers()
        company_data['market_data']['top_losers'] = self.get_top_losers()
        
        if company_data['market_data']['top_gainers']:
            print("   ✓ Top gainers data retrieved")
        if company_data['market_data']['top_losers']:
            print("   ✓ Top losers data retrieved")
        
        return company_data
    

    
    def save_data(self, company_data, filename_prefix=None):
        """Save data to files"""
        scrip_code = company_data['scrip_code']
        if filename_prefix:
            base_filename = f"data/{filename_prefix}_{scrip_code}"
        else:
            base_filename = f"data/bsedata_{scrip_code}"
        
        # Save as JSON
        json_filename = f"{base_filename}.json"
        try:
            with open(json_filename, 'w') as f:
                json.dump(company_data, f, indent=2, default=str)
            print(f"✓ Data saved to: {json_filename}")
        except Exception as e:
            print(f"✗ Error saving JSON: {e}")

    
    def batch_quotes(self, scrip_codes):
        """Get quotes for multiple companies"""
        results = {}
        
        for scrip_code in scrip_codes:
            print(f"\nFetching data for {scrip_code}...")
            quote = self.get_quote(scrip_code)
            if quote:
                results[scrip_code] = quote
                print(f"✓ Success: {quote.get('companyName', 'Unknown')}")
            else:
                print(f"✗ Failed to get data for {scrip_code}")
            
            time.sleep(0.5)  # Rate limiting
        
        return results

"""Main function demonstrating bsedata library usage"""
print("BSE Data Extractor - Pure bsedata Library")
print("=" * 50)

try:
    extractor = Stock()
except:
    print("Failed to initialize BSE data extractor")

# Get scrip code from user
scrip_code = input("Enter BSE scrip code (e.g., 500325 for Reliance): ").strip()

if not scrip_code:
    print("Using default scrip code: 500325 (Reliance)")
    scrip_code = "500325"

# Get comprehensive data
company_data = extractor.get_comprehensive_data(scrip_code)

# Save data
print(f"\n💾 SAVING DATA:")
extractor.save_data(company_data)

print(f"\n✅ Data extraction completed!")


# # Show what's available vs what's not
# print(f"\n📊 BSEDATA LIBRARY CAPABILITIES:")
# print("✓ Available:")
# print("  - Basic quote data (price, change, volume, etc.)")
# print("  - Top gainers and losers")
# print("  - Scrip codes list")

# print("\n✗ NOT Available (requires direct API calls):")
# print("  - Detailed financial statements")
# print("  - Historical price data")
# print("  - Company profile/fundamentals")
# print("  - Annual reports")
# print("  - Corporate actions")
    


# Example: Get data for multiple companies
def example_batch_processing():
    """Example of batch processing multiple companies"""
    extractor = Stock()
    
    # Popular stock scrip codes
    scrip_codes = [
        "500325",  # Reliance
        "500209",  # Infosys  
        "532540",  # TCS
        "500696",  # Hindunilever
        "500010"   # HDFC Bank
    ]
    
    print("Batch processing example:")
    results = extractor.batch_quotes(scrip_codes)
    
    # Create summary
    if results:
        print(f"\n📈 BATCH RESULTS SUMMARY:")
        print("-" * 60)
        for scrip_code, data in results.items():
            name = data.get('companyName', 'Unknown')
            price = data.get('currentValue', 'N/A')
            change = data.get('pChange', 'N/A')
            print(f"{scrip_code:8} | {name:20} | ₹{price:>8} | {change:>6}%")
    
    return results


    
# Uncomment to run batch example
# print("\n" + "="*60)
# example_batch_processing()