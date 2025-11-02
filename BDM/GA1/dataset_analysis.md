# Dataset Analysis - BDM Folder

## Dataset Overview

This document contains analysis and answers for questions related to two CSV files in the BDM folder:
- **dataset1.csv** - Consumer survey data with household characteristics
- **dataset2.csv** - Loan portfolio data from various financial institutions

---

## Dataset 1: Consumer Survey Data

### Structure and Columns
- **Total rows**: 102 (including header and 1 empty row at top)
- **Total columns**: 40

### Key Columns:
1. **STATE** - Indian state where respondent resides
2. **REGION_TYPE** - URBAN or RURAL
3. **RESPONSE_STATUS** - "Accepted" or "Non-Response"
4. **AGE_GROUP** - Household age composition (e.g., "Grown-up - dominant", "Balanced households with no Seniors")
5. **INCOME_GROUP** - Annual income ranges (e.g., "120000 - 150000")
6. **OCCUPATION_GROUP** - Primary occupation category
7. **EDUCATION_GROUP** - Educational attainment of household
8. **GENDER_GROUP** - Gender composition (Male Majority/Dominated, Female Majority/Dominated, Balanced)
9. **POWER_GROUP** - Power availability category
10. **TRAVEL_GROUP** - Time to travel 10 kms
11. **SIZE_GROUP** - Number of household members
12. **HAS_ACCESS_TO_ELECTRICITY** - Y/N
13. **POWER_AVAILABILITY_IN_HOURS_PER_DAY** - Numeric hours
14. **TIME_TO_TRAVEL_TEN_KMS** - Minutes to travel 10 km
15. **HOUSES_OWNED** - Number of houses
16. **BOUGHT_HOUSE** - Y/N
17. **WILL_BUY_HOUSE** - Y/N
18. **WILL_BUY_HOUSE_NOW** - Y/N
19. **GOOD_TIME_TO_BUY_HOUSE** - Y/N
20. **CARS_OWNED** - Number of cars
21. **TYPE_OF_CAR_OWNED** - Car type or "Not Applicable"
22. **BOUGHT_CAR** - Y/N
23. **WILL_BUY_CAR** - Y/N
24. **WILL_BUY_CAR_OF_TYPE** - Car type or "Not Applicable"
25. **WILL_BUY_CAR_NOW** - Y/N
26. **GOOD_TIME_TO_BUY_CAR** - Y/N
27. **TWO_WHEELERS_OWNED** - Number
28. **TYPE_OF_TWO_WHEELER_OWNED** - Type or "Not Applicable"
29. **BOUGHT_TWO_WHEELER** - Y/N
30. **WILL_BUY_TWO_WHEELER** - Y/N
31. **WILL_BUY_TWO_WHEELER_OF_TYPE** - Type or "Not Applicable"
32. **WILL_BUY_TWO_WHEELER_NOW** - Y/N
33. **GOOD_TIME_TO_BUY_TWO_WHEELER** - Empty in most rows
34. **HAS_OUTSTANDING_SAVING_IN_FIXED_DEPOSITS** - Y/N
35. **HAS_OUTSTANDING_BORROWING** - Y/N
36. **BORROWED_FOR_CONSUMPTION_EXPENDITURE** - Y/N
37. **BORROWED_FOR_CONSUMER_DURABLES** - Y/N
38. **BORROWED_FOR_VEHICLES** - Y/N
39. **BORROWED_FROM_BANK** - Y/N
40. **BORROWED_FROM_BANK_FOR_VEHICLES** - Y/N

### Data Quality Issues in Dataset 1:

1. **Missing Values Pattern**:
   - Rows with `RESPONSE_STATUS = "Non-Response"` have all other fields marked as "Data Not Available"
   - Approximately 30-35% of rows are Non-Response entries
   - Many numeric columns (POWER_AVAILABILITY_IN_HOURS_PER_DAY, TIME_TO_TRAVEL_TEN_KMS) are empty for Non-Response rows
   - Column 33 (GOOD_TIME_TO_BUY_TWO_WHEELER) is mostly empty even for Accepted responses

2. **Data Type Inconsistencies**:
   - Numeric columns contain both numbers and empty strings
   - Boolean-like columns use "Y", "N", and empty values
   - Some columns use "Not Applicable" as a value

3. **Valid Data Count**:
   - Only rows with `RESPONSE_STATUS = "Accepted"` contain usable data
   - Estimated 60-70 rows with complete data out of 102 total

---

## Dataset 2: Loan Portfolio Data

### Structure and Columns
- **Total rows**: 2,242 (including header)
- **Total columns**: 12

