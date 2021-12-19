from collections import Counter
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from view.template import create_template

class Viewer(object):
    def __init__(self, controller):
        controller.register(self)
        self._load_slack_token()
        self._client = WebClient(token=self._secret_key)
        self.get_channel_id()

    def _load_slack_token(self):
        with open("config.json", "r") as f:
            content = json.load(f)
        self._secret_key = content["slack_token"]

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

    def notify(self, event):
        if isinstance(event,str):
            print("received event", event)
        elif isinstance(event,Counter):
            msg = create_template(event.most_common())
            result = self._client.chat_postMessage(
                channel=self.channel_id,
                blocks=msg
                # You could also use a blocks[] array to send richer content
            )
            print(msg)
            print(result)