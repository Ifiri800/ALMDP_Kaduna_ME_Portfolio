from pathlib import Path
import pandas as pd


# ============================================================
# ALMDP Kaduna M&E Portfolio
# Automated Baseline Data Quality Assessment
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_FILE = BASE_DIR / "05_Raw_Data" / "baseline_raw.csv"
DQA_DIR = BASE_DIR / "06_Data_Quality"

OUTPUT_LOG = DQA_DIR / "Validation_Log.csv"
OUTPUT_SUMMARY = DQA_DIR / "Validation_Summary.csv"


# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------

df = pd.read_csv(RAW_FILE)

issues = []


def add_issue(
    issue_id,
    respondent_id,
    variable,
    rule,
    issue,
    observed_value,
    severity,
    recommended_action,
):
    issues.append(
        {
            "issue_id": issue_id,
            "respondent_id": respondent_id,
            "variable": variable,
            "rule": rule,
            "issue": issue,
            "observed_value": observed_value,
            "severity": severity,
            "recommended_action": recommended_action,
            "status": "Open",
        }
    )


issue_counter = 1


def record_issue(
    respondent_id,
    variable,
    rule,
    issue,
    observed_value,
    severity="High",
    recommended_action="Investigate and correct during cleaning",
):
    global issue_counter

    add_issue(
        f"DQA-{issue_counter:04d}",
        respondent_id,
        variable,
        rule,
        issue,
        observed_value,
        severity,
        recommended_action,
    )

    issue_counter += 1


# ------------------------------------------------------------
# 1. Duplicate respondent IDs
# ------------------------------------------------------------

duplicate_mask = df["respondent_id"].duplicated(keep=False)

for _, row in df.loc[duplicate_mask].iterrows():
    record_issue(
        respondent_id=row["respondent_id"],
        variable="respondent_id",
        rule="Unique respondent ID",
        issue="Duplicate respondent ID detected",
        observed_value=row["respondent_id"],
        severity="High",
        recommended_action="Investigate duplicate records and retain only the valid record after reconciliation",
    )


# ------------------------------------------------------------
# 2. Required identifiers
# ------------------------------------------------------------

required_fields = [
    "respondent_id",
    "survey_date",
    "enumerator_id",
    "supervisor_id",
    "state",
    "lga",
    "community",
    "beneficiary_type",
    "consent",
]

for field in required_fields:
    missing_mask = df[field].isna() | (df[field].astype(str).str.strip() == "")

    for _, row in df.loc[missing_mask].iterrows():
        record_issue(
            respondent_id=row.get("respondent_id", "MISSING"),
            variable=field,
            rule="Required field completeness",
            issue="Required field is missing",
            observed_value="Missing",
            severity="High",
            recommended_action="Verify source questionnaire and correct the missing value",
        )


# ------------------------------------------------------------
# 3. Consent
# ------------------------------------------------------------

invalid_consent = ~df["consent"].isin([0, 1])

for _, row in df.loc[invalid_consent].iterrows():
    record_issue(
        respondent_id=row["respondent_id"],
        variable="consent",
        rule="Consent must be coded 0 or 1",
        issue="Invalid consent code",
        observed_value=row["consent"],
        severity="Critical",
        recommended_action="Verify consent record before using the respondent's data",
    )


# ------------------------------------------------------------
# 4. State
# ------------------------------------------------------------

invalid_state = df["state"] != "KD"

for _, row in df.loc[invalid_state].iterrows():
    record_issue(
        respondent_id=row["respondent_id"],
        variable="state",
        rule="State must be Kaduna",
        issue="Invalid state code",
        observed_value=row["state"],
        severity="High",
        recommended_action="Verify respondent location against source questionnaire",
    )


# ------------------------------------------------------------
# 5. LGA
# ------------------------------------------------------------

approved_lgas = {
    "KDN",
    "KDS",
    "CHK",
    "IGB",
    "KAJ",
    "KAC",
    "ZAR",
}

invalid_lga = ~df["lga"].isin(approved_lgas)

for _, row in df.loc[invalid_lga].iterrows():
    record_issue(
        respondent_id=row["respondent_id"],
        variable="lga",
        rule="Approved project LGA",
        issue="Invalid LGA code",
        observed_value=row["lga"],
        severity="High",
        recommended_action="Verify LGA assignment",
    )


# ------------------------------------------------------------
# 6. Age
# ------------------------------------------------------------

