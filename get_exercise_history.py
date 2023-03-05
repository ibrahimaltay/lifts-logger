import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_exercise_history(exercise_name, property_name=None):
    # Check that the property name is valid
    if property_name and property_name.lower() not in ["weight", "rep", "reps"]:
        return "Invalid property name"

    # Set up the Notion API endpoint and parameters
    endpoint = f"https://api.notion.com/v1/databases/{os.environ.get('NOTION_DATABASE_ID')}/query"
    headers = {
        "Notion-Version": "2022-02-22",
        "Authorization": f"Bearer {os.environ.get('NOTION_KEY')}",
        "Content-Type": "application/json",
    }
    params = {
        "filter": {
            "and": [
                {
                    "property": "Name",
                    "title": {
                        "equals": exercise_name,
                    },
                },
                {
                    "property": "Date",
                    "date": {
                        "is_not_empty": True,
                    },
                },
            ],
        },
        "sorts": [
            {
                "property": "Date",
                "direction": "descending",
            },
        ],
    }

    # Send the request to the Notion API
    response = requests.post(endpoint, headers=headers, json=params)
    # print(response.json())
    # Parse the response and extract the exercise history
    history = []
    for result in response.json()["results"]:
        if property_name:
            if property_name.lower() == "weight":
                value = result["properties"]["Weight"]["number"]
            else:
                value = result["properties"]["Reps"]["number"]
            history.append(value)
        else:
            weight = result["properties"]["Weight"]["number"]
            reps = result["properties"]["Reps"]["number"]
            history.append((weight, reps))

    return history

if __name__ == '__main__':
    # Get the historical weight data for the "squat" exercise
    x = weight_history = get_exercise_history("squat", "weight")
    print(x)
    # Get the historical reps data for the "squat" exercise
    y = reps_history = get_exercise_history("squat", "rep")
    print(y)
    # Get the historical weight and reps data for the "squat" exercise
    z = get_exercise_history("squat")
    print(z)