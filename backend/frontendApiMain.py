# Make any API Calls here.

# Follow the format for generateSignal()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from datetime import datetime

import alpaca_api
import main

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Request model for trading
class TradeRequest(BaseModel):
    ticker: str
    amount: float

# @app.on_event("startup")
def startup_event():
    alpaca_api.load_keys_and_client()

@app.get("/signal")
def generate_signal():
    article_list = main.generateThreeSignal()   # list of 3 summaries

    packaged = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for article in article_list:
        packaged.append({
            "id": int(datetime.now().timestamp()),
            "timestamp": timestamp,
            "summary": article["summary"],
            "sentiment": article["sentiment"],
            "ticker_recommendations": article["ticker_recommendations"]
        })

    return packaged

@app.get("/positions")
def get_positions():
    try:
        # Replace with your actual Alpaca API calls
        # Example structure:
        positions_data = alpaca_api.get_positions()
        account_data = alpaca_api.get_account()

        if positions_data is None or account_data is None:
            return {"error": "Unable to fetch data"}

        total_unrealized = sum(float(p.unrealized_pl) for p in positions_data)
        
        # Format the response
        formatted_positions = []
        for pos in positions_data:
            formatted_positions.append({
                "symbol": pos.symbol,
                "qty": float(pos.qty),
                "market_value": float(pos.market_value),
                "unrealized_pl": float(pos.unrealized_pl),
                "unrealized_plpc": float(pos.unrealized_plpc),
                "change_today": float(pos.unrealized_intraday_pl),
                "change_today_pc": float(pos.unrealized_intraday_plpc),
                "price_per_share": round((float(pos.market_value) / float(pos.qty)),2)
            })
        
        return {
            "positions": formatted_positions,
            "equity": float(account_data.equity),
            "cash": float(account_data.cash),
            "buying_power": float(account_data.buying_power),
            "total_unrealized_pl": total_unrealized
        }
    except Exception as e:
        print(f"Error fetching positions: {e}")
        return {
            "positions": [],
            "equity": 0,
            "cash": 0,
            "buying_power": 0,
            "total_unrealized_pl": 0
        }

@app.post("/place-order")
def place_buy_order(trade: TradeRequest):
    """
    Place a buy order for a given ticker and dollar amount
    """
    try:
        # Validate inputs
        if not trade.ticker or trade.ticker.strip() == "":
            raise HTTPException(status_code=400, detail="Ticker symbol is required")
        
        if trade.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")
        
        # Place the order
        result = alpaca_api.place_order(trade.ticker.upper(), trade.amount)
        
        if result is None:
            raise HTTPException(status_code=400, detail="Order placement failed. Check your API connection and account status.")
        
        return {
            "success": True,
            "message": f"Successfully placed buy order for ${trade.amount} of {trade.ticker.upper()}",
            "order_id": str(result.id) if hasattr(result, 'id') else None,
            "symbol": trade.ticker.upper(),
            "amount": trade.amount
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error placing buy order: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to place order: {str(e)}")

@app.post("/sell-order")
def place_sell_order(trade: TradeRequest):
    """
    Place a sell order for a given ticker and dollar amount
    """
    try:
        # Validate inputs
        if not trade.ticker or trade.ticker.strip() == "":
            raise HTTPException(status_code=400, detail="Ticker symbol is required")
        
        if trade.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")
        
        # Place the sell order
        result = alpaca_api.sell_position(trade.ticker.upper(), amount=trade.amount)
        
        if result is None:
            raise HTTPException(status_code=400, detail="Sell order failed. Check if you have a position in this ticker.")
        
        return {
            "success": True,
            "message": f"Successfully placed sell order for ${trade.amount} of {trade.ticker.upper()}",
            "order_id": str(result.id) if hasattr(result, 'id') else None,
            "symbol": trade.ticker.upper(),
            "amount": trade.amount
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error placing sell order: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to place sell order: {str(e)}")


if __name__ == "__main__":
    startup_event()
    uvicorn.run(app, host="127.0.0.1", port=8000)