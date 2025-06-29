from bsedata.bse import BSE
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time

class BSECompanyDataExtractor:
    def __init__(self):
        """Initialize BSE data extractor"""
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
    
    def get_basic_quote(self, scrip_code):
        """Get basic quote data using bsedata library"""
        if not self.bse_available:
            return None
        
        try:
            quote = self.bse.getQuote(scrip_code)
            return quote
        except Exception as e:
            print(f"Error getting quote via bsedata: {e}")
            return None
    
    def get_company_data_api(self, scrip_code):
        """Get company data using direct BSE API calls"""
        try:
            # BSE Quote API
            quote_url = f"https://api.bseindia.com/BseIndiaAPI/api/StockReachGraph/w"
            
            params = {
                'scripcode': scrip_code,
                'flag': 'sp',
                'fromdate': (datetime.now() - timedelta(days=30)).strftime('%Y%m%d'),
                'todate': datetime.now().strftime('%Y%m%d'),
                'seriesid': ''
            }
            
            response = requests.get(quote_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"Error fetching from BSE API: {e}")
            return None
    
    def get_detailed_quote(self, scrip_code):
        """Get detailed quote information"""
        try:
            url = f"https://api.bseindia.com/BseIndiaAPI/api/ComHeader/w"
            params = {'quotetype': 'EQ', 'scripcode': scrip_code}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"Error getting detailed quote: {e}")
            return None
    

    
    def get_company_financials(self, scrip_code):
        """Get company financial data"""
        try:
            url = "https://api.bseindia.com/BseIndiaAPI/api/AnnualReport/w"
            params = {'scripcode': scrip_code}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"Error getting financials: {e}")
            return None
    
    def get_company_profile(self, scrip_code):
        """Get company profile and details"""
        try:
            url = "https://api.bseindia.com/BseIndiaAPI/api/CompanyMasterData/w"
            params = {'scripcode': scrip_code}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"Error getting company profile: {e}")
            return None
    
    def get_all_company_data(self, scrip_code):
        """Get comprehensive company data"""
        print(f"Fetching comprehensive data for scrip code: {scrip_code}")
        print("=" * 60)
        
        company_data = {
            'scrip_code': scrip_code,
            'fetch_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'basic_quote': None,
            'detailed_quote': None,
            'financials': None,
        }
        
        # 1. Basic Quote (using bsedata if available)
        print("1. Fetching basic quote...")
        company_data['basic_quote'] = self.get_basic_quote(scrip_code)
        if company_data['basic_quote']:
            print("   ✓ Basic quote retrieved")
        else:
            print("   ✗ Basic quote failed")

    
        time.sleep(0.5)  # Rate limiting
        
        # 2. Detailed Quote
        print("2. Fetching detailed quote...")
        company_data['detailed_quote'] = self.get_detailed_quote(scrip_code)
        if company_data['detailed_quote']:
            print("   ✓ Detailed quote retrieved")
        else:
            print("   ✗ Detailed quote failed")
        
        time.sleep(0.5)
        
        
        # 4. Company Financials
        print("4. Fetching financial data...")
        company_data['financials'] = self.get_company_financials(scrip_code)
        if company_data['financials']:
            print("   ✓ Financial data retrieved")
        else:
            print("   ✗ Financial data failed")
        
        time.sleep(0.5)
        
        # 5. Company Profile
        print("5. Fetching company profile...")
        company_data['company_profile'] = self.get_company_profile(scrip_code)
        if company_data['company_profile']:
            print("   ✓ Company profile retrieved")
        else:
            print("   ✗ Company profile failed")
        
        return company_data
    
    def save_to_files(self, company_data, prefix=None):
        """Save company data to various files"""
        scrip_code = company_data['scrip_code']
        if prefix:
            filename_base = f"{prefix}_{scrip_code}"
        else:
            filename_base = f"company_data_{scrip_code}"
        
        # Save complete data as JSON
        json_filename = f"{filename_base}_complete.json"
        try:
            with open(json_filename, 'w') as f:
                json.dump(company_data, f, indent=2, default=str)
            print(f"✓ Complete data saved to: {json_filename}")
        except Exception as e:
            print(f"✗ Error saving JSON: {e}")

        
        # Save summary as text
        try:
            summary_filename = f"{filename_base}_summary.txt"
            with open(summary_filename, 'w') as f:
                f.write(f"Company Data Summary - {scrip_code}\n")
                f.write(f"Generated on: {company_data['fetch_time']}\n")
                f.write("=" * 50 + "\n\n")
                
                # Basic quote summary
                basic_quote = company_data.get('basic_quote')
                if basic_quote:
                    f.write("BASIC QUOTE INFORMATION:\n")
                    for key, value in basic_quote.items():
                        f.write(f"  {key}: {value}\n")
                    f.write("\n")
            
            print(f"✓ Summary saved to: {summary_filename}")
        except Exception as e:
            print(f"✗ Error saving summary: {e}")

def main():
    """Main function to demonstrate usage"""
    extractor = BSECompanyDataExtractor()
    
    # Example usage
    print("BSE Company Data Extractor")
    print("=" * 40)
    
    # Get scrip code from user
    scrip_code = input("Enter BSE scrip code (e.g., 500325 for Reliance): ").strip()
    
    if not scrip_code:
        print("Using default scrip code: 500325 (Reliance)")
        scrip_code = "500325"
    
    # Fetch all company data
    company_data = extractor.get_all_company_data(scrip_code)
    
    # Save to files
    print(f"\n💾 SAVING DATA TO FILES:")
    extractor.save_to_files(company_data)
    
    print(f"\n✅ Data extraction completed for scrip code: {scrip_code}")
    return company_data

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

if __name__ == "__main__":
    # Single company extraction
    company_data = main()
