import re

INJECTION_PATTERNS = [
    r"ignore (all |previous |above )?instructions",
    r"you are now",
    r"forget (everything|all|your)",
    r"act as (a |an )?(?!financial)",
    r"jailbreak",
    r"pretend (you are|to be)",
    r"do anything now",
    r"dan mode",
]

HARMFUL_KEYWORDS = [
    "hack", "exploit", "illegal", "launder", "fraud",
    "insider trading", "manipulate market", "ponzi"
]

FINANCE_KEYWORDS = [
    "stock", "price", "invest", "portfolio", "market", "share",
    "return", "profit", "loss", "buy", "sell", "crypto", "etf",
    "bond", "dividend", "ticker", "company", "fund", "trade",
    "financial", "money", "wealth", "asset", "equity", "revenue",
    "earnings", "forecast", "analysis", "risk", "interest", "rate"
]

def check_input(user_input: str) -> dict:
    text = user_input.lower()

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text):
            return {
                "allowed": False,
                "reason": "prompt_injection",
                "message": "I detected a prompt injection attempt. I can only assist with financial queries."
            }

    for keyword in HARMFUL_KEYWORDS:
        if keyword in text:
            return {
                "allowed": False,
                "reason": "harmful_query",
                "message": f"I cannot assist with queries related to '{keyword}'. Please ask about legitimate financial topics."
            }

    has_finance = any(kw in text for kw in FINANCE_KEYWORDS)
    if not has_finance and len(text.split()) > 4:
        return {
            "allowed": False,
            "reason": "off_topic",
            "message": "I'm a financial assistant. Please ask me about stocks, investments, portfolios, or financial analysis."
        }

    return {"allowed": True, "reason": None, "message": None}