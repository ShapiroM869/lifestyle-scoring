from datetime import date

# ============================================
# WEIGHTS
# ============================================
FACILITY_TYPES = {

    "Lifestyle Plus Loan (Salary + Other Income)": {
        "interest_rate": 20,
        "currency": "USD",
        "max_dsr": 40
    },

    "Lifestyle Wealth Loan (Non-Salaried)": {
        "interest_rate": 22,
        "currency": "USD",
        "max_dsr": 0.4
    },

    "Lifestyle Asset-Backed Loan": {
        "interest_rate": 25,
        "currency": "USD",
        "max_dsr": 40
    }
}

WEIGHTS = {
    "Age": 0.01,
    "Marital Status": 0.01,
    "Residential Home Status": 0.03,
    "Period at Current Address": 0.02,
    "Employment Status": 0.11,
    "Time with Current Employer": 0.10,
    "Repayment Arrangement": 0.05,
    "Employer": 0.01,
    "Banking History": 0.15,
    "Credit History": 0.15,
    "Repayment Ratio": 0.16,
    "Alternative Income": 0.11,
    "Citizenship": 0.01,
    "Security": 0.08
}

# ============================================
# LOOKUP TABLES
# ============================================

MARITAL_STATUS = {
    "Single": 0,
    "Married": 1,
    "Separated": 0,
    "Divorced": 0,
    "Widow/er": 0
}

RESIDENTIAL_STATUS = {
    "Rented property": 2,
    "Provided by employer": 3,
    "Owned with a mortgage": 4,
    "Owned without mortgage": 5,
    "Staying with parents/relative": 0
}

ADDRESS_PERIOD = {
    "Less than 3 months": 1,
    "3 months to 6 months": 2,
    "6 months to 12 months": 3,
    "12 months to 24 months": 4,
    "More than 24 months": 5
}

EMPLOYMENT_STATUS = {
    "Fixed term contract aligned to tenor facility": 4,
    "Business owner": 5,
    "Permanently employed": 5,
    "Retired": 3,
    "Unemployed": 1,
    "Self-employed": 2
}

EMPLOYER_TENURE = {
    "Less than 3 months": 0,
    "3 months to 6 months": 1,
    "6 months to 12 months": 2,
    "12 months to 18 months": 3,
    "18 months to 24 months": 4,
    "More than 24 months": 5,
    "Not applicable": 0
}

REPAYMENT_ARRANGEMENT = {
    "Direct deduction from employer or Pension": 3,
    "Clients account supported by Dividend Income, Investment Portfolio Earnings and Directors Fees": 1,
    "Clients account supported by Rental Income or Foreign Currency Income": 2,
    "Executive Bonus": 0
}

EMPLOYER = {
    "Government, Blue Chip Corporate, Top tier Bank, Listed company": 5,
    "Established Corporate": 2,
    "Not on Bank Recommended List": 1
}

BANKING_HISTORY = {
    "Less than 3 months": 0,
    "3 months to 6 months": 1,
    "6 months to 12 months": 2,
    "12 months to 18 months": 3,
    "18 months to 24 months": 4,
    "More than 24 months": 5
}

CREDIT_HISTORY = {
    "Clean History": 5,
    "No History": 4,
    "Politically Exposed Person": 3,
    "Prior items due to proven unintentional circumstances": 2,
    "Prior adverse item/s": 1,
    "Defaulter": 0
}

ALTERNATIVE_INCOME = {
    "Salary income plus 4+ diversified, documented, and traceable income sources, income paid through formal CBZ banking channels and ring-fenced structures ": 4,
    "Salary income plus 3+ documented income sources": 3,
    "Non Salaried two or more income sources": 2,
    "2 or more income sources with limited evidence": 1,
    "No income": 0
}

CITIZENSHIP = {
    "Zimbabwean Citizen": 1,
    "Permanent Resident": 1,
    "Foreign National": 0
}

SECURITY = {
    "No Security": 0,
    "Vehicle Security (50% of loan value)": 1,
    "Business Asset Security (70% of loan value)": 2
}

# ============================================
# AGE SCORE
# ============================================

def age_score(age):

    if age < 18:
        return 0
    elif age < 28:
        return 2
    elif age < 38:
        return 3
    elif age < 48:
        return 4
    elif age < 55:
        return 5
    elif age < 65:
        return 4
    else:
        return 1


# ============================================
# REPAYMENT RATIO SCORE
# ============================================

def repayment_ratio_score(ratio):

    if ratio <= 10:
        return 5
    elif ratio <= 20:
        return 4
    elif ratio <= 30:
        return 3
    elif ratio <= 40:
        return 2
    elif ratio <= 100:
        return 1
    else:
        return 0


# ============================================
# WEIGHTED FACTOR
# ============================================

def weighted_factor(score, max_score, weight):
    return (score / max_score) * weight


# ============================================
# GRADE
# ============================================

def credit_grade(score):

    if score < 28:
        return "D"
    elif score < 32:
        return "CD-"
    elif score < 36:
        return "CD"
    elif score < 40:
        return "CD+"
    elif score < 44:
        return "C-"
    elif score < 48:
        return "C"
    elif score < 52:
        return "C+"
    elif score < 56:
        return "BC-"
    elif score < 60:
        return "BC"
    elif score < 64:
        return "BC+"
    elif score < 68:
        return "B-"
    elif score < 72:
        return "B"
    elif score < 76:
        return "B+"
    elif score < 80:
        return "AB-"
    elif score < 84:
        return "AB"
    elif score < 88:
        return "AB+"
    elif score < 92:
        return "A-"
    elif score < 96:
        return "A"
    else:
        return "A+"


# ============================================
# DECISION
# ============================================

def decision(score):

    if score >= 70:
        return "APPROVE"
    elif score >= 55:
        return "REFER"
    else:
        return "DECLINE"
    
    
def calculate_repayment(
    loan_amount,
    annual_interest_rate,
    tenure_months
):
    """
    Excel PMT equivalent
    """

    monthly_rate = annual_interest_rate / 100 / 12

    if monthly_rate == 0:
        return loan_amount / tenure_months

    repayment = (
        loan_amount
        * monthly_rate
        * (1 + monthly_rate) ** tenure_months
    ) / (
        (1 + monthly_rate) ** tenure_months - 1
    )

    return round(repayment, 2)
