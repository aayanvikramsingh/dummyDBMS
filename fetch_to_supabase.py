import requests
import os
import time
from datetime import datetime
from supabase import create_client, Client

# Load from GitHub Secrets (automatically available as env vars in Actions)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🧩 LeetCode usernames to track
USERS = [
    "aayanv5201",
    "Santhosh2005",
    "AbhishekSNair",
    "Adma777",
    "Adarsh200IQ"
]

def fetch_user_data(username):
    """Fetch real LeetCode stats for a given username."""
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
        response = requests.post(
            url,
            json={"query": query, "variables": {"username": username}},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        stats = data["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]
        record = {"username": username}

        # ✅ Skip the "all" field — only keep easy, medium, hard
        for s in stats:
            diff = s["difficulty"].lower()
            if diff == "all":
                continue
            record[diff] = s["count"]

        record["timestamp"] = datetime.utcnow().isoformat()
        print(f"✅ {username} fetched successfully.")
        return record

    except Exception as e:
        print(f"❌ Failed for {username}: {e}")
        return None


def upsert_to_supabase(records):
    """Insert new or update existing records based on username."""
    if not records:
        print("No records to upsert.")
        return
    try:
        data, count = (
            supabase.table("leetcode_stats")
            .upsert(records, on_conflict="username")
            .execute()
        )
        print(f"🔄 Upserted {len(records)} rows into Supabase.")
    except Exception as e:
        print(f"❌ Supabase upsert failed: {e}")


def main():
    all_records = []
    for user in USERS:
        record = fetch_user_data(user)
        if record:
            all_records.append(record)
        time.sleep(2)  # avoid hitting rate limits
    upsert_to_supabase(all_records)


if __name__ == "__main__":
    main()
