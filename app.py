import os
import math
from flask import Flask, render_template, request, jsonify
from loan_model import LoanEligibilityModel
from services.claude_service import get_financial_tips
from services.validation import validate_loan_input

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

model = LoanEligibilityModel()

@app.get("/")
def home():
    return render_template("dashboard.html")

@app.get("/loan-checker")
def loan_checker():
    return render_template("loan.html")

@app.get("/credit-analyzer")
def credit_analyzer():
    return render_template("credit.html")

@app.get("/emi-calculator")
def emi_calculator():
    return render_template("emi.html")

@app.get("/ai-tips")
def ai_tips_page():
    return render_template("tips.html")

@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "AI Loan Eligibility Checker"})

@app.post("/api/predict")
def predict():
    data = request.get_json(silent=True) or {}
    errors = validate_loan_input(data)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    result = model.predict(data)
    return jsonify({"success": True, **result})

@app.post("/api/emi")
def emi():
    data = request.get_json(silent=True) or {}
    try:
        principal = float(data.get("loan_amount", 0))
        annual_rate = float(data.get("interest_rate", 0))
        years = float(data.get("tenure_years", 0))

        if principal <= 0 or annual_rate < 0 or years <= 0:
            raise ValueError

        months = years * 12
        monthly_rate = annual_rate / 12 / 100

        if monthly_rate == 0:
            monthly_emi = principal / months
        else:
            monthly_emi = (
                principal * monthly_rate * (1 + monthly_rate) ** months
                / ((1 + monthly_rate) ** months - 1)
            )

        total_payment = monthly_emi * months
        total_interest = total_payment - principal

        return jsonify({
            "success": True,
            "monthly_emi": round(monthly_emi, 2),
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_interest, 2)
        })
    except (TypeError, ValueError, ZeroDivisionError):
        return jsonify({"success": False, "error": "Please enter valid EMI values."}), 400

@app.post("/api/credit-analysis")
def credit_analysis():
    data = request.get_json(silent=True) or {}
    try:
        score = int(data.get("credit_score"))
        if score < 300 or score > 900:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "Credit score must be between 300 and 900."}), 400

    if score >= 750:
        band, risk = "Excellent", "Low"
        advice = "Maintain timely payments and keep credit utilization under control."
    elif score >= 700:
        band, risk = "Good", "Low to Moderate"
        advice = "Continue timely payments and avoid unnecessary new credit applications."
    elif score >= 650:
        band, risk = "Fair", "Moderate"
        advice = "Focus on timely repayments and reducing outstanding balances."
    elif score >= 600:
        band, risk = "Needs Improvement", "Moderate to High"
        advice = "Prioritize repayment history and reduce high outstanding debt."
    else:
        band, risk = "Poor", "High"
        advice = "Review outstanding debts and repayment history before taking new credit."

    return jsonify({
        "success": True,
        "score": score,
        "band": band,
        "risk": risk,
        "advice": advice
    })

@app.post("/api/ai-tips")
def ai_tips():
    data = request.get_json(silent=True) or {}
    tips = get_financial_tips(data)
    return jsonify({"success": True, "tips": tips})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
