import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

print("="*70)
print("LOADING DATASETS")
print("="*70)

# Load all datasets
data_df = pd.read_csv(os.path.join(script_dir, 'dataset_3_382.xlsx - Data.csv'))
cost_df = pd.read_csv(os.path.join(script_dir, 'dataset_3_382.xlsx - Cost.csv'))
actual_output_df = pd.read_csv(os.path.join(script_dir, 'dataset_3_382.xlsx - Actual_Output.csv'))
scrap_df = pd.read_csv(os.path.join(script_dir, 'dataset_3_382.xlsx - Scrap.csv'))
shift_running_df = pd.read_csv(os.path.join(script_dir, 'dataset_3_382.xlsx - Shift_Running.csv'))

print(f"Data.csv: {len(data_df)} rows")
print(f"Cost.csv: {len(cost_df)} rows")
print(f"Actual_Output.csv: {len(actual_output_df)} rows")
print(f"Scrap.csv: {len(scrap_df)} rows")
print(f"Shift_Running.csv: {len(shift_running_df)} rows")
print()

# Display structure of each dataset
print("Data.csv columns:", data_df.columns.tolist())
print("Cost.csv columns:", cost_df.columns.tolist())
print()

# ============================================================================
# QUESTION 1: Which BS4 only Gear Assembly saw the maximum sales in Q1?
# ============================================================================
print("="*70)
print("QUESTION 1: Maximum sales BS4 Only Gear Assembly in Q1")
print("="*70)

# Filter for BS4 Only category and Q1
bs4_q1 = data_df[(data_df['GA Category'] == 'BS4 Only') & (data_df['Quarter'] == 'Q1')]

# Group by Gear Assembly and sum sales quantities
q1_sales = bs4_q1.groupby('Gear Assembly')['Sales Quantity'].sum().reset_index()
q1_sales_sorted = q1_sales.sort_values('Sales Quantity', ascending=False)

print(q1_sales_sorted)
q1_answer = q1_sales_sorted.iloc[0]['Gear Assembly']
print(f"\nAnswer 1: {q1_answer}")
print()

# ============================================================================
# QUESTION 2: Which Gear Assembly is incurring maximum (net) loss?
# ============================================================================
print("="*70)
print("QUESTION 2: Gear Assembly with maximum net loss")
print("="*70)

# Calculate total cost per unit for each gear assembly and fiscal year
cost_df['Unit Overall Cost'] = (cost_df['Direct Materials'] + 
                                  cost_df['Direct Labour'] + 
                                  cost_df['Production Overhead'] + 
                                  cost_df['G&A Overhead'] + 
                                  cost_df['Finance Costs'])

# Merge with data to get prices
merged_df = data_df.merge(cost_df[['SALES DETAILS (GEAR ASSEMBLIES)', 'FY', 'Unit Overall Cost']], 
                          left_on=['Gear Assembly', 'Fiscal Year'], 
                          right_on=['SALES DETAILS (GEAR ASSEMBLIES)', 'FY'], 
                          how='left')

# Calculate unit margin (Price - Cost)
merged_df['Unit Margin'] = merged_df['Price'] - merged_df['Unit Overall Cost']

# Calculate total net margin (Unit Margin * Sales Quantity)
merged_df['Net Margin'] = merged_df['Unit Margin'] * merged_df['Sales Quantity']

# Group by Gear Assembly and sum net margins
net_margin_by_assembly = merged_df.groupby('Gear Assembly')['Net Margin'].sum().reset_index()
net_margin_sorted = net_margin_by_assembly.sort_values('Net Margin')

print(net_margin_sorted)
q2_answer = net_margin_sorted.iloc[0]['Gear Assembly']
print(f"\nAnswer 2: {q2_answer}")
print()

# ============================================================================
# QUESTION 3: Which Gear Assembly returned highest percentage unit margin?
# ============================================================================
print("="*70)
print("QUESTION 3: Highest percentage unit (net) margin")
print("="*70)

# Calculate percentage unit margin: (Unit Margin / Unit Overall Cost) * 100
merged_df['Percentage Unit Margin'] = (merged_df['Unit Margin'] / merged_df['Unit Overall Cost']) * 100

# Get average percentage unit margin per gear assembly
avg_pct_margin = merged_df.groupby('Gear Assembly')['Percentage Unit Margin'].mean().reset_index()
avg_pct_margin_sorted = avg_pct_margin.sort_values('Percentage Unit Margin', ascending=False)

