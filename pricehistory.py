import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_stock_price_history(ticker, plot=True):
    """
    Get complete stock price history for Indian stocks.
    
    Parameters:
    ticker (str): Stock ticker (e.g., 'TCS.NS', 'RELIANCE.NS')
    plot (bool): Whether to plot the price history
    
    Returns:
    pandas.DataFrame: Stock price history with OHLCV data
    """
    
    # Add .NS suffix if not present
    if not ticker.endswith('.NS') and not ticker.endswith('.BO'):
        ticker = ticker + '.NS'
    
    # Get stock data
    stock = yf.Ticker(ticker)
    hist = stock.history(period='max')    
    stock_info = stock.balance_sheet
    print(stock_info)
    
    # Plot if requested
    if plot and not hist.empty:
        plt.figure(figsize=(12, 8))
        
        # Price plot
        plt.subplot(2, 1, 1)
        plt.plot(hist.index, hist['Close'], linewidth=1, color='blue')
        plt.title(f"{ticker} - Stock Price History")
        plt.ylabel('Price (₹)')
        plt.grid(True, alpha=0.3)
        
        # Volume plot
        plt.subplot(2, 1, 2)
        plt.plot(hist.index, hist['Volume'], linewidth=1, color='orange')
        plt.title('Trading Volume')
        plt.ylabel('Volume')
        plt.xlabel('Date')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    return hist

# Example usage
if __name__ == "__main__":
    # Single stock with plot
    ticker = "TCS.NS"
    data = get_stock_price_history(ticker, plot=True)
    
    print(f"Stock: {ticker}")
    print(f"Data from: {data.index[0].date()} to {data.index[-1].date()}")
    print(f"Total rows: {len(data)}")
    print("\nFirst 5 rows:")
    print(data.head())
    
    # Multiple stocks with plots
    stock = 'TCS.NS'
    
    print("\n" + "="*50)
    print("Multiple Stocks with Plots:")
    
    print(f"\nGetting data for {stock}...")
    data = get_stock_price_history(stock, plot=True)
    print(f"Rows: {len(data)}, From: {data.index[0].date()} to {data.index[-1].date()}")
    
    # If you want data without plots, set plot=False
    print("\n" + "="*50)
    print("Data only (no plots):")
    
    data_only = get_stock_price_history("INFY.NS", plot=False)
    print(data_only.head())