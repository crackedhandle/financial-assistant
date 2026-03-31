import os
import google.generativeai as genai
from dotenv import load_dotenv

def generate_response(user_query: str, tool_results: str) -> str:
    load_dotenv(override=True)
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""You are a financial critic agent. Review the data and answer the user query.
Rules:
- Never guarantee investment returns
- Always mention risks
- Be factual and cite the data provided
- Add a disclaimer at the end
- Use consider not will definitely

User Question: {user_query}

Data from tools:
{tool_results}

Provide your financial analysis:"""
    response = model.generate_content(prompt)
    return response.text.strip()