invalid_age = (df["age"] < 18) | (df["age"] > 100)

for _, row in df.loc[invalid_age].iterrows():
    record_issue(
        respondent_id=row["respondent_id"],
        variable="age",
        rule="Age must be between 18 and 100",
        issue="Age outside valid range",
        observed_value=row["age"],
        severity="High",
        recommended_action="Verify respondent age from source questionnaire",
    )


# ------------------------------------------------------------
# 7. Farm area
# ------------------------------------------------------------

farmer_mask = df["beneficiary_type"] == 1

invalid_farm_area = farmer_mask & (
    df["farm_area_ha"].isna() | (df["farm_area_ha"] <= 0)
)

for _, row in df.loc[invalid_farm_area].iterrows():
    record_issue(
        respondent_id=row["respondent_id"],
        variable="farm_area_ha",
        rule="Farmer farm area must be greater than zero",
        issue="Invalid or missing farmer farm area",
        observed_value=row["farm_area_ha"],
        severity="High",
        recommended_action="Verify farm area from source questionnaire",
    )


# ------------------------------------------------------------
# 8. Non-negative agricultural quantities
# ------------------------------------------------------------

quantity_fields = [
    "area_cultivated_ha",
    "quantity_harvested_t",
    "quantity_sold_t",
    "quantity_consumed_t",
    "quantity_lost_t",
]

for field in quantity_fields:
    invalid_quantity = farmer_mask & (
        df[field].notna() & (df[field] < 0)
    )

    for _, row in df.loc[invalid_quantity].iterrows():
        record_issue(
            respondent_id=row["respondent_id"],
            variable=field,
            rule="Agricultural quantities must not be negative",
            issue="Negative agricultural quantity detected",
            observed_value=row[field],
            severity="High",
            recommended_action="Verify source value and correct during cleaning",
        )


# ------------------------------------------------------------
# 9. Sold quantity cannot exceed harvested quantity
# ------------------------------------------------------------

invalid_sold = farmer_mask & (
    df["quantity_sold_t"] > df["quantity_harvested_t"]
)

for _, row in df.loc[invalid_sold].iterrows():
    record_issue(
        respondent_id=row["respondent_id"],
        variable="quantity_sold_t",
        rule="Quantity sold must be less than or equal to quantity harvested",
        issue="Quantity sold exceeds quantity harvested",
        observed_value=f"{row['quantity_sold_t']} > {row['quantity_harvested_t']}",
        severity="High",
        recommended_action="Reconcile production and sales quantities against source questionnaire",
    )


# ------------------------------------------------------------
# 10. Consumed quantity cannot exceed harvested quantity
# ------------------------------------------------------------

invalid_consumed = farmer_mask & (
    df["quantity_consumed_t"] > df["quantity_harvested_t"]
)

for _, row in df.loc[invalid_consumed].iterrows():
    record_issue(
        respondent_id=row["respondent_id"],
        variable="quantity_consumed_t",
        rule="Quantity consumed must be less than or equal to quantity harvested",
        issue="Quantity consumed exceeds quantity harvested",
        observed_value=f"{row['quantity_consumed_t']} > {row['quantity_harvested_t']}",
        severity="High",
        recommended_action="Reconcile production and consumption quantities",
    )


# ------------------------------------------------------------
# 11. Lost quantity cannot exceed harvested quantity
# ------------------------------------------------------------

invalid_lost = farmer_mask & (
    df["quantity_lost_t"] > df["quantity_harvested_t"]
)

for _, row in df.loc[invalid_lost].iterrows():
    record_issue(
        respondent_id=row["respondent_id"],
        variable="quantity_lost_t",
        rule="Quantity lost must be less than or equal to quantity harvested",
        issue="Quantity lost exceeds quantity harvested",
        observed_value=f"{row['quantity_lost_t']} > {row['quantity_harvested_t']}",
        severity="High",
        recommended_action="Reconcile production and loss quantities",
    )


# ------------------------------------------------------------
# 12. Knowledge response validation
# ------------------------------------------------------------

knowledge_response_fields = [
    f"knowledge_q{i}_response"
    for i in range(1, 11)
]

