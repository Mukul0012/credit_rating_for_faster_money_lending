import pandas as pd

from preprocessing import preprocess_input
from model import predict
from risk import calculate_risk


# Load dataset
df = pd.read_csv(
    "data/raw/ml_training_dataset.csv"
)


# Take one customer
customer = df.iloc[0].copy()


# Remove columns not used by the model
customer = customer.drop([
    "Application_ID",
    "City",
    "Gender",
    "Risk_Grade",
    "Decision"
])


# Convert to dictionary
customer_data = customer.to_dict()


# Preprocess
processed_data = preprocess_input(
    customer_data
)


# Predict
prediction, probability = predict(
    processed_data
)


# Generate risk assessment
result = calculate_risk(
    probability,
    customer_data
)


print("\nFinal Credit Assessment")
print("----------------------------")

for key, value in result.items():
    print(f"{key}: {value}")

import random

for index in random.sample(range(len(df)), 5):

    customer = df.iloc[index].copy()

    actual_decision = customer["Decision"]

    customer = customer.drop([
        "Application_ID",
        "City",
        "Gender",
        "Risk_Grade",
        "Decision"
    ])

    customer_data = customer.to_dict()

    processed_data = preprocess_input(customer_data)

    prediction, probability = predict(processed_data)

    result = calculate_risk(
        probability,
        customer_data
    )

    print("\n-----------------------------")
    print("Customer:", index)
    print("Actual:", actual_decision)
    print("Predicted:", result["decision"])
    print("Probability:", result["approval_probability"])
    print("Risk:", result["risk_level"])
    print("Score:", result["risk_score"])
    print("Factors:", result["risk_factors"])

import random

for index in random.sample(range(len(df)), 5):

    customer = df.iloc[index].copy()

    actual_decision = customer["Decision"]

    customer = customer.drop([
        "Application_ID",
        "City",
        "Gender",
        "Risk_Grade",
        "Decision"
    ])

    customer_data = customer.to_dict()

    processed_data = preprocess_input(customer_data)

    prediction, probability = predict(processed_data)

    result = calculate_risk(
        probability,
        customer_data
    )

    print("\n-----------------------------")
    print("Customer:", index)
    print("Actual:", actual_decision)
    print("Predicted:", result["decision"])
    print("Probability:", result["approval_probability"])
    print("Risk:", result["risk_level"])
    print("Score:", result["risk_score"])
    print("Factors:", result["risk_factors"])