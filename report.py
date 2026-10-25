import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from datetime import datetime
import os


REPORT_DIR = "reports"


# ==========================
# Generate PDF
# ==========================

def generate_pdf(data):

    os.makedirs(
        REPORT_DIR,
        exist_ok=True
    )

    file_path = os.path.join(
        REPORT_DIR,
        "sales_forecast_report.pdf"
    )

    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []


    title = Paragraph(
        "AI Sales Forecasting Report",
        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Spacer(1,20)
    )


    username = st.session_state.get(
        "username",
        "Guest"
    )


    elements.append(
        Paragraph(
            f"User: {username}",
            styles["Normal"]
        )
    )


    elements.append(
        Paragraph(
            f"Generated On: {datetime.now()}",
            styles["Normal"]
        )
    )


    elements.append(
        Spacer(1,20)
    )


    table_data = [
        ["Feature", "Value"]
    ]


    for key,value in data.items():

        table_data.append(
            [
                str(key),
                str(value)
            ]
        )


    table = Table(
        table_data
    )


    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                colors.blue
            ),

            (
                "TEXTCOLOR",
                (0,0),
                (-1,0),
                colors.white
            ),

            (
                "GRID",
                (0,0),
                (-1,-1),
                1,
                colors.black
            )
        ])
    )


    elements.append(table)


    elements.append(
        Spacer(1,20)
    )


    elements.append(
        Paragraph(
            "This report was generated using Machine Learning based Sales Forecasting.",
            styles["Normal"]
        )
    )


    doc.build(elements)


    return file_path



# ==========================
# Report Page
# ==========================

def report_page():

    st.title("📄 Sales Forecast Report")


    if "prediction_result" not in st.session_state:

        st.warning(
            "Generate a prediction first."
        )

        return


    result = st.session_state.prediction_result


    st.subheader(
        "Prediction Summary"
    )

    st.dataframe(
        result,
        use_container_width=True
    )


    if st.button(
        "Generate PDF Report"
    ):


        data = result.iloc[0].to_dict()


        file = generate_pdf(
            data
        )


        st.success(
            "Report Generated Successfully"
        )


        with open(
            file,
            "rb"
        ) as pdf:

            st.download_button(

                "📥 Download PDF",

                pdf,

                file_name="sales_report.pdf",

                mime="application/pdf"
            )