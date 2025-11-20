from dotenv import load_dotenv
import os
import chat

def getKeys():
    load_dotenv()
    
    # get the keys from .env
    keys_dict = {"chat_key": os.getenv("OPENAI_API_KEY"), 
                 "marketaux_key": os.getenv("MARKETAUX_API_KEY"), 
                 "alpaca_key": os.getenv("ALPACA_API_KEY"),
                 "alpaca_secret_key":os.getenv("ALPACA_SECRET_API_KEY")}
    return keys_dict


def main():
    
    # Testing chat.py and marketaux.py
    keys_dict = getKeys()
    chat.test_chat(keys_dict)
    
    return

if __name__ == "__main__":
    main()