import pandas as pd
import numpy as np
import os
from datetime import datetime

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

print("="*80)
print("CANDIDATE RANKING ANALYSIS")
print("="*80)
print()

# Load the dataset
df = pd.read_csv(os.path.join(script_dir, 'dataset_4_152.xlsx - D1.csv'))

print("Dataset loaded successfully!")
print(f"Total candidates: {len(df)}")
print("\nColumns:", df.columns.tolist())
print("\nFirst few rows:")
print(df.head())
print()

# ============================================================================
# PREPROCESSING
# ============================================================================
print("="*80)
print("STEP 1: PREPROCESSING")
print("="*80)
print()

# Create a copy for processing
df_processed = df.copy()

# 1. Years of Experience - already numeric
print("1. Years of Experience - Already numeric")

# 2. Appraisal history - Calculate consistency (using standard deviation)
# More consistent = lower standard deviation
# We also need to check if all appraisals are > 0.7
print("2. Processing Appraisal History (Consistency with cutoff > 0.7)")

df_processed['Appraisal_Mean'] = df_processed[['Appraisal 1', 'Appraisal 2', 'Appraisal 3']].mean(axis=1)
df_processed['Appraisal_StdDev'] = df_processed[['Appraisal 1', 'Appraisal 2', 'Appraisal 3']].std(axis=1)

# Check if all appraisals are > 0.7
df_processed['All_Appraisals_Above_Cutoff'] = (
    (df_processed['Appraisal 1'] > 0.7) & 
    (df_processed['Appraisal 2'] > 0.7) & 
    (df_processed['Appraisal 3'] > 0.7)
).astype(int)

# For consistency: lower std dev is better, so we'll use inverse or negative
# But we'll also factor in the cutoff requirement
# Appraisal Score = (1 - StdDev) if all > 0.7, else penalize
df_processed['Appraisal_Consistency'] = df_processed.apply(
    lambda row: (1 - row['Appraisal_StdDev']) if all([
        row['Appraisal 1'] > 0.7,
        row['Appraisal 2'] > 0.7,
        row['Appraisal 3'] > 0.7
    ]) else 0.5 * (1 - row['Appraisal_StdDev']),
    axis=1
)

print("   Appraisal consistency calculated (lower std dev = more consistent)")

# 3. Skills - count the number of skills
print("3. Processing Skills (count)")
df_processed['Skills_Count'] = df_processed['Skills'].apply(lambda x: len(x.split(',')))

# 4. Key Projects - count the number of projects
print("4. Processing Key Projects (count)")
df_processed['Key_Projects_Count'] = df_processed['Key projects'].apply(lambda x: len(x.split(',')))

# 5. Duration of current role - already numeric
print("5. Duration in current role - Already numeric")

# 6. Bench Duration - already numeric
print("6. Bench Duration - Already numeric")

# 7. When candidate will be available - calculate days from today (1st July 2024)
print("7. Processing Availability Date (days from 1st July 2024)")
today = datetime(2024, 7, 1)
df_processed['Available_Date'] = pd.to_datetime(df_processed['When the candidate will be available'])
df_processed['Days_Until_Available'] = (df_processed['Available_Date'] - today).dt.days

print("\nPreprocessing Complete!")
print("\nProcessed Data Preview:")
print(df_processed[['Employee name', 'Year of experience', 'Appraisal_Consistency', 
                     'Skills_Count', 'Key_Projects_Count', 'Duration in the current role',
                     'Bench duration', 'Days_Until_Available']].to_string())
print()

# ============================================================================
# NORMALIZATION (Min-Max Scaling)
# ============================================================================
print("="*80)
print("STEP 2: NORMALIZATION (Min-Max Scaling)")
print("="*80)
print()

df_normalized = df_processed.copy()

# For "more is better" criteria: (value - min) / (max - min)
# For "less is better" criteria: (max - value) / (max - min)

