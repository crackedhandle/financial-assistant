import re

UNSAFE_PATTERNS = [
    r"guaranteed (return|profit|gain)",
    r"will definitely (go up|rise|increase|make you rich)",
    r"100% (safe|certain|sure)",
    r"can't lose",
    r"risk.?free investment",
    r"double your money",
]

HALLUCINATION_TRIGGERS = [
    "as of today, the price is",
    "the current price is exactly",
    "i know for certain",
]

def check_output(response: str) -> dict:
    text = response.lower()

    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, text):
            return {
                "safe": False,
                "reason": "misleading_guarantee",
                "message": " Response blocked: contained financial guarantee language which is not allowed."
            }

    for trigger in HALLUCINATION_TRIGGERS:
        if trigger in text:
            return {
                "safe": False,
                "reason": "possible_hallucination",
                "message": " Response flagged for possible hallucination. Please verify with real-time data."
            }

    if len(response.strip()) < 20:
        return {
            "safe": False,
            "reason": "too_short",
            "message": " Response too short or empty. Please try again."
        }

    return {"safe": True, "reason": None, "message": None}