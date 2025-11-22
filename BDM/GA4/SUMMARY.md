# GA4 Analysis Summary

## Project Completed Successfully ✓

All 5 questions have been answered using comprehensive candidate ranking analysis.

---

## Quick Reference - Final Answers

| Question | Answer |
|----------|--------|
| 1. Rank of Akanksha using Method 1 | **3** |
| 2. Composite score of Praveen using Method 1 | **0.388818** |
| 3. Rank of Nanda using Method 2 | **9** |
| 4. Composite score of Sazid using Method 2 | **0.836852** |
| 5. Number of persons retaining same rank | **6** |

---

## Methodology

### Preprocessing
1. **Years of Experience**: Used raw numeric values
2. **Appraisal History**: Calculated consistency score based on standard deviation with cutoff > 0.7
3. **Skills**: Counted comma-separated skills
4. **Key Projects**: Counted comma-separated projects
5. **Duration in Current Role**: Used raw numeric values
6. **Bench Duration**: Used raw numeric values
7. **Availability Date**: Calculated days from reference date (1st July 2024)

### Normalization
Applied Min-Max normalization:
- **More is better**: `(value - min) / (max - min)`
- **Less is better**: `(max - value) / (max - min)`

### Composite Score Calculation

**Method 1 (Equal Weights)**:
- Each criterion: 14.29% (1/7)

**Method 2 (Weighted)**:
- Years of Experience: 20%
- Appraisal History: 10%
- Skills: 20%
- Key Projects: 10%
- Duration in Current Role: 10%
- Bench Duration: 10%
- Availability: 20%

### Ranking
Candidates ranked by composite score (descending order, highest = Rank 1)

---

## Top 3 Candidates

### Method 1 (Equal Weights)
1. **Abhijit** - Score: 0.9128
2. **Sazid** - Score: 0.8061
3. **Akanksha** - Score: 0.7734

### Method 2 (Weighted)
1. **Abhijit** - Score: 0.9116
2. **Sazid** - Score: 0.8369
3. **Akanksha** - Score: 0.7747

---

## Rank Changes Between Methods

**Candidates who retained same rank (6):**
- Abhijit (Rank 1)
- Sazid (Rank 2)
- Akanksha (Rank 3)
- Esha (Rank 4)
- Siva (Rank 7)
- Praveen (Rank 8)

**Candidates whose rank changed (4):**
- Anuj: Rank 5 → 6
- Shalini: Rank 6 → 5
- Lavanya: Rank 9 → 10
- Nanda: Rank 10 → 9

---

## Files Generated

1. **main.py** - Complete Python analysis script
2. **answers.md** - Detailed answers with all rankings and comparisons
3. **SUMMARY.md** - This summary document

---

## Verification Status

✓ Dataset loaded (10 candidates)  
✓ Preprocessing completed  
✓ Normalization applied  
✓ Method 1 rankings calculated  
✓ Method 2 rankings calculated  
✓ All answers verified  
✓ Output files created  

**Analysis Date:** November 22, 2025  
**Status:** COMPLETE
