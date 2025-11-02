import pandas as pd
import numpy as np
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the datasets using absolute paths
df1 = pd.read_csv(os.path.join(script_dir, 'data1.csv'))
df2 = pd.read_csv(os.path.join(script_dir, 'data2.csv'))

# Task 1: Add Lang-Adj column (Language * 4)
# Insert after Language column
lang_col_index = df1.columns.get_loc('Language')
df1.insert(lang_col_index + 1, 'Lang-Adj', df1['Language'] * 4)

# Task 5: Add Total_Avg_Marks column (average of Maths, Physics, Chemistry, Lang-Adj)
df1['Total_Avg_Marks'] = df1[['Maths', 'Physics', 'Chemistry', 'Lang-Adj']].mean(axis=1)

# Task 6: Add Grade column based on Total_Avg_Marks
def assign_grade(marks):
    if marks >= 90:
        return 'A'
    elif marks >= 75:
        return 'B'
    elif marks >= 60:
        return 'C'
    elif marks >= 50:
        return 'D'
    elif marks >= 35:
        return 'E'
    else:
        return 'F'

df1['Grade'] = df1['Total_Avg_Marks'].apply(assign_grade)

# Task 7: Add Grade Description using VLOOKUP (merge with data2)
grade_dict = dict(zip(df2['Grade'], df2['Grade Description']))
df1['Grade Description'] = df1['Grade'].map(grade_dict)

# Task 2: Add Avg row with column averages
avg_row = pd.DataFrame({
    'Roll Number': ['Avg'],
    'Department': [''],
    'Maths': [df1['Maths'].mean()],
    'Physics': [df1['Physics'].mean()],
    'Chemistry': [df1['Chemistry'].mean()],
    'Language': [df1['Language'].mean()],
    'Lang-Adj': [df1['Lang-Adj'].mean()],
    'Total_Avg_Marks': [''],
    'Grade': [''],
    'Grade Description': ['']
})

# Task 3: Add Max row
max_row = pd.DataFrame({
    'Roll Number': ['Max'],
    'Department': [''],
    'Maths': [df1['Maths'].max()],
    'Physics': [df1['Physics'].max()],
    'Chemistry': [df1['Chemistry'].max()],
    'Language': [df1['Language'].max()],
    'Lang-Adj': [df1['Lang-Adj'].max()],
    'Total_Avg_Marks': [''],
    'Grade': [''],
    'Grade Description': ['']
})

# Task 4: Add Min row
min_row = pd.DataFrame({
    'Roll Number': ['Min'],
    'Department': [''],
    'Maths': [df1['Maths'].min()],
    'Physics': [df1['Physics'].min()],
    'Chemistry': [df1['Chemistry'].min()],
    'Language': [df1['Language'].min()],
    'Lang-Adj': [df1['Lang-Adj'].min()],
    'Total_Avg_Marks': [''],
    'Grade': [''],
    'Grade Description': ['']
})

# Concatenate all rows
df_final = pd.concat([df1, avg_row, max_row, min_row], ignore_index=True)

# Save the final dataframe
df_final.to_csv(os.path.join(script_dir, 'output.csv'), index=False)

# Answer the questions
print("="*50)
print("ANSWERS TO QUESTIONS")
print("="*50)

# Question 1: Maximum score in Maths
max_maths = int(df1['Maths'].max())
print(f"1. Maximum score achieved in Maths: {max_maths}")

# Question 2: Minimum score in Physics
min_physics = int(df1['Physics'].min())
print(f"2. Minimum score achieved in Physics: {min_physics}")

# Question 3: Average score in Chemistry
avg_chemistry = float(df1['Chemistry'].mean())
print(f"3. Average score achieved in Chemistry: {avg_chemistry}")

# Question 4: Average score in Lang-Adj
avg_lang_adj = float(df1['Lang-Adj'].mean())
print(f"4. Average score achieved in Lang-Adj: {avg_lang_adj}")

# Question 5: Count MECH students with D grade
mech_d_count = int(len(df1[(df1['Department'] == 'MECH') & (df1['Grade'] == 'D')]))
print(f"5. Total number of MECH department students who got D grade: {mech_d_count}")

# Question 6: Count CS students with C grade
cs_c_count = int(len(df1[(df1['Department'] == 'CS') & (df1['Grade'] == 'C')]))
print(f"6. Total number of CS department students who got C grade: {cs_c_count}")

print("="*50)

# Create answer.md file
with open(os.path.join(script_dir, 'answer.md'), 'w', encoding='utf-8') as f:
    f.write("# Data Analysis Results\n\n")
    f.write("## Operations Performed\n\n")
    f.write("1. [DONE] Added Lang-Adj column (Language × 4)\n")
    f.write("2. [DONE] Added Avg row with column averages\n")
    f.write("3. [DONE] Added Max row with maximum scores\n")
    f.write("4. [DONE] Added Min row with minimum scores\n")
    f.write("5. [DONE] Added Total_Avg_Marks column\n")
    f.write("6. [DONE] Added Grade column with grading logic\n")
    f.write("7. [DONE] Added Grade Description using VLOOKUP\n\n")
    
    f.write("## Answers to Questions\n\n")
    f.write(f"1. **Maximum score achieved in Maths:** {max_maths}\n\n")
    f.write(f"2. **Minimum score achieved in Physics:** {min_physics}\n\n")
    f.write(f"3. **Average score achieved in Chemistry:** {avg_chemistry:.2f}\n\n")
    f.write(f"4. **Average score achieved in Lang-Adj:** {avg_lang_adj:.2f}\n\n")
    f.write(f"5. **Total number of MECH department students who got D grade:** {mech_d_count}\n\n")
    f.write(f"6. **Total number of CS department students who got C grade:** {cs_c_count}\n\n")
    
    f.write("## Summary Statistics\n\n")
    f.write("| Statistic | Maths | Physics | Chemistry | Lang-Adj |\n")
    f.write("|-----------|-------|---------|-----------|----------|\n")
    f.write(f"| Average   | {df1['Maths'].mean():.2f} | {df1['Physics'].mean():.2f} | {df1['Chemistry'].mean():.2f} | {df1['Lang-Adj'].mean():.2f} |\n")
    f.write(f"| Maximum   | {df1['Maths'].max()} | {df1['Physics'].max()} | {df1['Chemistry'].max()} | {df1['Lang-Adj'].max()} |\n")
    f.write(f"| Minimum   | {df1['Maths'].min()} | {df1['Physics'].min()} | {df1['Chemistry'].min()} | {df1['Lang-Adj'].min()} |\n\n")
    
    f.write("## Grade Distribution\n\n")
    grade_counts = df1['Grade'].value_counts().sort_index()
    for grade in ['A', 'B', 'C', 'D', 'E', 'F']:
        count = grade_counts.get(grade, 0)
        f.write(f"- **Grade {grade}:** {count} students\n")
    
    f.write("\n## Department-wise Grade Distribution\n\n")
    dept_grade = pd.crosstab(df1['Department'], df1['Grade'])
    f.write(dept_grade.to_markdown())
    f.write("\n\n*Note: The processed data has been saved to output.csv*\n")

print("\nResults saved to answer.md")
print("Processed data saved to output.csv")
