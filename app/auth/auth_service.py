from database.supabase_client import (
    supabase
)

#################################################
# GET USER BY EMAIL
#################################################


def get_user_by_email(email):

    response = (

        supabase

        .table("users")

        .select("*")

        .eq("email", email)

        .execute()
    )

    data = response.data

    if len(data) > 0:

        return data[0]

    return None

#################################################
# CREATE USER
#################################################


def create_user(

    name,

    email,

    pin
):

    response = (

        supabase

        .table("users")

        .insert({

            "name": name,

            "email": email,

            "pin": pin
        })

        .execute()
    )

    return response.data

#################################################
# VERIFY LOGIN
#################################################


def verify_login(

    email,

    pin
):

    user = get_user_by_email(email)

    if not user:

        return None

    if user["pin"] != pin:

        return None

    return user
