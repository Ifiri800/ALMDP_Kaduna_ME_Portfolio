# Agricultural Livelihoods and MSME Development Project (ALMDP)

## Baseline Survey Questionnaire

**Project Status:** Synthetic/Simulated Portfolio Project  
**Location:** Kaduna State, Nigeria  
**Implementation Period:** January 2027 – December 2030  
**Survey Type:** Baseline Survey  
**Instrument Type:** Structured Interviewer-Administered Questionnaire

---

## Portfolio Disclaimer

This questionnaire is a synthetic monitoring and evaluation instrument developed for a professional portfolio project. It is not an official ALMDP survey instrument and does not represent data collected from actual beneficiaries in Kaduna State.

The instrument is designed to demonstrate the development of a results-oriented baseline data collection system, including indicator measurement, respondent-level data capture, data quality controls, disaggregation, and reproducible analysis.

---

# 1. Survey Purpose

The baseline survey will establish the reference values against which changes in agricultural productivity, adoption of improved agricultural practices, market participation, post-harvest losses, agricultural and business income, MSME performance, inclusion, resilience, and knowledge will be monitored throughout implementation.

The survey will collect standardized respondent-level information that will support:

- Baseline indicator measurement.
- Beneficiary profiling and disaggregation.
- Measurement of agricultural production and productivity.
- Measurement of adoption of recommended agricultural practices.
- Assessment of market access and structured market participation.
- Measurement of post-harvest losses.
- Measurement of beneficiary and agricultural income.
- Assessment of agricultural MSME performance and financial management.
- Measurement of women and youth participation.
- Assessment of economic resilience.
- Measurement of knowledge of recommended agricultural practices.
- Subsequent outcome and impact monitoring.
- Data quality assurance and verification.
- Evidence-based project management and learning.

---

# 2. Target Respondents

The baseline survey will cover respondents within the project's target beneficiary population:

- Smallholder farmers.
- Agricultural MSME owners or representatives.
- Other eligible direct beneficiaries defined by the project.

The survey will distinguish between farmer and agricultural MSME respondents because some questions and indicators will apply only to specific respondent types.

---

# 3. Survey Administration

The questionnaire will be administered through a structured interview conducted by trained enumerators.

The digital questionnaire will be designed for implementation using a KoboToolbox/ODK-style data collection platform.

The questionnaire will incorporate:

- Mandatory fields for critical identification variables.
- Skip logic.
- Range checks.
- Required response validation.
- Consistency checks.
- Controlled response options.
- Unique respondent identification.
- Supervisor review.
- Digital timestamps and enumerator identification.

---

# 4. Respondent Identification and Survey Administration

## 4.1 Survey Identification

| Variable | Description | Response Type |
|---|---|---|
| respondent_id | Unique respondent identification number | Text |
| survey_date | Date of interview | Date |
| enumerator_id | Unique enumerator identification | Text |
| supervisor_id | Unique supervisor identification | Text |
| state | State of survey | Select |
| lga | Local Government Area | Select |
| community | Community of respondent | Select |
| beneficiary_type | Respondent beneficiary category | Select |
| consent | Respondent consent to participate | Yes/No |

### Enumerator Instruction

Before beginning the interview, the enumerator will:

1. Introduce the survey and its purpose.
2. Explain that participation is voluntary.
3. Explain how the information will be used.
4. Explain confidentiality arrangements.
5. Obtain informed consent.
6. Record the survey identification information.
7. Confirm the respondent's eligibility.

### Consent Question

**Q1. Do you agree to participate in this survey?**

- 1 = Yes
- 0 = No

**Validation:** If `consent = 0`, terminate the interview and record the appropriate survey disposition.

---

# 5. Respondent Profile

## 5.1 Demographic Information

| Variable | Question | Response Type |
|---|---|---|
| sex | What is the respondent's sex? | Select |
| age | How old are you? | Integer |
| education | What is your highest level of education completed? | Select |
| household_size | How many people normally live in your household? | Integer |
| disability_status | Do you have a disability that affects your daily activities or ability to participate in economic activities? | Yes/No |
| age_group | Derived age category | Derived |
| youth_status | Derived youth classification | Derived |

### Q2. Sex

- 1 = Male
- 2 = Female
- 3 = Prefer not to say

### Q3. Age

**How old are you?**

Record age in completed years.

**Validation:** 18–100 years.

### Q4. Highest Level of Education Completed

- 1 = No formal education
- 2 = Primary
- 3 = Secondary
- 4 = Technical/Vocational
- 5 = Tertiary
- 6 = Postgraduate
- 7 = Other

