import pandas as pd
import random
from datetime import datetime
import os

FILE_PATH = "leetcode_data.xlsx"

# Dummy usernames
USERS = ["aayan_vikram", "adithya_m", "abhishek_n", "shri_karthik"]

def get_dummy_data():
    """Simulate fetching data from LeetCode."""
    data = []
    for user in USERS:
        data.append({
            "Username": user,
            "Easy": random.randint(50, 300),
            "Medium": random.randint(30, 200),
            "Hard": random.randint(5, 100),
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return data

def update_excel(data):
    """Append new rows to Excel or create if not present."""
    new_df = pd.DataFrame(data)

    if os.path.exists(FILE_PATH):
        try:
            old_df = pd.read_excel(FILE_PATH)
            df = pd.concat([old_df, new_df], ignore_index=True)
        except Exception:
            df = new_df  # overwrite if reading fails
    else:
        df = new_df

    df.to_excel(FILE_PATH, index=False)
    print("✅ Excel updated:", FILE_PATH)

if __name__ == "__main__":
    dummy_data = get_dummy_data()
    update_excel(dummy_data)
