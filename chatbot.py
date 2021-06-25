from auth import Auth
import requests
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import datetime


class chatBot(Auth):
    def __init__(self):
        super().__init__()
        self._load_slack_token()
        self._client = WebClient(token=self._slack_token)
        self._response = None

    def _load_slack_token(self):
        with open("config.json", "r") as f:
            content = json.load(f)
        self._slack_token = content["slack_token"]
        return

    def check_db_exist(self):
        pass

    def query_notion(self):
        # if query==None
        #   query all
        # else
        #   do query
        date = (datetime.datetime.now()-datetime.timedelta(days=2)
                ).replace(microsecond=0).isoformat()
        date = date[:11]+'18:00:00.000Z'
        query = {
            "filter": {
                "property": "Last Edited Time",
                "date": {
                    "on_or_after": date
                }
            }
        }
        if query:
            secret_key = self._secret_key
            header = {"Authorization": secret_key,
                      "Notion-Version": "2021-05-13"}
            response = requests.post(
                self.base_url + self._database_id+ "/query", headers=header, json=query)
            if response.status_code == 200:
                self._response = len(response.json()["results"])
                # print(response.json()["results"])
                return self._response
            else:
                pass
        else:
            pass

    def get_channel_id(self, channel_name="chatbot-test"):
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
                        # Print result
                        # print(f"Found conversation ID: {conversation_id}")
                        return self.channel_id
                return -1
        except SlackApiError as e:
            print(f"Error: {e}")
            return -1

    def post_msg(self, texts=None):
        try:
            # Call the conversations.list method using the WebClient
            self.query_notion()
            if self._response == 0:
                result = self._client.chat_postMessage(
                    channel=self.channel_id,
                    # blocks=blocks,
                    text="There is no new article updated today! You guys suck..."
                    # You could also use a blocks[] array to send richer content
                )
                # Print result, which includes information about the message (like TS)
                print(result)
            else:
                date = (datetime.datetime.now()-datetime.timedelta(days=1)
                        ).replace(microsecond=0).isoformat()[:10]
                result = self._client.chat_postMessage(
                    channel=self.channel_id,
                    # blocks=blocks,
                    text="Total {} articles were updated on {}".format(self._response,date)
                    # You could also use a blocks[] array to send richer content
                )
                # Print result, which includes information about the message (like TS)
                print(result)

        except SlackApiError as e:
            print(f"Error: {e}")
