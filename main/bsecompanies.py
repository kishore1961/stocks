from bsedata.bse import BSE
import pandas as pd
import time
import requests
import json
import os


class BSECompaniesExtractor:

    def __init__(self):

        """
        Initialize the BSECompaniesExtractor class
        """
        self.bse = None         

    def fix_bsedata_library(self):
        """
        Fix the bsedata library by updating the stock list
        """
        try:
            print("Attempting to fix bsedata library...")
            b = BSE()
            # Try to update the stock list
            b.updateScripCodes()
            print("BSE data updated successfully!")
            return True
        except Exception as e:
            print(f"Failed to update BSE data: {str(e)}")
            return False


    def extract_all_company_names(self):
        """
        Extract all company names from BSE using bsedata library
        """
        # First try to fix the library
        if not self.fix_bsedata_library():
            print("Trying alternative approach...")
            return self.extract_companies_web_scraping()
        
        # Initialize BSE object
        b = BSE()
        
        try:
            # Get list of all companies
            print("Fetching company list from BSE...")
            company_list = b.getScripCodes()
            
            if not company_list:
                print("No companies found or API error")
                return self.extract_companies_web_scraping()
            
            # Extract company names and codes
            companies_data = []
            
            print(f"Found {len(company_list)} companies. Processing...")
            
            for i, (scrip_code, company_name) in enumerate(company_list.items()):
                companies_data.append({
                    'Scrip_Code': scrip_code,
                    'Company_Name': company_name
                })
                
                # Progress indicator
                if (i + 1) % 100 == 0:
                    print(f"Processed {i + 1} companies...")
            
            # Create DataFrame
            df = pd.DataFrame(companies_data)
            
            print(f"\nSuccessfully extracted {len(df)} company names!")
            return df
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None
        
    def save_to_file(self,df, filename='data/bse_companies.csv'):
        """
        Save company data to CSV file
        """
        try:
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving file: {str(e)}")

    def display_sample_data(self,df, n=10):
        """
        Display sample company data
        """
        print(f"\nSample of {n} companies:")
        print("-" * 50)
        print(df.head(n).to_string(index=False))
        print(f"\nTotal companies: {len(df)}")

    def search_company(self,df, search_term):
        """
        Search for companies containing specific term
        """
        if df is None:
            print("No data available")
            return
        
        matches = df[df['Company_Name'].str.contains(search_term, case=False, na=False)]
        
        if len(matches) > 0:
            print(f"\nFound {len(matches)} companies matching '{search_term}':")
            print("-" * 50)
            print(matches.to_string(index=False))
        else:
            print(f"No companies found matching '{search_term}'")

    def extract_companies_web_scraping(self):
        """
        Alternative method using direct web scraping approach
        """
        try:
            print("Using web scraping approach...")
            
            # BSE equity list URL
            url = "https://api.bseindia.com/BseIndiaAPI/api/ListOfScripData/w"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Referer': 'https://www.bseindia.com/'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                companies_data = []
                
                for item in data.get('Table', []):
                    companies_data.append({
                        'Scrip_Code': item.get('Scrip_Cd', ''),
                        'Company_Name': item.get('Scrip_Name', ''),
                        'Group': item.get('Group_Name', ''),
                        'Face_Value': item.get('Face_value', '')
                    })
                
                if companies_data:
                    df = pd.DataFrame(companies_data)
                    print(f"Successfully extracted {len(df)} companies using web scraping!")
                    return df
                
        except Exception as e:
            print(f"Web scraping failed: {str(e)}")
        
        # Fallback to manual company list
        return self.create_manual_company_list()
    
    def create_manual_company_list(self):
        """
        Create a manual list of popular BSE companies as fallback
        """
        print("Using manual company list as fallback...")
        
        manual_companies = [
            {'Scrip_Code': '500325', 'Company_Name': 'RELIANCE INDUSTRIES LTD'},
            {'Scrip_Code': '500209', 'Company_Name': 'INFOSYS LTD'},
            {'Scrip_Code': '532540', 'Company_Name': 'TATA CONSULTANCY SERVICES LTD'},
            {'Scrip_Code': '500010', 'Company_Name': 'HDFC BANK LTD'},
            {'Scrip_Code': '532215', 'Company_Name': 'AXIS BANK LTD'},
            {'Scrip_Code': '500034', 'Company_Name': 'BAJAJ FINANCE LTD'},
            {'Scrip_Code': '500696', 'Company_Name': 'HINDUSTAN UNILEVER LTD'},
            {'Scrip_Code': '500180', 'Company_Name': 'HDFC LTD'},
            {'Scrip_Code': '500112', 'Company_Name': 'STATE BANK OF INDIA'},
            {'Scrip_Code': '532281', 'Company_Name': 'HOUSING DEVELOPMENT FINANCE CORPORATION LTD'},
            {'Scrip_Code': '500820', 'Company_Name': 'ASIAN PAINTS LTD'},
            {'Scrip_Code': '500790', 'Company_Name': 'NESTLE INDIA LTD'},
            {'Scrip_Code': '532187', 'Company_Name': 'INDUSIND BANK LTD'},
            {'Scrip_Code': '500875', 'Company_Name': 'ITC LTD'},
            {'Scrip_Code': '532454', 'Company_Name': 'BHARTI AIRTEL LTD'},
            {'Scrip_Code': '500087', 'Company_Name': 'CIPLA LTD'},
            {'Scrip_Code': '532555', 'Company_Name': 'NTPC LTD'},
            {'Scrip_Code': '500550', 'Company_Name': 'TATA STEEL LTD'},
            {'Scrip_Code': '532424', 'Company_Name': 'COAL INDIA LTD'},
            {'Scrip_Code': '500440', 'Company_Name': 'HINDALCO INDUSTRIES LTD'}
        ]
        
        df = pd.DataFrame(manual_companies)
        print(f"Created manual list with {len(df)} popular companies")
        return df
    


bse_extractor = BSECompaniesExtractor()


# Extract all company names
companies_df = bse_extractor.extract_all_company_names()

if companies_df is not None:
    # Display sample data
    bse_extractor.display_sample_data(companies_df)
    
    # Save to CSV file
    bse_extractor.save_to_file(companies_df)
    