for field in knowledge_response_fields:
    invalid_response = (
        df[field].notna()
        & ~df[field].isin([1, 2, 3, 4])
    )

    for _, row in df.loc[invalid_response].iterrows():
        record_issue(
            respondent_id=row["respondent_id"],
            variable=field,
            rule="Knowledge response must be coded 1 to 4",
            issue="Knowledge response outside valid range",
            observed_value=row[field],
            severity="High",
            recommended_action="Verify questionnaire response and recalculate binary knowledge score",
        )


# ------------------------------------------------------------
# 13. Knowledge score validation
# ------------------------------------------------------------

invalid_knowledge_score = (
    df["knowledge_score"].notna()
    & (
        (df["knowledge_score"] < 0)
        | (df["knowledge_score"] > 10)
    )
)

for _, row in df.loc[invalid_knowledge_score].iterrows():
    record_issue(
        respondent_id=row["respondent_id"],
        variable="knowledge_score",
        rule="Knowledge score must be between 0 and 10",
        issue="Knowledge score outside valid range",
        observed_value=row["knowledge_score"],
        severity="High",
        recommended_action="Recalculate knowledge score from valid raw responses",
    )


# ------------------------------------------------------------
# 14. Resilience response validation
# ------------------------------------------------------------

resilience_fields = [
    "resilience_crop_failure",
    "resilience_price_shock",
    "resilience_input_price",
    "resilience_health_shock",
    "resilience_climate_shock",
    "resilience_income_loss",
]

for field in resilience_fields:
    invalid_resilience = (
        df[field].notna()
        & ~df[field].isin([1, 2, 3, 4])
    )

    for _, row in df.loc[invalid_resilience].iterrows():
        record_issue(
            respondent_id=row["respondent_id"],
            variable=field,
            rule="Resilience response must be coded 1 to 4",
            issue="Invalid resilience response",
            observed_value=row[field],
            severity="High",
            recommended_action="Verify questionnaire response",
        )


# ------------------------------------------------------------
# 15. Beneficiary-specific agricultural data
# ------------------------------------------------------------

msme_mask = df["beneficiary_type"] == 2

farmer_fields = [
    "primary_value_chain",
    "farm_area_ha",
    "area_cultivated_ha",
    "quantity_harvested_t",
    "quantity_sold_t",
    "quantity_consumed_t",
    "quantity_lost_t",
]

for field in farmer_fields:
    invalid_msme_values = msme_mask & df[field].notna()

    for _, row in df.loc[invalid_msme_values].iterrows():
        record_issue(
            respondent_id=row["respondent_id"],
            variable=field,
            rule="Farmer-specific fields must be blank for MSMEs",
            issue="Farmer-specific field populated for MSME respondent",
            observed_value=row[field],
            severity="Medium",
            recommended_action="Review skip pattern and clear value if not applicable",
        )


# ------------------------------------------------------------
# 16. MSME-specific data
# ------------------------------------------------------------

msme_fields = [
    "business_type",
    "years_in_operation",
    "number_of_employees",
    "annual_sales_ngn",
    "annual_operating_cost_ngn",
    "annual_profit_ngn",
    "sales_records",
    "expense_records",
    "inventory_records",
    "cashflow_records",
    "profit_loss_records",
    "business_bank_account",
]

for field in msme_fields:
    invalid_farmer_values = farmer_mask & df[field].notna()

    for _, row in df.loc[invalid_farmer_values].iterrows():
        record_issue(
            respondent_id=row["respondent_id"],
            variable=field,
            rule="MSME-specific fields must be blank for farmers",
            issue="MSME-specific field populated for farmer respondent",
            observed_value=row[field],
            severity="Medium",
            recommended_action="Review skip pattern and clear value if not applicable",
        )


# ------------------------------------------------------------
# 17. Negative income values
# ------------------------------------------------------------

income_fields = [
    "crop_income_ngn",
    "livestock_income_ngn",
    "processing_income_ngn",
    "other_agricultural_income_ngn",
    "business_income_ngn",
    "employment_income_ngn",
    "other_income_ngn",
    "total_annual_income_ngn",
]

for field in income_fields:
    invalid_income = df[field].notna() & (df[field] < 0)

    for _, row in df.loc[invalid_income].iterrows():
        record_issue(
            respondent_id=row["respondent_id"],
            variable=field,
            rule="Income values must not be negative",
            issue="Negative income value detected",
            observed_value=row[field],
            severity="High",
            recommended_action="Verify source value",
        )


# ------------------------------------------------------------
# 18. Productivity validation
# ------------------------------------------------------------

