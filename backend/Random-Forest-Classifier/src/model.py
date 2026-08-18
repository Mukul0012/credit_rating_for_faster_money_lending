import joblib


model = joblib.load(
    "models/random_forest_baseline.pkl"
)


def predict(processed_data):

    prediction = model.predict(
        processed_data
    )[0]

    probability = model.predict_proba(
        processed_data
    )[0][1]

    return prediction, probability