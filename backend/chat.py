# chat connection
import os
from dotenv import load_dotenv, find_dotenv
import json
import requests
from marketaux import getThreeArticles
import json
import re

def extract_json_block(text: str) -> str:
    """
    Extracts the primary JSON object in the string from marketaux, ignoring any extra text.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)

def article_analysis(chat_key, chat_responses_url, model, article_text: str, source: str = "unknown") -> dict:
    """
    Takes the entire article from marketaux and uses GPT-5-Nano to summarize these factors into a JSON dictionary:
    - summary
    - sentiment_score
    - sentiment_label
    - key_entities
    - suggested_action
    - confidence
    """
    
    prompt = f"""
You are a financial analysis machine that takes news about the latest financial and stock market developments and summarizes
them. Given the following full article, produce only a valid JSON object that contains these fields:
{{
    "summary" : "2-3 sentence summary of the article",
    "sentiment_score" : "float between -1.0 and 1.0 reflecting the overarching sentiment of the article",
    "sentiment_label" : "one of ["negative", "neutral", "positive"],
    "key_entities" : ["list of important companies, people, and tickers"],
    "suggested_action" : "one of ["buy", "hold", "sell"], reflecting your interpretation of short-term market impact",
    "confidence" : "float between 0.0 and 1.0 reflecting confidence in your analysis"
}}

article source: {source}

Here is the article:
{article_text}
"""

    headers = {
        "Authorization": f"Bearer {chat_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": model,
        "input": prompt,
        "max_output_tokens": 3000
    }

    # Sends the request to the chat api
    response = requests.post(chat_responses_url, headers=headers, json=body, timeout=30)
    data = response.json()

    # Extracts the text output from the response
    text = ""
    if "output" in data and isinstance(data["output"], list):
        for item in data["output"]:
            if "content" in item:
                for c in item["content"]:
                    if c.get("type") in ["text", "output_text"]:
                        text += c.get("text", "")
    text = text.strip()

    # Extracts only the JSON object from the text output
    json_text = extract_json_block(text)
    parsed = json.loads(json_text)

    return parsed


def test_chat(keys):
    chat_key = keys["chat_key"]
    chat_responses_url = "https://api.openai.com/v1/responses"
    model = "gpt-5-nano"

    articles = getThreeArticles(keys=keys)

    for i, text in enumerate(articles, start=1):
        result = article_analysis(
            chat_key=chat_key,
            chat_responses_url=chat_responses_url,
            model=model,
            article_text=text
            )

        # Save JSON to file
        with open(f"analysis_{i}.json", "w", encoding="utf-8") as out:
            json.dump(result, out, indent=4)

    print("Finished processing all articles.")


