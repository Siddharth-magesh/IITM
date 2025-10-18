#!/usr/bin/env python3
"""
Analyze BDM datasets and answer all questions
"""
import csv
from collections import defaultdict

def load_dataset1():
    """Load dataset1 and return valid records only"""
    with open('BDM/dataset1.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # Skip first empty line, use second line as header
        reader = csv.DictReader(lines[1:])
        data = []
        for row in reader:
            # Skip Non-Response and empty rows
            if row.get('RESPONSE_STATUS') == 'Accepted':
                data.append(row)
    return data

def load_dataset2():
    """Load dataset2"""
    with open('BDM/dataset2.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # Skip first empty line
        reader = csv.DictReader(lines[1:])
        data = list(reader)
    return data

def answer_questions():
    """Answer all questions with detailed methodology"""
    
    print("="*80)
    print("DATASET ANALYSIS - ANSWERS")
    print("="*80)
    
    # Load datasets
    ds1 = load_dataset1()
    ds2 = load_dataset2()
    
    print(f"\nDataset 1: {len(ds1)} valid households (after excluding Non-Response)")
    print(f"Dataset 2: {len(ds2)} loan records")
    print("\n" + "="*80)
    
    # QUESTION 1: Fraction with only one two wheeler
    print("\n1. What fraction of sample households have only one two wheeler?")
    count_one_tw = sum(1 for h in ds1 if h.get('TWO_WHEELERS_OWNED', '').strip() == '1')
    total_households = len(ds1)
    fraction_1 = count_one_tw / total_households if total_households > 0 else 0
    print(f"   Methodology: Count households where TWO_WHEELERS_OWNED = 1")
    print(f"   Households with 1 two-wheeler: {count_one_tw}")
    print(f"   Total households: {total_households}")
    print(f"   ANSWER: {fraction_1:.4f}")
    
    # QUESTION 2: No two wheeler but interested in buying
    print("\n2. What fraction don't have a two wheeler, but are interested in buying one?")
    no_tw_want_buy = sum(1 for h in ds1 
                         if h.get('TWO_WHEELERS_OWNED', '').strip() == '0' 
                         and h.get('WILL_BUY_TWO_WHEELER', '').strip() == 'Y')
    fraction_2 = no_tw_want_buy / total_households if total_households > 0 else 0
    print(f"   Methodology: Count where TWO_WHEELERS_OWNED=0 AND WILL_BUY_TWO_WHEELER=Y")
    print(f"   Households: {no_tw_want_buy}")
    print(f"   ANSWER: {fraction_2:.4f}")
    
    # QUESTION 3: Have two wheeler but want to buy more
    print("\n3. What proportion already have a two wheeler, but want to buy one more?")
    have_want_more = sum(1 for h in ds1 
                         if h.get('TWO_WHEELERS_OWNED', '').strip() not in ['0', ''] 
                         and h.get('WILL_BUY_TWO_WHEELER', '').strip() == 'Y')
    fraction_3 = have_want_more / total_households if total_households > 0 else 0
    print(f"   Methodology: Count where TWO_WHEELERS_OWNED>0 AND WILL_BUY_TWO_WHEELER=Y")
    print(f"   Households: {have_want_more}")
    print(f"   ANSWER: {fraction_3:.4f}")
    
    # QUESTION 4: Urban, no two wheeler, want to buy immediately
    print("\n4. What fraction of urban households don't have a two wheeler but intend to buy immediately?")
    urban_households = [h for h in ds1 if h.get('REGION_TYPE', '').strip() == 'URBAN']
    urban_no_tw_buy_now = sum(1 for h in urban_households
                               if h.get('TWO_WHEELERS_OWNED', '').strip() == '0'
                               and h.get('WILL_BUY_TWO_WHEELER_NOW', '').strip() == 'Y')
    total_urban = len(urban_households)
    fraction_4 = urban_no_tw_buy_now / total_urban if total_urban > 0 else 0
    print(f"   Methodology: Count urban households where TWO_WHEELERS_OWNED=0 AND WILL_BUY_TWO_WHEELER_NOW=Y")
    print(f"   Urban households matching criteria: {urban_no_tw_buy_now}")
    print(f"   Total urban households: {total_urban}")
    print(f"   ANSWER: {fraction_4:.4f}")
    
    # QUESTION 5: Market share of Commuter bikes
    print("\n5. Based on sample data, what is the existing market share of Commuter bikes?")
    commuter_bikes = sum(1 for h in ds1 if 'Commuter Bike' in h.get('TYPE_OF_TWO_WHEELER_OWNED', ''))
    total_with_tw = sum(1 for h in ds1 if h.get('TWO_WHEELERS_OWNED', '').strip() not in ['0', '', 'Not Applicable'])
    market_share_5 = commuter_bikes / total_with_tw if total_with_tw > 0 else 0
    print(f"   Methodology: Count households with 'Commuter Bike' / Total households with two-wheelers")
    print(f"   Households with Commuter Bike: {commuter_bikes}")
    print(f"   Total households with any two-wheeler: {total_with_tw}")
    print(f"   ANSWER: {market_share_5:.4f}")
    
    # QUESTION 6: Female households with scooter
    print("\n6. What proportion of Female majority/dominant/only households have a scooter?")
    female_households = [h for h in ds1 if 'Female' in h.get('GENDER_GROUP', '')]
    female_with_scooter = sum(1 for h in female_households if 'Scooter' in h.get('TYPE_OF_TWO_WHEELER_OWNED', ''))
    total_female = len(female_households)
    proportion_6 = female_with_scooter / total_female if total_female > 0 else 0
    print(f"   Methodology: Count Female households with 'Scooter' / Total Female households")
    print(f"   Female households with scooter: {female_with_scooter}")
    print(f"   Total Female households: {total_female}")
    print(f"   ANSWER: {proportion_6:.4f}")
    
    # QUESTION 7: Eligible for new loan (no outstanding loan)
    print("\n7. If outstanding loan disqualifies eligibility, how many households are eligible?")
    no_outstanding = sum(1 for h in ds1 if h.get('HAS_OUTSTANDING_BORROWING', '').strip() == 'N')
    proportion_7 = no_outstanding / total_households if total_households > 0 else 0
    print(f"   Methodology: Count where HAS_OUTSTANDING_BORROWING=N")
    print(f"   Households with no outstanding loan: {no_outstanding}")
    print(f"   ANSWER: {proportion_7:.4f}")
    
    # QUESTION 8: Want two wheeler and have FD for lower interest
    print("\n8. What proportion wanting two wheeler would be eligible for lower interest loan against FD?")
    want_tw = [h for h in ds1 if h.get('WILL_BUY_TWO_WHEELER', '').strip() == 'Y']
    want_tw_with_fd = sum(1 for h in want_tw if h.get('HAS_OUTSTANDING_SAVING_IN_FIXED_DEPOSITS', '').strip() == 'Y')
    total_want_tw = len(want_tw)
    proportion_8 = want_tw_with_fd / total_want_tw if total_want_tw > 0 else 0
    print(f"   Methodology: Among those with WILL_BUY_TWO_WHEELER=Y, count those with FD (HAS_OUTSTANDING_SAVING_IN_FIXED_DEPOSITS=Y)")
    print(f"   Want TW and have FD: {want_tw_with_fd}")
    print(f"   Total wanting TW: {total_want_tw}")
    print(f"   ANSWER: {proportion_8:.4f}")
    
    # QUESTION 9: Target market for electric two wheelers (24hr electricity)
    print("\n9. Target market share for electric two wheelers (24hr electricity needed)?")
    want_tw_24hr = sum(1 for h in want_tw if h.get('POWER_GROUP', '').strip() == '24 hours')
    proportion_9 = want_tw_24hr / total_want_tw if total_want_tw > 0 else 0
    print(f"   Methodology: Among those wanting TW, count those with POWER_GROUP='24 hours'")
    print(f"   Want TW with 24hr power: {want_tw_24hr}")
    print(f"   Total wanting TW: {total_want_tw}")
    print(f"   ANSWER: {proportion_9:.4f}")
    
    # QUESTION 10: Rural Farmers with at least one two wheeler
    print("\n10. What fraction of Rural Farmers have at least one two wheeler?")
    rural_farmers = [h for h in ds1 
                     if h.get('REGION_TYPE', '').strip() == 'RURAL' 
                     and 'Farmer' in h.get('OCCUPATION_GROUP', '')]
    farmers_with_tw = sum(1 for h in rural_farmers 
                          if h.get('TWO_WHEELERS_OWNED', '').strip() not in ['0', ''])
    total_rural_farmers = len(rural_farmers)
    fraction_10 = farmers_with_tw / total_rural_farmers if total_rural_farmers > 0 else 0
    print(f"   Methodology: Rural households with 'Farmer' in occupation and TWO_WHEELERS_OWNED > 0")
    print(f"   Rural farmers with TW: {farmers_with_tw}")
    print(f"   Total rural farmers: {total_rural_farmers}")
    print(f"   ANSWER: {fraction_10:.4f}")
    
    print("\n" + "="*80)
    print("DATASET 2 ANALYSIS - LOAN QUESTIONS")
    print("="*80)
    
    # QUESTION 11: NBFC market share in FY20
    print("\n11. In FY20, what proportion of total loans are serviced by NBFCs?")
    fy20_loans = [loan for loan in ds2 if loan.get('Years', '').strip() == 'FY20']
    fy20_nbfc_value = sum(float(loan.get('Original Loan size', 0)) for loan in fy20_loans if loan.get('Lender Name', '').strip() == 'NBFC')
    fy20_total_value = sum(float(loan.get('Original Loan size', 0)) for loan in fy20_loans)
    proportion_11 = fy20_nbfc_value / fy20_total_value if fy20_total_value > 0 else 0
    print(f"   Methodology: Sum of NBFC loan values / Total loan values in FY20")
    print(f"   FY20 NBFC loan value: {fy20_nbfc_value:,.0f}")
    print(f"   FY20 Total loan value: {fy20_total_value:,.0f}")
    print(f"   ANSWER: {proportion_11:.6f}")
    
    # QUESTION 12: Ratio of Retail loan value PVT/PSU in FY21
    print("\n12. What is the ratio of Retail loan value given by private bank to PSU bank in FY21?")
    # Note: Assuming "Retail" refers to Microfinance loans (smaller retail loans)
    fy21_loans = [loan for loan in ds2 if loan.get('Years', '').strip() == 'FY21']
    fy21_pvt_retail = sum(float(loan.get('Original Loan size', 0)) for loan in fy21_loans 
                          if loan.get('Lender Name', '').strip() == 'PVT Bank' 
                          and loan.get('Segment of Loan', '').strip() == 'Microfinance')
    fy21_psu_retail = sum(float(loan.get('Original Loan size', 0)) for loan in fy21_loans 
                          if loan.get('Lender Name', '').strip() == 'PSU Bank' 
                          and loan.get('Segment of Loan', '').strip() == 'Microfinance')
    ratio_12 = fy21_pvt_retail / fy21_psu_retail if fy21_psu_retail > 0 else 0
    print(f"   Methodology: PVT Bank Microfinance / PSU Bank Microfinance in FY21")
    print(f"   FY21 PVT retail: {fy21_pvt_retail:,.0f}")
    print(f"   FY21 PSU retail: {fy21_psu_retail:,.0f}")
    print(f"   ANSWER: {ratio_12:.6f}")
    
    # QUESTION 13: Growth % difference FY19 to FY20 for Private bank commercial loans
    print("\n13. Growth % difference between FY19 & FY20 in commercial loans by Private banks?")
    fy19_pvt_comm = sum(float(loan.get('Original Loan size', 0)) for loan in ds2 
                        if loan.get('Years', '').strip() == 'FY19' 
                        and loan.get('Lender Name', '').strip() == 'PVT Bank'
                        and loan.get('Segment of Loan', '').strip() == 'Commercial')
    fy20_pvt_comm = sum(float(loan.get('Original Loan size', 0)) for loan in ds2 
                        if loan.get('Years', '').strip() == 'FY20' 
                        and loan.get('Lender Name', '').strip() == 'PVT Bank'
                        and loan.get('Segment of Loan', '').strip() == 'Commercial')
    growth_13 = abs((fy20_pvt_comm - fy19_pvt_comm) / fy19_pvt_comm) if fy19_pvt_comm > 0 else 0
    print(f"   Methodology: |(FY20 - FY19) / FY19|")
    print(f"   FY19 PVT commercial: {fy19_pvt_comm:,.0f}")
    print(f"   FY20 PVT commercial: {fy20_pvt_comm:,.0f}")
    print(f"   ANSWER: {growth_13:.6f}")
    
    # QUESTION 14: Difference in avg microfinance loan from NBFC between FY20 and FY21
    print("\n14. Difference in average microfinance loan from NBFCs between FY20 and FY21?")
    fy20_nbfc_micro = [float(loan.get('Original Loan size', 0)) for loan in ds2 
                       if loan.get('Years', '').strip() == 'FY20' 
                       and loan.get('Lender Name', '').strip() == 'NBFC'
                       and loan.get('Segment of Loan', '').strip() == 'Microfinance']
    fy21_nbfc_micro = [float(loan.get('Original Loan size', 0)) for loan in ds2 
                       if loan.get('Years', '').strip() == 'FY21' 
                       and loan.get('Lender Name', '').strip() == 'NBFC'
                       and loan.get('Segment of Loan', '').strip() == 'Microfinance']
    avg_fy20 = sum(fy20_nbfc_micro) / len(fy20_nbfc_micro) if fy20_nbfc_micro else 0
    avg_fy21 = sum(fy21_nbfc_micro) / len(fy21_nbfc_micro) if fy21_nbfc_micro else 0
    diff_14 = int(abs(avg_fy21 - avg_fy20))
    print(f"   Methodology: |Avg(FY21) - Avg(FY20)| for NBFC Microfinance")
    print(f"   FY20 avg: {avg_fy20:,.2f} (n={len(fy20_nbfc_micro)})")
    print(f"   FY21 avg: {avg_fy21:,.2f} (n={len(fy21_nbfc_micro)})")
    print(f"   ANSWER: {diff_14}")
    
    # QUESTION 15-16: Credit card questions - NOTE: Dataset doesn't have credit card data
    print("\n15. Average credit card borrowings of Males in FY20?")
    print("   NOTE: Dataset 2 does not contain credit card specific data.")
    print("   ANSWER: Unable to calculate - no credit card column in dataset")
    
    print("\n16. Percentage difference in credit card transactions between males and females?")
    print("   NOTE: Dataset 2 does not contain credit card transaction data.")
    print("   ANSWER: Unable to calculate - no credit card transactions column")
    
    # QUESTION 17: % difference of new borrowers in RETAIL category FY21 vs FY20
    print("\n17. Percentage of new borrowers in RETAIL category in FY21 vs FY20?")
    fy20_retail = [loan for loan in ds2 if loan.get('Years', '').strip() == 'FY20' 
                   and loan.get('Segment of Loan', '').strip() == 'Microfinance']
    fy21_retail = [loan for loan in ds2 if loan.get('Years', '').strip() == 'FY21' 
                   and loan.get('Segment of Loan', '').strip() == 'Microfinance']
    fy20_new = sum(1 for loan in fy20_retail if loan.get('New to Credit (Y /N)', '').strip() == 'Y')
    fy21_new = sum(1 for loan in fy21_retail if loan.get('New to Credit (Y /N)', '').strip() == 'Y')
    fy20_pct = fy20_new / len(fy20_retail) if fy20_retail else 0
    fy21_pct = fy21_new / len(fy21_retail) if fy21_retail else 0
    relative_diff_17 = (fy21_pct - fy20_pct) / fy20_pct if fy20_pct > 0 else 0
    print(f"   Methodology: (FY21_new% - FY20_new%) / FY20_new%")
    print(f"   FY20: {fy20_new}/{len(fy20_retail)} = {fy20_pct:.4f}")
    print(f"   FY21: {fy21_new}/{len(fy21_retail)} = {fy21_pct:.4f}")
    print(f"   ANSWER: {relative_diff_17:.6f}")
    
    # QUESTION 18: Lender with highest avg commercial loan to women in FY19
    print("\n18. Lender with highest average commercial loans to Women in FY19?")
    fy19_comm_female = [loan for loan in ds2 
                        if loan.get('Years', '').strip() == 'FY19' 
                        and loan.get('Segment of Loan', '').strip() == 'Commercial'
                        and loan.get('Gender', '').strip() == 'F']
    lender_avgs = {}
    for lender in ['NBFC', 'PVT Bank', 'PSU Bank']:
        loans = [float(loan.get('Original Loan size', 0)) for loan in fy19_comm_female 
                 if loan.get('Lender Name', '').strip() == lender]
        if loans:
            lender_avgs[lender] = sum(loans) / len(loans)
    if lender_avgs:
        top_lender = max(lender_avgs, key=lender_avgs.get)
        print(f"   Methodology: Calculate avg commercial loan for female borrowers by each lender in FY19")
        for lender, avg in lender_avgs.items():
            print(f"   {lender}: {avg:,.2f}")
        print(f"   ANSWER: {top_lender}")
    else:
        print("   ANSWER: No data found")
    
    # QUESTION 19: Fraction with credit history
    print("\n19. What fraction of borrowers have credit history (not new to credit)?")
    has_history = sum(1 for loan in ds2 if loan.get('New to Credit (Y /N)', '').strip() == 'N')
    total_loans = len(ds2)
    fraction_19 = has_history / total_loans if total_loans > 0 else 0
    print(f"   Methodology: Count where 'New to Credit'=N / Total")
    print(f"   With credit history: {has_history}")
    print(f"   Total loans: {total_loans}")
    print(f"   ANSWER: {fraction_19:.6f}")
    
    # QUESTION 20: Female borrowers with income > average
    print("\n20. How many female borrowers have income more than average?")
    all_incomes = [float(loan.get('Borrower Income', 0)) for loan in ds2 if loan.get('Borrower Income', '')]
    avg_income = sum(all_incomes) / len(all_incomes) if all_incomes else 0
    female_above_avg = sum(1 for loan in ds2 
                           if loan.get('Gender', '').strip() == 'F' 
                           and float(loan.get('Borrower Income', 0)) > avg_income)
    print(f"   Methodology: Count female borrowers with income > average income")
    print(f"   Average income across all borrowers: {avg_income:,.2f}")
    print(f"   Female borrowers above average: {female_above_avg}")
    print(f"   ANSWER: {female_above_avg}")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)

if __name__ == '__main__':
    answer_questions()
