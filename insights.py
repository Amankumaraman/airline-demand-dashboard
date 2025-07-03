# insights.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ For Groq usage
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"  # ✅ Groq endpoint

def generate_insight(data_records):
    prompt = f"""
    Analyze this airline flight search trend data. Tell us peak days, increasing or decreasing interest,
    any anomalies or patterns. Keep it short and readable for hostel business owners.

    Data (last 10 days):\n{data_records[-10:]}
    """

    try:
        response = openai.ChatCompletion.create(
            model="llama3-8b-8192",  # ✅ Groq-supported model
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Failed to generate insight: {e}"
