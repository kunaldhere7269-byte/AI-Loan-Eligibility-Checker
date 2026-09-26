def validate_loan_input(data):
    required = [
        "age", "monthly_income", "credit_score", "employment_years",
        "existing_loan_amount", "loan_amount", "employment_type"
    ]
    errors = {}

    for field in required:
        if field not in data or data[field] in ("", None):
            errors[field] = "This field is required."

    if errors:
        return errors

    try:
        age = float(data["age"])
        income = float(data["monthly_income"])
        score = float(data["credit_score"])
        employment_years = float(data["employment_years"])
        existing = float(data["existing_loan_amount"])
        loan = float(data["loan_amount"])

        if not 18 <= age <= 80:
            errors["age"] = "Age must be between 18 and 80."
        if income <= 0:
            errors["monthly_income"] = "Income must be greater than 0."
        if not 300 <= score <= 900:
            errors["credit_score"] = "Credit score must be between 300 and 900."
        if employment_years < 0:
            errors["employment_years"] = "Employment years cannot be negative."
        if existing < 0:
            errors["existing_loan_amount"] = "Existing loan amount cannot be negative."
        if loan <= 0:
            errors["loan_amount"] = "Loan amount must be greater than 0."
    except (TypeError, ValueError):
        return {"form": "Please enter valid numeric values."}

    return errors
