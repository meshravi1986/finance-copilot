from openai import OpenAI

import streamlit as st


#################################################
# OPENAI CLIENT
#################################################

import os

from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

client = OpenAI(

    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)

#################################################
# RETIREMENT ADVISOR
#################################################


def generate_retirement_advice(

    advisor_data
):

    #################################################
    # PROMPT
    #################################################

    prompt = f"""

    You are an expert retirement strategist.

    Analyze the retirement profile below.

    IMPORTANT RESPONSE RULES:

    - Keep response concise.
    - Avoid generic financial advice.
    - Avoid long explanations.
    - Avoid repeating numbers excessively.
    - Be sharp and analytical.
    - Use bullet points.
    - Focus on meaningful insights only.
    - Mention only the most important risks.
    - Mention only actionable recommendations.
    - Do NOT add disclaimers.
    - Do NOT sound like a bank advisor.

    FORMAT:

    # Retirement Health
    (1 line overall assessment)

    # What Is Going Well
    (3 concise bullets)

    # Key Risks
    (2-3 concise bullets)

    # Suggested Changes
    (2-4 practical recommendations)

    ------------------------------------------------

    Current Age:
    {advisor_data['current_age']}

    Retirement Age:
    {advisor_data['retirement_age']}

    Monthly Expenses:
    ₹{advisor_data['monthly_expenses']}

    Current Corpus:
    ₹{advisor_data['current_corpus']}

    Monthly SIP:
    ₹{advisor_data['monthly_sip']}

    SIP Growth:
    {advisor_data['sip_growth']}%

    Blended Return:
    {advisor_data['blended_return']}%

    Retirement Corpus:
    ₹{advisor_data['retirement_corpus']}

    Required Corpus:
    ₹{advisor_data['required_corpus']}

    Monte Carlo Survivability:
    {advisor_data['survivability']}%

    
    ------------------------------------------------

    Use simple language.

    Do not give generic disclaimers.

    Be specific to the numbers provided.

    """

    #################################################
    # OPENAI CALL
    #################################################

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {

                "role": "system",

                "content": """
                You are a highly analytical retirement advisor.
                """
            },

            {

                "role": "user",

                "content": prompt
            }
        ],

        temperature=0.3
    )

    #################################################
    # RETURN
    #################################################

    return (

        response

        .choices[0]

        .message

        .content
    )
