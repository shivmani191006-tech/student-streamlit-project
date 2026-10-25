import os
import json
import joblib
import pandas as pd
import streamlit as st

from database import add_prediction

MODEL_PATH = "models/trained_model.pkl"


def prediction_page():

    st.title("📈 Sales Forecast")

    # -------------------------
    # Check Model
    # -------------------------

    if not os.path.exists(MODEL_PATH):
        st.warning("Please train a model first.")
        return

    model = joblib.load(MODEL_PATH)

    if "features" not in st.session_state:
        st.warning("Feature information not found. Train the model again.")
        return

    features = st.session_state.features

    st.subheader("Enter Feature Values")

    inputs = {}

    for feature in features:

        inputs[feature] = st.number_input(
            feature,
            value=0.0,
            step=1.0
        )

    st.divider()

    # -------------------------
    # Prediction
    # -------------------------

    if st.button("Predict Sales"):

        input_df = pd.DataFrame([inputs])

        prediction = model.predict(input_df)[0]

        st.success("Prediction Completed")

        st.metric(
            "Predicted Sales",
            f"{prediction:,.2f}"
        )

        # Save prediction in session
        result = input_df.copy()
        result["Predicted Sales"] = prediction

        st.session_state.prediction_result = result

        # -------------------------
        # Save to Database
        # -------------------------

        username = st.session_state.get(
            "username",
            "Guest"
        )

        add_prediction(
            username,
            float(prediction),
            json.dumps(inputs)
        )

        st.success("Prediction Saved to History")

        # -------------------------
        # Prediction Table
        # -------------------------

        st.subheader("Prediction Details")

        st.dataframe(
            result,
            use_container_width=True
        )

        # -------------------------
        # Download CSV
        # -------------------------

        csv = result.to_csv(index=False).encode()

        st.download_button(
            "📥 Download Prediction",
            csv,
            "prediction.csv",
            "text/csv"
        )

        # -------------------------
        # Simple AI Insights
        # -------------------------

        st.divider()

        st.subheader("💡 AI Insights")

        if prediction > 100000:
            st.success(
                "High sales expected. Consider increasing inventory."
            )

        elif prediction > 50000:
            st.info(
                "Moderate sales expected. Maintain current stock levels."
            )

        else:
            st.warning(
                "Lower sales expected. Consider promotions or marketing campaigns."
            )