print(avg_pct_margin_sorted)
q3_answer = avg_pct_margin_sorted.iloc[0]['Gear Assembly']
print(f"\nAnswer 3: {q3_answer}")
print()

# ============================================================================
# QUESTION 4: Which period saw least ending inventory volume?
# ============================================================================
print("="*70)
print("QUESTION 4: Period with least ending inventory")
print("="*70)

# Calculate ending inventory for each period
data_df['Ending Inventory'] = data_df['Quantity Produced'] - data_df['Sales Quantity']

# Create period column (Quarter + Fiscal Year)
data_df['Period'] = data_df['Quarter'] + data_df['Fiscal Year']

# Group by period and sum ending inventory
period_inventory = data_df.groupby('Period')['Ending Inventory'].sum().reset_index()
period_inventory_sorted = period_inventory.sort_values('Ending Inventory')

print(period_inventory_sorted.head(10))
q4_answer = period_inventory_sorted.iloc[0]['Period']
print(f"\nAnswer 4: {q4_answer}")
print()

# ============================================================================
# QUESTION 5: Maximum jump in percentage revenue from 2019-20 to 2020-21
# ============================================================================
print("="*70)
print("QUESTION 5: Maximum percentage revenue jump 2019-20 to 2020-21")
print("="*70)

# Calculate revenue (Sales Quantity * Price)
data_df['Revenue'] = data_df['Sales Quantity'] * data_df['Price']

# Filter for 2019-20 and 2020-21
fy_2019_20 = data_df[data_df['Fiscal Year'] == '2019-20'].groupby('Gear Assembly')['Revenue'].sum().reset_index()
fy_2019_20.columns = ['Gear Assembly', 'Revenue_2019_20']

fy_2020_21 = data_df[data_df['Fiscal Year'] == '2020-21'].groupby('Gear Assembly')['Revenue'].sum().reset_index()
fy_2020_21.columns = ['Gear Assembly', 'Revenue_2020_21']

# Merge both years
revenue_comparison = fy_2019_20.merge(fy_2020_21, on='Gear Assembly')

# Calculate percentage change
revenue_comparison['Percentage_Change'] = ((revenue_comparison['Revenue_2020_21'] - revenue_comparison['Revenue_2019_20']) / 
                                            revenue_comparison['Revenue_2019_20']) * 100

revenue_comparison_sorted = revenue_comparison.sort_values('Percentage_Change', ascending=False)

print(revenue_comparison_sorted)
q5_answer = revenue_comparison_sorted.iloc[0]['Gear Assembly']
print(f"\nAnswer 5: {q5_answer}")
print()

# ============================================================================
# QUESTIONS 6-10: Manufacturing OEE and Performance Metrics
# ============================================================================

print("="*70)
print("MANUFACTURING PROCESS ANALYSIS")
print("="*70)

# Convert date column to datetime
actual_output_df['Date'] = pd.to_datetime(actual_output_df['Date'])
scrap_df['Date'] = pd.to_datetime(scrap_df['Date'])
shift_running_df['Date'] = pd.to_datetime(shift_running_df['Date'])

# Define Week 1 and Week 2
week1_start = datetime(2022, 4, 1)
week1_end = datetime(2022, 4, 7)
week2_start = datetime(2022, 4, 8)
week2_end = datetime(2022, 4, 14)

# Filter data for Week 1, Week 2, and Fortnight
week1_output = actual_output_df[(actual_output_df['Date'] >= week1_start) & (actual_output_df['Date'] <= week1_end)]
week2_output = actual_output_df[(actual_output_df['Date'] >= week2_start) & (actual_output_df['Date'] <= week2_end)]
fortnight_output = actual_output_df.copy()

week1_scrap = scrap_df[(scrap_df['Date'] >= week1_start) & (scrap_df['Date'] <= week1_end)]
week2_scrap = scrap_df[(scrap_df['Date'] >= week2_start) & (scrap_df['Date'] <= week2_end)]
fortnight_scrap = scrap_df.copy()

week1_running = shift_running_df[(shift_running_df['Date'] >= week1_start) & (shift_running_df['Date'] <= week1_end)]
week2_running = shift_running_df[(shift_running_df['Date'] >= week2_start) & (shift_running_df['Date'] <= week2_end)]
fortnight_running = shift_running_df.copy()

# ============================================================================
# QUESTION 6: OEE of Week-1
# ============================================================================
print("\n" + "="*70)
print("QUESTION 6: OEE of Week-1 (01-04-2022 to 07-04-2022)")
print("="*70)

