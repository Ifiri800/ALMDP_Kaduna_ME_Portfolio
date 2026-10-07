from pathlib import Path
import random
from datetime import date, timedelta

import numpy as np
import pandas as pd


# ============================================================
# ALMDP KADUNA M&E PORTFOLIO
# Synthetic Baseline Dataset Generator
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "05_Raw_Data"
OUTPUT_FILE = OUTPUT_DIR / "baseline_raw.csv"

SEED = 20261006
N_RESPONDENTS = 2000

random.seed(SEED)
np.random.seed(SEED)


# ============================================================
# Project distributions
# ============================================================

LGAS = {
    "KDN": ("Kaduna North", 300),
    "KDS": ("Kaduna South", 300),
    "CHK": ("Chikun", 350),
    "IGB": ("Igabi", 300),
    "KAJ": ("Kajuru", 250),
    "KAC": ("Kachia", 250),
    "ZAR": ("Zaria", 250),
}

VALUE_CHAINS = {
    1: ("Maize", 400),
    2: ("Rice", 280),
    3: ("Soybean", 220),
    4: ("Ginger", 160),
    5: ("Tomato", 160),
    6: ("Vegetables", 160),
    7: ("Sorghum", 120),
    8: ("Groundnut", 100),
}

COMMUNITIES = {
    "KDN": ["Kawo", "Unguwan Dosa", "Badarawa"],
    "KDS": ["Tudun Wada", "Barnawa", "Kakuri"],
    "CHK": ["Kujama", "Sabon Tasha", "Kakuri-Kaduna"],
    "IGB": ["Rigachikun", "Turunku", "Afaka"],
    "KAJ": ["Kajuru", "Kufana", "Idon"],
    "KAC": ["Kachia", "Awon", "Gidan Tagwai"],
    "ZAR": ["Zaria City", "Wusasa", "Sabon Gari"],
}

FIRST_NAMES = [
    "Amina", "Fatima", "Hauwa", "Maryam", "Zainab",
    "Grace", "Esther", "Blessing", "Joy", "Patience",
    "Musa", "Abdullahi", "Ibrahim", "Sani", "Yusuf",
    "Usman", "Daniel", "Peter", "Samuel", "David",
]

LAST_NAMES = [
    "Abdullahi", "Musa", "Ibrahim", "Yusuf", "Sani",
    "Mohammed", "Bello", "Garba", "Aliyu", "Lawal",
    "James", "John", "Okoro", "Joseph", "Emeka",
]

ENUMERATORS = [f"ENUM-{i:02d}" for i in range(1, 21)]
SUPERVISORS = [f"SUP-{i:02d}" for i in range(1, 6)]


# ============================================================
# Helper functions
# ============================================================

def weighted_choice(values, probabilities=None):
    return random.choices(values, weights=probabilities, k=1)[0]


def yes_no(probability_yes=0.5):
    return 1 if random.random() < probability_yes else 0


def bounded_normal(mean, sd, lower=None, upper=None):
    value = np.random.normal(mean, sd)

    if lower is not None:
        value = max(lower, value)

    if upper is not None:
        value = min(upper, value)

    return value


def random_date():
    start = date(2026, 8, 1)
    end = date(2026, 9, 30)

    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


def choose_lga(index):
    cumulative = 0

    for code, (name, count) in LGAS.items():
        cumulative += count

        if index < cumulative:
            return code, name

    return "ZAR", "Zaria"


def choose_value_chain():
    values = []
    weights = []

    for code, (name, count) in VALUE_CHAINS.items():
        values.append(code)
        weights.append(count)

    return weighted_choice(values, weights)


def age_group(age):
    if age >= 18 and age <= 35:
        return 1
    if age >= 36 and age <= 59:
        return 2
    if age >= 60:
        return 3
    return np.nan


def education_level(age):
    if age < 25:
        return weighted_choice(
            [1, 2, 3, 4],
            [0.04, 0.16, 0.55, 0.25],
        )

    return weighted_choice(
        [1, 2, 3, 4],
        [0.12, 0.30, 0.40, 0.18],
    )


