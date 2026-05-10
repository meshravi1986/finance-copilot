import streamlit as st
import pandas as pd

from database.db_connection import (
    get_connection
)

#################################################
# ADMIN PAGE
#################################################


def render_admin_page():

    st.title("Admin Dashboard")

    conn = get_connection()

    #################################################
    # USERS
    #################################################

    st.subheader("Users")

    users_df = pd.read_sql(

        "SELECT * FROM users",

        conn
    )

    st.dataframe(
        users_df,
        use_container_width=True
    )

    #################################################
    # ASSETS
    #################################################

    st.subheader("Assets")

    assets_df = pd.read_sql(

        "SELECT * FROM assets",

        conn
    )

    st.dataframe(
        assets_df,
        use_container_width=True
    )

    #################################################
    # FINANCIAL DETAILS
    #################################################

    st.subheader("Financial Details")

    financial_df = pd.read_sql(

        "SELECT * FROM financial_details",

        conn
    )

    st.dataframe(
        financial_df,
        use_container_width=True
    )

    conn.close()
