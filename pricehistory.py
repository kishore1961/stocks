import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def get_indian_stock_history(ticker, save_to_csv=True, plot=True):
    """
    Extract complete Indian stock price history since inception.
    
    Parameters:
    ticker (str): Indian stock ticker symbol (e.g., 'RELIANCE.NS', 'TCS.NS')
    save_to_csv (bool): Whether to save data to CSV file
    plot (bool): Whether to plot the price history
    
    Returns:
    pandas.DataFrame: Complete stock price history
    """
    
    try:
        # Ensure ticker has correct suffix for Indian stocks
        if not ticker.endswith('.NS') and not ticker.endswith('.BO'):
            # Default to NSE (.NS) if no suffix provided
            ticker = ticker + '.NS'
        
        # Create ticker object
        stock = yf.Ticker(ticker)
        
        # Get maximum available historical data
        hist = stock.history(period='max')
        
        if hist.empty:
            print(f"No data found for ticker: {ticker}")
            # Try BSE if NSE fails
            if ticker.endswith('.NS'):
                bse_ticker = ticker.replace('.NS', '.BO')
                print(f"Trying BSE ticker: {bse_ticker}")
                stock = yf.Ticker(bse_ticker)
                hist = stock.history(period='max')
                ticker = bse_ticker
            
            if hist.empty:
                print(f"No data found on both NSE and BSE for this ticker")
                return None
        
        # Get stock info
        info = stock.info
        company_name = info.get('longName', ticker)
        exchange = 'NSE' if ticker.endswith('.NS') else 'BSE'
        
        # Display basic information
        print(f"\n=== {company_name} ({ticker}) ===")
        print(f"Exchange: {exchange}")
        print(f"Data available from: {hist.index[0].strftime('%Y-%m-%d')}")
        print(f"Data available to: {hist.index[-1].strftime('%Y-%m-%d')}")
        print(f"Total trading days: {len(hist)}")
        print(f"Current price: ₹{hist['Close'][-1]:.2f}")
        
        # Calculate statistics
        first_price = hist['Close'].iloc[0]
        last_price = hist['Close'].iloc[-1]
        total_return = ((last_price - first_price) / first_price) * 100
        
        print(f"First recorded price: ₹{first_price:.2f}")
        print(f"Total return since inception: {total_return:.2f}%")
        
        # Add calculated columns
        hist['Daily_Return'] = hist['Close'].pct_change()
        hist['Cumulative_Return'] = (hist['Close'] / hist['Close'].iloc[0] - 1) * 100
        
        # Save to CSV
        if save_to_csv:
            clean_ticker = ticker.replace('.NS', '').replace('.BO', '')
            filename = f"{clean_ticker}_stock_history_{datetime.now().strftime('%Y%m%d')}.csv"
            hist.to_csv(filename)
            print(f"Data saved to: {filename}")
        
        # Plot
        if plot:
            plt.figure(figsize=(12, 8))
            
            plt.subplot(2, 1, 1)
            plt.plot(hist.index, hist['Close'], linewidth=1, color='blue')
            plt.title(f"{company_name} ({ticker}) - Stock Price History")
            plt.ylabel('Price (₹)')
            plt.grid(True, alpha=0.3)
            
            plt.subplot(2, 1, 2)
            plt.plot(hist.index, hist['Volume'], linewidth=1, color='orange')
            plt.title('Trading Volume')
            plt.ylabel('Volume')
            plt.xlabel('Date')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.show()
        
        return hist
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None

def get_multiple_indian_stocks(tickers, save_to_csv=True):
    """
    Extract stock history for multiple Indian stocks.
    
    Parameters:
    tickers (list): List of Indian stock ticker symbols
    save_to_csv (bool): Whether to save combined data to CSV
    
    Returns:
    dict: Dictionary with ticker as key and DataFrame as value
    """
    
    all_data = {}
    combined_close = pd.DataFrame()
    
    for ticker in tickers:
        print(f"\nFetching data for {ticker}...")
        data = get_indian_stock_history(ticker, save_to_csv=False, plot=False)
        
        if data is not None:
            all_data[ticker] = data
            combined_close[ticker] = data['Close']
    
    # Save combined data
    if save_to_csv and combined_close.shape[1] > 0:
        filename = f"indian_stocks_combined_{datetime.now().strftime('%Y%m%d')}.csv"
        combined_close.to_csv(filename)
        print(f"\nCombined closing prices saved to: {filename}")
    
    return all_data