### Q5. Household Size

**How many people normally live in your household?**

Record the number of household members.

**Validation:** Positive integer.

### Q6. Disability Status

**Do you have a disability that affects your daily activities or ability to participate in economic activities?**

- 1 = Yes
- 0 = No
- 9 = Prefer not to say

---

# 6. Beneficiary Classification

### Q7. Beneficiary Type

**Which category best describes you?**

- 1 = Smallholder farmer
- 2 = Agricultural MSME owner
- 3 = Agricultural MSME representative
- 4 = Other eligible beneficiary

**Enumerator Instruction:** Select the category based on the respondent's primary beneficiary classification for the project.

The response to this question will determine the applicable sections of the questionnaire.

---

# 7. Agricultural Profile

**Applicability:** Farmer respondents.

## 7.1 Agricultural Characteristics

| Variable | Question | Response Type |
|---|---|---|
| primary_value_chain | What is your primary agricultural value chain? | Select |
| farm_area_ha | What is the total agricultural land area you currently cultivate? | Decimal |
| years_farming | How many years have you been engaged in farming? | Integer |
| farmer_group_member | Are you a member of a farmer group/cooperative? | Yes/No |
| extension_access | Have you received agricultural extension advice during the last 12 months? | Yes/No |
| extension_contacts | How many agricultural extension contacts did you receive during the last 12 months? | Integer |

### Q8. Primary Agricultural Value Chain

- 1 = Maize
- 2 = Rice
- 3 = Soybean
- 4 = Ginger
- 5 = Tomato
- 6 = Vegetables
- 7 = Sorghum
- 8 = Groundnut
- 9 = Other

### Q9. Cultivated Farm Area

**What is the total agricultural land area you currently cultivate?**

Record in hectares.

**Validation:** Greater than 0.

### Q10. Years of Farming Experience

**How many years have you been engaged in farming?**

Record completed years.

### Q11. Farmer Group Membership

**Are you currently a member of a farmer group or agricultural cooperative?**

- 1 = Yes
- 0 = No

### Q12. Access to Agricultural Extension

**Have you received agricultural extension advice during the last 12 months?**

- 1 = Yes
- 0 = No

### Q13. Number of Extension Contacts

**How many agricultural extension contacts did you receive during the last 12 months?**

Record the number of contacts.

**Validation:** Non-negative integer.

---

# 8. Baseline Data Quality Notes

The following controls will apply during questionnaire design and digital implementation:

- Respondent IDs must be unique.
- Consent must be obtained before substantive questions are administered.
- Age must fall within the defined eligibility range.
- Farm area must be greater than zero for farmer respondents.
- Farmer-specific questions must not be completed for respondents classified solely as MSMEs unless explicitly applicable.
- Categorical responses will use controlled response lists.
- Numerical variables will use defined minimum and maximum validation rules.
- Derived variables will be calculated programmatically rather than manually entered by enumerators.
- Missing values will be distinguished from valid zero values.
- Enumerators will not alter respondent responses to force validation rules to pass.

# 9. Agricultural Production

**Applicability:** Farmer respondents.

This section will collect production information for the respondent's primary agricultural production period used for baseline measurement.

## 9.1 Production Variables

| Variable | Question | Response Type |
|---|---|---|
| area_cultivated_ha | What area did you cultivate for your primary value chain during the reference production period? | Decimal |
| quantity_harvested_t | How much produce did you harvest? | Decimal |
| quantity_sold_t | How much of the harvested produce did you sell? | Decimal |
| quantity_consumed_t | How much of the harvested produce was consumed by the household? | Decimal |
| quantity_lost_t | How much of the harvested produce was lost or damaged before final use or sale? | Decimal |
| production_value_ngn | What was the total value of production? | Currency |

### Q14. Area Cultivated

**During the reference production period, what area did you cultivate for your primary agricultural value chain?**

Record in hectares.

**Validation:** Greater than 0.

### Q15. Quantity Harvested

**How much produce did you harvest from the cultivated area during the reference production period?**

Record in metric tonnes.

**Validation:** Greater than or equal to 0.

### Q16. Quantity Sold

**How much of the harvested produce did you sell?**

Record in metric tonnes.

**Validation:** Greater than or equal to 0 and must not exceed quantity harvested.

### Q17. Quantity Consumed

**How much of the harvested produce was consumed by your household?**

Record in metric tonnes.

**Validation:** Greater than or equal to 0 and must not exceed quantity harvested.

### Q18. Quantity Lost

**How much of the harvested produce was lost or damaged before final use or sale?**

Record in metric tonnes.