def calculate_resilience(values):
    valid = [v for v in values if pd.notna(v)]

    if len(valid) != 6:
        return np.nan, np.nan

    reverse_scores = [5 - v for v in valid]

    score = (
        (sum(reverse_scores) - 6)
        / 18
        * 100
    )

    status = 1 if score >= 60 else 0

    return round(score, 2), status


def generate_knowledge_response(question_number):
    # Four-option multiple-choice response.
    # The answer key is:
    # Q1=1, Q2=2, Q3=3, Q4=3, Q5=1,
    # Q6=3, Q7=2, Q8=1, Q9=2, Q10=3

    answer_key = {
        1: 1,
        2: 2,
        3: 3,
        4: 3,
        5: 1,
        6: 3,
        7: 2,
        8: 1,
        9: 2,
        10: 3,
    }

    response = random.randint(1, 4)

    score = int(response == answer_key[question_number])

    return response, score


# ============================================================
# Generate one respondent
# ============================================================

def generate_respondent(index):
    lga_code, lga_name = choose_lga(index)

    beneficiary_type = (
        1 if index < 1600 else 2
    )

    sex = weighted_choice(
        [1, 2],
        [0.41, 0.59],
    )

    # Approximately 30% youth.
    if random.random() < 0.30:
        age = random.randint(18, 35)
    else:
        age = random.randint(36, 75)

    education = education_level(age)

    household_size = random.randint(2, 10)

    respondent_id = f"ALMDP-{index + 1:04d}"

    community = random.choice(
        COMMUNITIES[lga_code]
    )

    row = {
        "respondent_id": respondent_id,
        "survey_date": random_date(),
        "enumerator_id": random.choice(ENUMERATORS),
        "supervisor_id": random.choice(SUPERVISORS),
        "state": "KD",
        "lga": lga_code,
        "community": community,
        "beneficiary_type": beneficiary_type,
        "consent": 1,
        "sex": sex,
        "age": age,
        "education": education,
        "household_size": household_size,
        "disability_status": yes_no(0.06),
        "age_group": age_group(age),
        "youth_status": int(18 <= age <= 35),
    }

    # --------------------------------------------------------
    # Agriculture section
    # --------------------------------------------------------

    if beneficiary_type == 1:

        value_chain = choose_value_chain()

        farm_area = round(
            bounded_normal(2.5, 1.7, 0.2, 12),
            2,
        )

        years_farming = max(
            1,
            int(
                bounded_normal(
                    max(age - 18, 5),
                    5,
                    1,
                    45,
                )
            ),
        )

        extension_access = yes_no(0.48)

        extension_contacts = (
            random.randint(1, 6)
            if extension_access
            else 0
        )

        area_cultivated = round(
            farm_area * random.uniform(0.75, 1.0),
            2,
        )

        productivity_by_crop = {
            1: (1.8, 0.55),
            2: (2.0, 0.60),
            3: (1.6, 0.45),
            4: (2.1, 0.70),
            5: (5.5, 1.6),
            6: (4.2, 1.2),
            7: (1.5, 0.40),
            8: (1.4, 0.40),
        }

        mean_productivity, sd_productivity = (
            productivity_by_crop[value_chain]
        )

        productivity = bounded_normal(
            mean_productivity,
            sd_productivity,
            0.3,
            10,
        )

        quantity_harvested = round(
            area_cultivated * productivity,
            2,
        )

        quantity_sold = round(
            quantity_harvested
            * random.uniform(0.40, 0.80),
            2,
        )

        quantity_consumed = round(
            quantity_harvested
            * random.uniform(0.05, 0.20),
            2,
        )

        quantity_lost = round(
            quantity_harvested
            * random.uniform(0.05, 0.30),
            2,
        )

        price = {
            1: 260000,
            2: 300000,
            3: 330000,
            4: 650000,
            5: 420000,
            6: 350000,
            7: 240000,
            8: 280000,
        }[value_chain]

        production_value = round(
            quantity_harvested
            * random.uniform(
                price * 0.85,
                price * 1.15,
            ),
            2,
        )

        practices = {
            "improved_seed": yes_no(0.45),
            "soil_testing": yes_no(0.28),
            "fertilizer_management": yes_no(0.52),
            "integrated_pest_management": yes_no(0.38),
            "conservation_agriculture": yes_no(0.34),
            "water_management": yes_no(0.42),
            "improved_storage": yes_no(0.40),
            "climate_smart_practice": yes_no(0.36),
        }

        practices_adopted = sum(
            practices.values()
        )

        adoption_status = int(
            practices_adopted >= 3
        )

        market_channel = weighted_choice(
            [1, 2, 3, 4, 5, 6, 7],
            [20, 25, 15, 12, 10, 12, 6],
        )

        regular_buyer = yes_no(0.55)

        structured_market = yes_no(0.26)

        market_information_received = yes_no(0.48)

        market_information_source = (
            weighted_choice(
                [1, 2, 3, 4, 5, 6, 7],
                [25, 20, 15, 15, 8, 12, 5],
            )
            if market_information_received
            else np.nan
        )

        buyer_access_improved = yes_no(0.31)

        average_selling_price = round(
            random.uniform(
                price * 0.85,
                price * 1.15,
            ),
            2,
        )

        # Post-harvest loss components.
        loss_total = quantity_lost

        loss_damaged = round(
            loss_total * random.uniform(0.20, 0.35),
            2,
        )

        loss_storage = round(
            loss_total * random.uniform(0.15, 0.30),
            2,
        )

        loss_transport = round(
            loss_total * random.uniform(0.10, 0.25),
            2,
        )

        loss_processing = round(
            loss_total * random.uniform(0.05, 0.15),
            2,
        )

        loss_other = round(
            max(
                0,
                loss_total
                - loss_damaged
                - loss_storage
                - loss_transport
                - loss_processing,
            ),
            2,
        )

        # Income components.
        crop_income = production_value * random.uniform(
            0.45, 0.80
        )

        livestock_income = random.uniform(
            0,
            180000,
        )

        processing_income = random.uniform(
            0,
            120000,
        )

        other_agricultural_income = random.uniform(
            0,
            100000,
        )

        business_income = random.uniform(
            0,
            100000,
        )

        employment_income = random.uniform(
            0,
            180000,
        )

        other_income = random.uniform(
            0,
            80000,
        )

        business_type = np.nan
        years_in_operation = np.nan
        number_of_employees = np.nan
        annual_sales = np.nan
        annual_operating_cost = np.nan
        annual_profit = np.nan

        financial_records = {
            "sales_records": np.nan,
            "expense_records": np.nan,
            "inventory_records": np.nan,
            "cashflow_records": np.nan,
            "profit_loss_records": np.nan,
            "business_bank_account": np.nan,
        }

    else:
        # ----------------------------------------------------
        # MSME section
        # ----------------------------------------------------

        value_chain = np.nan
        farm_area = np.nan
        years_farming = np.nan
        extension_access = np.nan
        extension_contacts = np.nan
        area_cultivated = np.nan
        quantity_harvested = np.nan
        quantity_sold = np.nan
        quantity_consumed = np.nan
        quantity_lost = np.nan
        production_value = np.nan

        practices = {
            "improved_seed": np.nan,
            "soil_testing": np.nan,
            "fertilizer_management": np.nan,
            "integrated_pest_management": np.nan,
            "conservation_agriculture": np.nan,
            "water_management": np.nan,
            "improved_storage": np.nan,
            "climate_smart_practice": np.nan,
        }

        practices_adopted = np.nan
        adoption_status = np.nan

        market_channel = np.nan
        regular_buyer = np.nan
        structured_market = np.nan
        market_information_received = np.nan
        market_information_source = np.nan
        buyer_access_improved = np.nan
        average_selling_price = np.nan

        loss_damaged = np.nan
        loss_storage = np.nan
        loss_transport = np.nan
        loss_processing = np.nan
        loss_other = np.nan

        crop_income = random.uniform(
            0,
            100000,
        )

        livestock_income = random.uniform(
            0,
            100000,
        )

        processing_income = random.uniform(
            50000,
            250000,
        )

        other_agricultural_income = random.uniform(
            0,
            100000,
        )

        business_income = random.uniform(
            150000,
            900000,
        )

        employment_income = random.uniform(
            0,
            200000,
        )

        other_income = random.uniform(
            0,
            100000,
        )

        business_type = weighted_choice(
            [1, 2, 3, 4, 5, 6, 7],
            [25, 25, 15, 10, 10, 5, 10],
        )

        years_in_operation = random.randint(1, 20)

        number_of_employees = random.randint(1, 30)

        annual_sales = round(
            bounded_normal(
                850000,
                450000,
                100000,
                5000000,
            ),
            2,
        )

        annual_operating_cost = round(
            annual_sales
            * random.uniform(0.55, 0.90),
            2,
        )

        annual_profit = round(
            annual_sales
            - annual_operating_cost,
            2,
        )

        financial_records = {
            "sales_records": yes_no(0.60),
            "expense_records": yes_no(0.55),
            "inventory_records": yes_no(0.50),
            "cashflow_records": yes_no(0.40),
            "profit_loss_records": yes_no(0.30),
            "business_bank_account": yes_no(0.45),
        }

    # --------------------------------------------------------
    # Income
    # --------------------------------------------------------

    total_income = (
        crop_income
        + livestock_income
        + processing_income
        + other_agricultural_income
        + business_income
        + employment_income
        + other_income
    )

    # --------------------------------------------------------
    # Derived financial-management variables
    # --------------------------------------------------------

    if beneficiary_type == 2:
        financial_record_count = sum(
            financial_records[x]
            for x in [
                "sales_records",
                "expense_records",
                "inventory_records",
                "cashflow_records",
                "profit_loss_records",
            ]
        )

        financial_management_status = int(
            financial_record_count >= 3
        )
    else:
        financial_record_count = np.nan
        financial_management_status = np.nan

    # --------------------------------------------------------
    # Inclusion variables
    # --------------------------------------------------------

    women_beneficiary = int(sex == 1)

    women_beneficiary_rate = np.nan

    youth_beneficiary_rate = np.nan

    income_increased = yes_no(0.30)

    # --------------------------------------------------------
    # Resilience
    # --------------------------------------------------------

    resilience_values = [
        random.randint(1, 4)
        for _ in range(6)
    ]

    (
        resilience_score,
        resilience_status,
    ) = calculate_resilience(
        resilience_values
    )

    # --------------------------------------------------------
    # Knowledge assessment
    # --------------------------------------------------------

    knowledge_responses = {}
    knowledge_scores = []

    for question in range(1, 11):
        response, score = generate_knowledge_response(
            question
        )

        knowledge_responses[
            f"knowledge_q{question}_response"
        ] = response

        knowledge_scores.append(score)

    knowledge_score = sum(knowledge_scores)

    adequate_knowledge = int(
        knowledge_score >= 7
    )

    # --------------------------------------------------------
    # Final row
    # --------------------------------------------------------

    row.update(
        {
            "primary_value_chain": value_chain,
            "farm_area_ha": farm_area,
            "years_farming": years_farming,
            "farmer_group_member": (
                yes_no(0.48)
                if beneficiary_type == 1
                else np.nan
            ),
            "extension_access": extension_access,
            "extension_contacts": extension_contacts,
            "area_cultivated_ha": area_cultivated,
            "quantity_harvested_t": quantity_harvested,
            "quantity_sold_t": quantity_sold,
            "quantity_consumed_t": quantity_consumed,
            "quantity_lost_t": quantity_lost,
            "production_value_ngn": production_value,
            **practices,
            "practices_adopted": practices_adopted,
            "adoption_status": adoption_status,
            "primary_market_channel": market_channel,
            "regular_buyer": regular_buyer,
            "structured_market": structured_market,
            "market_information_received": market_information_received,
            "market_information_source": market_information_source,
            "buyer_access_improved": buyer_access_improved,
            "average_selling_price_ngn": average_selling_price,
            "loss_damaged_t": loss_damaged,
            "loss_storage_t": loss_storage,
            "loss_transport_t": loss_transport,
            "loss_processing_t": loss_processing,
            "loss_other_t": loss_other,
            "total_postharvest_loss_t": quantity_lost,
            "postharvest_loss_rate": (
                quantity_lost
                / quantity_harvested
                * 100
                if beneficiary_type == 1
                and quantity_harvested > 0
                else np.nan
            ),
            "crop_income_ngn": round(crop_income, 2),
            "livestock_income_ngn": round(livestock_income, 2),
            "processing_income_ngn": round(
                processing_income,
                2,
            ),
            "other_agricultural_income_ngn": round(
                other_agricultural_income,
                2,
            ),
            "business_income_ngn": round(
                business_income,
                2,
            ),
            "employment_income_ngn": round(
                employment_income,
                2,
            ),
            "other_income_ngn": round(
                other_income,
                2,
            ),
            "total_annual_income_ngn": round(
                total_income,
                2,
            ),
            "business_type": business_type,
            "years_in_operation": years_in_operation,
            "number_of_employees": number_of_employees,
            "annual_sales_ngn": annual_sales,
            "annual_operating_cost_ngn": annual_operating_cost,
            "annual_profit_ngn": annual_profit,
            **financial_records,
            "financial_record_count": financial_record_count,
            "financial_management_status": financial_management_status,
            "women_beneficiary": women_beneficiary,
            "women_beneficiary_rate": women_beneficiary_rate,
            "youth_beneficiary_rate": youth_beneficiary_rate,
            "income_increased": income_increased,
            "resilience_crop_failure": resilience_values[0],
            "resilience_price_shock": resilience_values[1],
            "resilience_input_price": resilience_values[2],
            "resilience_health_shock": resilience_values[3],
            "resilience_climate_shock": resilience_values[4],
            "resilience_income_loss": resilience_values[5],
            "resilience_score": resilience_score,
            "resilience_status": resilience_status,
            **knowledge_responses,
            "knowledge_q1": knowledge_scores[0],
            "knowledge_q2": knowledge_scores[1],
            "knowledge_q3": knowledge_scores[2],
            "knowledge_q4": knowledge_scores[3],
            "knowledge_q5": knowledge_scores[4],
            "knowledge_q6": knowledge_scores[5],
            "knowledge_q7": knowledge_scores[6],
            "knowledge_q8": knowledge_scores[7],
            "knowledge_q9": knowledge_scores[8],
            "knowledge_q10": knowledge_scores[9],
            "knowledge_score": knowledge_score,
            "adequate_knowledge": adequate_knowledge,
        }
    )

    # Productivity is derived from the source values.
    if (
        beneficiary_type == 1
        and pd.notna(area_cultivated)
        and area_cultivated > 0
        and pd.notna(quantity_harvested)
    ):
        row["productivity_t_per_ha"] = round(
            quantity_harvested
            / area_cultivated,
            3,
        )
    else:
        row["productivity_t_per_ha"] = np.nan

    return row


