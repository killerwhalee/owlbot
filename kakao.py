import requests
import json


class Kakao:
    def __init__(self, api_key, json_src):
        self.api_key = api_key

        # Load token data from JSON file
        with open(json_src, "r") as f:
            self.tokens = json.load(f)

        self.refresh_token()
        
    def get_access_token(self, api_code):
        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": self.api_key,
            "redirect_url": "https://localhost:8000",
            "code": api_code,
        }
        response = requests.post(url, data=data)
        return response.json()

    # Refresh kakao API access token
    def refresh_token(self):
        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": self.api_key,
            "refresh_token": self.tokens["refresh_token"],
        }

        response = requests.post(url, data=data)

        # Check updated tokens information
        result = response.json()

        # Update JSON file
        if "access_token" in result:
            self.tokens["access_token"] = result["access_token"]

        if "refresh_token" in result:
            self.tokens["refresh_token"] = result["refresh_token"]
        else:
            pass

        with open("kakao_token.json", "w") as fp:
            json.dump(self.tokens, fp)

    def list_friends_uuid(self):
        url = "https://kapi.kakao.com/v1/api/talk/friends"

        # Set authorization header
        headers = {"Authorization": "Bearer " + self.tokens["access_token"]}

        # Call API and check result
        response = requests.get(url, headers=headers)
        return [user["uuid"] for user in response.json()["elements"]]
        

    def send_messages_self(self, text):
        # Use different api call regarding target
        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

        # Create message body
        content = {
            "object_type": "text",
            "text": text,
            "link": {"web_url": ""},
        }

        # Set authorization header
        headers = {"Authorization": "Bearer " + self.tokens["access_token"]}

        # Set message data
        data = {"template_object": json.dumps(content)}

        # Call API and check result
        response = requests.post(url, headers=headers, data=data)
        return response.json()

    def send_messages_to(self, text, target):
        # Use different api call regarding target
        url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

        # Create message body
        content = {
            "object_type": "text",
            "text": text,
            "link": {"web_url": ""},
        }

        # Set authorization header
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + self.tokens["access_token"],
        }

        # Set message data
        data = {
            "receiver_uuids": f'["{target}"]',
            "template_object": json.dumps(content),
        }

        print(data)

        # Call API and check result
        response = requests.post(url, headers=headers, data=data)
        return response.json()