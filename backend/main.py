from dotenv import load_dotenv
import os
import chat

def getKeys():
    load_dotenv()
    
    # get the keys from .env
    keys_dict = {"chat_key": os.getenv("OPENAI_API_KEY"), 
                 "marketaux_key": os.getenv("MARKETAUX_API_KEY"), 
                 "alpaca_key": os.getenv("ALPACA_API_KEY")}
    return keys_dict



def main():
    
    # Testing chat.py and marketaux.py
    keys_dict = getKeys()
    chat.test_chat(keys_dict)
    
    # figures, history, generate new
    return

if __name__ == "__main__":
    main()