def get_risk_factors(
    customer: dict
) -> list[str]:

    factors = []

    # =====================================================
    # Loan-to-income ratio (LTI)
    # =====================================================

    lti = customer.get(
        "Loan_to_Income_Ratio"
    )

    if lti is not None and lti > 200:
        factors.append(
            f"Excessive loan-to-income ratio ({lti:.1f}%): requested loan exceeds safe annual income limits"
        )
    elif lti is not None and lti > 100:
        factors.append(
            f"High loan-to-income ratio ({lti:.1f}%)"
        )

    # =====================================================
    # Debt-to-income ratio (DTI)
    # =====================================================

    dti = customer.get(
        "Debt_to_Income_Ratio"
    )

    if dti is not None and dti > 60:
        factors.append(
            f"Critical debt-to-income ratio ({dti:.1f}%): monthly repayment burden exceeds sustainable threshold"
        )
    elif dti is not None and dti > 40:
        factors.append(
            f"High debt-to-income ratio ({dti:.1f}%)"
        )

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
            f"Low credit score ({credit_score})"
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
            "Previous loan defaults on record"
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
            f"High credit utilization ({utilization:.1f}%)"
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
            "Multiple missed payments in credit history"
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
            "High payment delinquency (> 30 days past due)"
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

    return factors[:4]