**Validation:** Greater than or equal to 0 and must not exceed quantity harvested.

### Q19. Production Value

**What was the approximate total market value of the agricultural production harvested during the reference production period?**

Record in Nigerian Naira (₦).

**Validation:** Non-negative value.

---

# 10. Improved Agricultural Practices

**Applicability:** Farmer respondents.

This section will measure adoption of recommended agricultural practices. Individual practice variables will be combined to calculate the number and proportion of farmers adopting at least three recommended practices.

## 10.1 Practice Adoption Variables

| Variable | Question | Coding |
|---|---|---|
| improved_seed | Did you use improved or certified seed? | 1/0 |
| soil_testing | Did you conduct or obtain soil testing before making fertilizer or soil-management decisions? | 1/0 |
| fertilizer_management | Did you apply fertilizer using recommended rates, timing, or placement? | 1/0 |
| integrated_pest_management | Did you use integrated pest-management practices? | 1/0 |
| conservation_agriculture | Did you apply conservation-agriculture practices? | 1/0 |
| water_management | Did you apply recommended water-management or water-conservation practices? | 1/0 |
| improved_storage | Did you use improved storage methods to reduce post-harvest losses? | 1/0 |
| climate_smart_practice | Did you apply at least one climate-smart agricultural practice? | 1/0 |

### Enumerator Instruction

Ask each practice separately. Do not classify a practice as adopted based only on the respondent's general statement that they use "modern farming methods."

Where necessary, ask the respondent to describe what they did during the reference production period.

### Q20. Improved or Certified Seed

**Did you use improved or certified seed during the reference production period?**

- 1 = Yes
- 0 = No

### Q21. Soil Testing

**Did you conduct or obtain soil testing before making fertilizer or soil-management decisions?**

- 1 = Yes
- 0 = No

### Q22. Fertilizer Management

**Did you apply fertilizer using recommended rates, timing, or placement?**

- 1 = Yes
- 0 = No

### Q23. Integrated Pest Management

**Did you use integrated pest-management practices to manage crop pests and diseases?**

- 1 = Yes
- 0 = No

### Q24. Conservation Agriculture

**Did you apply conservation-agriculture practices such as minimum soil disturbance, residue management, or other approved conservation practices?**

- 1 = Yes
- 0 = No

### Q25. Water Management

**Did you apply recommended water-management or water-conservation practices?**

- 1 = Yes
- 0 = No

### Q26. Improved Storage

**Did you use an improved storage method intended to reduce post-harvest losses?**

- 1 = Yes
- 0 = No

### Q27. Climate-Smart Agricultural Practice

**Did you apply at least one climate-smart agricultural practice during the reference production period?**

- 1 = Yes
- 0 = No

### Training Participation

The questionnaire will distinguish participation in agricultural training from general extension access.

| Variable | Question | Response |
|---|---|---|
| training_received | Have you received agricultural training during the reference period? | Yes/No |
| training_topic | What was the main topic of the agricultural training received? | CSA / Improved Production Practices / Post-Harvest Management / Market Access / Financial Management / Other |
| training_sessions | How many agricultural training sessions did you attend during the reference period? | Integer |

---

# 11. Market Access and Participation

**Applicability:** Farmer respondents and relevant agricultural MSMEs.

This section will assess market participation, buyer access, market information, and selling arrangements.

## 11.1 Market Access Variables

| Variable | Question | Response Type |
|---|---|---|
| primary_market_channel | What was your primary market channel? | Select |
| regular_buyer | Do you have a regular buyer for your agricultural products? | Yes/No |
| structured_market | Did you sell through a structured market arrangement? | Yes/No |
| market_information_received | Did you receive agricultural market information during the reference period? | Yes/No |
| market_information_source | What was your main source of market information? | Select |
| buyer_access_improved | Do you consider your access to buyers to have improved compared with the previous production period? | Yes/No |
| average_selling_price_ngn | What was your average selling price for your primary product? | Currency |

### Q28. Primary Market Channel

**What was your primary channel for selling agricultural products?**

- 1 = Farm-gate buyer
- 2 = Local market
- 3 = Wholesale market
- 4 = Processor
- 5 = Cooperative/farmer group
- 6 = Contract buyer
- 7 = Direct consumer
- 8 = Digital/online market
- 9 = Other

### Q29. Regular Buyer

**Do you currently have a regular buyer for your primary agricultural product?**

- 1 = Yes
- 0 = No

### Q30. Structured Market Participation

**Did you sell any of your primary agricultural product through a structured market arrangement during the reference period?**

