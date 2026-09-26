# FinAI — AI Loan Eligibility Checker

A capstone-ready **AI-powered BFSI web prototype** with:

- Loan eligibility prediction using a scikit-learn classification model
- Credit score analysis
- EMI calculator
- Optional Claude API integration for general financial tips
- Responsive dark glassmorphism UI
- Server-side validation
- Synthetic training data (no real customer data)
- Flask backend + HTML/CSS/JavaScript frontend

> **Important:** This is an educational prototype. The ML model is trained on synthetic data and does not represent a bank's underwriting policy. The prediction is not a guaranteed loan approval and should not be treated as professional financial advice.

## 1. Project structure

```text
AI_Loan_Eligibility_Checker/
├── app.py
├── loan_model.py
├── requirements.txt
├── Procfile
├── .env.example
├── .gitignore
├── README.md
├── data/
│   └── loan_data.csv
├── models/
│   └── (created automatically on first run)
├── services/
│   ├── __init__.py
│   ├── validation.py
│   └── claude_service.py
├── templates/
│   └── dashboard.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## 2. Run in VS Code / Windows

Open the project folder in VS Code.

### Create virtual environment

```powershell
python -m venv venv
```

### Activate it

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
venv\Scripts\activate
```

### Install packages

```powershell
pip install -r requirements.txt
```

### Run

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

On the first run, the app automatically trains the model from the included synthetic dataset and saves it under `models/`.

## 3. Optional Claude API

The project works without an API key.

To enable live AI tips:

1. Copy `.env.example` to `.env`.
2. Put your own Anthropic API key in the environment.
3. Do **not** upload `.env` to GitHub.

The backend keeps the key away from frontend JavaScript.

## 4. Main API endpoints

- `POST /api/predict` — loan eligibility prediction
- `POST /api/credit-analysis` — credit score analysis
- `POST /api/emi` — EMI calculation
- `POST /api/ai-tips` — general financial tips
- `GET /health` — health check

## 5. Suggested capstone workflow

### EPIC 1 — Project Planning & Architecture
- Define requirements
- Create UI wireframe
- Decide Flask + JavaScript architecture
- Define API endpoints

### EPIC 2 — Frontend & UI Development
- Dashboard
- Glassmorphism cards
- Responsive forms
- Client-side interactions

### EPIC 3 — Core Financial Feature Development
- Loan eligibility model
- Credit score analyzer
- EMI calculator
- Risk insights

### EPIC 4 — Client Logic & Integration
- Connect frontend to Flask APIs
- Add validation
- Add optional Claude integration

### EPIC 5 — Testing & Deployment
- Test valid/invalid inputs
- Test mobile layout
- Run security checks
- Deploy backend/frontend appropriately

### EPIC 6 — Conclusion
- Document results
- Add screenshots
- Explain limitations
- List future enhancements

## 6. Future enhancements

- User authentication
- Database / Google Sheets integration with appropriate access controls
- Explainable ML (e.g. SHAP)
- PDF financial report
- Model comparison
- Admin dashboard
- Better real-world, legally/ethically reviewed datasets
- Fairness and bias evaluation

## 7. GitHub upload

Create a GitHub repository, for example:

`ai-loan-eligibility-checker`

Then from the project folder:

```powershell
git init
git add .
git commit -m "Initial capstone project"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Do not commit:
- API keys
- `.env`
- private credentials
- real user financial information
