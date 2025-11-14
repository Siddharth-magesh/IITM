# GA3 Analysis Summary

## Project Completed Successfully ✓

All 10 questions have been analyzed and answered using Python data analysis.

---

## Quick Reference - Final Answers

| Question | Answer |
|----------|--------|
| 1. BS4 Only Gear Assembly with max Q1 sales | **Gear Assembly 2 (BS4)** |
| 2. Gear Assembly with maximum net loss | **Gear Assembly 3 (BS4/6)** |
| 3. Highest percentage unit margin | **Gear Assembly 2 (BS4)** |
| 4. Period with least ending inventory | **Q22021-22** |
| 5. Maximum % revenue jump (2019-20 to 2020-21) | **Gear Assembly 3 (BS4/6)** |
| 6. OEE of Week-1 (01-04-2022 to 07-04-2022) | **0.816814** |
| 7. Overall quality during fortnight | **0.994815** |
| 8. Performance during Week-2 | **0.904245** |
| 9. Avg parts per hour during fortnight | **522** |
| 10. Shift with max process variability (MAPE) | **Shift 3** |

---

## Data Files Analyzed

1. **dataset_3_382.xlsx - Data.csv** (174 rows)
   - Gear assembly sales data by month, quarter, and fiscal year
   - Contains: Gear Assembly, Category, Sales Quantity, Price, etc.

2. **dataset_3_382.xlsx - Cost.csv** (18 rows)
   - Cost breakdown per gear assembly and fiscal year
   - Contains: Direct Materials, Labour, Overhead, Finance Costs

3. **dataset_3_382.xlsx - Actual_Output.csv** (14 rows)
   - Daily production output by shift (Apr 1-14, 2022)
   - 3 shifts per day, 8 hours each

4. **dataset_3_382.xlsx - Scrap.csv** (14 rows)
   - Daily scrap/waste by shift
   - Used for quality calculations

5. **dataset_3_382.xlsx - Shift_Running.csv** (14 rows)
   - Shift operational status (Operational, Maintenance, Breakdown, Power Cut)
   - Used for availability and OEE calculations

---

## Key Calculations Explained

### Questions 1-5: Sales & Financial Analysis

**Q1:** Filtered BS4 Only gear assemblies, Q1 periods → Summed sales quantities
- Gear Assembly 2 (BS4): 51,064 units
- Gear Assembly 1 (BS4): 47,454 units

**Q2:** Unit Margin = Price - Total Cost; Net Margin = Unit Margin × Sales Quantity
- Gear Assembly 3 (BS4/6) had net loss of -₹6,150,909

**Q3:** Percentage Unit Margin = (Unit Margin / Unit Cost) × 100
- Gear Assembly 2 (BS4): 28.56%

**Q4:** Ending Inventory = Quantity Produced - Sales Quantity
- Q22021-22 had lowest inventory: 5,814 units

**Q5:** Revenue = Sales Quantity × Price; % Change = (2020-21 - 2019-20) / 2019-20 × 100
- Gear Assembly 3 (BS4/6): 11.94% increase

### Questions 6-10: Manufacturing Process Analysis

**Q6 - OEE (Overall Equipment Effectiveness):**
```
OEE = Availability × Performance × Quality
- Availability: 1 if Operational, 0 otherwise
- Performance: Actual Output / Ideal Output
- Quality: Good Parts / Total Parts
Week-1 Average OEE: 0.816814
```

**Q7 - Overall Quality:**
```
Quality = Total Good Parts / (Good Parts + Scrap)
Fortnight: 150,613 / 151,398 = 0.994815 (99.48%)
```

**Q8 - Performance Week-2:**
```
Performance = Actual Output / (Planned Time × Ideal Rate)
Ideal Rate = Max Output / 8 hours = 577.38 parts/hour
Week-2: 71,004 / (136 × 577.38) = 0.904245
```

**Q9 - Average Parts per Hour:**
```
Only counted operational shifts (excluded maintenance, breakdown, power cut)
150,613 parts / 288 hours = 522.96 → Rounded down to 522
```

**Q10 - MAPE (Process Variability):**
```
MAPE = Mean Absolute Percentage Error
For each shift:
- Shift 1: 2.93%
- Shift 2: 2.29%
- Shift 3: 3.93% ← Maximum variability
```

---

## Files Generated

1. **main.py** - Complete Python analysis script
2. **answers.md** - Detailed answers with explanations
3. **SUMMARY.md** - This summary document

---

## Verification Status

✓ All data loaded successfully  
✓ All calculations verified  
✓ All answers generated and documented  
✓ Output files created  

**Analysis Date:** November 14, 2025  
**Status:** COMPLETE