### Key Columns:
1. **Loan Id** - Unique loan identifier with prefix indicating lender type
2. **Quarters** - Q1, Q2, Q3, Q4
3. **Years** - FY19, FY20, FY21
4. **Segment of Loan** - "Commercial" or "Microfinance"
5. **Lender Name** - NBFC, PVT Bank, PSU Bank
6. **Type of Loan** - "Commercial Loan" or "Microfinance Loan"
7. **Original Loan size** - Initial loan amount
8. **Outstanding loan amount** - Current outstanding balance
9. **Borrower Age** - Age in years
10. **Borrower Income** - Annual income
11. **New to Credit (Y /N)** - First-time borrower indicator
12. **Gender** - M or F

### Data Quality Issues in Dataset 2:

1. **Missing Values**:
   - Dataset appears relatively complete with minimal missing values
   - All numeric columns contain valid numbers
   - No obvious "Data Not Available" or null patterns observed in the sample

2. **Data Patterns Observed**:
   - **Commercial Loans**: Much larger amounts (millions), typically from NBFC, PVT Bank, PSU Bank
   - **Microfinance Loans**: Smaller amounts (thousands to hundred thousands)
   - Loan ID prefixes indicate lender type:
     - `NBFCIN` = NBFC loans
     - `PVT` = Private bank loans
     - `PSUIN` = PSU bank loans

3. **Value Ranges**:
   - **Commercial loans**: Original size 5M-157M, Outstanding 2.7M-80M
   - **Microfinance loans**: Original size 1,100-124,200, Outstanding 457-42,508
   - **Borrower Age**: 22-66 years
   - **Borrower Income**: Wide range from ~141K to ~2M+

---

## Important Notes for Analysis

### When answering questions, I will:

1. **Handle Missing Data**:
   - For Dataset 1: Filter out "Non-Response" rows unless the question specifically asks about response rates
   - Exclude rows where key fields are "Data Not Available"
   - Note when calculations exclude incomplete records

2. **Data Type Handling**:
   - Convert numeric strings to numbers where needed
   - Handle "Not Applicable" values appropriately
   - Treat empty strings as missing values

3. **Provide Clear Methodology**:
   - Document filtering criteria used
   - Show calculation steps
   - Indicate sample sizes after filtering
   - Note any assumptions made

4. **Be Explicit About**:
   - How many records were usable vs. total records
   - Which columns were used in calculations
   - Any data transformations applied
   - Confidence levels based on data quality

---

## Ready for Questions

I have analyzed both datasets and understand:
- Dataset 1: Consumer behavior survey with ~60-70 valid responses out of 102 rows
- Dataset 2: Loan portfolio with 2,241 loan records (relatively complete data)

---

## ANSWERS TO ALL QUESTIONS

### Dataset 1: Consumer Survey Questions

#### Q1: What fraction of sample households have only one two wheeler?
**Answer: 0.8657**

**Methodology:**
- Filter: Only "Accepted" responses (67 households)
- Count households where `TWO_WHEELERS_OWNED = '1'`
- Calculation: 58 households with 1 TW / 67 total = **0.8657**

---

#### Q2: What fraction don't have a two wheeler, but are interested in buying one?
**Answer: 0.0149**

**Methodology:**
- Filter: `TWO_WHEELERS_OWNED = '0'` AND `WILL_BUY_TWO_WHEELER = 'Y'`
- Count: 1 household
- Calculation: 1 / 67 = **0.0149**

---

#### Q3: What proportion already have a two wheeler, but want to buy one more?
**Answer: 0.1642**

**Methodology:**
- Filter: `TWO_WHEELERS_OWNED > 0` AND `WILL_BUY_TWO_WHEELER = 'Y'`
- Count: 11 households
- Calculation: 11 / 67 = **0.1642**

---

#### Q4: What fraction of urban households don't have a two wheeler but intend to buy immediately?
**Answer: 0.0250**

**Methodology:**
- Filter: `REGION_TYPE = 'URBAN'` (40 urban households)
- Then filter: `TWO_WHEELERS_OWNED = '0'` AND `WILL_BUY_TWO_WHEELER_NOW = 'Y'`
- Count: 1 household
- Calculation: 1 / 40 urban households = **0.0250**

---

#### Q5: Based on sample data, what is the existing market share of Commuter bikes?
**Answer: 0.7241**

**Methodology:**
- Count households with `'Commuter Bike'` in `TYPE_OF_TWO_WHEELER_OWNED`: 42 households
- Total households with any two-wheeler: 58 households
- Calculation: 42 / 58 = **0.7241**
- Note: Commuter Bike represents 72.41% of the two-wheeler market in the sample

