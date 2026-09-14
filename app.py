import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

from scoring_model import *
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

from datetime import date

APP_DIR = os.path.dirname(os.path.abspath(__file__))


# Pdf saving for audit(this better than auto cloaking beacuse of memory)

def build_application_pdf(status_text, fields):
    """
    Builds a single-page PDF for one scoring attempt.
    'fields' is an ordered list of (label, value) tuples.
    Returns a BytesIO buffer containing the PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("CBZ Lifestyle Loan Scoring — Application Record", styles["Title"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(status_text, styles["Heading2"]))
    story.append(Spacer(1, 12))

    for label, value in fields:
        story.append(Paragraph(f"<b>{label}:</b> {value}", styles["Normal"]))
        story.append(Spacer(1, 4))

    doc.build(story)
    buffer.seek(0)
    return buffer




# Commence1

st.set_page_config(
    page_title="CBZ Lifestyle Loan Scoring",
    layout="wide"
)

st.title("CBZ Lifestyle Loan Scoring Dashboard")
st.image(os.path.join(APP_DIR, "cbz_logo.png"), width=200)


# Clearing Logics, my reset button


if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

if st.button("Clear"):
    st.session_state.reset_counter += 1
    st.rerun()

suffix = st.session_state.reset_counter


# Client Information for credit


st.subheader("Customer Information")

col1, col2 = st.columns(2)

with col1:

    customer_name = st.text_input(
        "Customer Name",
        "",
        key=f"customer_name_{suffix}"
    )

    dob = st.date_input(
        "Date of Birth",
        value=date(1900, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date.today(),
        key=f"dob_{suffix}"
    )

    net_salary = st.number_input(
        "Net Salary",
        value=0,
        key=f"net_salary_{suffix}"
    )

    loan_amount = st.number_input(
        "Loan Amount",
        value=0,
        key=f"loan_amount_{suffix}"
    )

    existing_debt_repayments = st.number_input(
        "Existing Monthly Debt Repayments",
        value=0,
        key=f"existing_debt_repayments_{suffix}"
    )

    essential_living_expenses = st.number_input(
        "Essential Monthly Living Expenses",
        value=0,
        key=f"essential_living_expenses_{suffix}"
    )

    is_business_income = st.checkbox(
        "Applicant relies on business/self-employed income",
        key=f"is_business_income_{suffix}"
    )

    if is_business_income:
        avg_monthly_business_income = st.number_input(
            "Average Monthly Business Income (last 6 months)",
            value=0,
            key=f"avg_monthly_business_income_{suffix}"
        )

        lowest_monthly_business_income = st.number_input(
            "Lowest Monthly Business Income (last 6 months)",
            value=0,
            key=f"lowest_monthly_business_income_{suffix}"
        )

        business_tenure_years = st.number_input(
            "Years Business Has Been Operating",
            value=0,
            key=f"business_tenure_years_{suffix}"
        )
    else:
        avg_monthly_business_income = 0
        lowest_monthly_business_income = 0
        business_tenure_years = 0

with col2:

    facility_type = st.selectbox(
        "Type of Facility",
        list(FACILITY_TYPES.keys()),
        key=f"facility_type_{suffix}"
    )

    facility_info = FACILITY_TYPES[facility_type]

    interest_rate = facility_info["interest_rate"]
    currency = facility_info["currency"]
    max_dsr = facility_info["max_dsr"]

    tenure = st.number_input(
        "Tenure (Months)",
        value=50,
        key=f"tenure_{suffix}"
    )

    stress_haircut_percent = st.number_input(
        "Income Stress Test Haircut (%)",
        min_value=0,
        max_value=100,
        value=0,
        key=f"stress_haircut_percent_{suffix}"
    )

repayment = calculate_repayment(
    loan_amount=loan_amount,
    annual_interest_rate=interest_rate,
    tenure_months=tenure)

st.metric(
    "Monthly Repayment",
    f"{currency} {repayment:,.2f}"
)


# Scorecard input for For Credit


st.subheader("Scorecard Inputs")

col1, col2 = st.columns(2)

with col1:

    marital_status = st.selectbox(
        "Marital Status",
        [""] + list(MARITAL_STATUS.keys()),
        key=f"marital_status_{suffix}"
    )

    residential_status = st.selectbox(
        "Residential Home Status",
        [""] + list(RESIDENTIAL_STATUS.keys()),
        key=f"residential_status_{suffix}"
    )

    address_period = st.selectbox(
        "Period at Current Address",
        [""] + list(ADDRESS_PERIOD.keys()),
        key=f"address_period_{suffix}"
    )

    employment_status = st.selectbox(
        "Employment Status",
        [""] + list(EMPLOYMENT_STATUS.keys()),
        key=f"employment_status_{suffix}"
    )

    employer_tenure = st.selectbox(
        "Time with Current Employer",
        [""] + list(EMPLOYER_TENURE.keys()),
        key=f"employer_tenure_{suffix}"
    )

    repayment_arrangement = st.selectbox(
        "Repayment Arrangement",
        [""] + list(REPAYMENT_ARRANGEMENT.keys()),
        key=f"repayment_arrangement_{suffix}"
    )

    employer = st.selectbox(
        "Employer",
        [""] + list(EMPLOYER.keys()),
        key=f"employer_{suffix}"
    )

with col2:

    banking_history = st.selectbox(
        "Banking History",
        [""] + list(BANKING_HISTORY.keys()),
        key=f"banking_history_{suffix}"
    )

    credit_history = st.selectbox(
        "Credit History",
        [""] + list(CREDIT_HISTORY.keys()),
        key=f"credit_history_{suffix}"
    )

    alternative_income = st.selectbox(
        "Alternative Income",
        [""] + list(ALTERNATIVE_INCOME.keys()),
        key=f"alternative_income_{suffix}"
    )

    citizenship = st.selectbox(
        "Citizenship",
        [""] + list(CITIZENSHIP.keys()),
        key=f"citizenship_{suffix}"
    )

    security = st.selectbox(
        "Security",
        [""] + list(SECURITY.keys()),
        key=f"security_{suffix}"
    )

calculate_score = st.button(
    "Score Application",
    type="primary"
)


# My caluclation


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

    if existing_debt_repayments < 0:
        missing_fields.append("Existing Monthly Debt Repayments")

    if essential_living_expenses < 0:
        missing_fields.append("Essential Monthly Living Expenses")

    if is_business_income:
        if avg_monthly_business_income <= 0:
            missing_fields.append("Average Monthly Business Income")
        if lowest_monthly_business_income < 0:
            missing_fields.append("Lowest Monthly Business Income")
        if business_tenure_years <= 0:
            missing_fields.append("Years Business Has Been Operating")

    business_employment_statuses = ["Business owner", "Self-employed"]

    if is_business_income and employment_status not in business_employment_statuses:
        missing_fields.append(
            "Employment Status must be 'Business Owner' or 'Self Employed' "
            "when 'Applicant relies on business/self-employed income' is checked"
        )

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

    
    # Cut off, auto decline if debt service ratio (DSR) of client is more than 40% 


    if repayment_ratio > 40:
        st.subheader("Loan Score Results")

        st.error(
            f"🔴 APPLICATION DECLINED — "
            f"Debt Service Ratio ({repayment_ratio:.2f}%) exceeds the maximum allowed (40%)."
        )

        st.write(f"Age: {age:.2f}")
        st.write(f"Repayment Ratio: {repayment_ratio:.2f}%")

        st.stop()

    
    # Net disposable income (NDI) this is remaining oncome after all taxes and ddections
    

    total_dsr = (
        (existing_debt_repayments + repayment) / net_salary
    ) * 100 if net_salary > 0 else 0

    net_disposable_income = (
        net_salary
        - existing_debt_repayments
        - essential_living_expenses
        - repayment
    )

 
    # This is rare but just a tip for credit team, that if NDI ever goes below 0 then application should be declined
  

    if net_disposable_income <= 0:
        st.subheader("Loan Score Results")

        st.error(
            f"🔴 APPLICATION DECLINED — "
            f"Net Disposable Income ({currency} {net_disposable_income:,.2f}) is insufficient after "
            f"existing debt, living expenses, and this loan's repayment."
        )

        st.write(f"Age: {age:.2f}")
        st.write(f"Total DSR (all obligations): {total_dsr:.2f}%")
        st.write(f"Net Disposable Income: {currency} {net_disposable_income:,.2f}")

        st.stop()

    # Income stress testing was a suggestion from Credit team, this to be done by assuming reduction of ic=ncome by x%, and its
    # effect on net disposable income and debt service ratio (stressed)
   

    stress_haircut = stress_haircut_percent / 100

    stressed_net_salary = net_salary * (1 - stress_haircut)

    stressed_total_dsr = (
        (existing_debt_repayments + repayment) / stressed_net_salary
    ) * 100 if stressed_net_salary > 0 else 0

    stressed_ndi = (
        stressed_net_salary
        - existing_debt_repayments
        - essential_living_expenses
        - repayment
    )

    
    # CASH FLOW SUSTAINABILITY (BUSINESS INCOME) This was a suggestion by credit that not really in scoring engine but rather to take
    # insight of cashflow susatainibily and business inconme , this wont affect scoring rather to add flesh on decision choice
    

    if is_business_income:
        income_stability_ratio = (
            lowest_monthly_business_income / avg_monthly_business_income
        ) if avg_monthly_business_income > 0 else 0
    else:
        income_stability_ratio = None

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

    
    # My total weighted score calculation
    

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

    
    # This was disabled i replcaed this with hardcore 40% above as recommendation
    # max_dsr = FACILITY_TYPES[facility_type]["max_dsr"]
    # dsr_difference = max_dsr - repayment_ratio
    # if dsr_difference <= 0:
    #     weighted_score -= 0.4

    weighted_score = round(weighted_score, 2)

    
    # Decison and Grading
    

    grade = credit_grade(weighted_score)
    loan_decision = decision(weighted_score)

    
    # Results
    

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

    
    # Score breakdown (i left it visible however i can hide )
    

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

    
    # Credit Risk indicator, i added medium risk just to advice business
    

    if weighted_score >= 60:
        st.success("🟢 LOW RISK")

    elif weighted_score >= 55:
        st.warning("🟠 MEDIUM RISK")

    else:
        st.error("🔴 HIGH RISK")

    st.write(f"Age: {age:.2f}")
    st.write(f"Repayment Ratio: {repayment_ratio:.2f}%")
    st.write(f"Total DSR (all obligations): {total_dsr:.2f}%")
    st.write(f"Net Disposable Income: {currency} {net_disposable_income:,.2f}")

    
    # Income stress test results


    st.subheader(f"Income Stress Test ({stress_haircut_percent:.0f}% Income Reduction Scenario)")

    sc1, sc2 = st.columns(2)

    sc1.metric(
        "Stressed DSR",
        f"{stressed_total_dsr:.2f}%"
    )

    sc2.metric(
        "Stressed NDI",
        f"{currency} {stressed_ndi:,.2f}"
    )

    stress_test_flags = []

    if stressed_total_dsr > 40:
        stress_test_flags.append(
            f"Stressed DSR ({stressed_total_dsr:.2f}%) would exceed 40% "
            f"if net income dropped by {stress_haircut_percent:.0f}%."
        )

    if stressed_ndi <= 0:
        stress_test_flags.append(
            f"Stressed Net Disposable Income ({currency} {stressed_ndi:,.2f}) would be insufficient "
            f"if net income dropped by {stress_haircut_percent:.0f}%."
        )

    if stress_test_flags:
        st.warning(
            "⚠️ " + " ".join(stress_test_flags) +
            " Recommend manual review of income stability before approval."
        )
    else:
        st.success(
            f"✅ Applicant remains within acceptable DSR and disposable income "
            f"thresholds even under a {stress_haircut_percent:.0f}% income stress scenario."
        )

    
    # Contraints Rule (Assume those self employed and having business should only be subject to cashflow susataibility)
   

    if is_business_income:
        st.subheader("Cash Flow Sustainability (Business Income)")

        bc1, bc2 = st.columns(2)

        bc1.metric(
            "Income Stability Ratio",
            f"{income_stability_ratio*100:.0f}%"
        )

        bc2.metric(
            "Business Tenure",
            f"{business_tenure_years:.1f} yrs"
        )

        if income_stability_ratio < 0.5:
            st.warning(
                "⚠️ This applicant's business income shows high month-to-month volatility "
                f"(lowest month was only {income_stability_ratio*100:.0f}% of the average). "
                "Recommend manual review of cash flow sustainability."
            )
        elif business_tenure_years < 2:
            st.warning(
                "⚠️ This business has been operating for less than 2 years. "
                "Recommend manual review given limited operating history."
            )
        else:
            st.success(
                "✅ Business income shows reasonable stability and operating history."
            )

    # Audit and log off
  

    pdf_fields = [
        ("Customer Name", customer_name),
        ("Age", f"{age:.2f}"),
        ("Facility Type", facility_type),
        ("Loan Amount", f"{currency} {loan_amount:,.2f}"),
        ("Tenure", f"{tenure} months"),
        ("Monthly Repayment", f"{currency} {repayment:,.2f}"),
        ("Net Salary", f"{currency} {net_salary:,.2f}"),
        ("Repayment Ratio", f"{repayment_ratio:.2f}%"),
        ("Total DSR (all obligations)", f"{total_dsr:.2f}%"),
        ("Net Disposable Income", f"{currency} {net_disposable_income:,.2f}"),
        ("Stress Test Haircut Used", f"{stress_haircut_percent:.0f}%"),
        ("Stressed DSR", f"{stressed_total_dsr:.2f}%"),
        ("Stressed NDI", f"{currency} {stressed_ndi:,.2f}"),
        ("Weighted Score", f"{weighted_score:.2f}%"),
        ("Grade", grade),
        ("Decision", loan_decision),
    ]

    if is_business_income:
        pdf_fields.extend([
            ("Business Income Stability Ratio", f"{income_stability_ratio*100:.0f}%"),
            ("Business Tenure", f"{business_tenure_years:.1f} yrs"),
        ])

    pdf_buffer = build_application_pdf(
        f"Decision: {loan_decision} — Grade: {grade}",
        pdf_fields
    )

    st.download_button(
        "Save Application as PDF",
        data=pdf_buffer,
        file_name=f"{customer_name}_{date.today()}_{loan_decision}.pdf",
        mime="application/pdf"
    )
