import os
import json
import urllib.request
import urllib.error


def get_financial_tips(data):
    """
    Generate general financial planning tips using Anthropic Claude API.

    ANTHROPIC_API_KEY must be configured in the environment.
    If the API is unavailable, safe fallback tips are returned.
    """

    api_key = os.getenv("ANTHROPIC_API_KEY")

    # ---------------------------------------------------------
    # 1. Check API key
    # ---------------------------------------------------------
    if not api_key:
        print("Claude API Error: ANTHROPIC_API_KEY is not configured.")

        return [
            "AI service is not configured yet.",
            "Review your income, expenses, existing debt and credit history before borrowing.",
            "This application provides an educational estimate only."
        ]

    # ---------------------------------------------------------
    # 2. Prepare user information
    # ---------------------------------------------------------
    try:
        safe_data = {
            "monthly_income": data.get("monthly_income", 0),
            "monthly_expenses": data.get("monthly_expenses", 0),
            "loan_amount": data.get("loan_amount", 0),
            "credit_score": data.get("credit_score", 0),
            "existing_emi": data.get("existing_emi", 0),
            "employment_type": data.get("employment_type", "Not specified")
        }

        user_information = json.dumps(safe_data)

    except Exception as e:
        print("Data preparation error:", repr(e))

        return [
            "Unable to process the entered financial information.",
            "Please check your input values and try again.",
            "This application provides an educational estimate only."
        ]

    # ---------------------------------------------------------
    # 3. Anthropic API request
    # ---------------------------------------------------------
    payload = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 350,
        "messages": [
            {
                "role": "user",
                "content": (
                    "You are a financial education assistant inside an "
                    "AI Loan Eligibility Checker web application.\n\n"

                    "Based on the following user-provided information, "
                    "give exactly 3 concise and practical general financial "
                    "planning tips.\n\n"

                    "Rules:\n"
                    "- Keep each tip short and easy to understand.\n"
                    "- Do not claim to be a bank or lender.\n"
                    "- Do not guarantee loan approval or rejection.\n"
                    "- Do not provide regulated personalized financial advice.\n"
                    "- Do not mention internal AI/API details.\n"
                    "- Return only the 3 tips, one per line.\n\n"

                    "User information:\n"
                    + user_information
                )
            }
        ]
    }

    request = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )

    # ---------------------------------------------------------
    # 4. Send request
    # ---------------------------------------------------------
    try:

        with urllib.request.urlopen(request, timeout=30) as response:

            response_data = response.read().decode("utf-8")

            result = json.loads(response_data)

        # -----------------------------------------------------
        # 5. Extract Claude response
        # -----------------------------------------------------
        content = result.get("content", [])

        tips = []

        for block in content:

            if block.get("type") == "text":

                text = block.get("text", "").strip()

                if text:
                    tips.extend(
                        line.strip("-• ").strip()
                        for line in text.splitlines()
                        if line.strip()
                    )

        # Keep maximum 5 tips
        tips = tips[:5]

        # -----------------------------------------------------
        # 6. Check if response contained text
        # -----------------------------------------------------
        if not tips:

            print("Claude API Error: API response contained no text.")

            return [
                "AI generated tips are currently unavailable.",
                "Review your income, expenses and existing debt before borrowing.",
                "This application provides an educational estimate only."
            ]

        print("Claude API: Tips generated successfully.")

        return tips

    # ---------------------------------------------------------
    # 7. HTTP errors
    # ---------------------------------------------------------
    except urllib.error.HTTPError as e:

        try:
            error_body = e.read().decode("utf-8", errors="replace")
        except Exception:
            error_body = "Unable to read error response."

        print("Claude API HTTP Error:", e.code)
        print("Claude API Response:", error_body)

        return [
            "AI service is temporarily unavailable.",
            "Please try again after some time.",
            "This application provides an educational estimate only."
        ]

    # ---------------------------------------------------------
    # 8. Network / connection errors
    # ---------------------------------------------------------
    except urllib.error.URLError as e:

        print("Claude API URL Error:", repr(e.reason))

        return [
            "Unable to connect to the AI service.",
            "Please check the server connection and try again.",
            "This application provides an educational estimate only."
        ]

    # ---------------------------------------------------------
    # 9. Timeout
    # ---------------------------------------------------------
    except TimeoutError:

        print("Claude API Error: Request timed out.")

        return [
            "AI service took too long to respond.",
            "Please try again.",
            "This application provides an educational estimate only."
        ]

    # ---------------------------------------------------------
    # 10. Any other unexpected error
    # ---------------------------------------------------------
    except Exception as e:

        print("Claude API Unexpected Error:", repr(e))

        return [
            "AI service is temporarily unavailable.",
            "Please try again after some time.",
            "This application provides an educational estimate only."
        ]