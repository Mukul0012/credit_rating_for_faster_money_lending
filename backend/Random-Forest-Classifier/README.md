# Credit Risk Assessment – Machine Learning

## Overview

This repository contains the Machine Learning component of a Credit Risk Assessment system developed for faster lending decisions.

The system uses customer financial information, employment details, loan information, credit history, and repayment behavior to train a machine learning model that predicts the likely loan decision.

The ML pipeline also generates an approval probability that is used by the risk assessment layer to produce:

- Approval probability
- Risk score
- Risk level
- Approve / Review / Reject recommendation
- Key customer-level risk indicators

The trained model and preprocessing artifacts are designed to be consumed by the backend/API component of the overall lending application.

---

# Problem Statement

Traditional lending processes require the assessment of several customer attributes before a loan decision can be made.

These include:

- Income
- Existing debt
- Loan amount
- Credit score
- Credit utilization
- Previous defaults
- Missed payments
- Payment history
- Credit history
- Employment information

Manually evaluating these attributes can increase processing time and make it difficult to scale the lending process.

The objective of this project is to build a machine learning based credit risk assessment component that can perform an initial assessment of a loan application and provide a faster, consistent, and data-driven recommendation.

---

# Objectives

The main objectives of the ML component are:

1. Analyze historical customer and loan data.
2. Clean and preprocess the dataset.
3. Select appropriate features for credit risk prediction.
4. Encode categorical variables.
5. Train a classification model.
6. Evaluate the model using multiple classification metrics.
7. Compare the baseline model with a tuned model.
8. Analyze different prediction thresholds.
9. Generate approval probabilities for new customers.
10. Convert the probability into a simple risk score.
11. Classify applications into Low, Medium, and High risk.
12. Identify important customer-level risk indicators.
13. Provide reusable Python functions for backend integration.

---

# Dataset

The model is trained using a dataset containing customer, employment, loan, financial, and credit-related information.

### Dataset Size

```text
Rows:    30,000
Columns: 27