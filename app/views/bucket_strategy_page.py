import streamlit as st
import pandas as pd

from services.bucket_strategy_service import (
    generate_bucket_strategy
)

#################################################
# FORMATTER
#################################################


def format_indian_currency(value):

    if value >= 10000000:

        return f"₹{value / 10000000:.2f} Cr"

    elif value >= 100000:

        return f"₹{value / 100000:.2f} L"

    else:

        return f"₹{value:,.0f}"

#################################################
# PAGE
#################################################


def render_bucket_strategy_page():

    st.title(
        "Retirement Withdrawal Strategy"
    )

    #################################################
    # CHECK RETIREMENT DATA
    #################################################

    if (

        "retirement_results"

        not in st.session_state
    ):

        st.warning("""
        Please run the Retirement Simulator first.
        """)

        return

    #################################################
    # FETCH RESULTS
    #################################################

    results = st.session_state[
        "retirement_results"
    ]

    #################################################
    # USER CONTROLS
    #################################################

    st.subheader(
        "Withdrawal Scenario Planning"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        withdrawal_rate = st.slider(

            "Withdrawal Rate %",

            min_value=2.0,

            max_value=6.0,

            value=3.5,

            step=0.1
        )

    with col2:

        expected_return = st.slider(

            "Post Retirement Return %",

            min_value=4.0,

            max_value=14.0,

            value=10.0,

            step=0.5
        )

    with col3:

        life_expectancy = st.slider(

            "Life Expectancy",

            min_value=75,

            max_value=100,

            value=90,

            step=1
        )

    #################################################
    # GENERATE STRATEGY
    #################################################

    strategy = generate_bucket_strategy(

        retirement_corpus=results[
            "retirement_corpus"
        ],

        required_corpus=results[
            "required_corpus"
        ],

        survivability=results[
            "survivability"
        ],

        current_age=results[
            "current_age"
        ],

        retirement_age=results[
            "retirement_age"
        ],

        inflation_rate=results[
            "inflation_rate"
        ],

        expected_return=(
            expected_return / 100
        ),

        life_expectancy=life_expectancy,

        custom_swr=(
            withdrawal_rate / 100
        )
    )

    #################################################
    # SUMMARY
    #################################################

    st.subheader(
        "Safe Withdrawal Strategy"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "Withdrawal Rate",

            f"{strategy['swr']:.1f}%"
        )

    with col2:

        st.metric(

            "Monthly Withdrawal",

            format_indian_currency(

                strategy[
                    "monthly_withdrawal"
                ]
            )
        )

    with col3:

        st.metric(

            "Corpus Coverage Ratio",

            f"{strategy['corpus_ratio']:.2f}x"
        )

    with col4:

        st.metric(

            "Corpus At End",

            format_indian_currency(

                strategy[
                    "ending_corpus"
                ]
            )
        )

    #################################################
    # DEPLETION WARNING
    #################################################

    if strategy[
        "corpus_depleted"
    ]:

        st.error(

            f"""
            Corpus may get exhausted by age
            {strategy['depletion_age']}.
            """
        )

    else:

        st.success("""
        Corpus survives through full life expectancy.
        """)

    #################################################
    # BUCKETS
    #################################################

    st.subheader(
        "Recommended Bucket Allocation"
    )

    bucket_df = {

        "Bucket": [

            "Bucket 1 - Safety",

            "Bucket 2 - Income",

            "Bucket 3 - Growth"
        ],

        "Allocation %": [

            round(
                strategy[
                    "bucket_1_ratio"
                ],
                1
            ),

            round(
                strategy[
                    "bucket_2_ratio"
                ],
                1
            ),

            round(
                strategy[
                    "bucket_3_ratio"
                ],
                1
            )
        ],

        "Recommended Amount": [

            format_indian_currency(

                strategy[
                    "bucket_1"
                ]
            ),

            format_indian_currency(

                strategy[
                    "bucket_2"
                ]
            ),

            format_indian_currency(

                strategy[
                    "bucket_3"
                ]
            )
        ]
    }

    st.dataframe(

        bucket_df,

        use_container_width=True,

        hide_index=True
    )

    #################################################
    # YEARLY PROJECTION
    #################################################

    st.subheader(
        "Corpus Projection"
    )

    projection_df = pd.DataFrame(

        strategy[
            "yearly_projection"
        ]
    )

    projection_df[
        "corpus_display"
    ] = projection_df[
        "corpus"
    ].apply(
        format_indian_currency
    )

    st.line_chart(

        projection_df.set_index(
            "age"
        )[
            "corpus"
        ]
    )

    st.dataframe(

        projection_df[
            [
                "age",
                "corpus_display"
            ]
        ],

        use_container_width=True,

        hide_index=True
    )

    #################################################
    # REFILL STRATEGY
    #################################################

    st.subheader(
        "Bucket Refill Strategy"
    )

    for item in strategy[
        "refill_strategy"
    ]:

        st.markdown(
            f"- {item}"
        )
