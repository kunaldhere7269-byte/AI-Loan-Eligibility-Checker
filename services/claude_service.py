import os
import json
import urllib.request

def get_financial_tips(data):
    """
    Optional Claude integration.
    Add ANTHROPIC_API_KEY to the environment to enable live AI tips.
    Without a key, the project returns safe demo tips so the app still works.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        income = float(data.get("monthly_income", 0) or 0)
        expenses = float(data.get("monthly_expenses", 0) or 0)
        savings = max(income - expenses, 0)
        return [
            f"Estimated monthly surplus from the entered values: ₹{savings:,.0f}.",
            "Keep an emergency fund and review recurring expenses regularly.",
            "Treat the eligibility result as an estimate, not a guaranteed lending decision."
        ]

    # API integration intentionally kept isolated so the key never appears in frontend code.
    payload = {
        "model": "claude-3-5-sonnet-latest",
        "max_tokens": 350,
        "messages": [{
            "role": "user",
            "content": (
                "Give three concise, general financial planning tips based on this "
                "user-provided information. Do not claim to be a bank and do not "
                "provide regulated personalized financial advice.\n\n"
                + json.dumps(data)
            )
        }]
    }

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))
        text = "".join(
            block.get("text", "") for block in result.get("content", [])
            if block.get("type") == "text"
        )
        return [line.strip("-• ").strip() for line in text.splitlines() if line.strip()][:5]
    except Exception:
        return [
            "AI service is temporarily unavailable.",
            "Review your income, expenses, existing debt and credit history before borrowing.",
            "This application provides an educational estimate only."
        ]