valid_productivity = (
    farmer_mask
    & df["productivity_t_per_ha"].notna()
    & df["area_cultivated_ha"].notna()
    & (df["area_cultivated_ha"] > 0)
    & df["quantity_harvested_t"].notna()
)

expected_productivity = (
    df.loc[valid_productivity, "quantity_harvested_t"]
    / df.loc[valid_productivity, "area_cultivated_ha"]
)

productivity_difference = (
    df.loc[valid_productivity, "productivity_t_per_ha"]
    - expected_productivity
).abs()

# Stored productivity is rounded to three decimal places.
# Allow a small rounding tolerance when reconciling the
# stored derived value with the source variables.
PRODUCTIVITY_TOLERANCE = 0.001

invalid_productivity = (
    productivity_difference > PRODUCTIVITY_TOLERANCE
)

invalid_productivity_indices = (
    df.index[valid_productivity][invalid_productivity]
)

for idx in invalid_productivity_indices:
    row = df.loc[idx]

    record_issue(
        respondent_id=row["respondent_id"],
        variable="productivity_t_per_ha",
        rule="Productivity must equal harvested quantity divided by cultivated area",
        issue="Derived productivity does not reconcile with source variables",
        observed_value=row["productivity_t_per_ha"],
        severity="Medium",
        recommended_action="Recalculate productivity after source-data validation",
    )


# ------------------------------------------------------------
# 19. Extreme-value flags
# ------------------------------------------------------------


# ------------------------------------------------------------
# 19. Extreme-value flags
# ------------------------------------------------------------

extreme_rules = {
    "farm_area_ha": 50,
    "quantity_harvested_t": 100,
    "annual_sales_ngn": 20_000_000,
    "total_annual_income_ngn": 10_000_000,
}

for field, threshold in extreme_rules.items():

    extreme = df[field].notna() & (df[field] > threshold)

    for _, row in df.loc[extreme].iterrows():
        record_issue(
            respondent_id=row["respondent_id"],
            variable=field,
            rule=f"Extreme-value review threshold: {threshold}",
            issue="Extreme value detected; value should be reviewed, not automatically deleted",
            observed_value=row[field],
            severity="Review",
            recommended_action="Review source evidence and retain if valid",
        )


# ------------------------------------------------------------
# Create DQA outputs
# ------------------------------------------------------------

validation_log = pd.DataFrame(issues)

if validation_log.empty:
    validation_log = pd.DataFrame(
        columns=[
            "issue_id",
            "respondent_id",
            "variable",
            "rule",
            "issue",
            "observed_value",
            "severity",
            "recommended_action",
            "status",
        ]
    )

validation_log.to_csv(OUTPUT_LOG, index=False)


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

summary_rows = [
    {
        "metric": "Total records",
        "value": len(df),
    },
    {
        "metric": "Total variables",
        "value": len(df.columns),
    },
    {
        "metric": "Duplicate respondent IDs",
        "value": df["respondent_id"].duplicated().sum(),
    },
    {
        "metric": "Total DQA issues",
        "value": len(validation_log),
    },
]

if not validation_log.empty:
    for severity in ["Critical", "High", "Medium", "Review"]:
        summary_rows.append(
            {
                "metric": f"Issues - {severity}",
                "value": (validation_log["severity"] == severity).sum(),
            }
        )

summary = pd.DataFrame(summary_rows)

summary.to_csv(OUTPUT_SUMMARY, index=False)


# ------------------------------------------------------------
# Console report
# ------------------------------------------------------------

print("=" * 60)
print("ALMDP KADUNA - BASELINE DATA QUALITY ASSESSMENT")
print("=" * 60)

print(f"Raw dataset: {RAW_FILE}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns):,}")
print(f"Duplicate respondent IDs: {df['respondent_id'].duplicated().sum()}")
print(f"Total DQA issues: {len(validation_log):,}")

if not validation_log.empty:
    print("\nIssues by severity:")
    print(
        validation_log["severity"]
        .value_counts()
        .reindex(
            ["Critical", "High", "Medium", "Review"],
            fill_value=0,
        )
        .to_string()
    )

    print("\nIssues by variable:")
    print(
        validation_log["variable"]
        .value_counts()
        .head(20)
        .to_string()
    )

print("\nOutput files:")
print(f"Validation log: {OUTPUT_LOG}")
print(f"Validation summary: {OUTPUT_SUMMARY}")

print("\nDQA validation completed.")