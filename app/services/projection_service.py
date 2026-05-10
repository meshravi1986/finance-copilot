import pandas as pd


def project_corpus_growth(
    current_corpus,
    monthly_investment,
    annual_return,
    years,
    annual_sip_growth,
    yearly_lumpsum,
    yearly_lumpsum_growth
):

    corpus = current_corpus

    records = []

    monthly_return = (
        annual_return / 12 / 100
    )

    current_sip = monthly_investment

    current_lumpsum = yearly_lumpsum

    for year in range(years):

        for month in range(12):

            corpus = corpus * (
                1 + monthly_return
            )

            corpus += current_sip

        corpus += current_lumpsum

        records.append({
            "Year": year + 1,
            "Corpus": round(corpus),
            "Monthly SIP": round(current_sip),
            "Yearly Lumpsum": round(current_lumpsum)
        })

        current_sip = (
            current_sip *
            (
                1 +
                annual_sip_growth / 100
            )
        )

        current_lumpsum = (
            current_lumpsum *
            (
                1 +
                yearly_lumpsum_growth / 100
            )
        )

    return pd.DataFrame(records)
