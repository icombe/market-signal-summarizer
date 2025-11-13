import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest, GetOrdersRequest, MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import QueryOrderStatus, OrderSide, TimeInForce, AssetClass

# Global Variables
alpaca_key = None
secret_key = None
trading_client = None

def get_previous_orders():
    # Get the last 100 closed orders
    get_orders_data = GetOrdersRequest(
        status=QueryOrderStatus.CLOSED,
        limit=100,
        nested=True
    )

    orders = trading_client.get_orders(filter=get_orders_data)
    return orders

def place_order(ticker, amount):
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

    # not sure what these are doing yet
    # preparing limit order
    limit_order_data = LimitOrderRequest(
                        symbol="BTC/USD",
                        limit_price=17000,
                        notional=4000,
                        side=OrderSide.SELL,
                        time_in_force=TimeInForce.FOK
                    )

    # Limit order
    limit_order = trading_client.submit_order(
                    order_data=limit_order_data
                )
    return



def get_assets():
    global trading_client
    search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
    assets = trading_client.get_all_assets(search_params)
    return assets


def main():
    global alpaca_key, secret_key, trading_client

    load_dotenv()
    alpaca_key = os.getenv("TEST_KEY")
    secret_key = os.getenv("TEST_SECRET_KEY")
    trading_client = TradingClient(alpaca_key, secret_key, paper=True)

    # Get our account information.
    account = trading_client.get_account()
    # Get assets
    positions = trading_client.get_all_positions()

    print('Assets: {}'.format(positions))
    print('${} is available as buying power.'.format(account.buying_power))
    print('Portfolio is worth ${}.'.format(account.portfolio_value))


if __name__ == "__main__":
    main()
