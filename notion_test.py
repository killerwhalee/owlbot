import requests

url = "https://api.notion.com/v1/blocks/{}/children"
headers = {
    "Notion-Version": "2022-06-28",
    "Authorization": "Bearer ",
}

response = requests.get(url, headers=headers)
print(response.json())
