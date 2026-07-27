import streamlit as st
import pandas as pd
from datetime import date

from scoring_model import *

st.set_page_config(
    page_title="CBZ Lifestyle Loan Scoring",
    layout="wide"
)
# Hide Streamlit menu/footer
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("CBZ Lifestyle Loan Scoring Dashboard")
st.image("assets/cbz_logo.png", width=200)

# Clear all inputs and results
if st.button("Clear"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.rerun()
# ====================================================
# CUSTOMER SECTION
# ====================================================

st.subheader("Customer Information")

col1, col2 = st.columns(2)

with col1:

    customer_name = st.text_input(
        "Customer Name",
        ""
    )
  
    dob = st.date_input(
        "Date of Birth",
        value=date(1900, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )
    net_salary = st.number_input(
        "Net Salary",
        value=0
    )

    loan_amount = st.number_input(
        "Loan Amount",
        value=0
    )

with col2:

    facility_type = st.selectbox(
        "Type of Facility",
        list(FACILITY_TYPES.keys())
    )

    facility_info = FACILITY_TYPES[facility_type]

    interest_rate = facility_info["interest_rate"]
    currency = facility_info["currency"]
    max_dsr = facility_info["max_dsr"]

    tenure = st.number_input(
        "Tenure (Months)",
        value=50
    )

repayment = calculate_repayment(
    loan_amount=loan_amount,
    annual_interest_rate=interest_rate,
    tenure_months=tenure)

st.metric(
    "Monthly Repayment",
    f"{currency} {repayment:,.2f}"
)

# ====================================================
# SCORECARD INPUTS
# ====================================================

st.subheader("Scorecard Inputs")

col1, col2 = st.columns(2)

with col1:

    marital_status = st.selectbox(
        "Marital Status",
        [""] + list(MARITAL_STATUS.keys())
    )

    residential_status = st.selectbox(
        "Residential Home Status",
        [""] + list(RESIDENTIAL_STATUS.keys())
    )

    address_period = st.selectbox(
        "Period at Current Address",
       [""] + list(ADDRESS_PERIOD.keys())
    )

    employment_status = st.selectbox(
        "Employment Status",
       [""] + list(EMPLOYMENT_STATUS.keys())
    )

    employer_tenure = st.selectbox(
        "Time with Current Employer",
       [""] + list(EMPLOYER_TENURE.keys())
    )

    repayment_arrangement = st.selectbox(
        "Repayment Arrangement",
       [""] + list(REPAYMENT_ARRANGEMENT.keys())
    )

    employer = st.selectbox(
        "Employer",
      [""] +  list(EMPLOYER.keys())
    )

with col2:

    banking_history = st.selectbox(
        "Banking History",
       [""] + list(BANKING_HISTORY.keys())
    )

    credit_history = st.selectbox(
        "Credit History",
       [""] + list(CREDIT_HISTORY.keys())
    )

    alternative_income = st.selectbox(
        "Alternative Income",
       [""] + list(ALTERNATIVE_INCOME.keys())
    )

    citizenship = st.selectbox(
        "Citizenship",
       [""] + list(CITIZENSHIP.keys())
    )

    security = st.selectbox(
        "Security",
      [""] +  list(SECURITY.keys())
    )
calculate_score = st.button(
    "Score Application",
    type="primary"
)

# ====================================================
# CALCULATIONS
# ====================================================

if calculate_score:

    required_fields = {
        "Customer Name": customer_name,
        "Marital Status": marital_status,
        "Residential Home Status": residential_status,
        "Period at Current Address": address_period,
        "Employment Status": employment_status,
        "Time with Current Employer": employer_tenure,
        "Repayment Arrangement": repayment_arrangement,
        "Employer": employer,
        "Banking History": banking_history,
        "Credit History": credit_history,
        "Alternative Income": alternative_income,
        "Citizenship": citizenship,
        "Security": security
    }

    missing_fields = [
        field
        for field, value in required_fields.items()
        if value in ["", None]
    ]

    if net_salary <= 0:
        missing_fields.append("Net Salary")

    if loan_amount <= 0:
        missing_fields.append("Loan Amount")

    if tenure <= 0:
        missing_fields.append("Tenure")

    if missing_fields:
        st.error(
            "Please complete the following mandatory fields:\n\n- "
            + "\n- ".join(missing_fields)
        )
        st.stop()

    age = (
        date.today() - dob
    ).days / 365.25

    repayment_ratio = (
        repayment / net_salary
    ) * 100 if net_salary > 0 else 0

    scores = {

        "Age": age_score(age),

        "Marital Status":
            MARITAL_STATUS.get(marital_status, 0),

        "Residential Home Status":
            RESIDENTIAL_STATUS.get(residential_status, 0),

        "Period at Current Address":
            ADDRESS_PERIOD.get(address_period, 0),

        "Employment Status":
            EMPLOYMENT_STATUS.get(employment_status, 0),

        "Time with Current Employer":
            EMPLOYER_TENURE.get(employer_tenure, 0),

        "Repayment Arrangement":
            REPAYMENT_ARRANGEMENT.get(repayment_arrangement, 0),

        "Employer":
            EMPLOYER.get(employer, 0),

        "Banking History":
            BANKING_HISTORY.get(banking_history, 0),

        "Credit History":
            CREDIT_HISTORY.get(credit_history, 0),

        "Repayment Ratio":
            repayment_ratio_score(repayment_ratio),

        "Alternative Income":
            ALTERNATIVE_INCOME.get(alternative_income, 0),

        "Citizenship":
            CITIZENSHIP.get(citizenship, 0),

        "Security":
            SECURITY.get(security, 0)
    }

    # =========================================
    # TOTAL WEIGHTED SCORE
    # =========================================

    weighted_score = 0

    weighted_score += weighted_factor(scores["Age"], 5, 1)
    weighted_score += weighted_factor(scores["Marital Status"], 1, 1)
    weighted_score += weighted_factor(scores["Residential Home Status"], 5, 3)
    weighted_score += weighted_factor(scores["Period at Current Address"], 5, 2)
    weighted_score += weighted_factor(scores["Employment Status"], 5, 11)
    weighted_score += weighted_factor(scores["Time with Current Employer"], 5, 10)
    weighted_score += weighted_factor(scores["Repayment Arrangement"], 3, 5)
    weighted_score += weighted_factor(scores["Employer"], 5, 1)
    weighted_score += weighted_factor(scores["Banking History"], 5, 15)
    weighted_score += weighted_factor(scores["Credit History"], 5, 15)
    weighted_score += weighted_factor(scores["Repayment Ratio"], 5, 16)
    weighted_score += weighted_factor(scores["Alternative Income"], 4, 11)
    weighted_score += weighted_factor(scores["Citizenship"], 1, 1)
    weighted_score += weighted_factor(scores["Security"], 2, 8)

    # =========================================
    # DSR PENALTY (EXCEL LOGIC)
    # =========================================

    max_dsr = FACILITY_TYPES[facility_type]["max_dsr"]

    dsr_difference = max_dsr - repayment_ratio

    if dsr_difference <= 0:
        weighted_score -= 0.4

    weighted_score = round(weighted_score, 2)

    # =========================================
    # GRADE & DECISION
    # =========================================

    grade = credit_grade(weighted_score)
    loan_decision = decision(weighted_score)

    # =========================================
    # RESULTS
    # =========================================

    st.subheader("Loan Score Results")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Weighted Score",
        f"{weighted_score:.2f}%"
    )

    c2.metric(
        "Grade",
        grade
    )

    c3.metric(
        "Decision",
        loan_decision
    )

    # =========================================
    # SCORE BREAKDOWN
    # =========================================

    summary = pd.DataFrame({
        "Category": scores.keys(),
        "Raw Score": scores.values(),
        "Maximum Score": [
            {"Age":5,"Marital Status":1,"Residential Home Status":5,
             "Period at Current Address":5,"Employment Status":5,
             "Time with Current Employer":5,"Repayment Arrangement":3,
             "Employer":5,"Banking History":5,"Credit History":5,
             "Repayment Ratio":5,"Alternative Income":4,
             "Citizenship":1,"Security":2}[category]
            for category in scores.keys()
        ],
        "Weight (%)": [
            WEIGHTS[category]
            for category in scores.keys()
        ],
        "Weighted Score": [
            (scores[category] /
             {"Age":5,"Marital Status":1,"Residential Home Status":5,
              "Period at Current Address":5,"Employment Status":5,
              "Time with Current Employer":5,"Repayment Arrangement":3,
              "Employer":5,"Banking History":5,"Credit History":5,
              "Repayment Ratio":5,"Alternative Income":4,
              "Citizenship":1,"Security":2}[category]
            ) * WEIGHTS[category]
            for category in scores.keys()
        ]
    })

    st.subheader("Score Breakdown")

    st.dataframe(
        summary,
        use_container_width=True
    )

    # =========================================
    # RISK INDICATOR
    # =========================================

    if weighted_score >= 70:
        st.success("🟢 LOW RISK")

    elif weighted_score >= 55:
        st.warning("🟠 MEDIUM RISK")

    else:
        st.error("🔴 HIGH RISK")

    st.write(f"Age: {age:.2f}")
    st.write(f"Repayment Ratio: {repayment_ratio:.2f}%")
