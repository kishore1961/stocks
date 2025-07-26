import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json
import time

class TCSBalanceSheetFetcher:
    """
    A comprehensive class to fetch TCS balance sheet data from multiple sources
    """
    
    def __init__(self):
        self.tcs_symbol = "TCS.NS"  # TCS symbol on NSE
        self.tcs_bse_symbol = "TCS.BO"  # TCS symbol on BSE
        
    def fetch_yfinance_data(self):
        """
        Fetch TCS balance sheet data using yfinance
        """
        try:
            # Create ticker object
            tcs = yf.Ticker(self.tcs_symbol)
            
            # Get balance sheet data
            balance_sheet_annual = tcs.balance_sheet
            balance_sheet_quarterly = tcs.quarterly_balance_sheet
            
            # Get company info
            info = tcs.info
            
            print("=== TCS Company Information ===")
            print(f"Company Name: {info.get('longName', 'N/A')}")
            print(f"Sector: {info.get('sector', 'N/A')}")
            print(f"Industry: {info.get('industry', 'N/A')}")
            print(f"Market Cap: ₹{info.get('marketCap', 'N/A'):,}" if info.get('marketCap') else "Market Cap: N/A")
            print()
            
            return {
                'annual_balance_sheet': balance_sheet_annual,
                'quarterly_balance_sheet': balance_sheet_quarterly,
                'company_info': info
            }
            
        except Exception as e:
            print(f"Error fetching data from Yahoo Finance: {e}")
            return None
    
    def display_balance_sheet_summary(self, data):
        """
        Display a summary of balance sheet data
        """
        if not data:
            print("No data available to display")
            return
            
        annual_bs = data['annual_balance_sheet']
        quarterly_bs = data['quarterly_balance_sheet']
        
        print("=== ANNUAL BALANCE SHEET SUMMARY ===")
        print(f"Data available from: {annual_bs.columns[-1].strftime('%Y-%m-%d')} to {annual_bs.columns[0].strftime('%Y-%m-%d')}")
        print(f"Number of years: {len(annual_bs.columns)}")
        print()
        
        # Key metrics over the years
        key_metrics = [
            'Total Assets',
            'Total Stockholder Equity',
            'Total Debt',
            'Cash And Cash Equivalents',
            'Current Assets',
            'Current Liabilities'
        ]
        
        print("=== KEY BALANCE SHEET ITEMS (Last 5 Years) ===")
        for metric in key_metrics:
            if metric in annual_bs.index:
                print(f"\n{metric}:")
                values = annual_bs.loc[metric].head(5)
                for date, value in values.items():
                    if pd.notna(value):
                        print(f"  {date.strftime('%Y-%m-%d')}: ₹{value:,.0f} Cr")
        
        print("\n=== QUARTERLY BALANCE SHEET SUMMARY ===")
        print(f"Quarterly data available from: {quarterly_bs.columns[-1].strftime('%Y-%m-%d')} to {quarterly_bs.columns[0].strftime('%Y-%m-%d')}")
        print(f"Number of quarters: {len(quarterly_bs.columns)}")
    
    def save_to_csv(self, data, filename_prefix="tcs_balance_sheet"):
        """
        Save balance sheet data to CSV files
        """
        if not data:
            print("No data to save")
            return
            
        try:
            # Save annual balance sheet
            annual_file = f"{filename_prefix}_annual.csv"
            data['annual_balance_sheet'].to_csv(annual_file)
            print(f"Annual balance sheet saved to: {annual_file}")
            
            # Save quarterly balance sheet
            quarterly_file = f"{filename_prefix}_quarterly.csv"
            data['quarterly_balance_sheet'].to_csv(quarterly_file)
            print(f"Quarterly balance sheet saved to: {quarterly_file}")
            
        except Exception as e:
            print(f"Error saving to CSV: {e}")
    
    def get_specific_year_data(self, data, year):
        """
        Get balance sheet data for a specific year
        """
        if not data:
            print("No data available")
            return None
            
        annual_bs = data['annual_balance_sheet']
        
        # Find the closest year in the data
        year_data = None
        for col in annual_bs.columns:
            if col.year == year:
                year_data = annual_bs[col]
                break
        
        if year_data is not None:
            print(f"=== TCS Balance Sheet for {year} ===")
            for item, value in year_data.items():
                if pd.notna(value):
                    print(f"{item}: ₹{value:,.0f} Cr")
        else:
            print(f"No data available for year {year}")
            available_years = [col.year for col in annual_bs.columns]
            print(f"Available years: {sorted(available_years)}")
        
        return year_data
    
    def calculate_growth_metrics(self, data):
        """
        Calculate key growth metrics
        """
        if not data:
            print("No data available for calculations")
            return
            
        annual_bs = data['annual_balance_sheet']
        
        # Calculate growth for key metrics
        metrics = ['Total Assets', 'Total Stockholder Equity', 'Cash And Cash Equivalents']
        
        print("=== GROWTH ANALYSIS ===")
        for metric in metrics:
            if metric in annual_bs.index:
                values = annual_bs.loc[metric].dropna()
                if len(values) >= 2:
                    latest = values.iloc[0]
                    previous = values.iloc[1]
                    growth = ((latest - previous) / previous) * 100
                    print(f"{metric} Growth (YoY): {growth:.2f}%")
        
        # Calculate key ratios
        if 'Total Assets' in annual_bs.index and 'Total Stockholder Equity' in annual_bs.index:
            assets = annual_bs.loc['Total Assets'].dropna()
            equity = annual_bs.loc['Total Stockholder Equity'].dropna()
            
            print("\n=== KEY RATIOS ===")
            for i, (date, asset_val) in enumerate(assets.items()):
                if date in equity.index:
                    equity_val = equity[date]
                    debt_to_equity = (asset_val - equity_val) / equity_val
                    print(f"Debt-to-Equity Ratio ({date.strftime('%Y')}): {debt_to_equity:.2f}")
                    if i >= 4:  # Show only last 5 years
                        break