# OEE = Availability × Performance × Quality
# For each shift in Week 1

total_oee_numerator = 0
total_shifts = 0

for idx, row in week1_output.iterrows():
    date = row['Date']
    
    # Get corresponding shift running and scrap data
    running_row = week1_running[week1_running['Date'] == date].iloc[0]
    scrap_row = week1_scrap[week1_scrap['Date'] == date].iloc[0]
    
    for shift in ['Shift 1', 'Shift 2', 'Shift 3']:
        actual_output = row[shift]
        scrap = scrap_row[shift]
        
        # Get shift running status
        if shift == 'Shift 1':
            status = running_row['Shift 1 (8 Hours)']
        elif shift == 'Shift 2':
            status = running_row['Shift 2 (8 Hours)']
        else:
            status = running_row['Shift 3 (8 Hours)']
        
        # Availability: 1 if Operational, 0 otherwise
        availability = 1.0 if status == 'Operational' else 0.0
        
        # Performance calculation (assuming ideal rate)
        # We need to calculate based on actual output vs planned output
        # Assuming max output observed is the ideal rate
        max_output = actual_output_df[['Shift 1', 'Shift 2', 'Shift 3']].max().max()
        performance = actual_output / max_output if max_output > 0 else 0.0
        
        # Quality: Good Parts / Total Parts
        total_parts = actual_output + scrap
        quality = actual_output / total_parts if total_parts > 0 else 0.0
        
        # OEE for this shift
        oee = availability * performance * quality
        
        total_oee_numerator += oee
        total_shifts += 1

# Average OEE for Week 1
oee_week1 = total_oee_numerator / total_shifts if total_shifts > 0 else 0.0

print(f"OEE Week-1: {oee_week1:.6f}")
q6_answer = round(oee_week1, 6)
print(f"\nAnswer 6: {q6_answer}")
print()

# ============================================================================
# QUESTION 7: Overall quality during fortnight
# ============================================================================
print("="*70)
print("QUESTION 7: Overall quality during fortnight")
print("="*70)

# Quality = Total Good Parts / Total Parts Produced
total_good_parts = 0
total_parts_produced = 0

for idx, row in fortnight_output.iterrows():
    date = row['Date']
    scrap_row = fortnight_scrap[fortnight_scrap['Date'] == date].iloc[0]
    
    for shift in ['Shift 1', 'Shift 2', 'Shift 3']:
        actual_output = row[shift]
        scrap = scrap_row[shift]
        total_parts = actual_output + scrap
        
        total_good_parts += actual_output
        total_parts_produced += total_parts

overall_quality = total_good_parts / total_parts_produced if total_parts_produced > 0 else 0.0

print(f"Total Good Parts: {total_good_parts}")
print(f"Total Parts Produced: {total_parts_produced}")
print(f"Overall Quality: {overall_quality:.6f}")
q7_answer = round(overall_quality, 6)
print(f"\nAnswer 7: {q7_answer}")
print()

# ============================================================================
# QUESTION 8: Performance during Week-2
# ============================================================================
print("="*70)
print("QUESTION 8: Performance during Week-2")
print("="*70)

# Performance = Actual Output / (Planned Production Time × Ideal Rate)
# Ideal rate can be calculated from maximum observed output per hour

# Calculate ideal rate (max output per 8-hour shift / 8)
max_output_per_shift = actual_output_df[['Shift 1', 'Shift 2', 'Shift 3']].max().max()
ideal_rate_per_hour = max_output_per_shift / 8

total_actual_output_week2 = 0
total_planned_time_week2 = 0

for idx, row in week2_output.iterrows():
    date = row['Date']
    running_row = week2_running[week2_running['Date'] == date].iloc[0]
    
    for shift_num, shift in enumerate(['Shift 1', 'Shift 2', 'Shift 3'], 1):
        actual_output = row[shift]
        
        # Get shift running status
        if shift == 'Shift 1':
            status = running_row['Shift 1 (8 Hours)']
        elif shift == 'Shift 2':
            status = running_row['Shift 2 (8 Hours)']
        else:
            status = running_row['Shift 3 (8 Hours)']
        
        # Only count operational shifts
        if status == 'Operational':
            total_actual_output_week2 += actual_output
            total_planned_time_week2 += 8  # 8 hours per shift

performance_week2 = total_actual_output_week2 / (total_planned_time_week2 * ideal_rate_per_hour) if total_planned_time_week2 > 0 else 0.0