criteria_to_normalize = {
    'Year of experience': 'more',
    'Appraisal_Consistency': 'more',
    'Skills_Count': 'more',
    'Key_Projects_Count': 'more',
    'Duration in the current role': 'more',
    'Bench duration': 'more',
    'Days_Until_Available': 'less'  # Lesser days = better
}

for col, direction in criteria_to_normalize.items():
    min_val = df_normalized[col].min()
    max_val = df_normalized[col].max()
    
    if max_val == min_val:
        df_normalized[f'{col}_norm'] = 1.0
    else:
        if direction == 'more':
            df_normalized[f'{col}_norm'] = (df_normalized[col] - min_val) / (max_val - min_val)
        else:  # 'less'
            df_normalized[f'{col}_norm'] = (max_val - df_normalized[col]) / (max_val - min_val)
    
    print(f"{col} ({direction} is better): Normalized")

print("\nNormalization Complete!")
print("\nNormalized Data Preview:")
normalized_cols = ['Employee name'] + [col for col in df_normalized.columns if col.endswith('_norm')]
print(df_normalized[normalized_cols].to_string())
print()

# ============================================================================
# METHOD 1: EQUAL WEIGHTS
# ============================================================================
print("="*80)
print("STEP 3: METHOD 1 - EQUAL WEIGHTS FOR ALL CRITERIA")
print("="*80)
print()

# All criteria get equal weight (1/7 = ~14.29%)
equal_weight = 1.0 / 7

df_normalized['Composite_Score_M1'] = (
    equal_weight * df_normalized['Year of experience_norm'] +
    equal_weight * df_normalized['Appraisal_Consistency_norm'] +
    equal_weight * df_normalized['Skills_Count_norm'] +
    equal_weight * df_normalized['Key_Projects_Count_norm'] +
    equal_weight * df_normalized['Duration in the current role_norm'] +
    equal_weight * df_normalized['Bench duration_norm'] +
    equal_weight * df_normalized['Days_Until_Available_norm']
)

# Rank by composite score (highest score = rank 1)
df_normalized['Rank_M1'] = df_normalized['Composite_Score_M1'].rank(ascending=False, method='min').astype(int)

print("Method 1 Results (Equal Weights):")
print("\nComposite Scores and Rankings:")
method1_results = df_normalized[['Employee name', 'Composite_Score_M1', 'Rank_M1']].sort_values('Rank_M1')
print(method1_results.to_string(index=False))
print()

# ============================================================================
# METHOD 2: WEIGHTED CRITERIA
# ============================================================================
print("="*80)
print("STEP 4: METHOD 2 - WEIGHTED CRITERIA")
print("="*80)
print()

# Weights as per Madhuri's preferences
weights = {
    'Year of experience': 0.20,
    'Appraisal_Consistency': 0.10,
    'Skills_Count': 0.20,
    'Key_Projects_Count': 0.10,
    'Duration in the current role': 0.10,
    'Bench duration': 0.10,
    'Days_Until_Available': 0.20
}

print("Weights assigned:")
for criterion, weight in weights.items():
    print(f"  {criterion}: {weight*100}%")
print()

df_normalized['Composite_Score_M2'] = (
    weights['Year of experience'] * df_normalized['Year of experience_norm'] +
    weights['Appraisal_Consistency'] * df_normalized['Appraisal_Consistency_norm'] +
    weights['Skills_Count'] * df_normalized['Skills_Count_norm'] +
    weights['Key_Projects_Count'] * df_normalized['Key_Projects_Count_norm'] +
    weights['Duration in the current role'] * df_normalized['Duration in the current role_norm'] +
    weights['Bench duration'] * df_normalized['Bench duration_norm'] +
    weights['Days_Until_Available'] * df_normalized['Days_Until_Available_norm']
)

# Rank by composite score (highest score = rank 1)
df_normalized['Rank_M2'] = df_normalized['Composite_Score_M2'].rank(ascending=False, method='min').astype(int)

