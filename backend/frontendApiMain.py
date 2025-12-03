# Make any API Calls here.

# Follow the format for generateSignal()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

import main

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)