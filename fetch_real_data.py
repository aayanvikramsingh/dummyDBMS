import requests
import pandas as pd
from datetime import datetime
import os
import time

FILE_PATH = "leetcode_data.xlsx"

# 🔹 Replace with your real LeetCode usernames
USERS = [
    "aayanv5201",
    "Santhosh2005"
]

def fetch_user_data(username):
    """Fetch real data from LeetCode's GraphQL API."""
    url = "https://leetcode.com/graphql"
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """
    try:
        response = requests.post(url, json={"query": query, "variables": {"username": username}}, timeout=10)
        response.raise_for_status()
        data = response.json()

        stats = data["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]

        record = {"Username": username}
        for s in stats:
            record[s["difficulty"]] = s["count"]

        record["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"✅ Fetched: {username}")
        return record

    except Exception as e:
        print(f"❌ Failed for {username}: {e}")
        return {"Username": username, "Easy": None, "Medium": None, "Hard": None, "Timestamp": datetime.now()}


def save_to_excel(data):
    """Append new data to Excel file."""
    df_new = pd.DataFrame(data)

    if os.path.exists(FILE_PATH):
        old_df = pd.read_excel(FILE_PATH)
        df = pd.concat([old_df, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_excel(FILE_PATH, index=False)
    print("💾 Data saved to", FILE_PATH)


def run_fetch_cycle():
    all_data = []
    for user in USERS:
        record = fetch_user_data(user)
        all_data.append(record)
        time.sleep(2)  # small delay to avoid hitting rate limits
    save_to_excel(all_data)


if __name__ == "__main__":
    run_fetch_cycle()
