import streamlit as st

from auth.auth_service import (

    create_user,

    verify_login,

    get_user_by_email
)

from views.portfolio_page import (
    render_portfolio_page
)

from views.retirement_page import (
    render_retirement_page
)

from views.ai_assistant_page import (
    render_ai_page
)

from views.admin_page import (
    render_admin_page
)

from views.bucket_strategy_page import (
    render_bucket_strategy_page
)

#################################################
# PAGE CONFIG
#################################################

st.set_page_config(

    page_title="Finance Copilot",

    page_icon="💰",

    layout="wide"
)

#################################################
# SESSION STATE
#################################################

if "user" not in st.session_state:

    st.session_state.user = None

#################################################
# LOGIN / SIGNUP
#################################################

if st.session_state.user is None:

    st.title("Finance Copilot")

    auth_mode = st.radio(

        "Choose",

        [
            "Login",
            "Sign Up"
        ]
    )

    #################################################
    # LOGIN
    #################################################

    if auth_mode == "Login":

        email = st.text_input(
            "Email"
        )

        pin = st.text_input(
            "4 Digit PIN",
            type="password"
        )

        if st.button("Login"):

            user = verify_login(
                email,
                pin
            )

            if user:

                st.session_state.user = user

                st.rerun()

            else:

                st.error("""
                Invalid email or PIN
                """)

    #################################################
    # SIGNUP
    #################################################

    else:

        name = st.text_input(
            "Name"
        )

        email = st.text_input(
            "Email"
        )

        pin = st.text_input(
            "Create 4 Digit PIN",
            type="password"
        )

        if st.button("Create Account"):

            #################################################
            # VALIDATIONS
            #################################################

            if len(pin) != 4:

                st.error("""
                PIN must be 4 digits
                """)

            elif not pin.isdigit():

                st.error("""
                PIN must be numeric
                """)

            elif get_user_by_email(email):

                st.error("""
                Email already exists
                """)

            else:

                create_user(
                    name,
                    email,
                    pin
                )

                st.success("""
                Account created.
                Please login.
                """)

#################################################
# MAIN APP
#################################################

else:

    st.sidebar.success(

        f"""
        Logged in as:
        {st.session_state.user['name']}
        """
    )

    #################################################
    # LOGOUT
    #################################################

    if st.sidebar.button("Logout"):

        st.session_state.user = None

        st.rerun()

    #################################################
    # SIDEBAR TITLE
    #################################################

    st.sidebar.title(
        "Finance Copilot"
    )

    #################################################
    # PAGES
    #################################################

    pages = [

        "Portfolio",

        "Retirement",

        "AI Assistant",

        "Retirement Withdrawal Strategy"
    ]

    #################################################
    # ADMIN ACCESS
    #################################################

    if st.session_state.user["email"] == "mesh.ravi@gmail.com":

        pages.append("Admin")

    #################################################
    # NAVIGATION
    #################################################

    page = st.sidebar.radio(

        "Navigation",

        pages
    )

    #################################################
    # PAGE ROUTING
    #################################################

    if page == "Portfolio":

        render_portfolio_page()

    elif page == "Retirement":

        render_retirement_page()

    elif page == "AI Assistant":

        render_ai_page()

    elif page == "Admin":

        render_admin_page()
    elif page == "Retirement Withdrawal Strategy":

        render_bucket_strategy_page()