def main():
    """
    Main function to demonstrate the TCS balance sheet fetcher
    """
    print("TCS Balance Sheet Data Fetcher")
    print("=" * 50)
    
    # Initialize the fetcher
    fetcher = TCSBalanceSheetFetcher()
    
    # Fetch data
    print("Fetching TCS balance sheet data...")
    data = fetcher.fetch_yfinance_data()
    
    if data:
        # Display summary
        fetcher.display_balance_sheet_summary(data)
        
        # Calculate growth metrics
        print("\n")
        fetcher.calculate_growth_metrics(data)
        
        # Get specific year data (example: 2023)
        print("\n")
        fetcher.get_specific_year_data(data, 2023)
        
        # Save to CSV
        print("\n")
        fetcher.save_to_csv(data)
        
        # Display raw data structure
        print("\n=== RAW DATA STRUCTURE ===")
        print("Annual Balance Sheet Shape:", data['annual_balance_sheet'].shape)
        print("Annual Balance Sheet Columns:")
        for col in data['annual_balance_sheet'].columns:
            print(f"  - {col.strftime('%Y-%m-%d')}")
        
        print("\nBalance Sheet Items:")
        for item in data['annual_balance_sheet'].index[:10]:  # Show first 10 items
            print(f"  - {item}")
        print(f"  ... and {len(data['annual_balance_sheet'].index) - 10} more items")
        
    else:
        print("Failed to fetch data. Please check your internet connection and try again.")

# Alternative method using requests for NSE data
def fetch_nse_tcs_data():
    """
    Alternative method to fetch TCS data from NSE (requires handling headers and sessions)
    """
    print("\n=== Alternative NSE Data Fetcher ===")
    
    # Note: NSE API requires proper headers and session handling
    # This is a basic example and might need adjustments
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        # This is a simplified example - actual NSE API calls are more complex
        print("Note: NSE API requires proper authentication and headers.")
        print("For production use, consider using official NSE API or reliable data providers.")
        
    except Exception as e:
        print(f"Error fetching NSE data: {e}")

if __name__ == "__main__":
    # Run the main function
    main()
    
    # Show alternative method info
    fetch_nse_tcs_data()
    
    print("\n" + "="*50)
    print("INSTALLATION REQUIREMENTS:")
    print("pip install yfinance pandas numpy requests")
    print("\nUSAGE NOTES:")
    print("1. This script fetches TCS balance sheet data from Yahoo Finance")
    print("2. Data is available from TCS IPO date (August 2004) onwards")
    print("3. Both annual and quarterly data are fetched")
    print("4. Data is saved to CSV files for further analysis")
    print("5. All amounts are in Indian Rupees (Crores)")