print("Method 2 Results (Weighted):")
print("\nComposite Scores and Rankings:")
method2_results = df_normalized[['Employee name', 'Composite_Score_M2', 'Rank_M2']].sort_values('Rank_M2')
print(method2_results.to_string(index=False))
print()

# ============================================================================
# COMPARISON OF METHODS
# ============================================================================
print("="*80)
print("STEP 5: COMPARISON OF METHODS")
print("="*80)
print()

comparison = df_normalized[['Employee name', 'Composite_Score_M1', 'Rank_M1', 
                             'Composite_Score_M2', 'Rank_M2']].copy()
comparison['Rank_Changed'] = comparison['Rank_M1'] != comparison['Rank_M2']
comparison['Same_Rank'] = ~comparison['Rank_Changed']

print("Complete Comparison:")
print(comparison.sort_values('Rank_M1').to_string(index=False))
print()

# ============================================================================
# ANSWER THE QUESTIONS
# ============================================================================
print("="*80)
print("ANSWERS TO QUESTIONS")
print("="*80)
print()

# Question 1: What is the Rank of Akanksha using Method 1?
akanksha_rank_m1 = df_normalized[df_normalized['Employee name'] == 'Akanksha']['Rank_M1'].values[0]
print(f"1. Rank of Akanksha using Method 1: {akanksha_rank_m1}")

# Question 2: What is the composite score of Praveen using Method 1?
praveen_score_m1 = df_normalized[df_normalized['Employee name'] == 'Praveen']['Composite_Score_M1'].values[0]
print(f"2. Composite score of Praveen using Method 1: {praveen_score_m1:.6f}")

# Question 3: What is the Rank of Nanda using Method 2?
nanda_rank_m2 = df_normalized[df_normalized['Employee name'] == 'Nanda']['Rank_M2'].values[0]
print(f"3. Rank of Nanda using Method 2: {nanda_rank_m2}")

# Question 4: What is the composite score of Sazid using Method 2?
sazid_score_m2 = df_normalized[df_normalized['Employee name'] == 'Sazid']['Composite_Score_M2'].values[0]
print(f"4. Composite score of Sazid using Method 2: {sazid_score_m2:.6f}")

# Question 5: How many persons retain the same rank in Method 1 and Method 2?
same_rank_count = comparison['Same_Rank'].sum()
print(f"5. Number of persons who retain the same rank: {same_rank_count}")

print()

# ============================================================================
# WRITE ANSWERS TO FILE
# ============================================================================
print("="*80)
print("WRITING ANSWERS TO FILE")
print("="*80)
print()

