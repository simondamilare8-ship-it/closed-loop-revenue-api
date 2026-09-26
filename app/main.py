from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

from app.model import ConversionModel
from app.database import (
    initialize_database,
    save_prediction,
    save_feedback,
    get_predictions,
    get_feedback,
    get_model_performance
)

app = FastAPI(
    title="Closed-Loop Revenue Intelligence API",
    description="Predictive intelligence API for prospect conversion analysis.",
    version="1.0.0"
)

model = ConversionModel()

initialize_database()


class Prospect(BaseModel):
    prospect_id: str
    recent_engagement: float
    company_growth: float
    previous_interaction: float
    employee_count: int


class Feedback(BaseModel):
    prediction_id: int
    outcome: str


@app.get("/")
def home():
    return {
        "message": "Closed-Loop Revenue Intelligence API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/predict")
def predict(prospect: Prospect):

    data = pd.DataFrame([
        {
            "recent_engagement": prospect.recent_engagement,
            "company_growth": prospect.company_growth,
            "previous_interaction": prospect.previous_interaction,
            "employee_count": prospect.employee_count
        }
    ])

    result = model.predict(data)

    prediction_score = result["conversion_probability"]
    prediction_label = result["prediction"]

    prediction_id = save_prediction(
        prospect.prospect_id,
        prediction_score,
        prediction_label,
        model.model_version
    )

    return {
        "prediction_id": prediction_id,
        "prospect_id": prospect.prospect_id,
        **result
    }


@app.post("/feedback")
def feedback(feedback: Feedback):

    if feedback.outcome not in ["won", "lost"]:
        return {
            "status": "error",
            "message": "Outcome must be 'won' or 'lost'."
        }

    save_feedback(
        feedback.prospect_id,
        feedback.outcome
    )

    return {
        "status": "saved",
        "prospect_id": feedback.prospect_id,
        "outcome": feedback.outcome
    }


@app.get("/feedback")
def feedback_history():

    rows = get_feedback()

    return {
        "count": len(rows),
        "feedback": [
            {
                "id": row[0],
                "prospect_id": row[1],
                "outcome": row[2],
                "created_at": row[3]
            }
            for row in rows
        ]
    }


@app.get("/predictions")
def prediction_history():

    rows = get_predictions()

    return {
        "count": len(rows),
        "predictions": [
            {
                "id": row[0],
                "prospect_id": row[1],
                "prediction_score": row[2],
                "prediction_label": row[3],
                "model_version": row[4],
                "created_at": row[5]
            }
            for row in rows
        ]
    }


@app.get("/model-performance")
def model_performance():

    return get_model_performance()


@app.post("/retrain")
def retrain_model():

    result = model.retrain()

    return result