---

#### Q6: What proportion of Female majority/dominant/only households have a scooter?
**Answer: 0.3333**

**Methodology:**
- Filter: `GENDER_GROUP` contains 'Female' (Female Majority, Female Dominated)
- Total Female households: 21
- Count with `'Scooter'` in `TYPE_OF_TWO_WHEELER_OWNED`: 7
- Calculation: 7 / 21 = **0.3333** (33.33%)

---

#### Q7: If outstanding loan disqualifies eligibility, how many households (proportion) are eligible for a new loan?
**Answer: 0.6567**

**Methodology:**
- Filter: `HAS_OUTSTANDING_BORROWING = 'N'`
- Count: 44 households without outstanding borrowing
- Calculation: 44 / 67 = **0.6567** (65.67% eligible)

---

#### Q8: What proportion of households wanting two wheeler would be eligible for lower interest loan against FD?
**Answer: 0.4167**

**Methodology:**
- First filter: `WILL_BUY_TWO_WHEELER = 'Y'` → 12 households
- Among these, count with `HAS_OUTSTANDING_SAVING_IN_FIXED_DEPOSITS = 'Y'`: 5 households
- Calculation: 5 / 12 = **0.4167** (41.67%)

---

#### Q9: If 24-hour electricity needed for electric two wheeler, what is the target market share?
**Answer: 0.5833**

**Methodology:**
- Filter: Households wanting to buy TW (`WILL_BUY_TWO_WHEELER = 'Y'`): 12 households
- Among these, count with `POWER_GROUP = '24 hours'`: 7 households
- Calculation: 7 / 12 = **0.5833** (58.33% of potential TW buyers have 24hr power)

---

#### Q10: What fraction of Rural Farmers have at least one two wheeler?
**Answer: 0.7500**

**Methodology:**
- Filter: `REGION_TYPE = 'RURAL'` AND `OCCUPATION_GROUP` contains 'Farmer'
- Total Rural Farmers: 4 households
- Count with `TWO_WHEELERS_OWNED ≥ 1`: 3 households
- Calculation: 3 / 4 = **0.7500** (75%)

---

### Dataset 2: Loan Portfolio Questions

#### Q11: In FY20, what proportion of total loans are serviced by NBFCs?
**Answer: 0.177680**

**Methodology:**
- Filter: `Years = 'FY20'`
- Sum of NBFC loan values: ₹256,152,046
- Total FY20 loan value: ₹1,441,647,716
- Calculation: 256,152,046 / 1,441,647,716 = **0.177680** (17.77%)

---

#### Q12: What is the ratio of Retail loan value given by private bank to PSU bank in FY21?
**Answer: 0.616912**

**Methodology:**
- Filter: `Years = 'FY21'` AND `Segment of Loan = 'Microfinance'` (Retail loans)
- PVT Bank total: ₹4,466,020
- PSU Bank total: ₹7,239,320
- Calculation: 4,466,020 / 7,239,320 = **0.616912**

---

#### Q13: What is the growth % difference between FY19 & FY20 in commercial loans by Private banks?
**Answer: 0.454322**

**Methodology:**
- Filter: `Lender Name = 'PVT Bank'` AND `Segment = 'Commercial'`
- FY19 total: ₹204,182,210
- FY20 total: ₹111,417,660
- Absolute relative difference: |(111,417,660 - 204,182,210) / 204,182,210| = **0.454322** (45.43% decrease)

---

#### Q14: What is the difference in average microfinance loan from NBFCs between FY20 and FY21?
**Answer: 859**

**Methodology:**
- Filter: `Lender = 'NBFC'` AND `Segment = 'Microfinance'`
- FY20: 148 loans, avg = ₹40,806.22
- FY21: 134 loans, avg = ₹39,947.01
- Difference: |40,806.22 - 39,947.01| = **859** (truncated integer)

---

#### Q15: What is the average credit card borrowings of Males in FY20?
**Answer: Unable to calculate**

**Reason:** Dataset 2 does not contain credit card specific data. The dataset has loan information but no separate credit card borrowing column.

---

#### Q16: What is the percentage difference in credit card transactions between males and females?
**Answer: Unable to calculate**

**Reason:** Dataset 2 does not contain credit card transaction data.

---

#### Q17: What is the % (relative difference) of new borrowers in RETAIL category in FY21 vs FY20?
**Answer: 0.140114**

**Methodology:**
- Filter: `Segment = 'Microfinance'` (Retail category)
- FY20: 138 new borrowers / 447 total = 30.87%
- FY21: 151 new borrowers / 429 total = 35.20%
- Relative difference: (0.3520 - 0.3087) / 0.3087 = **0.140114** (14.01% increase)

