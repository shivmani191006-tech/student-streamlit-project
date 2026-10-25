import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def visualization_page():

    st.title("📊 Data Visualization Dashboard")

    if "processed_df" not in st.session_state:
        st.warning("Please upload and preprocess a dataset first.")
        return

    df = st.session_state.processed_df.copy()

    # Remove duplicate column names
    df = df.loc[:, ~df.columns.duplicated()]

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    st.subheader("Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    if len(numeric_cols) == 0:
        st.error("No numeric columns available.")
        return

    # =====================================
    # Histogram
    # =====================================

    st.divider()
    st.subheader("📊 Histogram")

    hist_col = st.selectbox(
        "Select Numeric Column",
        numeric_cols,
        key="hist"
    )

    fig = px.histogram(
        df,
        x=hist_col,
        nbins=30,
        color_discrete_sequence=["royalblue"]
    )

    st.plotly_chart(fig, use_container_width=True)

    # =====================================
    # Box Plot
    # =====================================

    st.divider()
    st.subheader("📦 Box Plot")

    box_col = st.selectbox(
        "Select Column",
        numeric_cols,
        key="box"
    )

    fig = px.box(
        df,
        y=box_col,
        color_discrete_sequence=["tomato"]
    )

    st.plotly_chart(fig, use_container_width=True)

    # =====================================
    # Scatter Plot
    # =====================================

    st.divider()
    st.subheader("🎯 Scatter Plot")

    if len(numeric_cols) >= 2:

        x = st.selectbox(
            "X Axis",
            numeric_cols,
            index=0,
            key="x_axis"
        )

        # Find a different column for Y axis
        y_options = [col for col in numeric_cols if col != x]

        y = st.selectbox(
            "Y Axis",
            y_options,
            index=0,
            key="y_axis"
        )

        fig = px.scatter(
            df,
            x=x,
            y=y,
            trendline="ols"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("At least two numeric columns are required for a scatter plot.")

    # =====================================
    # Line Chart
    # =====================================

    st.divider()
    st.subheader("📈 Line Chart")

    line_col = st.selectbox(
        "Select Column",
        numeric_cols,
        key="line"
    )

    fig = px.line(
        df,
        y=line_col
    )

    st.plotly_chart(fig, use_container_width=True)

    # =====================================
    # Correlation Heatmap
    # =====================================

    st.divider()
    st.subheader("🔥 Correlation Heatmap")

    corr = df[numeric_cols].corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="Viridis",
            text=corr.round(2).values,
            texttemplate="%{text}"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # =====================================
    # Pie Chart
    # =====================================

    if len(categorical_cols) > 0:

        st.divider()

        st.subheader("🥧 Category Distribution")

        cat = st.selectbox(
            "Select Category",
            categorical_cols
        )

        pie = (
            df[cat]
            .value_counts()
            .reset_index()
        )

        pie.columns = [cat, "Count"]

        fig = px.pie(
            pie,
            names=cat,
            values="Count",
            hole=0.4
        )

        st.plotly_chart(fig, use_container_width=True)

    # =====================================
    # Summary Statistics
    # =====================================

    st.divider()

    st.subheader("📋 Summary Statistics")

    st.dataframe(
        df.describe(),
        use_container_width=True
    )

    # =====================================
    # Download Dataset
    # =====================================

    csv = df.to_csv(index=False).encode()

    st.download_button(
        "📥 Download Dataset",
        csv,
        "processed_dataset.csv",
        "text/csv"
    )