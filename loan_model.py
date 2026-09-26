from pathlib import Path
import joblib
import pandas as pd

MODEL_PATH = Path("models/loan_eligibility_model.joblib")

class LoanEligibilityModel:
    def __init__(self):
        if not MODEL_PATH.exists():
            self._train()
        self.model = joblib.load(MODEL_PATH)

    def _train(self):
        from sklearn.compose import ColumnTransformer
        from sklearn.impute import SimpleImputer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import OneHotEncoder, StandardScaler

        df = pd.read_csv("data/loan_data.csv")
        features = [
            "age", "monthly_income", "credit_score", "employment_years",
            "existing_loan_amount", "loan_amount", "employment_type"
        ]
        X = df[features]
        y = df["eligible"]

        numeric = [
            "age", "monthly_income", "credit_score", "employment_years",
            "existing_loan_amount", "loan_amount"
        ]
        categorical = ["employment_type"]

        preprocessor = ColumnTransformer([
            ("num", Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ]), numeric),
            ("cat", Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore"))
            ]), categorical)
        ])

        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000))
        ])

        pipeline.fit(X, y)
        MODEL_PATH.parent.mkdir(exist_ok=True)
        joblib.dump(pipeline, MODEL_PATH)

    def predict(self, data):
        features = pd.DataFrame([{
            "age": float(data["age"]),
            "monthly_income": float(data["monthly_income"]),
            "credit_score": float(data["credit_score"]),
            "employment_years": float(data["employment_years"]),
            "existing_loan_amount": float(data["existing_loan_amount"]),
            "loan_amount": float(data["loan_amount"]),
            "employment_type": data["employment_type"]
        }])

        probability = float(self.model.predict_proba(features)[0][1])
        prediction = int(self.model.predict(features)[0])

        if probability >= 0.75:
            risk = "Low"
        elif probability >= 0.50:
            risk = "Moderate"
        else:
            risk = "High"

        reasons = []
        score = float(data["credit_score"])
        income = float(data["monthly_income"])
        loan = float(data["loan_amount"])

        if score >= 750:
            reasons.append("Strong credit score")
        elif score < 650:
            reasons.append("Credit score needs improvement")

        if loan <= income * 12:
            reasons.append("Loan amount is within a reasonable income range")
        else:
            reasons.append("Loan amount is relatively high compared with annual income")

        if float(data["employment_years"]) >= 2:
            reasons.append("Stable employment history")
        else:
            reasons.append("Short employment history")

        return {
            "prediction": "Likely Eligible" if prediction == 1 else "Needs Review",
            "probability": round(probability * 100, 2),
            "risk_level": risk,
            "reasons": reasons,
            "disclaimer": "This is an educational model-based estimate, not a bank approval or financial decision."
        }
