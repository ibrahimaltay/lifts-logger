import os
import requests
from dotenv import load_dotenv

load_dotenv()

database_id = os.environ.get('NOTION_DATABASE_ID')
notion_key = os.environ.get('NOTION_KEY')
def get_latest_data():
    # Set up the Notion API endpoint and parameters
    endpoint = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Notion-Version": "2021-05-13",
        "Authorization": f"Bearer {notion_key}",
        "Content-Type": "application/json",
    }
    params = {
        "filter": {
            "property": "Name",
            "title": {
                "is_not_empty": True,
            },
        },
    }

    # Send the request to the Notion API
    response = requests.post(endpoint, headers=headers, json=params)

    # Parse the response and get the latest data for each unique entry
    exercise_data = {}
    entries = set()
    for page in response.json()["results"]:
        entry_name = page["properties"]["Name"]["title"][0]["plain_text"]
        entries.add(entry_name)
    for entry in entries:
        pages = [page for page in response.json()["results"] if page["properties"]["Name"]["title"][0]["plain_text"] == entry]
        latest_page = max(pages, key=lambda p: p["last_edited_time"])
        weight = latest_page["properties"]["Weight"]["number"]
        reps = latest_page["properties"]["Reps"]["number"]
        exercise_data[entry] = (weight, reps)

    return exercise_data

if __name__ == '__main__':
    get_latest_data()