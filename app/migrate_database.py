import sqlite3


DATABASE = "data/revenue.db"


connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()


cursor.execute("""
    CREATE TABLE feedback_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prediction_id INTEGER,
        outcome TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (prediction_id)
            REFERENCES predictions(id)
    )
""")


cursor.execute("""
    SELECT
        id,
        prospect_id,
        outcome,
        created_at
    FROM feedback
    ORDER BY id
""")

feedback_rows = cursor.fetchall()


used_predictions = set()

matched = 0
unmatched = 0


for feedback_id, prospect_id, outcome, created_at in feedback_rows:

    cursor.execute("""
        SELECT
            id
        FROM predictions
        WHERE prospect_id = ?
          AND created_at <= ?
        ORDER BY created_at DESC
    """, (
        prospect_id,
        created_at
    ))

    predictions = cursor.fetchall()

    prediction_id = None

    for prediction in predictions:

        candidate_id = prediction[0]

        if candidate_id not in used_predictions:
            prediction_id = candidate_id
            used_predictions.add(candidate_id)
            break


    cursor.execute("""
        INSERT INTO feedback_new (
            id,
            prediction_id,
            outcome,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        feedback_id,
        prediction_id,
        outcome,
        created_at
    ))


    if prediction_id is not None:
        matched += 1
    else:
        unmatched += 1


cursor.execute("DROP TABLE feedback")

cursor.execute("""
    ALTER TABLE feedback_new
    RENAME TO feedback
""")


connection.commit()


print("Migration completed successfully.")
print(f"Matched feedback records: {matched}")
print(f"Unmatched feedback records: {unmatched}")


print("\nNew feedback records:")

cursor.execute("""
    SELECT
        id,
        prediction_id,
        outcome,
        created_at
    FROM feedback
    ORDER BY id
""")


for row in cursor.fetchall():
    print(row)


connection.close()