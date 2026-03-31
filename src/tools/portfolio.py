import json, os

def get_portfolio() -> dict:
    path = os.path.join(os.path.dirname(__file__), "../../data/mock_portfolio.json")
    with open(path, "r") as f:
        return json.load(f)

def get_portfolio_summary() -> str:
    portfolio = get_portfolio()
    lines = ["Your Portfolio:"]
    total = 0
    for holding in portfolio["holdings"]:
        value = holding["quantity"] * holding["avg_buy_price"]
        total += value
        lines.append(f"  {holding['ticker']}: {holding['quantity']} shares @ ${holding['avg_buy_price']} (Value: ${value:,.2f})")
    lines.append(f"Total Invested: ${total:,.2f}")
    return "\n".join(lines)