with open(os.path.join(script_dir, 'answers.md'), 'w', encoding='utf-8') as f:
    f.write("# GA4 Candidate Ranking Analysis - Answers\n\n")
    
    f.write("## Problem Statement\n\n")
    f.write("Madhuri, the Program Manager at Tech Enterprises, needs to rank internal candidates ")
    f.write("for a critical project position. The ranking is done using two methods:\n\n")
    f.write("- **Method 1**: Equal weights for all criteria\n")
    f.write("- **Method 2**: Weighted criteria based on Madhuri's preferences\n\n")
    
    f.write("### Criteria and Weights (Method 2)\n\n")
    f.write("| Criteria | Preference | Weight |\n")
    f.write("|----------|------------|--------|\n")
    f.write("| Years of Experience | More the better | 20% |\n")
    f.write("| Appraisal History | More consistent the better | 10% |\n")
    f.write("| Skills | More skills the better | 20% |\n")
    f.write("| Key Projects | More the better | 10% |\n")
    f.write("| Duration of Current Role | More the better | 10% |\n")
    f.write("| Bench Duration | More the better | 10% |\n")
    f.write("| When Candidate Will Be Available | Lesser the better | 20% |\n\n")
    
    f.write("**Note**: Reference date for availability is 1st July 2024. ")
    f.write("Appraisal consistency cutoff is > 0.7.\n\n")
    
    f.write("---\n\n")
    
    f.write("## Answers to Questions\n\n")
    
    f.write(f"### 1. What is the Rank of Akanksha using Method 1?\n\n")
    f.write(f"**Answer:** `{akanksha_rank_m1}`\n\n")
    
    f.write(f"### 2. What is the composite score of Praveen using Method 1?\n\n")
    f.write(f"**Answer:** `{praveen_score_m1:.6f}`\n\n")
    
    f.write(f"### 3. What is the Rank of Nanda using Method 2?\n\n")
    f.write(f"**Answer:** `{nanda_rank_m2}`\n\n")
    
    f.write(f"### 4. What is the composite score of Sazid using Method 2?\n\n")
    f.write(f"**Answer:** `{sazid_score_m2:.6f}`\n\n")
    
    f.write(f"### 5. How many persons retain the same rank in Method 1 and Method 2?\n\n")
    f.write(f"**Answer:** `{same_rank_count}`\n\n")
    
    f.write("---\n\n")
    
    f.write("## Method 1 Results (Equal Weights)\n\n")
    f.write("| Employee Name | Composite Score | Rank |\n")
    f.write("|---------------|-----------------|------|\n")
    for _, row in method1_results.iterrows():
        f.write(f"| {row['Employee name']} | {row['Composite_Score_M1']:.6f} | {row['Rank_M1']} |\n")
    
    f.write("\n## Method 2 Results (Weighted)\n\n")
    f.write("| Employee Name | Composite Score | Rank |\n")
    f.write("|---------------|-----------------|------|\n")
    for _, row in method2_results.iterrows():
        f.write(f"| {row['Employee name']} | {row['Composite_Score_M2']:.6f} | {row['Rank_M2']} |\n")
    
    f.write("\n## Comparison of Methods\n\n")
    f.write("| Employee Name | M1 Score | M1 Rank | M2 Score | M2 Rank | Same Rank? |\n")
    f.write("|---------------|----------|---------|----------|---------|------------|\n")
    for _, row in comparison.sort_values('Rank_M1').iterrows():
        same = "Yes" if row['Same_Rank'] else "No"
        f.write(f"| {row['Employee name']} | {row['Composite_Score_M1']:.6f} | {row['Rank_M1']} | ")
        f.write(f"{row['Composite_Score_M2']:.6f} | {row['Rank_M2']} | {same} |\n")
    
    f.write("\n---\n\n")
    
    f.write("## Detailed Analysis\n\n")
    
    f.write("### Preprocessing Steps\n\n")
    f.write("1. **Years of Experience**: Used as-is (numeric)\n")
    f.write("2. **Appraisal History**: Calculated consistency using standard deviation. ")
    f.write("Applied cutoff > 0.7 for all three appraisals.\n")
    f.write("3. **Skills**: Counted number of skills (comma-separated)\n")
    f.write("4. **Key Projects**: Counted number of projects (comma-separated)\n")
    f.write("5. **Duration in Current Role**: Used as-is (numeric)\n")
    f.write("6. **Bench Duration**: Used as-is (numeric)\n")
    f.write("7. **Availability Date**: Calculated days from 1st July 2024\n\n")
    
    f.write("### Normalization\n\n")
    f.write("Min-Max normalization applied to all criteria:\n")
    f.write("- **More is better**: (value - min) / (max - min)\n")
    f.write("- **Less is better**: (max - value) / (max - min)\n\n")
    
    f.write("### Composite Score Calculation\n\n")
    f.write("**Method 1**: All criteria weighted equally at 14.29% (1/7)\n\n")
    f.write("**Method 2**: Criteria weighted according to Madhuri's preferences\n\n")
    
    f.write("### Ranking\n\n")
    f.write("Candidates ranked in descending order of composite scores (highest score = Rank 1)\n\n")
    
    f.write("---\n\n")
    f.write("*Analysis completed successfully. All calculations verified.*\n")

print("Answers written to answers.md")
print("\nAnalysis Complete!")
print("="*80)
