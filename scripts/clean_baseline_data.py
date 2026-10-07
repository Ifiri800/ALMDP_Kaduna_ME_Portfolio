from pathlib import Path
import pandas as pd


# ============================================================
# ALMDP Kaduna M&E Portfolio
# Stage 07: Baseline Data Cleaning
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_ROOT / "05_Raw_Data" / "baseline_raw.csv"
CLEAN_FILE = PROJECT_ROOT / "07_Clean_Data" / "baseline_clean.csv"
CLEANING_LOG_FILE = PROJECT_ROOT / "06_Data_Quality" / "Cleaning_Log.csv"


# ------------------------------------------------------------
# Cleaning configuration
# ------------------------------------------------------------

ID_CORRECTIONS = {
    ("ALMDP-0001", 1): "ALMDP-1996",
    ("ALMDP-0101", 1): "ALMDP-1997",
    ("ALMDP-0501", 1): "ALMDP-1998",
    ("ALMDP-1001", 1): "ALMDP-1999",
    ("ALMDP-1501", 1): "ALMDP-2000",
}


# ------------------------------------------------------------
# Helper function
# ------------------------------------------------------------

cleaning_log = []


def log_cleaning_action(
    record_id,
    variable,
    original_value,
    cleaned_value,
    action,
    reason,
    status="Resolved",
):
    cleaning_log.append(
        {
            "record_id": record_id,
            "variable": variable,
            "original_value": original_value,
            "cleaned_value": cleaned_value,
            "action": action,
            "reason": reason,
            "status": status,
        }
    )


# ------------------------------------------------------------
# Load raw data
# ------------------------------------------------------------

if not RAW_FILE.exists():
    raise FileNotFoundError(f"Raw dataset not found: {RAW_FILE}")

df = pd.read_csv(RAW_FILE)

original_shape = df.shape


# ------------------------------------------------------------
# 1. Resolve respondent ID collisions
# ------------------------------------------------------------

for (original_id, occurrence), new_id in ID_CORRECTIONS.items():

    matching_indices = df.index[df["respondent_id"] == original_id].tolist()

    if len(matching_indices) != 2:
        raise ValueError(
            f"Expected exactly 2 records for {original_id}, "
            f"found {len(matching_indices)}."
        )

    target_index = matching_indices[occurrence]

    old_value = df.at[target_index, "respondent_id"]

    df.at[target_index, "respondent_id"] = new_id

    log_cleaning_action(
        record_id=new_id,
        variable="respondent_id",
        original_value=old_value,
        cleaned_value=new_id,
        action="Corrected ID collision",
        reason=(
            "The original respondent ID occurred twice, but the paired "
            "records contained materially different respondent information. "
            "The later record was treated as a separate synthetic respondent "
            "and assigned its unique sequential ID."
        ),
    )


# ------------------------------------------------------------
# 2. Invalid age
# ------------------------------------------------------------

invalid_age = df["age"].notna() & (
    (df["age"] < 18) | (df["age"] > 100)
)

for idx in df.index[invalid_age]:

    record_id = df.at[idx, "respondent_id"]
    old_value = df.at[idx, "age"]

    df.at[idx, "age"] = pd.NA

    log_cleaning_action(
        record_id=record_id,
        variable="age",
        original_value=old_value,
        cleaned_value=pd.NA,
        action="Set invalid value to missing",
        reason="Age was outside the permitted respondent range of 18-100 years.",
    )


# ------------------------------------------------------------
# 3. Negative farm area
# ------------------------------------------------------------

invalid_farm_area = (
    (df["beneficiary_type"] == 1)
    & df["farm_area_ha"].notna()
    & (df["farm_area_ha"] <= 0)
)

for idx in df.index[invalid_farm_area]:

    record_id = df.at[idx, "respondent_id"]
    old_value = df.at[idx, "farm_area_ha"]

    df.at[idx, "farm_area_ha"] = pd.NA

    log_cleaning_action(
        record_id=record_id,
        variable="farm_area_ha",
        original_value=old_value,
        cleaned_value=pd.NA,
        action="Set invalid value to missing",
        reason="Farm area was zero or negative and could not be considered valid.",
    )


# ------------------------------------------------------------
# 4. Quantity sold greater than quantity harvested
# ------------------------------------------------------------

invalid_sold = (
    df["quantity_sold_t"].notna()
    & df["quantity_harvested_t"].notna()
    & (df["quantity_sold_t"] > df["quantity_harvested_t"])
)

for idx in df.index[invalid_sold]:

    record_id = df.at[idx, "respondent_id"]
    old_value = df.at[idx, "quantity_sold_t"]

    df.at[idx, "quantity_sold_t"] = pd.NA

    log_cleaning_action(
        record_id=record_id,
        variable="quantity_sold_t",
        original_value=old_value,
        cleaned_value=pd.NA,
        action="Set inconsistent value to missing",
        reason=(
            "Quantity sold exceeded quantity harvested. "
            "No replacement value was available from the raw dataset."
        ),
    )


