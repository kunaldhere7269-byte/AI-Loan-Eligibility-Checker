const money = n => new Intl.NumberFormat("en-IN", {
  style: "currency", currency: "INR", maximumFractionDigits: 0
}).format(n);

async function postJSON(url, body) {
  const response = await fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || Object.values(data.errors || {}).join(" "));
  return data;
}

// Loan Checker
const loanForm = document.getElementById("loanForm");
if (loanForm) {
  loanForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target).entries());
    ["age","monthly_income","credit_score","employment_years","existing_loan_amount","loan_amount"]
      .forEach(k => data[k] = Number(data[k]));
    const box = document.getElementById("loanResult");
    box.classList.remove("hidden");
    box.innerHTML = "Analysing...";
    try {
      const r = await postJSON("/api/predict", data);
      const cls = r.risk_level === "Low" ? "success" : r.risk_level === "Moderate" ? "warning" : "danger";
      box.innerHTML = `<div class="metric ${cls}">${r.prediction}</div><strong>Model confidence:</strong> ${r.probability}%<br><strong>Estimated risk:</strong> ${r.risk_level}<ul>${r.reasons.map(x => `<li>${x}</li>`).join("")}</ul><small>${r.disclaimer}</small>`;
    } catch(err) { box.innerHTML = `<span class="danger">${err.message}</span>`; }
  });
}

// Credit Analyzer
const creditBtn = document.getElementById("creditBtn");
if (creditBtn) {
  creditBtn.addEventListener("click", async () => {
    const score = Number(document.getElementById("creditScore").value);
    const box = document.getElementById("creditResult");
    box.classList.remove("hidden");
    try {
      const r = await postJSON("/api/credit-analysis", {credit_score: score});
      box.innerHTML = `<div class="metric">${r.band}</div><strong>Score:</strong> ${r.score}<br><strong>Risk band:</strong> ${r.risk}<br>${r.advice}`;
    } catch(err) { box.innerHTML = `<span class="danger">${err.message}</span>`; }
  });
}

// EMI Calculator
const emiBtn = document.getElementById("emiBtn");
if (emiBtn) {
  emiBtn.addEventListener("click", async () => {
    const payload = {
      loan_amount: Number(document.getElementById("emiAmount").value),
      interest_rate: Number(document.getElementById("emiRate").value),
      tenure_years: Number(document.getElementById("emiYears").value)
    };
    const box = document.getElementById("emiResult");
    box.classList.remove("hidden");
    try {
      const r = await postJSON("/api/emi", payload);
      box.innerHTML = `<div class="metric">${money(r.monthly_emi)}</div>Monthly EMI<br><br><strong>Total interest:</strong> ${money(r.total_interest)}<br><strong>Total payment:</strong> ${money(r.total_payment)}`;
    } catch(err) { box.innerHTML = `<span class="danger">${err.message}</span>`; }
  });
}

// AI Financial Tips
const tipsBtn = document.getElementById("tipsBtn");
if (tipsBtn) {
  tipsBtn.addEventListener("click", async () => {
    const payload = {
      monthly_income: Number(document.getElementById("tipIncome").value),
      monthly_expenses: Number(document.getElementById("tipExpenses").value)
    };
    const box = document.getElementById("tipsResult");
    box.classList.remove("hidden");
    box.innerHTML = "Generating tips...";
    try {
      const r = await postJSON("/api/ai-tips", payload);
      box.innerHTML = `<ul>${r.tips.map(x => `<li>${x}</li>`).join("")}</ul>`;
    } catch(err) { box.innerHTML = `<span class="danger">${err.message}</span>`; }
  });
}
