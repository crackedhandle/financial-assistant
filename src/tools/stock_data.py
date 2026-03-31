import yfinance as yf

def get_stock_price(ticker: str) -> dict:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get("currentPrice") or info.get("regularMarketPrice")
        if not price:
            hist = stock.history(period="1d")
            if not hist.empty:
                price = round(hist["Close"].iloc[-1], 2)
        return {
            "ticker": ticker.upper(),
            "price": price,
            "name": info.get("longName", ticker),
            "currency": info.get("currency", "USD"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "pe_ratio": info.get("trailingPE"),
            "market_cap": info.get("marketCap"),
        }
    except Exception as e:
        return {"error": f"Could not fetch data for {ticker}: {str(e)}"}