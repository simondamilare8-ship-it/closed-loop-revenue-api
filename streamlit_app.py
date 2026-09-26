import streamlit as st
import requests
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

# Local development:
#     http://127.0.0.1:8000
#
# Streamlit Cloud:
#     Set API_URL inside Streamlit Cloud Secrets.
#
# Example:
#     API_URL = "https://your-fastapi-url.com"
try:
    API_URL = st.secrets["API_URL"]
except (FileNotFoundError, KeyError):
    API_URL = "http://127.0.0.1:8000"

API_URL = API_URL.rstrip("/")


st.set_page_config(
    page_title="Closed-Loop Revenue Intelligence",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def api_get(endpoint):
    """Send GET request to FastAPI backend."""

    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=60
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.exceptions.RequestException:
        return None


def api_post(endpoint, payload=None):
    """Send POST request to FastAPI backend."""

    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=120
        )

        return response

    except requests.exceptions.RequestException as e:
        st.error(f"API connection error: {e}")
        return None


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


# ============================================================
# API HEALTH CHECK
# ============================================================

health = api_get("/health")


if health and health.get("status") == "healthy":

    st.sidebar.success("API Online")

else:

    st.sidebar.error("API Offline")


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
    # GET DASHBOARD DATA
    # --------------------------------------------------------

    predictions_data = api_get("/predictions")

    feedback_data = api_get("/feedback")

    performance_data = api_get("/model-performance")


    # --------------------------------------------------------
    # DEFAULT VALUES
    # --------------------------------------------------------

    total_predictions = 0

    total_feedback = 0

    matched_predictions = 0

    accuracy = 0


    # --------------------------------------------------------
    # PREDICTIONS
    # --------------------------------------------------------

    if predictions_data:

        total_predictions = predictions_data.get(
            "count",
            0
        )


    # --------------------------------------------------------
    # FEEDBACK
    # --------------------------------------------------------

    if feedback_data:

        total_feedback = feedback_data.get(
            "count",
            0
        )


    # --------------------------------------------------------
    # MODEL PERFORMANCE
    # --------------------------------------------------------

    if performance_data:

        matched_predictions = performance_data.get(
            "total_matched_predictions",
            0
        )

        accuracy = performance_data.get(
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
    # CLOSED LOOP PROCESS
    # --------------------------------------------------------

    st.subheader("🔗 How the Closed Loop Works")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.info(
            """
            **1. Predict**

            Analyze prospect signals and generate a
            conversion probability.
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
    # API INFORMATION
    # --------------------------------------------------------

    st.subheader("🚀 API Information")


    col1, col2 = st.columns(2)


    with col1:

        st.write("**API:**")

        st.code(API_URL)


    with col2:

        st.write("**API Status:**")


        if health:

            st.success("Healthy")

        else:

            st.error("Unable to connect")


# ============================================================
# PREDICT PROSPECT
# ============================================================

elif page == "🔮 Predict Prospect":

    st.title("🔮 Predict Prospect Conversion")

    st.write(
        "Enter the prospect's current revenue signals."
    )


    # --------------------------------------------------------
    # FORM
    # --------------------------------------------------------

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

            payload = {

                "prospect_id": prospect_id,

                "recent_engagement":
                    recent_engagement,

                "company_growth":
                    company_growth,

                "previous_interaction":
                    previous_interaction,

                "employee_count":
                    employee_count
            }


            response = api_post(
                "/predict",
                payload
            )


            if response and response.status_code == 200:

                result = response.json()


                st.success(
                    "Prediction generated successfully."
                )


                st.divider()


                probability = result.get(
                    "conversion_probability",
                    0
                )


                prediction = result.get(
                    "prediction",
                    "N/A"
                )


                prediction_id = result.get(
                    "prediction_id",
                    "N/A"
                )


                model_version = result.get(
                    "model_version",
                    "N/A"
                )


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

                    st.write(
                        f"• {signal}"
                    )


                st.divider()


                # ------------------------------------------------
                # API RESPONSE
                # ------------------------------------------------

                st.subheader("📦 API Response")

                st.json(result)


            else:

                if response:

                    st.error(
                        f"Prediction failed: "
                        f"{response.status_code}"
                    )

                    st.code(
                        response.text
                    )


# ============================================================
# PREDICTIONS
# ============================================================

elif page == "📋 Predictions":

    st.title("📋 Prediction History")


    data = api_get(
        "/predictions"
    )


    if data and data.get("predictions"):

        predictions = data["predictions"]


        df = pd.DataFrame(
            predictions
        )


        if not df.empty:

            df["prediction_score"] = (
                df["prediction_score"] * 100
            ).round(1)


            df = df.rename(
                columns={

                    "id":
                        "Prediction ID",

                    "prospect_id":
                        "Prospect ID",

                    "prediction_score":
                        "Probability (%)",

                    "prediction_label":
                        "Prediction",

                    "model_version":
                        "Model Version",

                    "created_at":
                        "Created At"
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
                "No predictions found."
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
        Connect the prediction to the actual CRM outcome.
        This is what creates the closed feedback loop.
        """
    )


    # --------------------------------------------------------
    # GET PREDICTIONS
    # --------------------------------------------------------

    predictions_data = api_get(
        "/predictions"
    )


    if (
        predictions_data
        and predictions_data.get("predictions")
    ):

        predictions = predictions_data[
            "predictions"
        ]


        # ----------------------------------------------------
        # CREATE DROPDOWN OPTIONS
        # ----------------------------------------------------

        prediction_options = {

            f"#{p['id']} — "
            f"{p['prospect_id']} — "
            f"{p['prediction_label'].upper()} "
            f"({p['prediction_score'] * 100:.1f}%)":

            p["id"]

            for p in predictions
        }


        selected = st.selectbox(
            "Select Prediction",
            list(
                prediction_options.keys()
            )
        )


        prediction_id = prediction_options[
            selected
        ]


        # ----------------------------------------------------
        # OUTCOME
        # ----------------------------------------------------

        outcome = st.radio(
            "Actual CRM Outcome",
            ["won", "lost"],
            horizontal=True
        )


        # ----------------------------------------------------
        # SAVE OUTCOME
        # ----------------------------------------------------

        if st.button(
            "💾 Save CRM Outcome",
            use_container_width=True
        ):

            payload = {

                "prediction_id":
                    prediction_id,

                "outcome":
                    outcome
            }


            response = api_post(
                "/feedback",
                payload
            )


            if (
                response
                and response.status_code == 200
            ):

                result = response.json()


                if result.get(
                    "status"
                ) == "saved":

                    st.success(
                        "CRM outcome saved successfully."
                    )


                    st.json(
                        result
                    )


                else:

                    st.error(
                        result.get(
                            "message",
                            "Unable to save feedback."
                        )
                    )


            elif response:

                st.error(
                    f"Feedback failed: "
                    f"{response.status_code}"
                )


                st.code(
                    response.text
                )


    else:

        st.info(
            "Generate a prediction first before "
            "adding CRM feedback."
        )


    st.divider()


    # --------------------------------------------------------
    # FEEDBACK HISTORY
    # --------------------------------------------------------

    st.subheader(
        "📜 Feedback History"
    )


    feedback_data = api_get(
        "/feedback"
    )


    if (
        feedback_data
        and feedback_data.get("feedback")
    ):

        feedback = feedback_data[
            "feedback"
        ]


        df = pd.DataFrame(
            feedback
        )


        df = df.rename(
            columns={

                "id":
                    "Feedback ID",

                "prediction_id":
                    "Prediction ID",

                "prospect_id":
                    "Prospect ID",

                "outcome":
                    "Outcome",

                "created_at":
                    "Created At"
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


    data = api_get(
        "/model-performance"
    )


    if data:

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


        # ----------------------------------------------------
        # PERFORMANCE METRICS
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # CONFUSION MATRIX
        # ----------------------------------------------------

        st.subheader(
            "Confusion Matrix"
        )


        cm_col1, cm_col2 = st.columns(2)


        with cm_col1:

            st.metric(
                "True Positives",
                data.get(
                    "true_positives",
                    0
                )
            )


            st.metric(
                "False Positives",
                data.get(
                    "false_positives",
                    0
                )
            )


        with cm_col2:

            st.metric(
                "True Negatives",
                data.get(
                    "true_negatives",
                    0
                )
            )


            st.metric(
                "False Negatives",
                data.get(
                    "false_negatives",
                    0
                )
            )


        st.divider()


        # ----------------------------------------------------
        # RAW PERFORMANCE DATA
        # ----------------------------------------------------

        st.subheader(
            "Performance Data"
        )


        st.json(
            data
        )


    else:

        st.warning(
            "Unable to retrieve model performance."
        )


# ============================================================
# RETRAIN MODEL
# ============================================================

elif page == "🤖 Retrain Model":

    st.title(
        "🤖 Model Retraining"
    )


    st.warning(
        """
        Retraining creates a new model version using the
        current training dataset.
        """
    )


    # --------------------------------------------------------
    # RETRAIN BUTTON
    # --------------------------------------------------------

    if st.button(
        "🔄 Retrain Model",
        use_container_width=True
    ):

        with st.spinner(
            "Retraining model..."
        ):

            response = api_post(
                "/retrain"
            )


        if (
            response
            and response.status_code == 200
        ):

            result = response.json()


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


            st.json(
                result
            )


        elif response:

            st.error(
                f"Retraining failed: "
                f"{response.status_code}"
            )


            st.code(
                response.text
            )