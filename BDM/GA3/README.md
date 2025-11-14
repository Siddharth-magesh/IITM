# GA3 Data Analysis Project

## Overview

This directory contains a comprehensive analysis of gear assembly sales, cost, and manufacturing data. The analysis answers 10 specific business and operational questions using Python and pandas.

## Files in This Directory

### Data Files (Input)
- `dataset_3_382.xlsx - Data.csv` - Sales data for 6 gear assemblies across 3 fiscal years
- `dataset_3_382.xlsx - Cost.csv` - Cost breakdown by gear assembly and fiscal year
- `dataset_3_382.xlsx - Actual_Output.csv` - Daily production output by shift (April 2022)
- `dataset_3_382.xlsx - Scrap.csv` - Daily scrap/waste by shift
- `dataset_3_382.xlsx - Shift_Running.csv` - Shift operational status

### Analysis Files (Output)
- **`main.py`** - Complete Python analysis script with all calculations
- **`answers.md`** - Detailed answers with explanations and summary statistics
- **`FINAL_ANSWERS.md`** - Quick reference for all 10 answers
- **`SUMMARY.md`** - Analysis summary with calculation methodologies
- **`README.md`** - This file

## How to Run

To execute the analysis:

```bash
cd d:\IITM-1\workspace
uv run ../BDM/GA3/main.py
```

Or from the GA3 directory:

```bash
cd d:\IITM-1\BDM\GA3
python main.py
```

## Questions Analyzed

### Business & Sales Analysis (Q1-Q5)
1. Maximum sales BS4 Only gear assembly in Q1
2. Gear assembly with maximum net loss
3. Highest percentage unit margin
4. Period with least ending inventory
5. Maximum revenue jump percentage (2019-20 to 2020-21)

### Manufacturing Process Analysis (Q6-Q10)
6. Overall Equipment Effectiveness (OEE) - Week 1
7. Overall quality during fortnight
8. Performance during Week 2
9. Average parts manufactured per hour
10. Shift with maximum process variability (MAPE)

## Key Metrics Calculated

### Financial Metrics
- **Unit Margin** = Price - Unit Overall Cost
- **Net Margin** = Unit Margin × Sales Quantity
- **Percentage Unit Margin** = (Unit Margin / Unit Overall Cost) × 100
- **Revenue** = Sales Quantity × Price
- **Ending Inventory** = Quantity Produced - Sales Quantity

### Manufacturing Metrics
- **OEE** = Availability × Performance × Quality
- **Availability** = Operational Status (1 if operational, 0 otherwise)
- **Performance** = Actual Output / (Planned Time × Ideal Rate)
- **Quality** = Good Parts / Total Parts Produced
- **MAPE** = Mean(|Actual - Mean| / Mean) × 100

## Dependencies

- Python 3.x
- pandas
- numpy

Install dependencies:
```bash
uv add pandas numpy
```

## Results

All results are documented in:
- **`answers.md`** - For detailed explanations
- **`FINAL_ANSWERS.md`** - For quick reference

## Verification

All calculations have been verified and tested. The script includes:
- Data validation
- Comprehensive error checking
- Statistical verification
- Output formatting

## Analysis Date

November 14, 2025

---

*For questions or clarifications about the analysis, refer to the detailed explanations in `answers.md`.*