def get_nifty_sensex_data():
    """
    Get Nifty 50 and Sensex index data.
    
    Returns:
    dict: Dictionary with index data
    """
    
    indices = {
        'NIFTY 50': '^NSEI',
        'SENSEX': '^BSESN',
        'NIFTY Bank': '^NSEBANK',
        'NIFTY IT': '^CNXIT'
    }
    
    index_data = {}
    
    for name, ticker in indices.items():
        print(f"\nFetching {name} data...")
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period='max')
            if not hist.empty:
                index_data[name] = hist
                print(f"{name}: Data from {hist.index[0].strftime('%Y-%m-%d')} to {hist.index[-1].strftime('%Y-%m-%d')}")
        except Exception as e:
            print(f"Error fetching {name}: {str(e)}")
    
    return index_data

# Popular Indian stock tickers (you can modify these)
POPULAR_INDIAN_STOCKS = {
    # IT Companies
    'TCS': 'TCS.NS',
    'Infosys': 'INFY.NS',
    'Wipro': 'WIPRO.NS',
    'HCL Tech': 'HCLTECH.NS',
    'Tech Mahindra': 'TECHM.NS',
    
    # Banking
    'HDFC Bank': 'HDFCBANK.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'SBI': 'SBIN.NS',
    'Kotak Bank': 'KOTAKBANK.NS',
    'Axis Bank': 'AXISBANK.NS',
    
    # Conglomerates
    'Reliance': 'RELIANCE.NS',
    'Tata Motors': 'TATAMOTORS.NS',
    'L&T': 'LT.NS',
    'ITC': 'ITC.NS',
    'Bharti Airtel': 'BHARTIARTL.NS',
    
    # Pharma
    'Sun Pharma': 'SUNPHARMA.NS',
    'Dr Reddy': 'DRREDDY.NS',
    'Cipla': 'CIPLA.NS',
    
    # FMCG
    'Hindustan Unilever': 'HINDUNILVR.NS',
    'Nestle India': 'NESTLEIND.NS',
    'Britannia': 'BRITANNIA.NS'
}

# Example usage
if __name__ == "__main__":
    print("=== Indian Stock Price History Extractor ===")
    
    # Single stock example
    print("\n1. Single Stock Example:")
    ticker = "TCS.NS"  # Change this to your desired ticker
    print(f"Fetching complete history for {ticker}...")
    
    stock_data = get_indian_stock_history(ticker)
    
    if stock_data is not None:
        print(f"\nFirst 5 rows:")
        print(stock_data.head())
        print(f"\nLast 5 rows:")
        print(stock_data.tail())
    
    # Multiple stocks example
    print("\n" + "="*60)
    print("2. Multiple Indian Stocks Example:")
    
    # Top 10 Indian stocks
    top_stocks = ['TCS.NS', 'RELIANCE.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS']
    all_stocks = get_multiple_indian_stocks(top_stocks)
    
    print(f"\nSuccessfully fetched data for {len(all_stocks)} stocks")
    
    # Display comparison
    if len(all_stocks) > 1:
        print("\n=== COMPARISON SINCE INCEPTION ===")
        for ticker, data in all_stocks.items():
            first_price = data['Close'].iloc[0]
            last_price = data['Close'].iloc[-1]
            total_return = ((last_price - first_price) / first_price) * 100
            print(f"{ticker}: {total_return:.2f}% total return")
    
    # Index data example
    print("\n" + "="*60)
    print("3. Indian Market Indices:")
    
    indices = get_nifty_sensex_data()
    
    print(f"\nAvailable indices: {list(indices.keys())}")
    
    # Show how to use popular stock symbols
    print("\n" + "="*60)
    print("4. Popular Indian Stock Symbols:")
    print("\nYou can use these tickers:")
    for company, ticker in list(POPULAR_INDIAN_STOCKS.items())[:10]:
        print(f"{company}: {ticker}")
    
    print(f"\n... and {len(POPULAR_INDIAN_STOCKS) - 10} more!")
    print("\nNote: Use .NS for NSE or .BO for BSE")