A structured market arrangement may include a formal contract, organized buyer arrangement, cooperative marketing arrangement, processor linkage, or other documented market linkage.

- 1 = Yes
- 0 = No

### Q31. Market Information

**Did you receive agricultural market information during the reference period?**

- 1 = Yes
- 0 = No

### Q32. Main Source of Market Information

**What was your main source of agricultural market information?**

- 1 = Extension officer
- 2 = Farmer group/cooperative
- 3 = Trader/buyer
- 4 = Radio
- 5 = Television
- 6 = Mobile phone/SMS
- 7 = Internet/social media
- 8 = Government agency
- 9 = Other

### Q33. Buyer Access

**Compared with the previous production period, do you consider your access to buyers to have improved?**

- 1 = Yes
- 0 = No
- 9 = Not applicable/first production period

### Q34. Average Selling Price

**What was your average selling price for your primary agricultural product during the reference production period?**

Record in Nigerian Naira per relevant unit.

The unit used for the response will be recorded consistently with the product measurement system used by the project.

---

# 12. Practice Adoption and Productivity Derivation

The following variables will be calculated during data processing and will not be entered manually by enumerators.

| Derived Variable | Calculation |
|---|---|
| practices_adopted | Sum of the eight practice-adoption variables coded 1 |
| adoption_status | 1 if practices_adopted ≥ 3; otherwise 0 |
| productivity_t_per_ha | quantity_harvested_t ÷ area_cultivated_ha |

The resulting variables will support measurement of:

- **OUT-01:** Average crop productivity.
- **OUT-02:** Percentage of farmers adopting at least three recommended practices.

The practice variables will also provide explanatory information for interpreting changes in adoption performance.

# 13. Post-Harvest Loss

**Applicability:** Farmer respondents.

This section will collect information on the quantity of agricultural produce lost at different stages between harvest and final use or sale.

## 13.1 Loss Variables

| Variable | Question | Response Type |
|---|---|---|
| loss_damaged_t | Quantity lost due to physical damage | Decimal |
| loss_storage_t | Quantity lost during storage | Decimal |
| loss_transport_t | Quantity lost during transportation | Decimal |
| loss_processing_t | Quantity lost during processing | Decimal |
| loss_other_t | Quantity lost from other causes | Decimal |

### Q35. Loss Due to Physical Damage

**How much of your harvested produce was lost due to physical damage during harvesting or handling?**

Record in metric tonnes.

### Q36. Storage Loss

**How much of your harvested produce was lost during storage?**

Record in metric tonnes.

### Q37. Transport Loss

**How much of your harvested produce was lost during transportation?**

Record in metric tonnes.

### Q38. Processing Loss

**How much of your harvested produce was lost during processing?**

Record in metric tonnes.

### Q39. Other Losses

**How much of your harvested produce was lost from other causes not already recorded?**

Record in metric tonnes.

**Validation:** Each loss component must be non-negative.

The sum of all loss components must not exceed `quantity_harvested_t`.

---

# 14. Agricultural and Livelihood Income

This section will collect annual income information for the respondent or beneficiary household from relevant economic activities.

**Reference Period:** Previous 12 months.

## 14.1 Income Variables

| Variable | Description | Response Type |
|---|---|---|
| crop_income_ngn | Annual income from crop production | Currency |
| livestock_income_ngn | Annual income from livestock activities | Currency |
| processing_income_ngn | Annual income from agricultural processing | Currency |
| other_agricultural_income_ngn | Annual income from other agricultural activities | Currency |
| business_income_ngn | Annual income from business activities | Currency |
| employment_income_ngn | Annual income from employment or wages | Currency |
| other_income_ngn | Annual income from other sources | Currency |
| total_annual_income | Derived total annual income | Derived |

### Q40. Crop Income

**Approximately how much income did you receive from crop production during the previous 12 months?**

Record in Nigerian Naira.

### Q41. Livestock Income

**Approximately how much income did you receive from livestock-related activities during the previous 12 months?**

Record in Nigerian Naira.

### Q42. Agricultural Processing Income

**Approximately how much income did you receive from agricultural processing during the previous 12 months?**

Record in Nigerian Naira.

### Q43. Other Agricultural Income

**Approximately how much income did you receive from other agricultural activities during the previous 12 months?**

Record in Nigerian Naira.

### Q44. Business Income

**Approximately how much income did you receive from business activities during the previous 12 months?**

Record in Nigerian Naira.

### Q45. Employment Income

**Approximately how much income did you receive from employment, wages, salaries, or casual labour during the previous 12 months?**

Record in Nigerian Naira.

### Q46. Other Income

