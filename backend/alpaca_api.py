import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest, MarketOrderRequest
from alpaca.trading.enums import QueryOrderStatus, OrderSide, TimeInForce

# Global Variables
alpaca_key = None
secret_key = None
trading_client = None


def load_keys_and_client():
    global alpaca_key, secret_key, trading_client

    load_dotenv()
    alpaca_key = os.getenv("TEST_KEY")
    secret_key = os.getenv("TEST_SECRET_KEY")
    trading_client = TradingClient(alpaca_key, secret_key, paper=True)

    return

def get_positions():
    account = trading_client.get_account()
    return trading_client.get_all_positions()
    
def get_previous_orders():
    # Get the last 100 orders made
    # returns a list of orders
    get_orders_data = GetOrdersRequest(
        status=QueryOrderStatus.CLOSED,
        limit=100,
        nested=True
    )

    orders = trading_client.get_orders(filter=get_orders_data)
    return orders

def place_order(ticker, amount):
    # place an order for a specified amount
    global trading_client
    # preparing market order
    market_order_data = MarketOrderRequest(
                        symbol=ticker,
                        qty=amount, # calculate amount of shares
                        side=OrderSide.BUY, # buy or sell here
                        time_in_force=TimeInForce.DAY
                        )

    # Market order
    market_order = trading_client.submit_order(
                    order_data=market_order_data
                )

    return


def main():
    load_keys_and_client()
    place_order('NVDA', 1)  # places 1 unit of ticker


if __name__ == "__main__":
    main()
