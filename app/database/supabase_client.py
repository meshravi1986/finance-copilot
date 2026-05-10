import os

from dotenv import load_dotenv

from supabase import create_client


#################################################
# LOAD ENV
#################################################

load_dotenv()

#################################################
# SUPABASE CONFIG
#################################################

SUPABASE_URL = os.getenv(
    "SUPABASE_URL"
)

print("SUPABASE_URL =", SUPABASE_URL)

SUPABASE_KEY = os.getenv(
    "SUPABASE_KEY"
)

#################################################
# CLIENT
#################################################


supabase = create_client(

    SUPABASE_URL,

    SUPABASE_KEY
)