**Approximately how much income did you receive from other sources during the previous 12 months?**

Record in Nigerian Naira.

### Income Enumerator Instruction

Respondents should be encouraged to provide the best reasonable estimate where formal financial records are unavailable.

Enumerators must not invent or infer an income value.

A genuine zero value must be recorded as zero rather than treated as missing.

---

# 15. Income Calculation

The following variable will be calculated during data processing:

**Total Annual Income**

```text
total_annual_income_ngn =
    crop_income_ngn
    + livestock_income_ngn
    + processing_income_ngn
    + other_agricultural_income_ngn
    + business_income_ngn
    + employment_income_ngn
    + other_income_ngn

    **Validation Rules:**

- All income components must be non-negative.
- `total_annual_income_ngn` must equal the sum of all reported income components.
- Missing income components must not automatically be converted to zero unless the respondent confirms that the income source was not applicable or no income was received.

---

# 16. Agricultural MSME Profile

This section will be administered to respondents identified as agricultural MSMEs or beneficiaries operating an agricultural or agriculture-related business.

## 16.1 MSME Business Variables

| Variable | Description | Response Type |
|---|---|---|
| business_type | Main type of agricultural/MSME business | Categorical |
| years_in_operation | Number of years business has operated | Numeric |
| number_of_employees | Number of people currently employed | Numeric |
| annual_sales_ngn | Annual business sales/revenue | Currency |
| annual_operating_cost_ngn | Annual operating costs | Currency |
| annual_profit_ngn | Derived annual business profit | Derived |

### Q47. Business Type

**What is the main type of agricultural or agriculture-related business operated by the respondent?**

Record the main business category.

Suggested categories:

1. Agricultural input supply
2. Produce aggregation/trading
3. Food processing
4. Agricultural equipment/services
5. Storage/warehousing
6. Transportation/logistics
7. Retail/wholesale
8. Other agricultural business

### Q48. Years in Operation

**How many years has the business been operating?**

Record completed years.

### Q49. Number of Employees

**How many people currently work for the business, including the owner where applicable?**

Record the number of employees/personnel.

### Q50. Annual Sales

**Approximately how much did the business generate in sales/revenue during the previous 12 months?**

Record in Nigerian Naira.

### Q51. Annual Operating Costs

**Approximately how much did the business spend on operating costs during the previous 12 months?**

Record in Nigerian Naira.

**Validation:** Annual operating costs must be non-negative and should not exceed annual sales without an explanatory note.

---

# 17. MSME Financial Management

This section will assess whether the respondent maintains basic financial and business records.

## 17.1 Financial Record Variables

| Variable | Description | Response Type |
|---|---|---|
| sales_records | Business maintains sales records | Yes/No |
| expense_records | Business maintains expense records | Yes/No |
| inventory_records | Business maintains inventory records | Yes/No |
| cashflow_records | Business maintains cash-flow records | Yes/No |
| profit_loss_records | Business maintains profit/loss records | Yes/No |
| business_bank_account | Business has a bank account | Yes/No |

### Q52. Sales Records

**Does the business maintain records of sales or revenue?**

1 = Yes  
0 = No

### Q53. Expense Records

**Does the business maintain records of business expenses?**

1 = Yes  
0 = No

### Q54. Inventory Records

**Does the business maintain records of inventory or stock?**

1 = Yes  
0 = No

### Q55. Cash-Flow Records

**Does the business maintain records of cash inflows and outflows?**

1 = Yes  
0 = No

### Q56. Profit and Loss Records

**Does the business maintain a profit and loss statement or equivalent record?**

1 = Yes  
0 = No

### Q57. Business Bank Account

**Does the business have a bank account used for business transactions?**

1 = Yes  
0 = No

---

# 18. MSME Financial Performance Derivation

The following variables will be calculated during data processing.

## 18.1 Annual Profit

Annual business profit will be calculated as:

```text
annual_profit_ngn =
    annual_sales_ngn
    - annual_operating_cost_ngn

## 18.2 Financial Record Count

    financial_record_count =
    sales_records
    + expense_records
    + inventory_records
    + cashflow_records
    + profit_loss_records

## 18.3 Basic Financial Management Status

    financial_management_status =
    1 if financial_record_count >= 3
    0 if financial_record_count < 3

    ---

# 19. Inclusion and Participation

This section will support measurement of participation and inclusion of women and young people among direct project beneficiaries.

## 19.1 Gender Inclusion

The respondent's sex will be recorded in Section 5.

The following derived variable will be used:

