import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# ==========================
# Upload Dataset
# ==========================

def upload_dataset():

    st.title("📂 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel File",
        type=["csv", "xlsx"]
    )

    if uploaded_file is None:
        return

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        st.session_state.df = df

        st.success("Dataset Uploaded Successfully")

        st.subheader("Dataset Preview")

        st.dataframe(df, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows", df.shape[0])

        with col2:
            st.metric("Columns", df.shape[1])

        st.subheader("Data Types")

        st.dataframe(
            pd.DataFrame({
                "Column": df.columns,
                "Type": df.dtypes.astype(str)
            })
        )

    except Exception as e:

        st.error(str(e))


# ==========================
# Preprocessing
# ==========================

def preprocess_data():

    st.title("🧹 Data Preprocessing")

    if "df" not in st.session_state:

        st.warning("Upload Dataset First")

        return

    df = st.session_state.df.copy()

    st.subheader("Original Dataset")

    st.dataframe(df.head())

    st.divider()

    # ----------------------
    # Remove Duplicates
    # ----------------------

    duplicates = df.duplicated().sum()

    st.write(f"Duplicate Rows : {duplicates}")

    if st.button("Remove Duplicates"):

        df = df.drop_duplicates()

        st.success("Duplicates Removed")

    # ----------------------
    # Missing Values
    # ----------------------

    st.divider()

    st.subheader("Missing Values")

    st.dataframe(df.isnull().sum())

    option = st.selectbox(

        "Missing Value Strategy",

        [
            "Do Nothing",
            "Drop Missing Rows",
            "Fill Numeric Mean",
            "Fill Numeric Median",
            "Fill Categorical Mode"
        ]

    )

    if st.button("Apply Missing Value Strategy"):

        if option == "Drop Missing Rows":

            df = df.dropna()

        elif option == "Fill Numeric Mean":

            num = df.select_dtypes(include="number").columns

            df[num] = df[num].fillna(df[num].mean())

        elif option == "Fill Numeric Median":

            num = df.select_dtypes(include="number").columns

            df[num] = df[num].fillna(df[num].median())

        elif option == "Fill Categorical Mode":

            cat = df.select_dtypes(include="object").columns

            for col in cat:
                df[col] = df[col].fillna(df[col].mode()[0])

        st.success("Missing Values Processed")

    # ----------------------
    # Date Conversion
    # ----------------------

    st.divider()

    st.subheader("Convert Date Column")

    date_col = st.selectbox(
        "Select Date Column",
        ["None"] + list(df.columns)
    )

    if st.button("Convert Date"):

        if date_col != "None":

            try:

                df[date_col] = pd.to_datetime(df[date_col])

                st.success("Date Converted")

            except:

                st.error("Conversion Failed")

    # ----------------------
    # Encode
    # ----------------------

    st.divider()

    st.subheader("Encode Categorical Columns")

    categorical = df.select_dtypes(include="object").columns

    if len(categorical) > 0:

        st.write(list(categorical))

        if st.button("Encode Columns"):

            encoder = LabelEncoder()

            for col in categorical:

                df[col] = encoder.fit_transform(
                    df[col].astype(str)
                )

            st.success("Encoding Completed")

    # ----------------------
    # Save
    # ----------------------

    st.session_state.processed_df = df

    st.divider()

    st.subheader("Processed Dataset")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode()

    st.download_button(

        "📥 Download Processed Dataset",

        csv,

        "processed_dataset.csv",

        "text/csv"

    )