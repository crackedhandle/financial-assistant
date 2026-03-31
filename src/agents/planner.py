import os, json
import google.generativeai as genai
from dotenv import load_dotenv

def create_plan(user_query: str) -> dict:
    load_dotenv(override=True)
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = """You are a financial planning agent. Output a JSON plan only.
Available tools: get_stock_price (ticker), get_news (ticker), get_portfolio (), calculate_return (buy_price, current_price, quantity), compound_interest (principal, rate, years), sharpe_ratio (avg_return, risk_free_rate, std_dev).
Rules: use get_stock_price if ticker mentioned, get_news for outlook, get_portfolio for holdings. Output ONLY valid JSON.
Example: {"tasks": [{"tool": "get_stock_price", "params": {"ticker": "AAPL"}}]}"""
    response = model.generate_content(prompt + f"\n\nUser query: {user_query}\n\nJSON plan:")
    text = response.text.strip().replace("`json", "").replace("`", "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"tasks": []}
