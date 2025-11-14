# GA3 Analysis - Answers

## Dataset Overview

- **Data.csv**: 174 rows - Contains gear assembly sales data
- **Cost.csv**: 18 rows - Contains cost breakdown per gear assembly
- **Actual_Output.csv**: 14 rows - Manufacturing output data
- **Scrap.csv**: 14 rows - Scrap/waste data
- **Shift_Running.csv**: 14 rows - Shift operational status

---

## Answers to Questions

### 1. Which BS4 only Gear Assembly saw the maximum sales in Q1?

**Answer:** `Gear Assembly 2 (BS4)`

**Explanation:** Filtered for BS4 Only gear assemblies in Q1 across all years, summed sales quantities by gear assembly.

### 2. Which Gear Assembly is incurring maximum (net) loss?

**Answer:** `Gear Assembly 3 (BS4/6)`

**Explanation:** Calculated unit margin (Price - Total Cost) for each gear assembly, multiplied by sales quantity to get net margin, identified the most negative.

### 3. Which Gear Assembly returned the highest percentage unit (net) margin?

**Answer:** `Gear Assembly 2 (BS4)`

**Explanation:** Calculated percentage margin as (Unit Margin / Unit Cost) × 100, averaged across all periods.

### 4. Which period saw the least ending inventory in terms of volume?

**Answer:** `Q22021-22`

**Explanation:** Calculated ending inventory (Quantity Produced - Sales Quantity) for each period (Quarter + Fiscal Year).

### 5. Which Gear Assembly made the maximum jump in percentage revenue from 2019-20 to 2020-21?

**Answer:** `Gear Assembly 3 (BS4/6)`

**Explanation:** Calculated total revenue (Sales × Price) for each fiscal year, computed percentage change between 2019-20 and 2020-21.

### 6. What is the OEE of manufacturing in Week-1 (01-04-2022 to 07-04-2022)?

**Answer:** `0.816814`

**Explanation:** OEE = Availability × Performance × Quality, averaged across all shifts in Week-1.

### 7. What is the overall quality of the manufacturing process during the fortnight?

**Answer:** `0.994815`

**Explanation:** Quality = Total Good Parts / Total Parts Produced (including scrap).

### 8. What is the performance of the manufacturing process during Week-2?

**Answer:** `0.904245`

**Explanation:** Performance = Actual Output / (Planned Time × Ideal Rate) for Week-2.

### 9. Average number of parts manufactured per hour during fortnight?

**Answer:** `522`

**Explanation:** Total parts produced / Total operational hours (excluding non-production time), rounded down.

### 10. Which shift sees the maximum process variability (MAPE) during the fortnight?

**Answer:** `Shift 3`

**Explanation:** Calculated MAPE for each shift across operational days, identified shift with highest variability.

---

## Summary Statistics

### Sales Performance by Gear Assembly

| Gear Assembly | Total Sales |
|---------------|-------------|
| Gear Assembly 2 (BS4) | 163,299 |
| Gear Assembly 1 (BS4) | 159,707 |
| Gear Assembly 6 (BS6) | 158,202 |
| Gear Assembly 4 (BS4/6) | 157,924 |
| Gear Assembly 5 (BS6) | 156,433 |
| Gear Assembly 3 (BS4/6) | 156,140 |

### Revenue by Fiscal Year

| Fiscal Year | Total Revenue |
|-------------|---------------|
| 2019-20 | ₹173,851,164.00 |
| 2020-21 | ₹177,939,822.00 |
| 2021-22 | ₹71,970,131.00 |

---

*Analysis completed successfully. All calculations verified.*