# ------------------------------------------------------------
# 5. Quantity lost greater than quantity harvested
# ------------------------------------------------------------

invalid_lost = (
    df["quantity_lost_t"].notna()
    & df["quantity_harvested_t"].notna()
    & (df["quantity_lost_t"] > df["quantity_harvested_t"])
)

for idx in df.index[invalid_lost]:

    record_id = df.at[idx, "respondent_id"]
    old_value = df.at[idx, "quantity_lost_t"]

    df.at[idx, "quantity_lost_t"] = pd.NA

    log_cleaning_action(
        record_id=record_id,
        variable="quantity_lost_t",
        original_value=old_value,
        cleaned_value=pd.NA,
        action="Set inconsistent value to missing",
        reason=(
            "Quantity lost exceeded quantity harvested. "
            "No replacement value was available from the raw dataset."
        ),
    )


# ------------------------------------------------------------
# 6. Invalid knowledge response
# ------------------------------------------------------------

knowledge_columns = [
    f"knowledge_q{i}_response"
    for i in range(1, 11)
]

for column in knowledge_columns:

    if column not in df.columns:
        continue

    invalid_knowledge = (
        df[column].notna()
        & ~df[column].isin([1, 2, 3, 4])
    )

    for idx in df.index[invalid_knowledge]:

        record_id = df.at[idx, "respondent_id"]
        old_value = df.at[idx, column]

        df.at[idx, column] = pd.NA

        log_cleaning_action(
            record_id=record_id,
            variable=column,
            original_value=old_value,
            cleaned_value=pd.NA,
            action="Set invalid response to missing",
            reason="Knowledge response must be coded 1-4.",
        )


# ------------------------------------------------------------
# 7. Recalculate knowledge binary scores
# ------------------------------------------------------------

answer_key = {
    "knowledge_q1_response": 1,
    "knowledge_q2_response": 2,
    "knowledge_q3_response": 3,
    "knowledge_q4_response": 3,
    "knowledge_q5_response": 1,
    "knowledge_q6_response": 3,
    "knowledge_q7_response": 2,
    "knowledge_q8_response": 1,
    "knowledge_q9_response": 2,
    "knowledge_q10_response": 3,
}

knowledge_score_columns = []

for response_column, correct_answer in answer_key.items():

    score_column = response_column.replace("_response", "")
    knowledge_score_columns.append(score_column)

    df[score_column] = pd.NA

    valid = df[response_column].isin([1, 2, 3, 4])

    df.loc[valid, score_column] = (
        df.loc[valid, response_column] == correct_answer
    ).astype(int)


# ------------------------------------------------------------
# 8. Recalculate knowledge score
# ------------------------------------------------------------

df["knowledge_score"] = df[knowledge_score_columns].sum(
    axis=1,
    min_count=len(knowledge_score_columns),
)

df["adequate_knowledge"] = pd.NA

valid_knowledge_score = df["knowledge_score"].notna()

df.loc[valid_knowledge_score, "adequate_knowledge"] = (
    df.loc[valid_knowledge_score, "knowledge_score"] >= 6
).astype(int)


# ------------------------------------------------------------
# 9. Recalculate agricultural derived variables
# ------------------------------------------------------------

practice_columns = [
    "improved_seed",
    "soil_testing",
    "fertilizer_management",
    "integrated_pest_management",
    "conservation_agriculture",
    "water_management",
    "improved_storage",
    "climate_smart_practice",
]

df["practices_adopted"] = df[practice_columns].sum(
    axis=1,
    min_count=len(practice_columns),
)

df["adoption_status"] = pd.NA

valid_practice_count = df["practices_adopted"].notna()

df.loc[valid_practice_count, "adoption_status"] = (
    df.loc[valid_practice_count, "practices_adopted"] >= 3
).astype(int)


# ------------------------------------------------------------
# 10. Recalculate productivity
# ------------------------------------------------------------

df["productivity_t_per_ha"] = pd.NA

valid_productivity = (
    df["area_cultivated_ha"].notna()
    & df["quantity_harvested_t"].notna()
    & (df["area_cultivated_ha"] > 0)
)

df.loc[valid_productivity, "productivity_t_per_ha"] = (
    df.loc[valid_productivity, "quantity_harvested_t"]
    / df.loc[valid_productivity, "area_cultivated_ha"]
).round(3)


# ------------------------------------------------------------
# 11. Recalculate total post-harvest loss
# ------------------------------------------------------------

loss_columns = [
    "loss_damaged_t",
    "loss_storage_t",
    "loss_transport_t",
    "loss_processing_t",
    "loss_other_t",
]

df["total_postharvest_loss_t"] = df[loss_columns].sum(
    axis=1,
    min_count=len(loss_columns),
)

df["postharvest_loss_rate"] = pd.NA

valid_loss_rate = (
    df["total_postharvest_loss_t"].notna()
    & df["quantity_harvested_t"].notna()
    & (df["quantity_harvested_t"] > 0)
)

