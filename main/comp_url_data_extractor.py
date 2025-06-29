from bsedata.bse import BSE
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time

class BSECompanyDataExtractor:
    def __init__(self,scrip_code=None):
        """Initialize BSE data extractor"""
        self.scrip_code = scrip_code

        try:
            self.bse = BSE()
            self.bse_available = True
        except:
            self.bse_available = False
            print("Warning: bsedata library not working, using alternative methods")
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.bseindia.com/',
            'Connection': 'keep-alive'
        }
    
    def get_basic_quote(self):
        """Get basic quote data using bsedata library"""
        if not self.bse_available:
            return None
        
        try:
            quote = self.bse.getQuote(self.scrip_code)
            return quote
        except Exception as e:
            print(f"Error getting quote via bsedata: {e}")
            return None

    def get_detailed_quote(self):
        """Get detailed quote information"""
        try:
            url = f"https://api.bseindia.com/BseIndiaAPI/api/ComHeader/w"
            params = {'quotetype': 'EQ', 'scripcode': self.scrip_code}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"Error getting detailed quote: {e}")
            return None
    
    def get_company_financials(self ):
        """Get company financial data"""
        try:
            url = "https://api.bseindia.com/BseIndiaAPI/api/AnnualReport/w"
            params = {'scripcode': self.scrip_code}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"Error getting financials: {e}")
            return None

    def get_all_company_data(self):
        """Get comprehensive company data"""
        print(f"Fetching comprehensive data for scrip code: {self.scrip_code}")
        print("=" * 60)
        
        company_data = {
            'scrip_code': self.scrip_code,
            'fetch_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'basic_quote': None,
            'detailed_quote': None,
            'financials': None,
        }
        
        # 1. Basic Quote (using bsedata if available)
        print("1. Fetching basic quote...")
        company_data['basic_quote'] = self.get_basic_quote()
        if company_data['basic_quote']:
            print("   ✓ Basic quote retrieved")
        else:
            print("   ✗ Basic quote failed")

    
        time.sleep(0.5)  # Rate limiting
        
        # 2. Detailed Quote
        print("2. Fetching detailed quote...")
        company_data['detailed_quote'] = self.get_detailed_quote()
        if company_data['detailed_quote']:
            print("   ✓ Detailed quote retrieved")
        else:
            print("   ✗ Detailed quote failed")
        
        time.sleep(0.5)
        
        
        # 3. Company Financials
        print("3. Fetching financial data...")
        company_data['financials'] = self.get_company_financials()
        if company_data['financials']:
            print("   ✓ Financial data retrieved")
        else:
            print("   ✗ Financial data failed")
        
        time.sleep(0.5)
        
        return company_data
    
    def save_to_files(self, company_data, prefix=None):
        """Save company data to various files"""
        scrip_code = company_data['scrip_code']
        company_name = company_data['company_name'] if 'company_name' in company_data else 'company_data'
        if prefix:
            filename_base = f"data/{prefix}_{self.scrip_code}"
        else:
            filename_base = f"data/{company_name}_url_{self.scrip_code}"
        
        # Save complete data as JSON
        json_filename = f"{filename_base}_complete.json"
        try:
            with open(json_filename, 'w') as f:
                json.dump(company_data, f, indent=2, default=str)
            print(f"✓ Complete data saved to: {json_filename}")
        except Exception as e:
            print(f"✗ Error saving JSON: {e}")


# Example usage for multiple companies
def batch_extract_companies(scrip_codes):
    """Extract data for multiple companies"""
    extractor = BSECompanyDataExtractor()
    all_companies_data = {}
    
    for scrip_code in scrip_codes:
        print(f"\nProcessing {scrip_code}...")
        company_data = extractor.get_all_company_data(scrip_code)
        all_companies_data[scrip_code] = company_data
        
        # Small delay between requests
        time.sleep(2)
    
    return all_companies_data


# This code uses the BSE URL directly, which is not recommended due to potential issues with scraping and rate limiting.
# However, it is included here for demonstration purposes.
bse_url = True

# fetch data using bse url which is not good to do

if bse_url:

    # Example usage
    print("BSE Company Data Extractor")
    print("=" * 40)

    # Get scrip code from user
    scrip_code = input("Enter BSE scrip code (e.g., 500325 for Reliance): ").strip()

    if not scrip_code:
        print("Using default scrip code: 500325 (Reliance)")
        scrip_code = "500325"
    
    start = time.time()
    print("Fetching data using BSE URL...")

    """Main function to demonstrate usage"""
    extractor = BSECompanyDataExtractor(scrip_code)

    company_data = extractor.get_all_company_data()

    # Save to files
    print(f"\n💾 SAVING DATA TO FILES:")
    extractor.save_to_files(company_data)

    print(f"\n✅ Data extraction completed for scrip code: {scrip_code}")
    end = time.time()
    print(f"Total time taken: {end - start:.2f} seconds")


else:
    print("Nothing to do, bse_url is set to False. This is not recommended for production use.")


