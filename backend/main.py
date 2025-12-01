from dotenv import load_dotenv
import os
import chat
import marketaux

def generateThreeSignal():
    articles = marketaux.getThreeArticles()
    article_dicts = chat.get_dicts(articles)
    front_end_dicts = []
    for article in article_dicts:
        new_dict = {}
        new_dict['summary'] = article['summary']
        new_dict['sentiment'] = article['sentiment_label']
        new_dict['action'] = article['suggested_action']
        front_end_dicts.append(new_dict)
        
    return front_end_dicts

def generateSignal():
    articles = marketaux.getOneArticle()
    article_dicts = chat.get_dicts([articles])
    front_end_dicts = []
    for article in article_dicts:
        new_dict = {}
        new_dict['summary'] = article['summary']
        new_dict['sentiment'] = article['sentiment_score']
        new_dict['action'] = article['suggested_action']
        front_end_dicts.append(new_dict)
        
    return front_end_dicts[0]

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
    # keys_dict = getKeys()
    # chat.test_chat()
    print(generateSignal())
    
    return

if __name__ == "__main__":
    main()