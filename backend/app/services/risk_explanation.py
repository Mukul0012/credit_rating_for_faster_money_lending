def get_risk_factors(
    customer: dict
) -> list[str]:

    factors = []

    # =====================================================
    # Credit score
    # =====================================================

    credit_score = customer.get(
        "Credit_Score"
    )

    if (
        credit_score is not None
        and credit_score < 650
    ):
        factors.append(
            "Low credit score"
        )

    # =====================================================
    # Debt-to-income ratio
    # =====================================================

    dti = customer.get(
        "Debt_to_Income_Ratio"
    )

    if (
        dti is not None
        and dti > 40
    ):
        factors.append(
            "High debt-to-income ratio"
        )

    # =====================================================
    # Credit utilization
    # =====================================================

    utilization = customer.get(
        "Credit_Utilization"
    )

    if (
        utilization is not None
        and utilization > 70
    ):
        factors.append(
            "High credit utilization"
        )

    # =====================================================
    # Previous defaults
    # =====================================================

    previous_defaults = customer.get(
        "Previous_Defaults"
    )

    if (
        previous_defaults is not None
        and previous_defaults > 0
    ):
        factors.append(
            "Previous loan defaults"
        )

    # =====================================================
    # Missed payments
    # =====================================================

    missed_payments = customer.get(
        "Missed_Payments"
    )

    if (
        missed_payments is not None
        and missed_payments > 2
    ):
        factors.append(
            "Multiple missed payments"
        )

    # =====================================================
    # Payment delinquency
    # =====================================================

    maximum_days_past_due = customer.get(
        "Maximum_Days_Past_Due"
    )

    if (
        maximum_days_past_due is not None
        and maximum_days_past_due > 30
    ):
        factors.append(
            "High payment delinquency"
        )

    # =====================================================
    # Recent credit enquiries
    # =====================================================

    recent_enquiries = customer.get(
        "Recent_Credit_Enquiries"
    )

    if (
        recent_enquiries is not None
        and recent_enquiries > 3
    ):
        factors.append(
            "Multiple recent credit enquiries"
        )

    # Original project returns maximum 3 factors
    return factors[:3]