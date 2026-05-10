import streamlit as st

from repositories.asset_repository import (
    fetch_all_assets
)

from services.ai_service import (
    ask_finance_question
)


def render_ai_page():

    st.title("AI Finance Assistant")

    st.info("""
    Ask questions like:
    
    - Can I retire at 50?
    - Is my equity allocation too high?
    - Am I investing enough?
    - What corpus will I have in 20 years?
    """)

    question = st.text_input(
        "Ask your finance question"
    )

    if st.button("Ask AI"):

        df = fetch_all_assets()

        if df.empty:

            st.warning("""
            Please add portfolio assets first.
            """)

            return

        portfolio_summary = (
            df.to_string()
        )

        answer = ask_finance_question(
            question,
            portfolio_summary
        )

        st.write(answer)
