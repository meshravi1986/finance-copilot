from app.database.db_connection import (
    get_connection
)

conn = get_connection()

cursor = conn.cursor()

#################################################
# USERS TABLE
#################################################

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    pin_hash TEXT NOT NULL,

    created_at TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
)

""")

#################################################
# ASSETS TABLE
#################################################

cursor.execute("""

CREATE TABLE IF NOT EXISTS assets (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    asset_name TEXT NOT NULL,

    asset_type TEXT NOT NULL,

    current_value REAL NOT NULL,

    monthly_contribution REAL NOT NULL,

    FOREIGN KEY(user_id)
    REFERENCES users(id)
)

""")

#################################################
# FINANCIAL DETAILS
#################################################

cursor.execute("""

CREATE TABLE IF NOT EXISTS financial_details (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    monthly_income REAL,

    monthly_emi REAL,
               
    age INTEGER,

    FOREIGN KEY(user_id)
    REFERENCES users(id)
)

""")

conn.commit()

conn.close()

print("Database initialized")
