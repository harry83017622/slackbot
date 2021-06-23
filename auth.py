import json
import requests

class Auth():
    def __init__(self):
        self.base_url = "https://api.notion.com/v1/databases/"
        self._secret_key = None
        self._database_id = None
        self._load_config()
    
    def _load_config(self):
        with open("config.json", "r") as f:
            content = json.load(f)
        self._secret_key = content["secret_key"]
        self._database_id = content["database_id"]
        return

    def check_status(self):
        secret_key = self._secret_key
        header = {"Authorization":secret_key, "Notion-Version":"2021-05-13"}
        response = requests.get(self.base_url + self._database_id , headers=header)
        return response.status_code == 200

auth_ = Auth()