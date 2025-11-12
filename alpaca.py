# alpaca connection
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

alpaca_key = os.getenv("ALPACA_API_KEY")
