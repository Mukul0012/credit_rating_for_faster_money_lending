from app.ml.predictor import Predictor


features = {

    "Age": 30,

    "Annual_Income": 800000,

    "Employment_Duration_Years": 5,

    "Number_of_Dependents": 2,

    "Loan_Amount": 500000,

    "Loan_Tenure_Months": 36,

    "Existing_Loans_Count": 2,

    "Total_Outstanding_Debt": 150000,

    "Existing_Monthly_EMI": 8000,

    "Debt_to_Income_Ratio": 0.30,

    "Loan_to_Income_Ratio": 0.625,

    "Credit_Utilization": 25,

    "Previous_Defaults": 0,

    "Missed_Payments": 1,

    "Maximum_Days_Past_Due": 5,

    "Recent_Credit_Enquiries": 2,

    "Credit_History_Length": 7,

    "Number_of_Credit_Accounts": 4,

    "Payment_History": 95,

    "Credit_Score": 742,

    "Employment_Type": "Salaried",

    "Loan_Purpose": "Personal"
}


result = Predictor.predict(
    features
)

print("\nPrediction:")
print(result)