import os
import joblib
import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)
import numpy as np


MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "trained_model.pkl")


def train_model_page():

    st.title("🤖 Train Machine Learning Model")

    if "processed_df" not in st.session_state:
        st.warning("Please preprocess the dataset first.")
        return

    df = st.session_state.processed_df

    st.subheader("Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # ----------------------------
    # Target Column
    # ----------------------------

    target = st.selectbox(
        "Select Target Column",
        df.columns
    )

    X = df.drop(columns=[target])

    # Keep only numeric features
    X = X.select_dtypes(include=["number"])

    y = df[target]

    if X.empty:
        st.error("No numeric feature columns available.")
        return

    # ----------------------------
    # Test Size
    # ----------------------------

    test_size = st.slider(
        "Test Size",
        min_value=0.10,
        max_value=0.50,
        value=0.20,
        step=0.05
    )

    # ----------------------------
    # Model Selection
    # ----------------------------

    model_name = st.selectbox(
        "Choose Model",
        [
            "Linear Regression",
            "Decision Tree",
            "Random Forest"
        ]
    )

    # ----------------------------
    # Train
    # ----------------------------

    if st.button("🚀 Train Model"):

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=42
        )

        if model_name == "Linear Regression":
            model = LinearRegression()

        elif model_name == "Decision Tree":
            model = DecisionTreeRegressor(random_state=42)

        else:
            model = RandomForestRegressor(
                n_estimators=100,
                random_state=42
            )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        r2 = r2_score(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))

        st.success("Model Trained Successfully!")

        c1, c2, c3 = st.columns(3)

        c1.metric("R² Score", f"{r2:.4f}")
        c2.metric("MAE", f"{mae:.4f}")
        c3.metric("RMSE", f"{rmse:.4f}")


        # ----------------------------
        # Save Model
        # ----------------------------

        os.makedirs(MODEL_DIR, exist_ok=True)

        joblib.dump(model, MODEL_PATH)

        st.success("Model Saved Successfully")

        st.session_state.model = model
        st.session_state.features = X.columns.tolist()
        st.session_state.target = target

        # ----------------------------
        # Feature Importance
        # ----------------------------

        if model_name == "Random Forest":

            importance = pd.DataFrame({
                "Feature": X.columns,
                "Importance": model.feature_importances_
            }).sort_values(
                by="Importance",
                ascending=False
            )

            st.subheader("Feature Importance")

            st.dataframe(
                importance,
                use_container_width=True
            )