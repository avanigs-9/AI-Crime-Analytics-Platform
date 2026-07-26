import random
import pandas as pd

districts = [
    "Bengaluru","Mysuru","Hubli","Mangaluru","Belagavi",
    "Tumakuru","Shivamogga","Ballari","Davanagere",
    "Kalaburagi","Bidar","Raichur"
]

crime_types = [
    "Theft","Cyber Crime","Fraud","Robbery",
    "Murder","Assault","Kidnapping","Burglary"
]

rows = []

for i in range(100):
    rows.append({
        "District": random.choice(districts),
        "Crime_Type": random.choice(crime_types),
        "Year": random.choice([2022,2023,2024,2025]),
        "Cases": random.randint(20,500)
    })

df = pd.DataFrame(rows)

df.to_csv("crime_data.csv", index=False)

print("Dataset Generated Successfully!")