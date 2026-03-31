def calculate_return(buy_price: float, current_price: float, quantity: int = 1) -> dict:
    profit = (current_price - buy_price) * quantity
    percent = ((current_price - buy_price) / buy_price) * 100
    return {
        "buy_price": buy_price,
        "current_price": current_price,
        "quantity": quantity,
        "profit_loss": round(profit, 2),
        "percent_return": round(percent, 2),
    }

def compound_interest(principal: float, rate: float, years: int) -> dict:
    amount = principal * ((1 + rate / 100) ** years)
    return {
        "principal": principal,
        "rate_percent": rate,
        "years": years,
        "final_amount": round(amount, 2),
        "total_gain": round(amount - principal, 2),
    }

def sharpe_ratio(avg_return: float, risk_free_rate: float, std_dev: float) -> dict:
    if std_dev == 0:
        return {"error": "Standard deviation cannot be zero"}
    ratio = (avg_return - risk_free_rate) / std_dev
    return {
        "sharpe_ratio": round(ratio, 4),
        "interpretation": "Good" if ratio > 1 else "Average" if ratio > 0 else "Poor"
    }