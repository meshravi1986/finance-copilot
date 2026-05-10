# app/views/retirement_page.py

import streamlit as st
import plotly.express as px
import pandas as pd

from repositories.asset_repository import (
    fetch_all_assets
)

from services.retirement_service import (
    calculate_retirement_corpus
)

from services.portfolio_service import (
    calculate_blended_return
)

from services.projection_service import (
    project_corpus_growth
)

from services.monte_carlo_service import (
    run_monte_carlo_simulation
)

from utils.helpers import (
    format_indian_currency_rupee
)

from services.retirement_advisor_service import (
    generate_retirement_advice
)


def render_retirement_page():

    #################################################
    # USER
    #################################################

    user_id = (
        st.session_state.user["id"]
    )

    #################################################
    # PAGE TITLE
    #################################################

    st.title("Retirement Simulator")

    st.markdown("""
    <style>

    .block-container {

        padding-top: 2.2rem;

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

        font-size: 0.85rem;
    }

    </style>
    """, unsafe_allow_html=True)

    #################################################
    # FETCH PORTFOLIO
    #################################################

    df = fetch_all_assets(user_id)

    if df.empty:

        st.warning("""
        Please add assets first.
        """)

        return

    #################################################
    # CURRENT PORTFOLIO
    #################################################

    current_corpus = (
        df["current_value"].sum()
    )

    monthly_investment = (
        df["monthly_contribution"].sum()
    )

    blended_return = (
        calculate_blended_return(df)
    )

    #################################################
    # INPUTS
    #################################################

    st.subheader(
        "Retirement Assumptions"
    )

    col1, col2 = st.columns(2)

    with col1:

        years_to_retirement = (
            st.number_input(
                "Years To Retirement",
                value=12
            )
        )

        life_expectancy = (
            st.number_input(
                "Life Expectancy",
                value=85
            )
        )

        current_monthly_expense = (
            st.number_input(
                "Current Monthly Expense",
                value=100000,
                step=10000
            )
        )

    with col2:

        inflation_rate = (
            st.number_input(
                "Inflation Rate (%)",
                value=6.0,
                step=0.5
            )
        )

        annual_sip_growth = (
            st.number_input(
                "Annual SIP Growth (%)",
                value=10.0,
                step=1.0
            )
        )

        yearly_lumpsum = (
            st.number_input(
                "Yearly Lumpsum Investment",
                value=0
            )
        )

        yearly_lumpsum_growth = (
            st.number_input(
                "Yearly Lumpsum Growth (%)",
                value=5.0,
                step=1.0
            )
        )

    #################################################
    # INFLATED EXPENSE
    #################################################

    current_annual_expense = (
        current_monthly_expense * 12
    )

    retirement_annual_expense = (

        current_annual_expense *

        (
            (
                1 +
                inflation_rate / 100
            )

            **

            years_to_retirement
        )
    )

    #################################################
    # PROJECTION
    #################################################

    projection_df = (

        project_corpus_growth(

            current_corpus,

            monthly_investment,

            blended_return,

            years_to_retirement,

            annual_sip_growth,

            yearly_lumpsum,

            yearly_lumpsum_growth
        )
    )

    corpus_at_retirement = (
        projection_df.iloc[-1]["Corpus"]
    )

    #################################################
    # RETIREMENT YEARS
    #################################################

    current_age = 40

    retirement_age = (
        current_age +
        years_to_retirement
    )

    years_in_retirement = (
        life_expectancy -
        retirement_age
    )

    #################################################
    # REQUIRED CORPUS
    #################################################

    required_corpus = (

        calculate_retirement_corpus(

            retirement_annual_expense,

            0.035
        )
    )

    #################################################
    # MONTE CARLO
    #################################################

    simulation_result = (

        run_monte_carlo_simulation(

            corpus_at_retirement,

            retirement_annual_expense,

            years_in_retirement,

            inflation_rate
        )
    )

    survivability = (
        simulation_result["success_rate"]
    )

    advisor_data = {

        "current_age": current_age,

        "retirement_age": retirement_age,

        "monthly_expenses": current_monthly_expense,

        "current_corpus": current_corpus,

        "monthly_sip": monthly_investment,

        "sip_growth": annual_sip_growth,

        "blended_return": blended_return,

        "retirement_corpus": corpus_at_retirement,

        "required_corpus": required_corpus,

        "survivability": survivability,

    }

    advisor_response = generate_retirement_advice(
        advisor_data
    )

    #################################################
    # STORE RETIREMENT RESULTS
    #################################################

    st.session_state[
        "retirement_results"
    ] = {

        "retirement_corpus": corpus_at_retirement,

        "required_corpus": required_corpus,

        "survivability": survivability,

        "current_age": current_age,

        "retirement_age": retirement_age,

        "inflation_rate": inflation_rate
    }

    #################################################
    # KPI CARDS
    #################################################

    st.subheader(
        "Retirement Summary"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "Corpus At Retirement",
            format_indian_currency_rupee(
                corpus_at_retirement
            )
        )

    with col2:

        st.metric(
            "Required Corpus",
            format_indian_currency_rupee(
                required_corpus
            )
        )

    with col3:

        st.metric(
            "Blended Return",
            f"{blended_return}%"
        )

    with col4:

        st.metric(
            "Survivability",
            f"{survivability}%"
        )

    with col5:

        st.metric(
            "Retirement Expense",
            format_indian_currency_rupee(
                retirement_annual_expense
            )
        )

    #################################################
    # STATUS
    #################################################

    if survivability >= 90:

        st.success("""
        Excellent retirement survivability.
        """)

    elif survivability >= 75:

        st.warning("""
        Moderate retirement survivability.
        """)

    else:

        st.error("""
        High retirement risk.
        """)

    #################################################
    # CHARTS
    #################################################

    chart_col1, chart_col2 = st.columns(2)

    #################################################
    # CORPUS GROWTH
    #################################################

    with chart_col1:

        projection_df["Formatted Corpus"] = (

            projection_df["Corpus"]

            .apply(
                format_indian_currency_rupee
            )
        )

        fig = px.line(

            projection_df,

            x="Year",

            y="Corpus",

            title="Corpus Growth Till Retirement",

            hover_data={
                "Formatted Corpus": True,
                "Corpus": False
            }
        )

        fig.update_layout(
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    #################################################
    # MONTE CARLO
    #################################################

    with chart_col2:

        ending_df = pd.DataFrame({

            "Ending Corpus":
            simulation_result[
                "ending_values"
            ]
        })

        hist_fig = px.histogram(

            ending_df,

            x="Ending Corpus",

            nbins=40,

            title="Monte Carlo Outcomes"
        )

        hist_fig.update_layout(
            height=400
        )

        st.plotly_chart(
            hist_fig,
            use_container_width=True
        )

    #################################################
    # RETIREMENT ADVISOR
    #################################################

    st.subheader(
        "Retirement Advisor"
    )

    st.markdown(
        advisor_response
    )
    #################################################
    # ASSUMPTIONS
    #################################################

    st.subheader(
        "Simulation Assumptions"
    )

    st.info(f"""

    • Current Corpus:
      {format_indian_currency_rupee(current_corpus)}

    • Monthly Investment:
      {format_indian_currency_rupee(monthly_investment)}

    • Blended Portfolio Return:
      {blended_return}%

    • Inflation:
      {inflation_rate}%

    • Annual SIP Growth:
      {annual_sip_growth}%

    • Yearly Lumpsum:
      {format_indian_currency_rupee(yearly_lumpsum)}

    • Lumpsum Growth:
      {yearly_lumpsum_growth}%

    • Retirement Age:
      {retirement_age}

    • Retirement Duration:
      {years_in_retirement} years

    • Retirement Expense:
      {format_indian_currency_rupee(retirement_annual_expense)}
    """)
