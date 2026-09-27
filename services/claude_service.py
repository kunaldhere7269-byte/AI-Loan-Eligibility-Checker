import os
import json
import urllib.request
import urllib.error


def get_demo_tips(data):
    """
    Safe fallback tips used when Claude API is unavailable.
    These tips allow the project to work in demo mode.
    """

    try:
        income = float(data.get("monthly_income", 0) or 0)
        expenses = float(data.get("monthly_expenses", 0) or 0)
        loan_amount = float(data.get("loan_amount", 0) or 0)
        credit_score = int(data.get("credit_score", 0) or 0)

        monthly_surplus = max(income - expenses, 0)

        tips = []

        if income > 0 and expenses > 0:

            if expenses >= income:
                tips.append(
                    "Your monthly expenses are high compared with your income. "
                    "Try reducing unnecessary expenses before taking a new loan."
                )
            else:
                tips.append(
                    f"Your estimated monthly surplus is ₹{monthly_surplus:,.0f}. "
                    "Maintain part of this amount as savings or an emergency fund."
                )

        if credit_score >= 750:
            tips.append(
                "Your credit score is in a strong range. Continue making loan "
                "and credit-card payments on time."
            )
        elif credit_score >= 650:
            tips.append(
                "Your credit score can be improved by maintaining timely payments "
                "and reducing outstanding debt."
            )
        elif credit_score > 0:
            tips.append(
                "Focus on timely repayments and reducing outstanding balances "
                "to improve your credit profile."
            )

        if loan_amount > 0 and income > 0:
            if loan_amount > income * 24:
                tips.append(
                    "The requested loan amount is relatively large compared with "
                    "your monthly income. Consider whether the EMI will remain affordable."
                )
            else:
                tips.append(
                    "Before taking the loan, compare the expected EMI with your "
                    "monthly income and existing financial commitments."
                )

        # Always provide general financial guidance
        tips.append(
            "Keep an emergency fund and avoid taking new debt only to manage existing debt."
        )

        tips.append(
            "This application provides an educational estimate and is not a guaranteed lending decision."
        )

        return tips[:3]

    except Exception as e:
        print("Demo tips error:", repr(e))

        return [
            "Review your income, expenses and existing debt before borrowing.",
            "Maintain timely repayments and keep an emergency fund.",
            "This application provides an educational estimate only."
        ]


def get_financial_tips(data):
    """
    Generate financial tips using Anthropic Claude.

    If Anthropic API credits are unavailable, the function automatically
    falls back to demo tips so the application continues working.
    """

    api_key = os.getenv("ANTHROPIC_API_KEY")

    # ---------------------------------------------------------
    # 1. API key check
    # ---------------------------------------------------------
    if not api_key:
        print("Claude API: ANTHROPIC_API_KEY is not configured.")
        print("Using demo financial tips.")

        return get_demo_tips(data)

    # ---------------------------------------------------------
    # 2. Prepare user data
    # ---------------------------------------------------------
    try:

        safe_data = {
            "monthly_income": data.get("monthly_income", 0),
            "monthly_expenses": data.get("monthly_expenses", 0),
            "loan_amount": data.get("loan_amount", 0),
            "credit_score": data.get("credit_score", 0),
            "existing_emi": data.get("existing_emi", 0),
            "employment_type": data.get(
                "employment_type",
                "Not specified"
            )
        }

        user_information = json.dumps(safe_data)

    except Exception as e:

        print("Data preparation error:", repr(e))
        print("Using demo financial tips.")

        return get_demo_tips(data)

    # ---------------------------------------------------------
    # 3. Claude API request
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
                    "provide exactly 3 concise and practical general "
                    "financial planning tips.\n\n"

                    "Rules:\n"
                    "- Give exactly 3 tips.\n"
                    "- Keep each tip short and easy to understand.\n"
                    "- Do not claim to be a bank or lender.\n"
                    "- Do not guarantee loan approval or rejection.\n"
                    "- Do not provide regulated personalized financial advice.\n"
                    "- Do not mention API, Claude, or internal system details.\n"
                    "- Return only the tips, one per line.\n\n"

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
    # 4. Call Anthropic API
    # ---------------------------------------------------------

    try:

        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            response_data = response.read().decode("utf-8")

            result = json.loads(response_data)

        # -----------------------------------------------------
        # 5. Extract Claude text
        # -----------------------------------------------------

        content = result.get("content", [])

        tips = []

        for block in content:

            if block.get("type") == "text":

                text = block.get("text", "").strip()

                if text:

                    lines = text.splitlines()

                    for line in lines:

                        cleaned_line = line.strip("-• ").strip()

                        if cleaned_line:

                            tips.append(cleaned_line)

        tips = tips[:3]

        # -----------------------------------------------------
        # 6. Empty response
        # -----------------------------------------------------

        if not tips:

            print("Claude API: No tips returned.")
            print("Using demo financial tips.")

            return get_demo_tips(data)

        print("Claude API: Tips generated successfully.")

        return tips

    # ---------------------------------------------------------
    # 7. Anthropic HTTP error
    # ---------------------------------------------------------

    except urllib.error.HTTPError as e:

        try:

            error_body = e.read().decode(
                "utf-8",
                errors="replace"
            )

        except Exception:

            error_body = "Unable to read API error response."

        print("Claude API HTTP Error:", e.code)
        print("Claude API Response:", error_body)

        # -----------------------------------------------------
        # Credit / billing problem
        # -----------------------------------------------------

        if e.code == 400 and "credit balance" in error_body.lower():

            print(
                "Anthropic credit balance is too low. "
                "Switching to demo financial tips."
            )

        elif e.code == 401:

            print(
                "Anthropic API key authentication failed. "
                "Switching to demo financial tips."
            )

        elif e.code == 402:

            print(
                "Anthropic billing/payment problem. "
                "Switching to demo financial tips."
            )

        elif e.code == 403:

            print(
                "Anthropic API permission problem. "
                "Switching to demo financial tips."
            )

        elif e.code == 429:

            print(
                "Anthropic API rate limit reached. "
                "Switching to demo financial tips."
            )

        else:

            print(
                "Anthropic API request failed. "
                "Switching to demo financial tips."
            )

        return get_demo_tips(data)

    # ---------------------------------------------------------
    # 8. Network error
    # ---------------------------------------------------------

    except urllib.error.URLError as e:

        print("Claude API URL Error:", repr(e.reason))
        print("Using demo financial tips.")

        return get_demo_tips(data)

    # ---------------------------------------------------------
    # 9. Timeout
    # ---------------------------------------------------------

    except TimeoutError:

        print("Claude API Error: Request timed out.")
        print("Using demo financial tips.")

        return get_demo_tips(data)

    # ---------------------------------------------------------
    # 10. Unexpected error
    # ---------------------------------------------------------

    except Exception as e:

        print(
            "Claude API Unexpected Error:",
            repr(e)
        )

        print("Using demo financial tips.")

        return get_demo_tips(data)