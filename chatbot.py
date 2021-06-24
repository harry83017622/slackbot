from auth import Auth
import requests
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class chatBot(Auth):
    def __init__(self):
        super().__init__()
        self._load_slack_token()
        self._client = WebClient(token=self._slack_token)

    def _load_slack_token(self):
        with open("config.json", "r") as f:
            content = json.load(f)
        self._slack_token = content["slack_token"]
        return

    def check_db_exist(self):
        pass

    def query_notion(self, query=None):
        # if query==None
        #   query all
        # else
        #   do query
        if query:
            secret_key = self._secret_key
            header = {"Authorization": secret_key,
                      "Notion-Version": "2021-05-13"}
            response = requests.post(
                self.base_url + self._database_id, headers=header, json=query)
            if response.status_code==200:
                return response.json()["results"]
            else:
                pass
        else:
            pass
    
    def get_channel_id(self,channel_name="chatbot-test"):
        # channel_name = "chatbot-test"
        channel_id = None
        try:
            # Call the conversations.list method using the WebClient
            for result in self._client.conversations_list():
                if channel_id is not None:
                    break
                for channel in result["channels"]:
                    if channel["name"] == channel_name:
                        channel_id = channel["id"]
                        self.channel_id = channel_id
                        #Print result
                        # print(f"Found conversation ID: {conversation_id}")
                        return self.channel_id
                return -1
        except SlackApiError as e:
            print(f"Error: {e}")
            return -1
    
    def post_msg(self):
        try:
            # Call the conversations.list method using the WebClient
            result = self._client.chat_postMessage(
                channel=self.channel_id,
                # blocks=blocks,
                text="There is no new article updated today! You guys suck..."
                # You could also use a blocks[] array to send richer content
            )
            # Print result, which includes information about the message (like TS)
            print(result)

        except SlackApiError as e:
            print(f"Error: {e}")