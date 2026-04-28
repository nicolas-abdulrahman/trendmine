import json
import os
from datetime import datetime

from apify_client import ApifyClient

# --- CONFIGURATION ---
# ⚠️ WARNING: Rotate this token on Apify after running this!
SEARCH_TERM = "futebol"
LOCATION = "BR"
# Time range for "Last 5 Months" in Google Trends format is 'today 5-m'
TIME_RANGE = "today 3-m"

# 1. Setup the Folder Path: data/4-27-2026-7-19
current_time = datetime.now().strftime("%m-%d-%Y-%H-%M")
folder_path = os.path.join("data", current_time)
os.makedirs(folder_path, exist_ok=True)

file_path = os.path.join(folder_path, "football_trends.json")

# 2. Initialize Apify Client
client = ApifyClient(MY_TOKEN)

# 3. Prepare Input for the Google Trends Scraper
run_input = {
    "searchTerms": [SEARCH_TERM],
    "isMultiple": False,
    "timeRange": TIME_RANGE,
    "geo": LOCATION,
    "viewedFrom": LOCATION.lower(),
    "category": "",
    "maxItems": 50,  # Getting a good amount of related queries
}

print(f"🚀 Starting Apify Scraper for '{SEARCH_TERM}' in {LOCATION}...")

try:
    # 4. Run the Actor
    run = client.actor("apify/google-trends-scraper").call(run_input=run_input)

    # 5. Fetch Results
    print("✅ Scrape complete. Downloading dataset...")
    dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items

    # 6. Process and Filter (The "No Futebol" Game Rule)
    processed_data = []
    for item in dataset_items:
        # Extract both Top and Rising queries
        top = item.get("relatedQueries", {}).get("top", [])
        rising = item.get("relatedQueries", {}).get("rising", [])

        all_queries = top + rising

        for q in all_queries:
            query_text = q.get("query", "")
            # Filter out the word 'futebol' so the game stays hard!
            if "futebol" not in query_text.lower() and query_text:
                processed_data.append(
                    {
                        "query": query_text,
                        "value": q.get("value"),
                        "extracted_at": datetime.now().isoformat(),
                    }
                )

    # 7. Save to the specific folder
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(dataset_items, f, indent=4, ensure_ascii=False)

    print(f"🎉 Success! Saved {len(processed_data)} queries to {file_path}")

except Exception as e:
    print(f"❌ An error occurred: {e}")