- Relative difference: (0.3520 - 0.3087) / 0.3087 = **0.140114** (14.01% increase)

---

#### Q18: Who is the lender who gave out the highest average commercial loans to Women in FY19?
**Answer: NBFC**

**Methodology:**
- Filter: `Years = 'FY19'` AND `Segment = 'Commercial'` AND `Gender = 'F'`
- Calculate average loan size per lender:
  - **NBFC**: ₹65,373,131.67 (3 loans)
  - PVT Bank: ₹11,962,297.50 (4 loans)
  - PSU Bank: ₹7,879,060.00 (1 loan)
- **Winner: NBFC** with highest average

---

#### Q19: What fraction of borrowers have credit history (not new to credit)?
**Answer: 0.680357**

**Methodology:**
- Filter: `New to Credit (Y /N) = 'N'`
- Count: 1,524 borrowers with credit history
- Total borrowers: 2,240
- Calculation: 1,524 / 2,240 = **0.680357** (68.04%)

---

#### Q20: How many female borrowers have income more than average income of borrowers?
**Answer: 36**

**Methodology:**
- Calculate average income across all borrowers: ₹1,715,233.52
- Filter: `Gender = 'F'` AND `Borrower Income > 1,715,233.52`
- Count: **36 female borrowers**

---

## Summary of Key Findings

### Dataset 1 Insights:
- **86.57%** of households own exactly one two-wheeler (very high single ownership)
- **72.41%** market share for Commuter Bikes (dominant segment)
- Only **1.49%** don't have but want to buy a two-wheeler (low untapped market)
- **16.42%** already own but want to buy another (replacement/addition market)
- **65.67%** eligible for new loans (no outstanding borrowing)
- **58.33%** of potential TW buyers have 24hr electricity (good for electric TWs)
- **75%** of rural farmers own at least one two-wheeler

### Dataset 2 Insights:
- NBFCs service **17.77%** of FY20 loan market by value
- Private banks decreased commercial lending by **45.43%** from FY19 to FY20
- **68.04%** of borrowers have credit history (established market)
- NBFC gives highest average commercial loans to women (₹65.4M avg)
- New borrowers in retail segment increased by **14.01%** from FY20 to FY21
- Average microfinance loan from NBFC decreased by ₹859 (FY20 to FY21)

---

**Analysis completed**: 2025-10-18  
**Total questions answered**: 20 (18 with data, 2 noted as unavailable due to dataset limitations)  
**Methodology**: Filtered valid responses, handled missing data, used appropriate denominators for each calculation

---

## Quick Reference: All Answers

| # | Question Summary | Answer | Type |
|---|-----------------|--------|------|
| 1 | Fraction with only 1 two-wheeler | 0.8657 | FLOAT |
| 2 | Fraction: no TW, want to buy | 0.0149 | FLOAT |
| 3 | Proportion: have TW, want more | 0.1642 | FLOAT |
| 4 | Urban: no TW, buy immediately | 0.0250 | FLOAT |
| 5 | Market share: Commuter bikes | 0.7241 | FLOAT |
| 6 | Female households with scooter | 0.3333 | FLOAT |
| 7 | Eligible for new loan (no outstanding) | 0.6567 | FLOAT |
| 8 | Want TW + have FD (lower interest) | 0.4167 | FLOAT |
| 9 | Target market: electric TW (24hr power) | 0.5833 | FLOAT |
| 10 | Rural farmers with ≥1 TW | 0.7500 | FLOAT |
| 11 | NBFC market share FY20 | 0.177680 | FLOAT |
| 12 | Ratio: PVT/PSU retail loans FY21 | 0.616912 | FLOAT |
| 13 | Growth % PVT commercial FY19→FY20 | 0.454322 | FLOAT |
| 14 | Diff: avg microfinance NBFC FY20-FY21 | 859 | INTEGER |
| 15 | Avg credit card: Males FY20 | N/A | - |
| 16 | % diff credit card: M vs F | N/A | - |
| 17 | Relative diff: new borrowers retail FY21/FY20 | 0.140114 | FLOAT |
| 18 | Highest avg commercial to women FY19 | NBFC | STRING |
| 19 | Fraction with credit history | 0.680357 | FLOAT |
| 20 | Female borrowers: income > avg | 36 | INTEGER |

---

**Files created during analysis:**
- `dataset_analysis.md` - This comprehensive analysis document
- `analyze_datasets.py` - Python script with all calculations
- `analysis_results.txt` - Raw output from analysis script