```text
women_beneficiary =
    1 if sex = Female
    0 otherwise

## 19.2 Youth Participation

    youth_status =
    1 if age >= 18 and age <= 35
    0 otherwise

---

# 20. Economic Resilience

This section will assess the respondent's ability to cope with common economic, agricultural, market, and climate-related shocks.

For each question, record one response:

1 = Can cope without assistance  
2 = Can cope with some difficulty  
3 = Requires assistance  
4 = Unable to cope

## 20.1 Shock Response Variables

| Variable | Shock/Challenge |
|---|---|
| resilience_crop_failure | Crop failure or major production loss |
| resilience_price_shock | Major fall in agricultural prices |
| resilience_input_price | Major increase in input prices |
| resilience_health_shock | Serious household health or medical expense |
| resilience_climate_shock | Flood, drought, extreme weather, or similar climate shock |
| resilience_income_loss | Major loss of household/business income |

### Q59. Crop Failure

**If you experienced a major crop failure or production loss, how able would your household or business be to cope?**

Record response using the four-point resilience scale.

### Q60. Agricultural Price Shock

**If the selling price of your main agricultural product fell substantially, how able would your household or business be to cope?**

Record response using the four-point resilience scale.

### Q61. Input Price Increase

**If the price of major agricultural inputs increased substantially, how able would your household or business be to cope?**

Record response using the four-point resilience scale.

### Q62. Health or Medical Shock

**If your household experienced a serious health problem requiring significant expenditure, how able would your household be to cope?**

Record response using the four-point resilience scale.

### Q63. Climate Shock

**If your household or business experienced a major flood, drought, extreme weather event, or similar climate shock, how able would you be to cope?**

Record response using the four-point resilience scale.

### Q64. Income Loss

**If your household or business experienced a major loss of income, how able would you be to cope?**

Record response using the four-point resilience scale.

## 20.2 Resilience Score

Each response will be reverse-coded so that a higher score represents stronger resilience.

```text
reverse_score = 5 - response

---

# 21. Agricultural Knowledge Assessment

This section will assess respondents' knowledge of recommended agricultural, market, post-harvest, climate-smart, and basic business management practices relevant to the ALMDP intervention areas.

The assessment will use ten multiple-choice questions. Each question will have one correct answer and three plausible incorrect answers.

Respondents will select one answer for each question. Enumerators will record the selected response using the corresponding response code.

## 21.1 Knowledge Questions

### Q65. Improved Seed

**Which of the following is a major benefit of using suitable improved or certified seed?**

1. It can improve crop performance when properly selected and managed.
2. It guarantees that crops will not be affected by pests.
3. It eliminates the need for fertilizer.
4. It guarantees a fixed market price for the harvested crop.

**Correct answer:** 1

**Variable:** `knowledge_q1`

---

### Q66. Soil Testing

**What is one important purpose of soil testing before making fertilizer decisions?**

1. To determine the age of the farmer.
2. To determine the nutrient status of the soil and guide nutrient management.
3. To determine the selling price of the crop.
4. To determine the number of people in the household.

**Correct answer:** 2

**Variable:** `knowledge_q2`

---

### Q67. Fertilizer Management

**Which practice is most appropriate for efficient fertilizer management?**

1. Applying fertilizer at any rate regardless of crop requirements.
2. Applying fertilizer only after harvesting.
3. Applying fertilizer according to recommended rates, timing, and crop needs.
4. Applying the same fertilizer quantity to every farm regardless of conditions.

**Correct answer:** 3

**Variable:** `knowledge_q3`

---

### Q68. Integrated Pest Management

**What is the main purpose of integrated pest management (IPM)?**

1. To use pesticides as frequently as possible.
2. To eliminate all insects from the farm.
3. To combine appropriate pest-management methods while reducing unnecessary pesticide use.
4. To prevent farmers from monitoring their crops.

**Correct answer:** 3

**Variable:** `knowledge_q4`

---

### Q69. Water Management

**Which of the following can help reduce crop stress when rainfall is inadequate?**

1. Appropriate water management and efficient use of available water.
2. Delaying all farm operations until the end of the season.
3. Increasing post-harvest storage losses.
4. Harvesting crops before they mature regardless of crop condition.

**Correct answer:** 1

**Variable:** `knowledge_q5`

---

### Q70. Safe Storage

**Which practice can help reduce post-harvest losses during storage?**

1. Storing produce in damp conditions.
2. Mixing damaged produce with healthy produce.
3. Maintaining appropriate storage conditions and protecting produce from pests and moisture.
4. Leaving harvested produce exposed to rain.

**Correct answer:** 3

**Variable:** `knowledge_q6`

---

### Q71. Post-Harvest Handling

