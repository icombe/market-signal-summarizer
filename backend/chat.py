# chat connection
import os
from dotenv import load_dotenv, find_dotenv
import json
import requests

load_dotenv()

chat_key = os.getenv("OPENAI_API_KEY")
chat_responses_url = "https://api.openai.com/v1/responses"
model = "gpt-5-nano"

def article_analysis(article_text: str, source: str = "unknown") -> dict:
    """
    Takes the entire article from marketaux and uses gpt-5-nano to summarize these factors into a JSON dictionary:
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
        "Authorization" : f"Bearer {chat_key}",
        "Content-Type" : "application/json:"
    }

    body = {
        "model" : model,
        "input" : prompt,
        "temperature" : 0.0,
        "max_output_tokens" : 500
    }

    # Sends the prompt request to OpenAi's API
    response = requests.post(chat_responses_url, headers=headers, json=body, timeout=30)

    # Parses the JSON outpute
    data = response.json()

    # Extracts the output from the model
    text = ""
    if "output" in data and isinstance(data["outpout"], list):
        for item in data["output"]:
            if "content" in item:
                for c in item["content"]:
                    if c.get("type") == "output_text":
                        text += c.get("text", "")
    
    # Converts JSON output into a Python dictionary
    return json.loads(text)


