ASSET_RETURN_MAPPING = {

    "Equity": 12,

    "Company Stocks": 12,

    "Debt": 7,

    "EPF": 8,

    "PPF": 7.5,

    "FD": 6.5,

    "Metals": 8,

    "Secondary Real Estate": 9,

    "Crypto": 18,

    "NPS": 10
}


def calculate_asset_allocation(df):

    allocation = (
        df.groupby("asset_type")[
            "current_value"
        ]
        .sum()
    )

    total = allocation.sum()

    allocation_percent = (
        allocation / total
    ) * 100

    return allocation_percent


def calculate_blended_return(df):

    total_portfolio = (
        df["current_value"].sum()
    )

    if total_portfolio == 0:

        return 0

    weighted_return = 0

    for _, row in df.iterrows():

        asset_type = row["asset_type"]

        current_value = row["current_value"]

        asset_return = (
            ASSET_RETURN_MAPPING.get(
                asset_type,
                8
            )
        )

        asset_weight = (
            current_value /
            total_portfolio
        )

        weighted_return += (
            asset_weight *
            asset_return
        )

    return round(
        weighted_return,
        2
    )
