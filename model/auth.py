import json


class Auth:
    def __init__(self):
        self.base_url = "https://api.notion.com/v1/databases/"
        self._secret_key = None
        self._database_id = None
        self._load_notion_token()

    def _load_notion_token(self):
        with open("secret.json", "r") as f:
            content = json.load(f)
        self._secret_key = content["secret_key"]
        self._database_id = content["database_id"]
        return
