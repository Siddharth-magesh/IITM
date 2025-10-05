import pandas as pd

# Define the target symbols
target_symbols = {"˜", "ƒ", "‹"}

# Read each file with correct encoding (use raw strings to avoid \t escape)
data1 = pd.read_csv(r"D:\IITM\tds\q-unicode-data\data1.csv", encoding="cp1252")         # CSV CP-1252
data2 = pd.read_csv(r"D:\IITM\tds\q-unicode-data\data2.csv", encoding="utf-8")          # CSV UTF-8
data3 = pd.read_csv(r"D:\IITM\tds\q-unicode-data\data3.txt", encoding="utf-16", sep="\t")  # TSV UTF-16

# Combine them into one DataFrame
df = pd.concat([data1, data2, data3], ignore_index=True)

# Filter for the required symbols and sum their values
total_sum = df[df["symbol"].isin(target_symbols)]["value"].sum()

print("Sum of values for symbols ˜, ƒ, ‹:", total_sum)