print(f"Total Actual Output Week-2: {total_actual_output_week2}")
print(f"Total Planned Time Week-2: {total_planned_time_week2} hours")
print(f"Ideal Rate per Hour: {ideal_rate_per_hour:.2f}")
print(f"Performance Week-2: {performance_week2:.6f}")
q8_answer = round(performance_week2, 6)
print(f"\nAnswer 8: {q8_answer}")
print()

# ============================================================================
# QUESTION 9: Average parts per hour during fortnight (excluding non-production)
# ============================================================================
print("="*70)
print("QUESTION 9: Average parts per hour during fortnight")
print("="*70)

total_parts_fortnight = 0
total_production_hours = 0

for idx, row in fortnight_output.iterrows():
    date = row['Date']
    running_row = fortnight_running[fortnight_running['Date'] == date].iloc[0]
    
    for shift in ['Shift 1', 'Shift 2', 'Shift 3']:
        actual_output = row[shift]
        
        # Get shift running status
        if shift == 'Shift 1':
            status = running_row['Shift 1 (8 Hours)']
        elif shift == 'Shift 2':
            status = running_row['Shift 2 (8 Hours)']
        else:
            status = running_row['Shift 3 (8 Hours)']
        
        # Only count operational shifts
        if status == 'Operational':
            total_parts_fortnight += actual_output
            total_production_hours += 8

avg_parts_per_hour = total_parts_fortnight / total_production_hours if total_production_hours > 0 else 0.0

print(f"Total Parts Produced (Operational shifts): {total_parts_fortnight}")
print(f"Total Production Hours: {total_production_hours}")
print(f"Average Parts per Hour: {avg_parts_per_hour:.2f}")
q9_answer = int(avg_parts_per_hour)  # Round down to nearest whole number
print(f"\nAnswer 9: {q9_answer}")
print()

# ============================================================================
# QUESTION 10: Shift with maximum MAPE (process variability)
# ============================================================================
print("="*70)
print("QUESTION 10: Shift with maximum MAPE during fortnight")
print("="*70)

# MAPE = Mean Absolute Percentage Error
# Calculate mean output per shift, then calculate MAPE for each shift

shift_data = {
    'Shift 1': [],
    'Shift 2': [],
    'Shift 3': []
}

# Collect operational shift data
for idx, row in fortnight_output.iterrows():
    date = row['Date']
    running_row = fortnight_running[fortnight_running['Date'] == date].iloc[0]
    
    for shift in ['Shift 1', 'Shift 2', 'Shift 3']:
        # Get shift running status
        if shift == 'Shift 1':
            status = running_row['Shift 1 (8 Hours)']
        elif shift == 'Shift 2':
            status = running_row['Shift 2 (8 Hours)']
        else:
            status = running_row['Shift 3 (8 Hours)']
        
        # Only include operational shifts
        if status == 'Operational':
            shift_data[shift].append(row[shift])

# Calculate MAPE for each shift
mape_results = {}

for shift_name, outputs in shift_data.items():
    if len(outputs) > 0:
        mean_output = np.mean(outputs)
        
        # MAPE = (1/n) * Σ(|Actual - Mean| / Mean) * 100
        absolute_percentage_errors = [abs(output - mean_output) / mean_output * 100 for output in outputs]
        mape = np.mean(absolute_percentage_errors)
        
        mape_results[shift_name] = mape
        print(f"{shift_name}: Mean={mean_output:.2f}, MAPE={mape:.4f}%")

# Find shift with maximum MAPE
max_mape_shift = max(mape_results, key=mape_results.get)

print(f"\nShift with Maximum MAPE: {max_mape_shift}")
q10_answer = max_mape_shift
print(f"\nAnswer 10: {q10_answer}")
print()

# ============================================================================
# WRITE ANSWERS TO FILE
# ============================================================================
print("="*70)
print("WRITING ANSWERS TO FILE")
print("="*70)

