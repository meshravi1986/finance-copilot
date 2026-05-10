# ARCHITECTURE.md
## 6. utils/

Purpose:
- Shared helper functions
- Formatting
- Reusable utility logic

Examples:
- Indian currency formatter
- percentage formatting
- reusable calculations

---

# Database Schema

## users

| Column | Type |
|---|---|
| id | INTEGER |
| name | TEXT |
| email | TEXT |
| pin | TEXT |

---

## assets

| Column | Type |
|---|---|
| id | INTEGER |
| user_id | INTEGER |
| asset_name | TEXT |
| asset_type | TEXT |
| current_value | REAL |
| monthly_contribution | REAL |

---

## financial_details

| Column | Type |
|---|---|
| id | INTEGER |
| user_id | INTEGER |
| monthly_income | REAL |
| monthly_emi | REAL |
| age | INTEGER |

---

# Import Conventions

IMPORTANT:

Current imports use:

```python
from views...
from repositories...
from services...