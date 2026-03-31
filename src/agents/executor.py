from src.tools.stock_data import get_stock_price
from src.tools.calculator import calculate_return, compound_interest, sharpe_ratio
from src.tools.portfolio import get_portfolio_summary
from src.tools.news_fetch import get_stock_news

def execute_plan(plan: dict) -> str:
    results = []
    tasks = plan.get("tasks", [])

    for task in tasks:
        tool = task.get("tool")
        params = task.get("params", {})

        if tool == "get_stock_price":
            data = get_stock_price(params.get("ticker", ""))
            if "error" in data:
                results.append(f"Stock data error: {data['error']}")
            else:
                results.append(
                    f"Stock: {data['name']} ({data['ticker']})\n"
                    f"  Price: ${data['price']} {data['currency']}\n"
                    f"  52W High: ${data['52w_high']} | 52W Low: ${data['52w_low']}\n"
                    f"  P/E Ratio: {data['pe_ratio']} | Market Cap: ${data['market_cap']:,}"
                    if data.get("market_cap") else
                    f"Stock: {data['name']} ({data['ticker']}) - Price: ${data['price']}"
                )

        elif tool == "calculate_return":
            data = calculate_return(**params)
            results.append(
                f"Return Analysis:\n"
                f"  Buy: ${data['buy_price']} → Now: ${data['current_price']}\n"
                f"  P&L: ${data['profit_loss']} ({data['percent_return']}%)"
            )

        elif tool == "compound_interest":
            data = compound_interest(**params)
            results.append(
                f"Compound Interest:\n"
                f"  ${data['principal']} at {data['rate_percent']}% for {data['years']} years\n"
                f"  Final: ${data['final_amount']} (Gain: ${data['total_gain']})"
            )

        elif tool == "get_portfolio":
            results.append(get_portfolio_summary())

        elif tool == "get_news":
            results.append(get_stock_news(params.get("ticker", "")))

        elif tool == "sharpe_ratio":
            data = sharpe_ratio(**params)
            results.append(f"Sharpe Ratio: {data.get('sharpe_ratio')} — {data.get('interpretation')}")

    return "\n\n".join(results) if results else "No tools were executed."