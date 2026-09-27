import os
import sqlite3
from datetime import datetime


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE = os.path.join(
    BASE_DIR,
    "data",
    "revenue.db"
)


def get_connection():

    os.makedirs(
        os.path.dirname(DATABASE),
        exist_ok=True
    )

    return sqlite3.connect(DATABASE)


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prospect_id TEXT NOT NULL,
            prediction_score REAL NOT NULL,
            prediction_label TEXT NOT NULL,
            model_version TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_id INTEGER,
            outcome TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (prediction_id)
                REFERENCES predictions(id)
        )
    """)

    connection.commit()
    connection.close()


def save_prediction(
    prospect_id,
    prediction_score,
    prediction_label,
    model_version
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            prospect_id,
            prediction_score,
            prediction_label,
            model_version,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        prospect_id,
        prediction_score,
        prediction_label,
        model_version,
        datetime.utcnow().isoformat()
    ))

    prediction_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return prediction_id


def save_feedback(prediction_id, outcome):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO feedback (
            prediction_id,
            outcome,
            created_at
        )
        VALUES (?, ?, ?)
    """, (
        prediction_id,
        outcome,
        datetime.utcnow().isoformat()
    ))

    connection.commit()
    connection.close()


def get_feedback():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            f.id,
            f.prediction_id,
            p.prospect_id,
            f.outcome,
            f.created_at
        FROM feedback f
        LEFT JOIN predictions p
            ON f.prediction_id = p.id
        ORDER BY f.id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_predictions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            prospect_id,
            prediction_score,
            prediction_label,
            model_version,
            created_at
        FROM predictions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_model_performance():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            p.prediction_label,
            f.outcome
        FROM predictions p
        INNER JOIN feedback f
            ON p.id = f.prediction_id
    """)

    rows = cursor.fetchall()

    connection.close()

    total = len(rows)

    if total == 0:

        return {
            "total_matched_predictions": 0,
            "correct_predictions": 0,
            "incorrect_predictions": 0,
            "accuracy": 0,
            "true_positives": 0,
            "true_negatives": 0,
            "false_positives": 0,
            "false_negatives": 0,
            "precision": 0,
            "recall": 0
        }

    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0

    for prediction, outcome in rows:

        predicted_positive = (
            prediction == "high"
        )

        actual_positive = (
            outcome == "won"
        )

        if predicted_positive and actual_positive:

            true_positives += 1

        elif not predicted_positive and not actual_positive:

            true_negatives += 1

        elif predicted_positive and not actual_positive:

            false_positives += 1

        else:

            false_negatives += 1

    correct = (
        true_positives +
        true_negatives
    )

    incorrect = (
        false_positives +
        false_negatives
    )

    accuracy = correct / total

    precision = (
        true_positives /
        (true_positives + false_positives)
        if true_positives + false_positives > 0
        else 0
    )

    recall = (
        true_positives /
        (true_positives + false_negatives)
        if true_positives + false_negatives > 0
        else 0
    )

    return {
        "total_matched_predictions": total,
        "correct_predictions": correct,
        "incorrect_predictions": incorrect,
        "accuracy": round(accuracy, 3),
        "true_positives": true_positives,
        "true_negatives": true_negatives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "precision": round(precision, 3),
        "recall": round(recall, 3)
    }