import yfinance as yf

def get_stock_news(ticker: str) -> str:
    try:
        stock = yf.Ticker(ticker)
        news = stock.news[:5]
        if not news:
            return f"No recent news found for {ticker}."
        lines = [f"Latest news for {ticker.upper()}:"]
        for item in news:
            title = item.get("content", {}).get("title", "No title")
            lines.append(f"- {title}")
        return "\n".join(lines)
    except Exception as e:
        return f"Could not fetch news for {ticker}: {str(e)}"