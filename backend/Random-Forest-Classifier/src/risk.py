def get_risk_factors(customer):
    factors = []

    if customer["Credit_Score"] < 650:
        factors.append("Low credit score")

    if customer["Debt_to_Income_Ratio"] > 40:
        factors.append("High debt-to-income ratio")

    if customer["Credit_Utilization"] > 70:
        factors.append("High credit utilization")

    if customer["Previous_Defaults"] > 0:
        factors.append("Previous loan defaults")

    if customer["Missed_Payments"] > 2:
        factors.append("Multiple missed payments")

    if customer["Maximum_Days_Past_Due"] > 30:
        factors.append("High payment delinquency")

    if customer["Recent_Credit_Enquiries"] > 3:
        factors.append("Multiple recent credit enquiries")

    return factors[:3]

def calculate_risk(probability, customer):

    risk_score = (1 - probability) * 100

    if risk_score <= 30:
        risk_level = "LOW"
        decision = "APPROVE"
    elif risk_score <= 60:
        risk_level = "MEDIUM"
        decision = "REVIEW"
    else:
        risk_level = "HIGH"
        decision = "REJECT"

    return {
        "decision": decision,
        "risk_level": risk_level,
        "risk_score": round(risk_score, 2),
        "approval_probability": round(probability, 3),
        "risk_factors": get_risk_factors(customer)
    }