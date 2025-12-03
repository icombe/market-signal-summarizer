# alpaca connection
import os
import http.client, urllib.parse
import json
import requests
from dotenv import load_dotenv
from datetime import date
import trafilatura



def getArticles(num_articles):
    load_dotenv()
    # marketaux_key = keys["marketaux_key"]
    marketaux_key = os.getenv("MARKETAUX_API_KEY")
    
    # Build a request

    conn = http.client.HTTPSConnection('api.marketaux.com')
    
    formatted_date = date.today().strftime("%Y-%m-%d")

    params = urllib.parse.urlencode({
        'api_token': marketaux_key,             # our api key
        # 'symbols': ",".join(company_symbols),   # what companies we want to focus on
        'limit': num_articles,                             # number of articles
        # 'published_after': formatted_date,      # getting articles from today
        # 'entity_types':["index","equity"],      # example entity_types    (use join)
        # 'industries': [Technology,Industrials], # example industries      (use join)
        'countries': 'us',    # example countries
        # 'sentiment_gte': (-1, 1),               # gets sentiment greater than number provided
        # 'filter_entities': True,                # uncomment if you want to only get your company entities
        # 'must_have_entities': True,             # uncomment if you want only articles that have your companies in them
        # 'language': 'en'                        # uncomment if you only want english articles
        })

    # requests data
    conn.request('GET', '/v1/news/all?{}'.format(params))
    res = conn.getresponse()
    data = res.read()
    decoded_data = data.decode('utf-8')
    full_json = json.loads(decoded_data)
    # with open("full_json.json", "w") as json_file: # Removed .json files
    #     json.dump(full_json, json_file, indent=4)
    
    article_dict = full_json['data'] # using json to load the data into python dict

    return article_dict

def getFullArticle(article_dict):
    url = article_dict['url']

    html = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0"
    }).text
    text = trafilatura.extract(html)
    return text

def getOneArticle():
    article = getArticles(1)
    full_text = getFullArticle(article[0])
    return full_text
        
def getThreeArticles():
    articles = getArticles(3)
    i = 1
    print(f"Found {len(articles)} articles.")
    full_text_list = []
    for article in articles:
        full_text_list.append(getFullArticle(article))
        # file_path = f"article_jsons/article {i}.json"
        # with open(file_path, "w") as json_file:
        #     json.dump(article, json_file, indent=4)
        i += 1
        
    return full_text_list

def main():
    getOneArticle()
    
    

if __name__ == "__main__":
    main()