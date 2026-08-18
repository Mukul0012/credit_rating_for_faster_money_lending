from typing import Any

import pandas as pd

from app.ml.model_loader import ModelLoader


class Predictor:

    NUMERICAL_FEATURES = [

        "Age",

        "Annual_Income",

        "Employment_Duration_Years",

        "Number_of_Dependents",

        "Loan_Amount",

        "Loan_Tenure_Months",

        "Existing_Loans_Count",

        "Total_Outstanding_Debt",

        "Existing_Monthly_EMI",

        "Debt_to_Income_Ratio",

        "Loan_to_Income_Ratio",

        "Credit_Utilization",

        "Previous_Defaults",

        "Missed_Payments",

        "Maximum_Days_Past_Due",

        "Recent_Credit_Enquiries",

        "Credit_History_Length",

        "Number_of_Credit_Accounts",

        "Payment_History",

        "Credit_Score"
    ]

    CATEGORICAL_FEATURES = [

        "Employment_Type",

        "Loan_Purpose"
    ]

    @classmethod
    def predict(
        cls,
        raw_features: dict[str, Any]
    ):

        model = ModelLoader.get_model()

        encoder = ModelLoader.get_encoder()

        # =================================================
        # 1. Check all required features
        # =================================================

        required_features = (
            cls.NUMERICAL_FEATURES
            +
            cls.CATEGORICAL_FEATURES
        )

        missing_features = [
            feature
            for feature in required_features
            if raw_features.get(feature) is None
        ]

        if missing_features:

            raise ValueError(
                "Missing ML features: "
                +
                ", ".join(
                    missing_features
                )
            )

        # =================================================
        # 2. Numerical features
        # =================================================

        numerical_df = pd.DataFrame(
            [
                {
                    feature:
                        raw_features[feature]
                    for feature
                    in cls.NUMERICAL_FEATURES
                }
            ]
        )

        # =================================================
        # 3. Categorical features
        # =================================================

        categorical_df = pd.DataFrame(
            [
                {
                    feature:
                        raw_features[feature]
                    for feature
                    in cls.CATEGORICAL_FEATURES
                }
            ]
        )

        # =================================================
        # 4. Encode categorical values
        # =================================================

        encoded = encoder.transform(
            categorical_df
        )

        encoded_names = (
            encoder.get_feature_names_out(
                cls.CATEGORICAL_FEATURES
            )
        )

        encoded_df = pd.DataFrame(
            encoded,
            columns=encoded_names
        )

        # =================================================
        # 5. Combine features
        # =================================================

        final_df = pd.concat(
            [
                numerical_df,
                encoded_df
            ],
            axis=1
        )

        # =================================================
        # 6. Validate feature count
        # =================================================

        expected_features = (
            model.n_features_in_
        )

        actual_features = (
            final_df.shape[1]
        )

        if actual_features != expected_features:

            raise ValueError(
                f"Feature mismatch: "
                f"model expects "
                f"{expected_features}, "
                f"received "
                f"{actual_features}"
            )

        # =================================================
        # 7. Validate exact feature names/order
        # =================================================

        expected_names = (
            list(
                model.feature_names_in_
            )
        )

        actual_names = (
            final_df.columns.tolist()
        )

        if actual_names != expected_names:

            raise ValueError(
                "Feature order/name mismatch.\n"
                f"Expected: {expected_names}\n"
                f"Received: {actual_names}"
            )

        # =================================================
        # 8. Prediction
        # =================================================

        prediction = model.predict(
            final_df
        )[0]

        result = {

            "prediction":
                int(prediction),

            "feature_count":
                actual_features
        }

        # =================================================
        # 9. Prediction probabilities
        # =================================================

        if hasattr(
            model,
            "predict_proba"
        ):

            probabilities = (
                model.predict_proba(
                    final_df
                )[0]
            )

            result["probabilities"] = {

                str(label):
                    float(probability)

                for label, probability
                in zip(
                    model.classes_,
                    probabilities
                )
            }

        return result