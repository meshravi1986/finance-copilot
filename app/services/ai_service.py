import os

from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


def ask_finance_question(
    question,
    portfolio_summary
):

    if not api_key:
        return """
        OpenAI API key not configured.

        Add OPENAI_API_KEY in .env file.
        """

    client = OpenAI(
        api_key=api_key
    )

    prompt = f"""
    You are a personal finance advisor.

    Portfolio:
    {portfolio_summary}

    User Question:
    {question}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return (
        response
        .choices[0]
        .message
        .content
    )
