import streamlit as st
import pandas as pd
import plotly.express as px

from io import BytesIO

from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import (
    DataValidation
)

from repositories.asset_repository import (

    fetch_all_assets,

    delete_asset,

    save_financial_details,

    fetch_financial_details,

    bulk_add_assets,

    update_assets,

    delete_all_assets
)

from services.portfolio_service import (

    calculate_asset_allocation,

    calculate_blended_return
)

from services.projection_service import (
    project_corpus_growth
)

from utils.helpers import (
    format_indian_currency_rupee
)


#################################################
# PORTFOLIO PAGE
#################################################

def render_portfolio_page():

    #################################################
    # USER
    #################################################

    user_id = (
        st.session_state.user["id"]
    )

    #################################################
    # PAGE TITLE
    #################################################

    st.title("Finance Dashboard")

    #################################################
    # CSS
    #################################################

    st.markdown("""

    <style>

    .block-container {

        padding-top: 2rem;

        padding-bottom: 1rem;
    }

    div[data-testid="stMetric"] {

        background-color: #f8f9fa;

        padding: 10px;

        border-radius: 10px;
    }

    div[data-testid="stMetricValue"] {

        font-size: 1.8rem;
    }

    div[data-testid="stMetricLabel"] {

        font-size: 0.9rem;
    }

    .stButton > button {

        background-color: #2563eb;

        color: white;

        border-radius: 8px;

        border: none;

        font-weight: 600;
    }

    .stButton > button:hover {

        background-color: #1d4ed8;

        color: white;
    }

    </style>

    """, unsafe_allow_html=True)

    #################################################
    # FETCH FINANCIAL DETAILS
    #################################################

    financials = (
        fetch_financial_details(user_id)
    )

    #################################################
    # FINANCIAL SNAPSHOT
    #################################################

    st.subheader(
        "Monthly Financial Snapshot"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        monthly_income = st.number_input(

            "Monthly Income",

            value=float(financials["income"]),

            step=10000.0
        )

    with col2:

        monthly_emi = st.number_input(

            "Monthly EMI",

            value=float(financials["emi"]),

            step=5000.0
        )

    with col3:

        age = st.number_input(

            "Age",

            value=int(financials["age"]),

            step=1
        )

    #################################################
    # SAVE FINANCIAL DETAILS
    #################################################

    if st.button(
        "Save Financial Details"
    ):

        save_financial_details(

            user_id,

            monthly_income,

            monthly_emi,

            age
        )

        st.success("""
        Financial details saved
        """)

    #################################################
    # ASSET TYPES
    #################################################

    asset_types = [

        "Equity",

        "Debt",

        "EPF",

        "PPF",

        "FD",

        "Company Stocks",

        "Metals",

        "Secondary Real Estate",

        "Crypto",

        "NPS"
    ]

    #################################################
    # EXCEL TEMPLATE
    #################################################

    st.subheader(
        "Portfolio Upload"
    )

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Portfolio"

    headers = [

        "asset_name",

        "asset_type",

        "current_value",

        "monthly_contribution"
    ]

    sheet.append(headers)

    sample_rows = [

        [
            "EPF",
            "EPF",
            4000000,
            42000
        ],

        [
            "HDFC Flexicap",
            "Equity",
            2500000,
            25000
        ],

        [
            "Bitcoin",
            "Crypto",
            500000,
            5000
        ]
    ]

    for row in sample_rows:

        sheet.append(row)

    st.warning("""

    Uploading a new Excel file will completely replace your existing portfolio.

    For smaller edits or adding individual assets, use the Current Portfolio table below.

    """)

    #################################################
    # DROPDOWN VALIDATION
    #################################################

    asset_type_string = (
        ",".join(asset_types)
    )

    validation = DataValidation(

        type="list",

        formula1=f'"{asset_type_string}"',

        allow_blank=False
    )

    sheet.add_data_validation(validation)

    validation.add("B2:B1000")

    #################################################
    # SAVE EXCEL
    #################################################

    excel_buffer = BytesIO()

    workbook.save(excel_buffer)

    excel_buffer.seek(0)

    #################################################
    # DOWNLOAD BUTTON
    #################################################

    st.download_button(

        label="Download Sample Excel Template",

        data=excel_buffer,

        file_name="sample_portfolio_template.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    #################################################
    # UPLOAD FILE
    #################################################

    uploaded_file = st.file_uploader(

        "Upload Portfolio Excel",

        type=["xlsx"]
    )

    if uploaded_file is not None:

        excel_df = pd.read_excel(
            uploaded_file
        )

        st.success("""
        Excel file loaded successfully.
        Click below to import portfolio.
        """)
        if st.button(
            "Import Excel Assets"
        ):

            #################################################
            # DELETE EXISTING ASSETS
            #################################################

            delete_all_assets(user_id)

            #################################################
            # IMPORT NEW ASSETS
            #################################################

            bulk_add_assets(

                user_id,

                excel_df
            )

            st.success("""
            Portfolio replaced successfully
            """)

            st.rerun()

    #################################################
    # FETCH ASSETS
    #################################################

    df = fetch_all_assets(user_id)

    if df.empty:

        st.warning("""
        No assets added yet.
        """)

        return

    #################################################
    # CALCULATIONS
    #################################################

    total_corpus = (
        df["current_value"].sum()
    )

    total_monthly_investments = (
        df["monthly_contribution"].sum()
    )

    monthly_expenses = (

        monthly_income

        -

        (
            monthly_emi +
            total_monthly_investments
        )
    )

    blended_return = (
        calculate_blended_return(df)
    )

    #################################################
    # KPI CARDS
    #################################################

    st.subheader(
        "Portfolio Summary"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "Corpus",

            format_indian_currency_rupee(
                total_corpus
            )
        )

    with col2:

        st.metric(

            "Monthly Savings",

            format_indian_currency_rupee(
                total_monthly_investments
            )
        )

    with col3:

        st.metric(

            "Monthly EMI",

            format_indian_currency_rupee(
                monthly_emi
            )
        )

    with col4:

        st.metric(

            "Blended Return",

            f"{blended_return}%"
        )

    #################################################
    # CHARTS
    #################################################

    chart_col1, chart_col2 = st.columns(2)

    #################################################
    # INCOME DISTRIBUTION
    #################################################

    with chart_col1:

        finance_chart = px.pie(

            names=[
                "Expenses",
                "EMI",
                "Savings"
            ],

            values=[
                monthly_expenses,
                monthly_emi,
                total_monthly_investments
            ],

            title="Income Distribution"
        )

        finance_chart.update_layout(
            height=350
        )

        st.plotly_chart(

            finance_chart,

            use_container_width=True
        )

    #################################################
    # ASSET ALLOCATION
    #################################################

    with chart_col2:

        allocation = (
            calculate_asset_allocation(df)
        )

        allocation_chart = px.pie(

            names=allocation.index,

            values=allocation.values,

            title="Asset Allocation"
        )

        allocation_chart.update_layout(
            height=350
        )

        st.plotly_chart(

            allocation_chart,

            use_container_width=True
        )

    #################################################
    # CURRENT PORTFOLIO
    #################################################

    st.subheader(
        "Current Portfolio"
    )

    editable_df = df.copy()

    #################################################
    # BLANK ROWS FOR QUICK ADD
    #################################################

    blank_rows = pd.DataFrame([

        {

            "id": None,

            "asset_name": "",

            "asset_type": "Equity",

            "current_value": 0,

            "monthly_contribution": 0
        },

        {

            "id": None,

            "asset_name": "",

            "asset_type": "Equity",

            "current_value": 0,

            "monthly_contribution": 0
        }
    ])

    editable_df = pd.concat(

        [
            editable_df,
            blank_rows
        ],

        ignore_index=True
    )

    #################################################
    # EDITABLE TABLE
    #################################################

    edited_portfolio_df = st.data_editor(

        editable_df,

        num_rows="dynamic",

        use_container_width=True,

        hide_index=True,

        column_config={

            "id": st.column_config.NumberColumn(
                disabled=True
            ),

            "asset_type": st.column_config.SelectboxColumn(

                "Asset Type",

                options=asset_types
            )
        }
    )

    #################################################
    # SAVE EDITS
    #################################################

    if st.button(
        "Save Portfolio Changes"
    ):

        #################################################
        # EXISTING ROWS
        #################################################

        existing_rows = edited_portfolio_df[

            edited_portfolio_df["id"].notnull()
        ]

        update_assets(
            existing_rows
        )

        #################################################
        # NEW ROWS
        #################################################

        new_rows = edited_portfolio_df[

            edited_portfolio_df["id"].isnull()
        ]

        #################################################
        # REMOVE EMPTY ROWS
        #################################################

        new_rows = new_rows[
            new_rows["asset_name"] != ""
        ]

        if not new_rows.empty:

            bulk_add_assets(

                user_id,

                new_rows
            )

        st.success("""
        Portfolio updated successfully
        """)

        st.rerun()

    #################################################
    # CORPUS PROJECTION
    #################################################

    st.subheader(
        "Corpus Projection"
    )

    projection_df = (

        project_corpus_growth(

            total_corpus,

            total_monthly_investments,

            blended_return,

            20,

            10,

            0,

            0
        )
    )

    projection_df["Formatted Corpus"] = (

        projection_df["Corpus"]

        .apply(
            format_indian_currency_rupee
        )
    )

    projection_chart = px.line(

        projection_df,

        x="Year",

        y="Corpus",

        title="Projected Corpus Growth",

        hover_data={

            "Formatted Corpus": True,

            "Corpus": False
        }
    )

    projection_chart.update_layout(
        height=450
    )

    st.plotly_chart(

        projection_chart,

        use_container_width=True
    )
