from dotenv import load_dotenv
import os
import requests

load_dotenv()


def add_exercise(name, weight, reps):
    database_id = "931c12cb8d134638a30c503003d6a91a" # Enter your database ID here
    database_id = os.environ.get('NOTION_DATABASE_ID') # Enter your database ID here
    notion_api_key = os.environ.get('NOTION_KEY') # Get your Notion API key from an environment variable

    # Set up the request headers and body
    headers = {
        "Notion-Version": "2021-05-13",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {notion_api_key}"
    }
    data = {
        "parent": {
            "database_id": database_id
        },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": name.lower()
                        }
                    }
                ]
            },
            "Weight": {
                "number": weight
            },
            "Reps": {
                "number": reps
            }
        }
    }

    # Send the request to the Notion API
    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)

    # Check the response status code and print the result
    if response.status_code == 200:
        print(f"Successfully added exercise '{name}' to database!")
    else:
        print(f"Error: {response.status_code} - {response.text}")


if __name__ == '__main__':
    add_exercise("Squat", 20, 100)