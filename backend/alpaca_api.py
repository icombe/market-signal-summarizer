import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest, MarketOrderRequest
from alpaca.trading.enums import QueryOrderStatus, OrderSide, TimeInForce
from alpaca.data import StockHistoricalDataClient, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

# Global Variables
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
        return []

def get_previous_orders():
    try:
        get_orders_data = GetOrdersRequest(
            status=QueryOrderStatus.CLOSED,
            limit=100,
            nested=True
        )
        orders = trading_client.get_orders(filter=get_orders_data)
        return orders

    except Exception as e:
        print("Error fetching previous orders:", e)
        return []

def place_order(ticker, amount):
    try:
        market_order_data = MarketOrderRequest(
            symbol=ticker,
            notional=10,
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
            return {"error": "Not enough data for YTD calculation"}

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

def main():
    load_keys_and_client()

    print(get_account())
    print(get_positions())
    print(get_previous_orders())

if __name__ == "__main__":
    main()
