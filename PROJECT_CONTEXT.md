# Finance Copilot - Project Context
- Retirement age planning
- Inflation-adjusted expenses
- Monte Carlo simulation
- Sequence of return risk
- SIP growth assumptions
- Lump sum yearly investment support

## AI Roadmap

Planned AI agents:

1. Retirement Readiness Agent
2. Bucket Strategy Retirement Agent
3. Scenario Recommendation Engine

---

# Current Architecture

## Frontend

- Streamlit

## Backend

- Python

## Database

- SQLite

## Deployment

- Streamlit Cloud

---

# Important UX Rules

## Excel Upload

Uploading a new Excel file REPLACES the existing portfolio.

It does NOT append to old assets.

## Inline Editing

The Current Portfolio table supports:
- Editing
- Adding rows
- Saving changes
- Deleting assets

## Indian Currency Formatting

All financial values should display in:
- Lakhs
- Crores

Never use:
- Millions
- Billions

---

# Deployment Notes

## Local Run Command

```powershell
python -m streamlit run app/main.py