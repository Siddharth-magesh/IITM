# GA4 Candidate Ranking Analysis - Answers

## Problem Statement

Madhuri, the Program Manager at Tech Enterprises, needs to rank internal candidates for a critical project position. The ranking is done using two methods:

- **Method 1**: Equal weights for all criteria
- **Method 2**: Weighted criteria based on Madhuri's preferences

### Criteria and Weights (Method 2)

| Criteria | Preference | Weight |
|----------|------------|--------|
| Years of Experience | More the better | 20% |
| Appraisal History | More consistent the better | 10% |
| Skills | More skills the better | 20% |
| Key Projects | More the better | 10% |
| Duration of Current Role | More the better | 10% |
| Bench Duration | More the better | 10% |
| When Candidate Will Be Available | Lesser the better | 20% |

**Note**: Reference date for availability is 1st July 2024. Appraisal consistency cutoff is > 0.7.

---

## Answers to Questions

### 1. What is the Rank of Akanksha using Method 1?

**Answer:** `3`

### 2. What is the composite score of Praveen using Method 1?

**Answer:** `0.388818`

### 3. What is the Rank of Nanda using Method 2?

**Answer:** `9`

### 4. What is the composite score of Sazid using Method 2?

**Answer:** `0.836852`

### 5. How many persons retain the same rank in Method 1 and Method 2?

**Answer:** `6`

---

## Method 1 Results (Equal Weights)

| Employee Name | Composite Score | Rank |
|---------------|-----------------|------|
| Abhijit | 0.912826 | 1 |
| Sazid | 0.806085 | 2 |
| Akanksha | 0.773408 | 3 |
| Esha | 0.617010 | 4 |
| Anuj | 0.583944 | 5 |
| Shalini | 0.516998 | 6 |
| Siva | 0.463884 | 7 |
| Praveen | 0.388818 | 8 |
| Lavanya | 0.333333 | 9 |
| Nanda | 0.321206 | 10 |

## Method 2 Results (Weighted)

| Employee Name | Composite Score | Rank |
|---------------|-----------------|------|
| Abhijit | 0.911571 | 1 |
| Sazid | 0.836852 | 2 |
| Akanksha | 0.774719 | 3 |
| Esha | 0.614499 | 4 |
| Shalini | 0.564491 | 5 |
| Anuj | 0.521353 | 6 |
| Siva | 0.474719 | 7 |
| Praveen | 0.422172 | 8 |
| Nanda | 0.312251 | 9 |
| Lavanya | 0.266667 | 10 |

## Comparison of Methods

| Employee Name | M1 Score | M1 Rank | M2 Score | M2 Rank | Same Rank? |
|---------------|----------|---------|----------|---------|------------|
| Abhijit | 0.912826 | 1 | 0.911571 | 1 | Yes |
| Sazid | 0.806085 | 2 | 0.836852 | 2 | Yes |
| Akanksha | 0.773408 | 3 | 0.774719 | 3 | Yes |
| Esha | 0.617010 | 4 | 0.614499 | 4 | Yes |
| Anuj | 0.583944 | 5 | 0.521353 | 6 | No |
| Shalini | 0.516998 | 6 | 0.564491 | 5 | No |
| Siva | 0.463884 | 7 | 0.474719 | 7 | Yes |
| Praveen | 0.388818 | 8 | 0.422172 | 8 | Yes |
| Lavanya | 0.333333 | 9 | 0.266667 | 10 | No |
| Nanda | 0.321206 | 10 | 0.312251 | 9 | No |

---

## Detailed Analysis

### Preprocessing Steps

1. **Years of Experience**: Used as-is (numeric)
2. **Appraisal History**: Calculated consistency using standard deviation. Applied cutoff > 0.7 for all three appraisals.
3. **Skills**: Counted number of skills (comma-separated)
4. **Key Projects**: Counted number of projects (comma-separated)
5. **Duration in Current Role**: Used as-is (numeric)
6. **Bench Duration**: Used as-is (numeric)
7. **Availability Date**: Calculated days from 1st July 2024

### Normalization

Min-Max normalization applied to all criteria:
- **More is better**: (value - min) / (max - min)
- **Less is better**: (max - value) / (max - min)

### Composite Score Calculation

**Method 1**: All criteria weighted equally at 14.29% (1/7)

**Method 2**: Criteria weighted according to Madhuri's preferences

### Ranking

Candidates ranked in descending order of composite scores (highest score = Rank 1)

---

*Analysis completed successfully. All calculations verified.*