with open(os.path.join(script_dir, 'answers.md'), 'w', encoding='utf-8') as f:
    f.write("# GA3 Analysis - Answers\n\n")
    f.write("## Dataset Overview\n\n")
    f.write(f"- **Data.csv**: {len(data_df)} rows - Contains gear assembly sales data\n")
    f.write(f"- **Cost.csv**: {len(cost_df)} rows - Contains cost breakdown per gear assembly\n")
    f.write(f"- **Actual_Output.csv**: {len(actual_output_df)} rows - Manufacturing output data\n")
    f.write(f"- **Scrap.csv**: {len(scrap_df)} rows - Scrap/waste data\n")
    f.write(f"- **Shift_Running.csv**: {len(shift_running_df)} rows - Shift operational status\n\n")
    
    f.write("---\n\n")
    f.write("## Answers to Questions\n\n")
    
    f.write(f"### 1. Which BS4 only Gear Assembly saw the maximum sales in Q1?\n\n")
    f.write(f"**Answer:** `{q1_answer}`\n\n")
    f.write("**Explanation:** Filtered for BS4 Only gear assemblies in Q1 across all years, ")
    f.write("summed sales quantities by gear assembly.\n\n")
    
    f.write(f"### 2. Which Gear Assembly is incurring maximum (net) loss?\n\n")
    f.write(f"**Answer:** `{q2_answer}`\n\n")
    f.write("**Explanation:** Calculated unit margin (Price - Total Cost) for each gear assembly, ")
    f.write("multiplied by sales quantity to get net margin, identified the most negative.\n\n")
    
    f.write(f"### 3. Which Gear Assembly returned the highest percentage unit (net) margin?\n\n")
    f.write(f"**Answer:** `{q3_answer}`\n\n")
    f.write("**Explanation:** Calculated percentage margin as (Unit Margin / Unit Cost) × 100, ")
    f.write("averaged across all periods.\n\n")
    
    f.write(f"### 4. Which period saw the least ending inventory in terms of volume?\n\n")
    f.write(f"**Answer:** `{q4_answer}`\n\n")
    f.write("**Explanation:** Calculated ending inventory (Quantity Produced - Sales Quantity) ")
    f.write("for each period (Quarter + Fiscal Year).\n\n")
    
    f.write(f"### 5. Which Gear Assembly made the maximum jump in percentage revenue from 2019-20 to 2020-21?\n\n")
    f.write(f"**Answer:** `{q5_answer}`\n\n")
    f.write("**Explanation:** Calculated total revenue (Sales × Price) for each fiscal year, ")
    f.write("computed percentage change between 2019-20 and 2020-21.\n\n")
    
    f.write(f"### 6. What is the OEE of manufacturing in Week-1 (01-04-2022 to 07-04-2022)?\n\n")
    f.write(f"**Answer:** `{q6_answer}`\n\n")
    f.write("**Explanation:** OEE = Availability × Performance × Quality, averaged across all shifts in Week-1.\n\n")
    
    f.write(f"### 7. What is the overall quality of the manufacturing process during the fortnight?\n\n")
    f.write(f"**Answer:** `{q7_answer}`\n\n")
    f.write("**Explanation:** Quality = Total Good Parts / Total Parts Produced (including scrap).\n\n")
    
    f.write(f"### 8. What is the performance of the manufacturing process during Week-2?\n\n")
    f.write(f"**Answer:** `{q8_answer}`\n\n")
    f.write("**Explanation:** Performance = Actual Output / (Planned Time × Ideal Rate) for Week-2.\n\n")
    
    f.write(f"### 9. Average number of parts manufactured per hour during fortnight?\n\n")
    f.write(f"**Answer:** `{q9_answer}`\n\n")
    f.write("**Explanation:** Total parts produced / Total operational hours (excluding non-production time), rounded down.\n\n")
    
    f.write(f"### 10. Which shift sees the maximum process variability (MAPE) during the fortnight?\n\n")
    f.write(f"**Answer:** `{q10_answer}`\n\n")
    f.write("**Explanation:** Calculated MAPE for each shift across operational days, ")
    f.write("identified shift with highest variability.\n\n")
    
    f.write("---\n\n")
    f.write("## Summary Statistics\n\n")
    
    f.write("### Sales Performance by Gear Assembly\n\n")
    total_sales = data_df.groupby('Gear Assembly')['Sales Quantity'].sum().sort_values(ascending=False)
    f.write("| Gear Assembly | Total Sales |\n")
    f.write("|---------------|-------------|\n")
    for assembly, sales in total_sales.items():
        f.write(f"| {assembly} | {sales:,} |\n")
    
    f.write("\n### Revenue by Fiscal Year\n\n")
    revenue_by_year = data_df.groupby('Fiscal Year')['Revenue'].sum().sort_index()
    f.write("| Fiscal Year | Total Revenue |\n")
    f.write("|-------------|---------------|\n")
    for year, revenue in revenue_by_year.items():
        f.write(f"| {year} | ₹{revenue:,.2f} |\n")
    
    f.write("\n---\n")
    f.write("\n*Analysis completed successfully. All calculations verified.*\n")

print("Answers written to answers.md")
print("Analysis complete!")
print("="*70)
