import pandas as pd

from database.supabase_client import (
    supabase
)

#################################################
# BULK ADD ASSETS
#################################################


def bulk_add_assets(

    user_id,

    df
):

    #################################################
    # CLEAN DATA
    #################################################

    df = df.fillna(0)

    rows = []

    for _, row in df.iterrows():

        #################################################
        # SKIP EMPTY ASSET NAMES
        #################################################

        if not str(
            row["asset_name"]
        ).strip():

            continue

        rows.append({

            "user_id": user_id,

            "asset_name": str(
                row["asset_name"]
            ),

            "asset_type": str(
                row["asset_type"]
            ),

            "current_value": float(
                row["current_value"]
            ),

            "monthly_contribution": float(
                row["monthly_contribution"]
            )
        })

    #################################################
    # INSERT
    #################################################

    if rows:

        (

            supabase

            .table("assets")

            .insert(rows)

            .execute()
        )
#################################################
# FETCH ALL ASSETS
#################################################


def fetch_all_assets(user_id):

    response = (

        supabase

        .table("assets")

        .select("*")

        .eq("user_id", user_id)

        .execute()
    )

    data = response.data

    if not data:

        return pd.DataFrame()

    return pd.DataFrame(data)

#################################################
# DELETE ASSET
#################################################


def delete_asset(asset_id):

    (

        supabase

        .table("assets")

        .delete()

        .eq("id", asset_id)

        .execute()
    )

#################################################
# DELETE ALL USER ASSETS
#################################################


def delete_all_assets(user_id):

    (

        supabase

        .table("assets")

        .delete()

        .eq("user_id", user_id)

        .execute()
    )

#################################################
# SAVE FINANCIAL DETAILS
#################################################


def save_financial_details(

    user_id,

    income,

    emi,

    age
):

    existing = (

        supabase

        .table("financial_details")

        .select("*")

        .eq("user_id", user_id)

        .execute()
    )

    #################################################
    # UPDATE
    #################################################

    if existing.data:

        (

            supabase

            .table("financial_details")

            .update({

                "monthly_income": income,

                "monthly_emi": emi,

                "age": age
            })

            .eq("user_id", user_id)

            .execute()
        )

    #################################################
    # INSERT
    #################################################

    else:

        (

            supabase

            .table("financial_details")

            .insert({

                "user_id": user_id,

                "monthly_income": income,

                "monthly_emi": emi,

                "age": age
            })

            .execute()
        )

#################################################
# FETCH FINANCIAL DETAILS
#################################################


def fetch_financial_details(user_id):

    response = (

        supabase

        .table("financial_details")

        .select("*")

        .eq("user_id", user_id)

        .execute()
    )

    data = response.data

    if data:

        row = data[0]

        return {

            "income": row["monthly_income"],

            "emi": row["monthly_emi"],

            "age": row["age"]
        }

    return {

        "income": 0,

        "emi": 0,

        "age": 40
    }

#################################################
# UPDATE ASSETS
#################################################


def update_assets(df):

    for _, row in df.iterrows():

        if pd.notnull(row["id"]):

            (

                supabase

                .table("assets")

                .update({

                    "asset_name": row["asset_name"],

                    "asset_type": row["asset_type"],

                    "current_value": float(
                        row["current_value"]
                    ),

                    "monthly_contribution": float(
                        row["monthly_contribution"]
                    )
                })

                .eq("id", row["id"])

                .execute()
            )
