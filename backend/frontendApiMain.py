# Make any API Calls here.

# Follow the format for generateSignal()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
# @app.on_event("startup")
def startup_event():
    alpaca_api.load_keys_and_client()

@app.get("/signal")
def generate_signal():
    apiData = main.generateSignal()
    print(f'''
        "id": {int(datetime.now().timestamp())},
        "timestamp": {datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        "summary": "{apiData['summary']}",
        "sentiment": "{apiData['sentiment']}",
        "action": "{apiData['action']}"
    ''')
    return {
        "id": int(datetime.now().timestamp()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": apiData['summary'],
        "sentiment": apiData['sentiment'],
        "action": apiData['action']
    }

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


if __name__ == "__main__":
    startup_event()
    uvicorn.run(app, host="127.0.0.1", port=8000)