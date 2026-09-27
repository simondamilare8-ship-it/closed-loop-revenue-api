import os
import pandas as pd
import streamlit as st

from model import ConversionModel
from database import (
    initialize_database,
    save_prediction,
    save_feedback,
    get_predictions,
    get_feedback,
    get_model_performance
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Closed-Loop Revenue Intelligence",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return ConversionModel()


model = load_model()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📈 Closed-Loop AI")

st.sidebar.markdown(
    """
    **Revenue Intelligence Platform**

    Predict prospect conversion, capture CRM outcomes,
    evaluate model performance and continuously improve
    the prediction system.
    """
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🔮 Predict Prospect",
        "📋 Predictions",
        "🔄 CRM Feedback",
        "📊 Model Performance",
        "🤖 Retrain Model"
    ]
)

st.sidebar.divider()

st.sidebar.success("🟢 System Online")
st.sidebar.caption(
    f"Model Version: {model.model_version}"
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.title("📈 Closed-Loop Revenue Intelligence")

    st.markdown(
        """
        ### Predict. Learn. Improve.

        A predictive intelligence layer that uses prospect
        engagement signals and real CRM outcomes to continuously
        evaluate revenue conversion predictions.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # DATABASE DATA
    # --------------------------------------------------------

    predictions = get_predictions()
    feedback = get_feedback()
    performance = get_model_performance()

    total_predictions = len(predictions)
    total_feedback = len(feedback)

    matched_predictions = performance.get(
        "total_matched_predictions",
        0
    )

    accuracy = performance.get(
        "accuracy",
        0
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Predictions",
            total_predictions
        )

    with col2:
        st.metric(
            "CRM Outcomes",
            total_feedback
        )

    with col3:
        st.metric(
            "Matched Predictions",
            matched_predictions
        )

    with col4:
        st.metric(
            "Closed-Loop Accuracy",
            f"{accuracy * 100:.1f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # CLOSED LOOP
    # --------------------------------------------------------

    st.subheader("🔗 How the Closed Loop Works")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info(
            """
            **1. Predict**

            Analyze prospect signals and generate
            a conversion probability.
            """
        )

    with col2:
        st.info(
            """
            **2. Track**

            Store predictions and model versions
            for every prospect.
            """
        )

    with col3:
        st.info(
            """
            **3. Learn**

            Capture actual CRM outcomes:
            won or lost.
            """
        )

    with col4:
        st.info(
            """
            **4. Improve**

            Evaluate performance and retrain
            the model.
            """
        )

    st.divider()

    # --------------------------------------------------------
    # SYSTEM INFORMATION
    # --------------------------------------------------------

    st.subheader("🚀 System Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Architecture:**")
        st.code("Streamlit → ML Model → SQLite")

    with col2:
        st.write("**System Status:**")
        st.success("Running")


# ============================================================
# PREDICT PROSPECT
# ============================================================

elif page == "🔮 Predict Prospect":

    st.title("🔮 Predict Prospect Conversion")

    st.write(
        "Enter the prospect's current revenue signals."
    )

    with st.form("prediction_form"):

        col1, col2 = st.columns(2)

        with col1:

            prospect_id = st.text_input(
                "Prospect ID",
                value="CLAY-001"
            )

            recent_engagement = st.slider(
                "Recent Engagement",
                min_value=0.0,
                max_value=10.0,
                value=8.0,
                step=0.1
            )

            company_growth = st.slider(
                "Company Growth",
                min_value=0.0,
                max_value=10.0,
                value=9.0,
                step=0.1
            )

        with col2:

            previous_interaction = st.slider(
                "Previous Interaction",
                min_value=0.0,
                max_value=10.0,
                value=7.0,
                step=0.1
            )

            employee_count = st.number_input(
                "Employee Count",
                min_value=1,
                value=250,
                step=1
            )

        submitted = st.form_submit_button(
            "🚀 Predict Conversion",
            use_container_width=True
        )

    # --------------------------------------------------------
    # PROCESS PREDICTION
    # --------------------------------------------------------

    if submitted:

        if not prospect_id.strip():

            st.warning(
                "Please enter a Prospect ID."
            )

        else:

            data = pd.DataFrame([
                {
                    "recent_engagement": recent_engagement,
                    "company_growth": company_growth,
                    "previous_interaction": previous_interaction,
                    "employee_count": employee_count
                }
            ])

            try:

                result = model.predict(data)

                probability = result[
                    "conversion_probability"
                ]

                prediction = result[
                    "prediction"
                ]

                model_version = result[
                    "model_version"
                ]

                prediction_id = save_prediction(
                    prospect_id=prospect_id,
                    prediction_score=probability,
                    prediction_label=prediction,
                    model_version=model_version
                )

                st.success(
                    "Prediction generated successfully."
                )

                st.divider()

                # ------------------------------------------------
                # RESULT METRICS
                # ------------------------------------------------

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Conversion Probability",
                        f"{probability * 100:.1f}%"
                    )

                with col2:
                    st.metric(
                        "Prediction",
                        prediction.upper()
                    )

                with col3:
                    st.metric(
                        "Prediction ID",
                        prediction_id
                    )

                with col4:
                    st.metric(
                        "Model Version",
                        model_version
                    )

                st.divider()

                # ------------------------------------------------
                # KEY SIGNALS
                # ------------------------------------------------

                st.subheader("🔍 Key Signals")

                signals = result.get(
                    "key_signals",
                    []
                )

                for signal in signals:
                    st.write(f"• {signal}")

                st.divider()

                st.subheader("📦 Prediction Details")

                st.json({
                    "prediction_id": prediction_id,
                    "prospect_id": prospect_id,
                    **result
                })

            except Exception as e:

                st.error(
                    f"Prediction failed: {e}"
                )


# ============================================================
# PREDICTIONS
# ============================================================

elif page == "📋 Predictions":

    st.title("📋 Prediction History")

    rows = get_predictions()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "id",
                "prospect_id",
                "prediction_score",
                "prediction_label",
                "model_version",
                "created_at"
            ]
        )

        df["prediction_score"] = (
            df["prediction_score"] * 100
        ).round(1)

        df = df.rename(
            columns={
                "id": "Prediction ID",
                "prospect_id": "Prospect ID",
                "prediction_score": "Probability (%)",
                "prediction_label": "Prediction",
                "model_version": "Model Version",
                "created_at": "Created At"
            }
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Total predictions: {len(df)}"
        )

    else:

        st.info(
            "No predictions have been generated yet."
        )


# ============================================================
# CRM FEEDBACK
# ============================================================

elif page == "🔄 CRM Feedback":

    st.title("🔄 CRM Outcome Feedback")

    st.write(
        """
        Connect each prediction to the actual CRM outcome.
        This creates the closed feedback loop.
        """
    )

    predictions = get_predictions()

    if predictions:

        prediction_options = {}

        for p in predictions:

            prediction_id = p[0]
            prospect_id = p[1]
            score = p[2]
            label = p[3]

            option = (
                f"#{prediction_id} — "
                f"{prospect_id} — "
                f"{label.upper()} "
                f"({score * 100:.1f}%)"
            )

            prediction_options[option] = prediction_id

        selected = st.selectbox(
            "Select Prediction",
            list(prediction_options.keys())
        )

        prediction_id = prediction_options[selected]

        outcome = st.radio(
            "Actual CRM Outcome",
            ["won", "lost"],
            horizontal=True
        )

        if st.button(
            "💾 Save CRM Outcome",
            use_container_width=True
        ):

            try:

                save_feedback(
                    prediction_id,
                    outcome
                )

                st.success(
                    "CRM outcome saved successfully."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Unable to save feedback: {e}"
                )

    else:

        st.info(
            "Generate a prediction first before adding CRM feedback."
        )

    st.divider()

    # --------------------------------------------------------
    # FEEDBACK HISTORY
    # --------------------------------------------------------

    st.subheader("📜 Feedback History")

    feedback = get_feedback()

    if feedback:

        df = pd.DataFrame(
            feedback,
            columns=[
                "id",
                "prediction_id",
                "prospect_id",
                "outcome",
                "created_at"
            ]
        )

        df = df.rename(
            columns={
                "id": "Feedback ID",
                "prediction_id": "Prediction ID",
                "prospect_id": "Prospect ID",
                "outcome": "Outcome",
                "created_at": "Created At"
            }
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No CRM feedback has been recorded yet."
        )


# ============================================================
# MODEL PERFORMANCE
# ============================================================

elif page == "📊 Model Performance":

    st.title(
        "📊 Closed-Loop Model Performance"
    )

    data = get_model_performance()

    total = data.get(
        "total_matched_predictions",
        0
    )

    accuracy = data.get(
        "accuracy",
        0
    )

    precision = data.get(
        "precision",
        0
    )

    recall = data.get(
        "recall",
        0
    )

    # --------------------------------------------------------
    # PERFORMANCE METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Matched Predictions",
            total
        )

    with col2:
        st.metric(
            "Accuracy",
            f"{accuracy * 100:.1f}%"
        )

    with col3:
        st.metric(
            "Precision",
            f"{precision * 100:.1f}%"
        )

    with col4:
        st.metric(
            "Recall",
            f"{recall * 100:.1f}%"
        )

    st.divider()

    # --------------------------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------------------------

    st.subheader("Confusion Matrix")

    cm_col1, cm_col2 = st.columns(2)

    with cm_col1:

        st.metric(
            "True Positives",
            data.get("true_positives", 0)
        )

        st.metric(
            "False Positives",
            data.get("false_positives", 0)
        )

    with cm_col2:

        st.metric(
            "True Negatives",
            data.get("true_negatives", 0)
        )

        st.metric(
            "False Negatives",
            data.get("false_negatives", 0)
        )

    st.divider()

    st.subheader("Performance Data")

    st.json(data)


# ============================================================
# RETRAIN MODEL
# ============================================================

elif page == "🤖 Retrain Model":

    st.title("🤖 Model Retraining")

    st.warning(
        """
        Retraining creates a new model version using the
        current training dataset.
        """
    )

    st.write(
        f"Current model version: **{model.model_version}**"
    )

    if st.button(
        "🔄 Retrain Model",
        use_container_width=True
    ):

        with st.spinner(
            "Retraining model..."
        ):

            try:

                result = model.retrain()

                st.success(
                    "Model retrained successfully."
                )

                # ------------------------------------------------
                # MODEL INFORMATION
                # ------------------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Model Version",
                        result.get(
                            "model_version",
                            "N/A"
                        )
                    )

                    st.metric(
                        "Training Records",
                        result.get(
                            "training_records",
                            0
                        )
                    )

                with col2:

                    st.metric(
                        "Validation Records",
                        result.get(
                            "validation_records",
                            0
                        )
                    )

                st.divider()

                # ------------------------------------------------
                # VALIDATION METRICS
                # ------------------------------------------------

                st.subheader(
                    "Validation Metrics"
                )

                metrics = result.get(
                    "validation_metrics",
                    {}
                )

                if metrics:

                    m1, m2, m3, m4 = st.columns(4)

                    with m1:
                        st.metric(
                            "Accuracy",
                            f"{metrics.get('accuracy', 0) * 100:.1f}%"
                        )

                    with m2:
                        st.metric(
                            "Precision",
                            f"{metrics.get('precision', 0) * 100:.1f}%"
                        )

                    with m3:
                        st.metric(
                            "Recall",
                            f"{metrics.get('recall', 0) * 100:.1f}%"
                        )

                    with m4:
                        st.metric(
                            "F1 Score",
                            f"{metrics.get('f1_score', 0) * 100:.1f}%"
                        )

                st.divider()

                st.subheader("Retraining Result")

                st.json(result)

            except Exception as e:

                st.error(
                    f"Retraining failed: {e}"
                )