# ============================================================
# Build dataset
# ============================================================

def generate_dataset():
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = [
        generate_respondent(i)
        for i in range(N_RESPONDENTS)
    ]

    df = pd.DataFrame(rows)

    # --------------------------------------------------------
    # Controlled raw-data quality issues
    # --------------------------------------------------------

    # 1. Five duplicate respondent IDs.
    duplicate_pairs = [
        (1995, 0),
        (1996, 100),
        (1997, 500),
        (1998, 1000),
        (1999, 1500),
    ]

    for duplicate_index, source_index in duplicate_pairs:
        df.loc[
            duplicate_index,
            "respondent_id"
        ] = df.loc[
            source_index,
            "respondent_id"
        ]

    # 2. Missing household size.
    household_missing = [
        17, 83, 211, 347, 512,
        688, 777, 914, 1101, 1288,
        1450, 1611, 1788, 1902, 1975,
    ]

    df.loc[
        household_missing,
        "household_size"
    ] = np.nan

    # 3. Missing annual income component.
    income_missing = [
        35, 142, 275, 411, 590,
        735, 862, 1005, 1198, 1340,
        1512, 1666, 1810, 1933, 1981,
    ]

    df.loc[
        income_missing,
        "crop_income_ngn"
    ] = np.nan

    # Recalculate total income only for affected rows.
    for index in income_missing:
        components = [
            "crop_income_ngn",
            "livestock_income_ngn",
            "processing_income_ngn",
            "other_agricultural_income_ngn",
            "business_income_ngn",
            "employment_income_ngn",
            "other_income_ngn",
        ]

        values = df.loc[index, components]

        if values.notna().all():
            df.loc[
                index,
                "total_annual_income_ngn"
            ] = values.sum()
        else:
            df.loc[
                index,
                "total_annual_income_ngn"
            ] = np.nan

    # 4. Missing farm area.
    farm_area_missing = [
        51, 229, 418, 631, 805,
        978, 1166, 1325, 1499, 1710,
    ]

    # Ensure these are farmer records.
    farmer_indices = df.index[
        df["beneficiary_type"] == 1
    ].tolist()

    for position, index in enumerate(
        farm_area_missing
    ):
        target = farmer_indices[
            position
        ]

        df.loc[
            target,
            "farm_area_ha"
        ] = np.nan

    # 5. Invalid age.
    df.loc[147, "age"] = 15

    # 6. Negative farm area.
    negative_area_index = farmer_indices[250]
    df.loc[
        negative_area_index,
        "farm_area_ha"
    ] = -2.0

    # 7. Invalid knowledge response.
    df.loc[
        14,
        "knowledge_q3_response"
    ] = 5

    # Make the derived score inconsistent intentionally.
    df.loc[
        14,
        "knowledge_q3"
    ] = 0

    # 8. Quantity sold greater than harvested.
    sold_error_index = farmer_indices[400]

    harvested = df.loc[
        sold_error_index,
        "quantity_harvested_t"
    ]

    df.loc[
        sold_error_index,
        "quantity_sold_t"
    ] = round(
        harvested * 1.20,
        2,
    )

    # 9. Quantity lost greater than harvested.
    loss_error_index = farmer_indices[600]

    harvested = df.loc[
        loss_error_index,
        "quantity_harvested_t"
    ]

    df.loc[
        loss_error_index,
        "quantity_lost_t"
    ] = round(
        harvested * 1.15,
        2,
    )

    # 10. Extreme farm-size outlier.
    outlier_area_index = farmer_indices[750]

    df.loc[
        outlier_area_index,
        "farm_area_ha"
    ] = 85.0

    # 11. Extreme income outlier.
    outlier_income_index = 1200

    df.loc[
        outlier_income_index,
        "business_income_ngn"
    ] = 25000000

    df.loc[
        outlier_income_index,
        "total_annual_income_ngn"
    ] = (
        df.loc[
            outlier_income_index,
            [
                "crop_income_ngn",
                "livestock_income_ngn",
                "processing_income_ngn",
                "business_income_ngn",
                "employment_income_ngn",
                "other_agricultural_income_ngn",
                "other_income_ngn",
            ],
        ]
        .sum(min_count=1)
    )

    # 12. Extreme production outlier.
    production_outlier_index = farmer_indices[900]

    df.loc[
        production_outlier_index,
        "quantity_harvested_t"
    ] = 250.0

    # Do not automatically "fix" derived productivity.
    area = df.loc[
        production_outlier_index,
        "area_cultivated_ha"
    ]

    if pd.notna(area) and area > 0:
        df.loc[
            production_outlier_index,
            "productivity_t_per_ha"
        ] = round(
            250.0 / area,
            3,
        )

    # 13. Extreme MSME revenue outlier.
    msme_indices = df.index[
        df["beneficiary_type"] == 2
    ].tolist()

    revenue_outlier_index = msme_indices[100]

    df.loc[
        revenue_outlier_index,
        "annual_sales_ngn"
    ] = 50000000

    # Recalculate profit while preserving the outlier.
    cost = df.loc[
        revenue_outlier_index,
        "annual_operating_cost_ngn"
    ]

    df.loc[
        revenue_outlier_index,
        "annual_profit_ngn"
    ] = (
        50000000 - cost
    )

    # --------------------------------------------------------
    # Preserve raw-data ordering.
    # --------------------------------------------------------

    dictionary_order = [
        "respondent_id",
        "survey_date",
        "enumerator_id",
        "supervisor_id",
        "state",
        "lga",
        "community",
        "beneficiary_type",
        "consent",
        "sex",
        "age",
        "education",
        "household_size",
        "disability_status",
        "age_group",
        "youth_status",
        "primary_value_chain",
        "farm_area_ha",
        "years_farming",
        "farmer_group_member",
        "extension_access",
        "extension_contacts",
        "area_cultivated_ha",
        "quantity_harvested_t",
        "quantity_sold_t",
        "quantity_consumed_t",
        "quantity_lost_t",
        "production_value_ngn",
        "improved_seed",
        "soil_testing",
        "fertilizer_management",
        "integrated_pest_management",
        "conservation_agriculture",
        "water_management",
        "improved_storage",
        "climate_smart_practice",
        "practices_adopted",
        "adoption_status",
        "primary_market_channel",
        "regular_buyer",
        "structured_market",
        "market_information_received",
        "market_information_source",
        "buyer_access_improved",
        "average_selling_price_ngn",
        "productivity_t_per_ha",
        "loss_damaged_t",
        "loss_storage_t",
        "loss_transport_t",
        "loss_processing_t",
        "loss_other_t",
        "total_postharvest_loss_t",
        "postharvest_loss_rate",
        "crop_income_ngn",
        "livestock_income_ngn",
        "processing_income_ngn",
        "other_agricultural_income_ngn",
        "business_income_ngn",
        "employment_income_ngn",
        "other_income_ngn",
        "total_annual_income_ngn",
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
        "financial_record_count",
        "financial_management_status",
        "women_beneficiary",
        "women_beneficiary_rate",
        "youth_beneficiary_rate",
        "income_increased",
        "resilience_crop_failure",
        "resilience_price_shock",
        "resilience_input_price",
        "resilience_health_shock",
        "resilience_climate_shock",
        "resilience_income_loss",
        "resilience_score",
        "resilience_status",
    ]

    for question in range(1, 11):
        dictionary_order.append(
            f"knowledge_q{question}_response"
        )

    for question in range(1, 11):
        dictionary_order.append(
            f"knowledge_q{question}"
        )

    dictionary_order.extend(
        [
            "knowledge_score",
            "adequate_knowledge",
        ]
    )

    # Keep only columns actually present.
    dictionary_order = [
        column
        for column in dictionary_order
        if column in df.columns
    ]

    df = df[dictionary_order]

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        date_format="%Y-%m-%d",
    )

    print(f"Created: {OUTPUT_FILE}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(f"Seed: {SEED}")
    print()
    print("Beneficiary distribution:")
    print(
        df["beneficiary_type"]
        .value_counts()
        .sort_index()
        .to_string()
    )
    print()
    print("LGA distribution:")
    print(
        df["lga"]
        .value_counts()
        .sort_index()
        .to_string()
    )
    print()
    print(
        "Duplicate respondent IDs:",
        df["respondent_id"].duplicated().sum(),
    )


if __name__ == "__main__":
    generate_dataset()