import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest, MarketOrderRequest
from alpaca.trading.enums import QueryOrderStatus, OrderSide, TimeInForce
from alpaca.data import StockHistoricalDataClient, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

alpaca_key = None
secret_key = None
trading_client = None


def load_keys_and_client():
    global alpaca_key, secret_key, trading_client
    try:
        load_dotenv()
        alpaca_key = os.getenv("TEST_KEY")
        secret_key = os.getenv("TEST_SECRET_KEY")

        if not alpaca_key or not secret_key:
            raise ValueError("Missing API keys from environment variables")

        trading_client = TradingClient(alpaca_key, secret_key, paper=True)
    except Exception as e:
        print("Error loading keys or initializing client:", e)
        trading_client = None
    return


def get_porfolio():
    return trading_client.get_portfolio_history()


def get_account():
    try:
        return trading_client.get_account()
    except Exception as e:
        print("Error fetching account:", e)
        return None


def get_positions():
    try:
        return trading_client.get_all_positions()
    except Exception as e:
        print("Error fetching positions:", e)
        return None


def get_previous_orders():
    try:
        get_orders_data = GetOrdersRequest(
            status=QueryOrderStatus.CLOSED,
            limit=100,
            nested=True
        )
        return trading_client.get_orders(filter=get_orders_data)
    except Exception as e:
        print("Error fetching previous orders:", e)
        return None


def place_order(ticker, amount):
    try:
        market_order_data = MarketOrderRequest(
            symbol=ticker,
            notional=amount,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY
        )
        return trading_client.submit_order(order_data=market_order_data)
    except Exception as e:
        print(f"Error placing order for {ticker}:", e)
        return None


def get_ytd_percent_change(ticker):
    try:
        data_client = StockHistoricalDataClient(alpaca_key, secret_key)
        year_start = datetime(datetime.now().year, 1, 1)

        req = StockBarsRequest(
            symbol_or_symbols=ticker,
            timeframe=TimeFrame.Day,
            start=year_start
        )

        bars = data_client.get_stock_bars(req)[ticker].bars
        if len(bars) < 2:
            return {"error": "Not enough data"}

        first_close = bars[0].close
        last_close = bars[-1].close
        pct_change = ((last_close - first_close) / first_close) * 100

        return {
            "symbol": ticker.upper(),
            "ytd_percent_change": pct_change,
            "start_close": first_close,
            "current_close": last_close,
        }
    except Exception as e:
        print(f"Error calculating YTD percent change for {ticker}:", e)
        return {"error": str(e)}


############################################################
# New features: history fetch, current price, performance, plots
############################################################

def get_history(ticker, days=90):
    try:
        data_client = StockHistoricalDataClient(alpaca_key, secret_key)
        end = datetime.utcnow()
        start = end - timedelta(days=days)

        req = StockBarsRequest(
            symbol_or_symbols=ticker,
            timeframe=TimeFrame.Day,
            start=start,
            end=end
        )

        result = data_client.get_stock_bars(req)
        return result[ticker].bars

    except Exception as e:
        print(f"Error fetching history for {ticker}:", e)
        return None


def get_current_price(ticker):
    bars = get_history(ticker, days=2)
    if not bars:
        return None
    return bars[-1].close


def get_position_performance(position):
    symbol = position.symbol
    qty = float(position.qty)
    current_price = get_current_price(symbol)

    if current_price is None:
        return {"error": "Unable to fetch price"}

    cost_basis = float(position.cost_basis)
    market_value = qty * current_price
    dollar_change = market_value - cost_basis
    percent_change = (dollar_change / cost_basis) * 100

    return {
        "symbol": symbol,
        "qty": qty,
        "current_price": current_price,
        "cost_basis": cost_basis,
        "market_value": market_value,
        "dollar_change": dollar_change,
        "percent_change": percent_change
    }


def plot_history(ticker, days=90):
    bars = get_history(ticker, days)

    if not bars:
        print(f"No data for {ticker}")
        return

    dates = [b.timestamp for b in bars]
    closes = [b.close for b in bars]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, closes)
    plt.title(f"{ticker} Price History ({days} days)")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def show_portfolio_dashboard():
    positions = get_positions()

    if not positions:
        print("No positions found.")
        return

    for p in positions:
        perf = get_position_performance(p)
        if "error" in perf:
            print(f"{p.symbol}: {perf['error']}")
            continue

        print("\nTicker:", perf["symbol"])
        print("Quantity:", perf["qty"])
        print("Current Price:", perf["current_price"])
        print("Cost Basis:", perf["cost_basis"])
        print("Market Value:", perf["market_value"])
        print("Change ($):", perf["dollar_change"])
        print("Change (%):", perf["percent_change"])

        plot_history(p.symbol, days=120)


############################################################

def main():
    load_keys_and_client()
    show_portfolio_dashboard()


if __name__ == "__main__":
    main()
