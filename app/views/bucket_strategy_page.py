import streamlit as st

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
        ]
    )

    #################################################
    # SUMMARY
    #################################################

    st.subheader(
        "Safe Withdrawal Strategy"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Safe Withdrawal Rate",

            f"{strategy['swr']:.1f}%"
        )

    with col2:

        st.metric(

            "Safe Monthly Withdrawal",

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
