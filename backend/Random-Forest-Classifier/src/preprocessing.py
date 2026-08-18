import joblib
import pandas as pd


encoder = joblib.load("models/encoder.pkl")


def preprocess_input(data: dict) -> pd.DataFrame:

    df = pd.DataFrame([data])

    categorical_cols = [
        "Employment_Type",
        "Loan_Purpose"
    ]

    numerical_cols = [
        col for col in df.columns
        if col not in categorical_cols
    ]

    encoded = encoder.transform(
        df[categorical_cols]
    )

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(
            categorical_cols
        )
    )

    final_data = pd.concat(
        [
            df[numerical_cols],
            encoded_df
        ],
        axis=1
    )

    return final_data