**Which practice can help reduce physical damage to harvested produce?**

1. Throwing produce into storage containers without care.
2. Using careful handling and appropriate containers during harvesting and transportation.
3. Keeping damaged produce with undamaged produce.
4. Delaying all handling until produce begins to deteriorate.

**Correct answer:** 2

**Variable:** `knowledge_q7`

---

### Q72. Market Information

**Why is reliable market information useful to farmers?**

1. It can help farmers make informed decisions about buyers, prices, and timing of sales.
2. It guarantees that every farmer will receive the highest possible price.
3. It eliminates all production risks.
4. It removes the need for record keeping.

**Correct answer:** 1

**Variable:** `knowledge_q8`

---

### Q73. Climate-Smart Agriculture

**What is a key objective of climate-smart agriculture?**

1. To increase agricultural production without considering climate risks.
2. To improve productivity and resilience while considering climate-related risks.
3. To eliminate the need for agricultural inputs.
4. To prevent farmers from using improved technologies.

**Correct answer:** 2

**Variable:** `knowledge_q9`

---

### Q74. Record Keeping

**Why is maintaining accurate farm or business records important?**

1. It guarantees that a business will always make a profit.
2. It eliminates the need for financial planning.
3. It supports financial management, monitoring, and informed decision-making.
4. It guarantees access to credit.

**Correct answer:** 3

**Variable:** `knowledge_q10`

---

## 21.2 Knowledge Score

Each knowledge question will be recoded during data processing as follows:

```text
1 = Correct answer
0 = Incorrect answer

## 21.3 Adequate Knowledge

Respondents scoring at least 7 out of 10 will be classified as having adequate knowledge.

```text
adequate_knowledge =
    1 if knowledge_score >= 7
    0 if knowledge_score < 7

## 21.4 Knowledge Scoring and Data Quality Controls

The correct-answer key will be retained in the data-processing documentation and will not be used to influence respondents' answers during questionnaire administration.

The following checks will be performed during data processing:

1. Each knowledge response must contain a valid response code from 1–4.
2. Missing knowledge responses will not be automatically treated as correct.
3. Each response will be compared against the approved answer key.
4. The corresponding binary knowledge variable will be generated as 1 or 0.
5. `knowledge_score` must range from 0 to 10.
6. `adequate_knowledge` must equal 1 only when `knowledge_score >= 7`.
7. Records with missing or invalid responses will be flagged for data-quality review.
8. The answer key will remain separate from the respondent-facing questionnaire during field administration.
---

# 22. Derived Variables and Final Questionnaire QA

The following variables will be generated during data processing rather than entered directly by enumerators. Derived variables will be calculated after the raw dataset has undergone validation and cleaning.

## 22.1 Derived Variable Summary

| Derived Variable | Definition / Calculation |
|---|---|
| `age_group` | Age category derived from respondent age. |
| `youth_status` | 1 if age is 18–35; 0 otherwise. |
| `total_annual_income_ngn` | Sum of crop, livestock, processing, other agricultural, business, employment, and other income. |
| `productivity_t_per_ha` | Quantity harvested in tonnes divided by cultivated area in hectares. |
| `practices_adopted` | Sum of the eight improved-practice variables coded 1 for adoption and 0 for non-adoption. |
| `adoption_status` | 1 if at least three recommended practices are adopted; 0 otherwise. |
| `total_postharvest_loss_t` | Sum of damaged, storage, transport, processing, and other post-harvest losses. |
| `postharvest_loss_rate` | Total post-harvest loss divided by quantity harvested × 100. |
| `annual_profit_ngn` | Annual sales minus annual operating costs for MSMEs. |
| `financial_record_count` | Number of basic financial records maintained, ranging from 0 to 5. |
| `financial_management_status` | 1 if at least three of the five financial records are maintained; 0 otherwise. |
| `women_beneficiary` | 1 if respondent is female; 0 otherwise. |
| `income_increased` | Respondent-reported increase in agricultural or business income compared with the previous production or business period. |
| `resilience_score` | Normalized composite resilience score ranging from 0 to 100. |
| `resilience_status` | 1 if resilience score is at least 60; 0 otherwise. |
| `knowledge_score` | Sum of the ten binary knowledge variables, ranging from 0 to 10. |
| `adequate_knowledge` | 1 if knowledge score is at least 7; 0 otherwise. |

Aggregate measures such as women beneficiary rate, youth beneficiary rate, adequate knowledge rate, adoption rate, average productivity, average income, and post-harvest loss rate will be calculated from the cleaned dataset.

## 22.2 Derived Variable Calculation Rules