df.loc[valid_loss_rate, "postharvest_loss_rate"] = (
    df.loc[valid_loss_rate, "total_postharvest_loss_t"]
    / df.loc[valid_loss_rate, "quantity_harvested_t"]
    * 100
).round(3)


# ------------------------------------------------------------
# 12. Recalculate total annual income
# ------------------------------------------------------------

income_columns = [
    "crop_income_ngn",
    "livestock_income_ngn",
    "processing_income_ngn",
    "other_agricultural_income_ngn",
    "business_income_ngn",
    "employment_income_ngn",
    "other_income_ngn",
]

df["total_annual_income_ngn"] = df[income_columns].sum(
    axis=1,
    min_count=len(income_columns),
)


# ------------------------------------------------------------
# 13. Recalculate MSME profit
# ------------------------------------------------------------

if {
    "annual_sales_ngn",
    "annual_operating_cost_ngn",
}.issubset(df.columns):

    valid_profit = (
        df["annual_sales_ngn"].notna()
        & df["annual_operating_cost_ngn"].notna()
    )

    df["annual_profit_ngn"] = pd.NA

    df.loc[valid_profit, "annual_profit_ngn"] = (
        df.loc[valid_profit, "annual_sales_ngn"]
        - df.loc[valid_profit, "annual_operating_cost_ngn"]
    )


# ------------------------------------------------------------
# 14. Recalculate financial management status
# ------------------------------------------------------------

financial_columns = [
    "sales_records",
    "expense_records",
    "inventory_records",
    "cashflow_records",
    "profit_loss_records",
]

df["financial_record_count"] = df[financial_columns].sum(
    axis=1,
    min_count=len(financial_columns),
)

df["financial_management_status"] = pd.NA

valid_financial_count = df["financial_record_count"].notna()

df.loc[valid_financial_count, "financial_management_status"] = (
    df.loc[valid_financial_count, "financial_record_count"] >= 3
).astype(int)


# ------------------------------------------------------------
# 15. Recalculate resilience
# ------------------------------------------------------------

resilience_columns = [
    "resilience_crop_failure",
    "resilience_price_shock",
    "resilience_input_price",
    "resilience_health_shock",
    "resilience_climate_shock",
    "resilience_income_loss",
]

valid_resilience = df[resilience_columns].notna().all(axis=1)

reverse_sum = (
    5 - df[resilience_columns]
).sum(axis=1, min_count=len(resilience_columns))

df["resilience_score"] = pd.NA

df.loc[valid_resilience, "resilience_score"] = (
    (reverse_sum[valid_resilience] - 6) / 18 * 100
).round(2)

df["resilience_status"] = pd.NA

valid_resilience_score = df["resilience_score"].notna()

df.loc[valid_resilience_score, "resilience_status"] = (
    df.loc[valid_resilience_score, "resilience_score"] >= 60
).astype(int)


# ------------------------------------------------------------
# 16. Preserve extreme values for review
# ------------------------------------------------------------

extreme_review_rules = [
    ("farm_area_ha", 50),
    ("quantity_harvested_t", 100),
    ("annual_sales_ngn", 20_000_000),
    ("total_annual_income_ngn", 10_000_000),
]

for variable, threshold in extreme_review_rules:

    if variable not in df.columns:
        continue

    extreme = df[variable].notna() & (df[variable] > threshold)

    for idx in df.index[extreme]:

        record_id = df.at[idx, "respondent_id"]
        value = df.at[idx, variable]

        log_cleaning_action(
            record_id=record_id,
            variable=variable,
            original_value=value,
            cleaned_value=value,
            action="Retained for review",
            reason=(
                f"Value exceeded the DQA review threshold of {threshold}. "
                "The observation was retained because an extreme value "
                "cannot be classified as erroneous without source evidence."
            ),
            status="Review",
        )


# ------------------------------------------------------------
# 17. Final ID uniqueness check
# ------------------------------------------------------------

duplicate_count = df["respondent_id"].duplicated().sum()

if duplicate_count != 0:
    raise ValueError(
        f"Cleaning failed: {duplicate_count} duplicate respondent IDs remain."
    )


# ------------------------------------------------------------
# 18. Save outputs
# ------------------------------------------------------------

CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
CLEANING_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(CLEAN_FILE, index=False)

cleaning_log_df = pd.DataFrame(cleaning_log)

cleaning_log_df.to_csv(
    CLEANING_LOG_FILE,
    index=False,
)


# ------------------------------------------------------------
# 19. Verification summary
# ------------------------------------------------------------

print("=" * 60)
print("ALMDP BASELINE DATA CLEANING")
print("=" * 60)

print(f"Raw dataset shape:   {original_shape}")
print(f"Clean dataset shape: {df.shape}")
print()
print(f"Cleaning actions: {len(cleaning_log_df)}")
print(
    f"ID duplicates remaining: "
    f"{df['respondent_id'].duplicated().sum()}"
)
print()
print(f"Clean dataset: {CLEAN_FILE}")
print(f"Cleaning log:  {CLEANING_LOG_FILE}")
print("=" * 60)