import streamlit as st
import pandas as pd


def insights_page():

    st.title("💡 AI Sales Insights")


    # -------------------------
    # Check Dataset
    # -------------------------

    if "processed_df" not in st.session_state:

        st.warning(
            "Please upload and preprocess dataset first."
        )

        return


    df = st.session_state.processed_df


    st.subheader(
        "📊 Dataset Overview"
    )


    # -------------------------
    # Basic Statistics
    # -------------------------

    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns


    if len(numeric_cols) == 0:

        st.error(
            "No numeric data available."
        )

        return



    avg_values = df[numeric_cols].mean()

    max_values = df[numeric_cols].max()

    min_values = df[numeric_cols].min()



    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Average Value",
            round(avg_values.mean(),2)
        )


    with col2:

        st.metric(
            "Maximum Value",
            round(max_values.max(),2)
        )


    with col3:

        st.metric(
            "Minimum Value",
            round(min_values.min(),2)
        )


    st.divider()



    # -------------------------
    # Prediction Insights
    # -------------------------


    if "prediction_result" in st.session_state:


        prediction = (

            st.session_state
            .prediction_result
            ["Predicted Sales"]
            .iloc[0]

        )


        st.subheader(
            "🤖 Forecast Analysis"
        )


        average_sales = avg_values.mean()


        if prediction > average_sales:


            st.success(
                f"""
                📈 Expected sales ({prediction:.2f})
                are above average.

                Recommendation:
                - Increase inventory
                - Prepare marketing campaigns
                - Focus on high-demand products
                """
            )


        else:


            st.warning(
                f"""
                📉 Expected sales ({prediction:.2f})
                are below average.

                Recommendation:
                - Review pricing strategy
                - Improve promotions
                - Analyze customer demand
                """
            )


    else:


        st.info(
            "Generate a prediction to get forecast insights."
        )


    st.divider()



    # -------------------------
    # Column Analysis
    # -------------------------


    st.subheader(
        "📌 Feature Analysis"
    )


    selected = st.selectbox(

        "Select Feature",

        numeric_cols

    )


    st.write(
        f"""
        Analysis for **{selected}**

        Average:
        {df[selected].mean():.2f}

        Highest:
        {df[selected].max():.2f}

        Lowest:
        {df[selected].min():.2f}
        """
    )



    # -------------------------
    # Dataset Download
    # -------------------------


    csv = df.to_csv(
        index=False
    ).encode()


    st.download_button(

        "📥 Download Analysis Dataset",

        csv,

        "sales_analysis.csv",

        "text/csv"

    )