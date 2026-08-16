import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

FEATURES = [
    "recent_engagement",
    "company_growth",
    "previous_interaction",
    "employee_count"
]


class ConversionModel:

    def __init__(self, data_path="data/training_data.csv"):

        self.data_path = data_path

        self.model_version = "1.0.0"

        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=4,
            min_samples_leaf=2,
            random_state=42,
            class_weight="balanced"
        )

        self.metrics = {}

        self.train_from_file()


    def train_from_file(self):

        data = pd.read_csv(self.data_path)

        X = data[FEATURES]
        y = data["converted"]

        X_train, X_validation, y_train, y_validation = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )

        self.model.fit(X_train, y_train)

        validation_predictions = self.model.predict(
            X_validation
        )

        self.metrics = {
            "accuracy": round(
                float(
                    accuracy_score(
                        y_validation,
                        validation_predictions
                    )
                ),
                3
            ),

            "precision": round(
                float(
                    precision_score(
                        y_validation,
                        validation_predictions,
                        zero_division=0
                    )
                ),
                3
            ),

            "recall": round(
                float(
                    recall_score(
                        y_validation,
                        validation_predictions,
                        zero_division=0
                    )
                ),
                3
            ),

            "f1_score": round(
                float(
                    f1_score(
                        y_validation,
                        validation_predictions,
                        zero_division=0
                    )
                ),
                3
            ),

            "training_records": len(X_train),
            "validation_records": len(X_validation)
        }


    def predict(self, data):

        probability = self.model.predict_proba(
            data[FEATURES]
        )[0][1]

        if probability >= 0.70:
            prediction = "high"

        elif probability >= 0.40:
            prediction = "medium"

        else:
            prediction = "low"

        signals = self.explain_signals(data)

        return {
            "conversion_probability": round(
                float(probability),
                3
            ),

            "prediction": prediction,

            "key_signals": signals,

            "model_version": self.model_version
        }


    def explain_signals(self, data):

        row = data.iloc[0]

        signals = []

        if row["recent_engagement"] >= 7:
            signals.append(
                "Strong recent engagement"
            )

        elif row["recent_engagement"] <= 3:
            signals.append(
                "Weak recent engagement"
            )

        else:
            signals.append(
                "Moderate recent engagement"
            )


        if row["company_growth"] >= 7:
            signals.append(
                "Positive company growth"
            )

        elif row["company_growth"] <= 3:
            signals.append(
                "Low company growth"
            )

        else:
            signals.append(
                "Moderate company growth"
            )


        if row["previous_interaction"] >= 7:
            signals.append(
                "Strong previous interaction"
            )

        elif row["previous_interaction"] <= 3:
            signals.append(
                "Limited previous interaction"
            )

        else:
            signals.append(
                "Moderate previous interaction"
            )


        if row["employee_count"] >= 250:
            signals.append(
                "Large employee base"
            )

        elif row["employee_count"] <= 50:
            signals.append(
                "Small employee base"
            )

        else:
            signals.append(
                "Medium employee base"
            )


        return signals


    def retrain(self):

        data = pd.read_csv(self.data_path)

        X = data[FEATURES]
        y = data["converted"]

        X_train, X_validation, y_train, y_validation = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )

        new_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=4,
            min_samples_leaf=2,
            random_state=42,
            class_weight="balanced"
        )

        new_model.fit(
            X_train,
            y_train
        )

        validation_predictions = new_model.predict(
            X_validation
        )

        accuracy = accuracy_score(
            y_validation,
            validation_predictions
        )

        precision = precision_score(
            y_validation,
            validation_predictions,
            zero_division=0
        )

        recall = recall_score(
            y_validation,
            validation_predictions,
            zero_division=0
        )

        f1 = f1_score(
            y_validation,
            validation_predictions,
            zero_division=0
        )

        self.model = new_model

        major, minor, patch = map(
            int,
            self.model_version.split(".")
        )

        patch += 1

        self.model_version = (
            f"{major}.{minor}.{patch}"
        )

        self.metrics = {
            "accuracy": round(
                float(accuracy),
                3
            ),

            "precision": round(
                float(precision),
                3
            ),

            "recall": round(
                float(recall),
                3
            ),

            "f1_score": round(
                float(f1),
                3
            ),

            "training_records": len(X_train),
            "validation_records": len(X_validation)
        }

        return {
            "status": "retrained",

            "model_version": self.model_version,

            "training_records": len(X_train),

            "validation_records": len(X_validation),

            "validation_metrics": self.metrics
        }