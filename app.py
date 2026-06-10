import re
import streamlit as st

from modules.auth import login, signup
from ui.components import render_html
from ui.theme import load_theme


st.set_page_config(
    page_title="Cloud Expense Intelligence",
    page_icon=":material/cloud:",
    layout="wide",
    initial_sidebar_state="expanded",
)


load_theme()


if "user" not in st.session_state:
    st.session_state.user = None


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False



def valid_email(email):

    pattern = r"^[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook)\.com$"

    return re.match(pattern,email)



def login_page():


    render_html(
        """
        <style>

        [data-testid="stSidebar"]{
        display:none!important;
        }

        [data-testid="stSidebarCollapsedControl"]{
        display:none!important;
        }

        </style>
        """
    )


    brand_col, form_col = st.columns(
        [1.1,1],
        gap="large"
    )


    with brand_col:

        render_html(
        """
        <div class="login-brand-panel">


        <div class="login-brand-badge">
        AI powered finance
        </div>


        <h1 class="login-brand-title">
        Cloud Expense Intelligence
        </h1>


        <p class="login-brand-text">

        Monitor spending, forecast costs,
        and make smarter financial decisions
        with AI-powered insights.

        </p>


        <ul class="login-brand-features">

        <li>Real-time expense dashboards</li>

        <li>ML based forecasting</li>

        <li>AI financial assistant</li>

        </ul>


        </div>
        """
        )




    with form_col:


        render_html(
        """
        <div class="login-card-header">


        <div class="login-form-icon">
        CE
        </div>


        <h2>
        Sign in to your account
        </h2>


        <p>
        Access your expense intelligence workspace
        </p>


        </div>
        """
        )


        with st.container(border=True):


            tab_login, tab_signup = st.tabs(
            [
            "Login",
            "Create account"
            ]
            )


            with tab_login:


                email = st.text_input(
                    "Email",
                    key="login_email",
                    placeholder="you@gmail.com"
                )


                password = st.text_input(
                    "Password",
                    type="password",
                    key="login_password"
                )



                if st.button(
                    "Sign in",
                    type="primary",
                    use_container_width=True
                ):


                    if not valid_email(email):

                        st.warning(
                        "Enter valid Gmail, Yahoo or Outlook email."
                        )


                    else:

                        user = login(
                            email,
                            password
                        )


                        if user:

                            st.session_state.user=user
                            st.session_state.logged_in=True
                            st.session_state.user_id=user["id"]


                            st.switch_page(
                            "pages/1_Dashboard.py"
                            )


                        else:

                            st.error(
                            "Invalid credentials."
                            )





            with tab_signup:


                name = st.text_input(
                    "Full name",
                    key="signup_name"
                )


                email = st.text_input(
                    "Email",
                    key="signup_email"
                )


                password = st.text_input(
                    "Password",
                    type="password",
                    key="signup_password"
                )



                if st.button(
                    "Create account",
                    type="primary",
                    use_container_width=True
                ):


                    if not valid_email(email):

                        st.warning(
                        "Use Gmail, Yahoo or Outlook email."
                        )


                    elif not name or not password:

                        st.warning(
                        "Fill all fields."
                        )


                    else:


                        created = signup(
                            name,
                            email,
                            password
                        )


                        if created:

                            st.success(
                            "Account created successfully 🎉"
                            )

                            st.info(
                            "Switch to Login tab."
                            )


                        else:

                            st.warning(
                            "Email already registered. Login instead."
                            )



        render_html(
        """
        <p class="login-trust">

        Secure sign-in · Private expense workspace

        </p>
        """
        )




if st.session_state.user is None:

    login_page()


else:

    st.switch_page(
    "pages/1_Dashboard.py"
    )