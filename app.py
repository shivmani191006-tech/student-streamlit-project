import streamlit as st

# Import modules

from auth import (
    login_page,
    register_page,
    logout
)

from preprocess import (
    upload_dataset,
    preprocess_data
)

from train_model import (
    train_model_page
)

from predict import (
    prediction_page
)

from visualization import (
    visualization_page
)

from report import (
    report_page
)

from insights import (
    insights_page
)


# ==========================
# Page Configuration
# ==========================

st.set_page_config(

    page_title="AI Sales Forecasting Dashboard",

    page_icon="📈",

    layout="wide"

)



# ==========================
# Initialize Session
# ==========================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False



# ==========================
# Login/Register Section
# ==========================

if not st.session_state.logged_in:


    st.sidebar.title(
        "🔐 Account"
    )


    option = st.sidebar.radio(

        "Choose",

        [
            "Login",
            "Register"
        ]

    )


    if option == "Login":

        login_page()


    else:

        register_page()



# ==========================
# Main Application
# ==========================

else:


    # Sidebar User Info

    st.sidebar.success(

        f"Welcome {st.session_state.name}"

    )


    st.sidebar.write(

        f"Username: {st.session_state.username}"

    )


    st.sidebar.divider()



    menu = st.sidebar.selectbox(

        "Navigation",

        [

            "🏠 Dashboard",

            "📂 Upload Dataset",

            "🧹 Preprocessing",

            "🤖 Train Model",

            "📈 Sales Forecast",

            "📊 Visualization",

            "📄 Reports",

            "💡 AI Insights"

        ]

    )



    # ==========================
    # Pages
    # ==========================


    if menu == "🏠 Dashboard":

        st.title(
            "📈 AI Sales Forecasting Dashboard"
        )


        st.markdown(
            """
            ### Welcome to the AI Sales Forecasting System

            Features:

            ✅ Secure Login  
            ✅ Dataset Upload  
            ✅ Data Cleaning  
            ✅ Machine Learning Training  
            ✅ Sales Prediction  
            ✅ Interactive Analytics  
            ✅ PDF Reports  
            ✅ AI Business Insights  

            """
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.info(
                "🤖 Machine Learning"
            )


        with col2:

            st.success(
                "📊 Data Analytics"
            )


        with col3:

            st.warning(
                "📈 Future Forecasting"
            )




    elif menu == "📂 Upload Dataset":

        upload_dataset()



    elif menu == "🧹 Preprocessing":

        preprocess_data()



    elif menu == "🤖 Train Model":

        train_model_page()



    elif menu == "📈 Sales Forecast":

        prediction_page()



    elif menu == "📊 Visualization":

        visualization_page()



    elif menu == "📄 Reports":

        report_page()



    elif menu == "💡 AI Insights":

        insights_page()



    # ==========================
    # Logout
    # ==========================

    st.sidebar.divider()


    if st.sidebar.button(
        "🚪 Logout"
    ):

        logout()