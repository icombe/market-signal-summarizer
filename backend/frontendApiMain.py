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
    allow_origins=["http://localhost:5173"],  # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)