### Total Annual Income

```text
total_annual_income_ngn =
    crop_income_ngn
    + livestock_income_ngn
    + processing_income_ngn
    + other_agricultural_income_ngn
    + business_income_ngn
    + employment_income_ngn
    + other_income_ngn

## 22.3 Final Data Validation Rules

Before a record is included in the clean baseline dataset, the following validation checks will be performed:

1. `respondent_id` must be unique.
2. Required survey identification fields must be complete.
3. Respondent consent must be recorded.
4. State must equal Kaduna.
5. LGA must belong to the approved ALMDP implementation LGAs.
6. Community must correspond to the selected LGA.
7. Age must be between 18 and 100 years.
8. `farm_area_ha` must be greater than zero for farmers.
9. Agricultural quantities must not be negative.
10. Income values must not be negative.
11. Quantity sold, consumed, and lost must not exceed quantity harvested.
12. Total post-harvest losses must not exceed quantity harvested.
13. Productivity must only be calculated from valid cultivated area and harvested quantity.
14. MSME variables must be completed for respondents classified as MSMEs.
15. Agricultural variables must be completed for respondents classified as farmers.
16. Knowledge responses must contain valid response codes.
17. Binary knowledge variables must contain only 0 or 1.
18. Knowledge score must range from 0 to 10.
19. Resilience responses must contain valid values from 1 to 4.
20. Derived variables must be recalculated after data cleaning.
21. Duplicate records must be identified and investigated.
22. Extreme or unusual values must be reviewed and documented rather than automatically deleted.
23. All identified data-quality issues must be recorded in the DQA log.
24. A traceable relationship must be maintained between raw records, cleaned records, and derived indicators.

## 22.4 Enumerator Completion Checklist

Before submitting each completed questionnaire, the enumerator will confirm that:

- [ ] Consent was obtained.
- [ ] Respondent identification fields are complete.
- [ ] Beneficiary classification is correctly recorded.
- [ ] Applicable agricultural sections were completed.
- [ ] Applicable MSME sections were completed.
- [ ] Income information was reviewed with the respondent.
- [ ] No unexplained negative quantities or income values were entered.
- [ ] Production quantities are internally consistent.
- [ ] Post-harvest loss information was reviewed.
- [ ] Market-access questions were completed.
- [ ] All applicable resilience questions were answered.
- [ ] All knowledge questions were completed.
- [ ] The questionnaire is internally consistent.
- [ ] Any unusual response has been documented.

## 22.5 Supervisor Review Checklist

The supervisor will review submitted questionnaires for:

- Completeness.
- Eligibility.
- Correct beneficiary classification.
- Logical consistency.
- Missing values.
- Duplicate respondent identification.
- Skip-pattern compliance.
- Unusual or extreme values.
- Enumerator errors.
- Consistency between production, sales, consumption, and loss quantities.
- Consistency between MSME sales, operating costs, and calculated profit.
- Completion of knowledge and resilience modules.
- Appropriate documentation of corrections.

Where an error is identified, the correction will be documented and traceable. Original responses will not be silently overwritten without an audit trail.

## 22.6 Final Questionnaire Quality Assurance

Before the questionnaire is approved for synthetic baseline data generation and subsequent analysis, the M&E workflow will verify that:

1. All questionnaire sections are present.
2. All variables required for the ALMDP indicator framework are captured.
3. Indicator definitions are consistent with questionnaire variables.
4. Response options are clearly defined and appropriately coded.
5. Beneficiary-specific modules and skip patterns are clearly defined.
6. Derived-variable formulas are documented.
7. Data-quality rules are documented.
8. The questionnaire supports calculation of the required baseline indicators.
9. The questionnaire can be converted into a structured digital data-collection form.
10. A clear audit trail exists from respondent response to final indicator.

The completed questionnaire will serve as the primary baseline data-collection instrument for the synthetic ALMDP M&E portfolio dataset.

---

# End of Baseline Questionnaire

**Document Status:** Synthetic/Simulated Portfolio Instrument

**Project:** Agricultural Livelihoods and MSME Development Project (ALMDP)

**Location:** Kaduna State, Nigeria

**Implementation Period:** January 2027–December 2030

**Purpose:** Baseline measurement and establishment of indicator reference values for the ALMDP Monitoring and Evaluation system.

### Adequate Knowledge Among Trained Farmers

OUT-03 will be calculated among farmers who reported receiving agricultural training during the reference period.

```text
adequate_knowledge_rate_trained =
    number of trained farmers with adequate_knowledge = 1
    / total number of trained farmers assessed
    × 100