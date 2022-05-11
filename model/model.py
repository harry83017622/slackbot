import datetime
import json

import requests
from google.cloud import storage


class Modeler:
    def __init__(self, auth) -> None:
        self.auth = auth
        self.today_query = None

    def query_daily_notion(self) -> object:
        """
        return today update articles and their authors from notion api
        """
        auth = self.auth
        # print(auth.__dict__)

        def query_notion():
            date = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).replace(
                microsecond=0
            ).isoformat() + ".000Z"
            # date = date[:11]+'18:00:00.000Z'
            query = {
                "filter": {
                    "property": "Last Edited Time",
                    "date": {"on_or_after": date},
                }
            }

            header = {"Authorization": auth._secret_key, "Notion-Version": "2021-05-13"}
            response = requests.post(
                auth.base_url + auth._database_id + "/query", headers=header, json=query
            )
            return response

        self.today_query = query_notion()

        return self.today_query

    def article_count(self, nums: list) -> list:
        """
        input article number
        output count of articles
        """
        auth = self.auth
        ret = []

        for num in nums:
            query = {"filter": {"property": "題號", "number": {"equals": num}}}

            header = {"Authorization": auth._secret_key, "Notion-Version": "2021-05-13"}
            response = requests.post(
                auth.base_url + auth._database_id + "/query", headers=header, json=query
            )
            # print(num)
            ret.append(len(response.json()["results"]))
        return ret

    def query_past_record(self, use_local_src: bool) -> dict:
        """
        return query of articles(key) and author(value) from local db
        """
        if use_local_src:
            return Modeler.load_past_record_from_file()
        else:
            return Modeler.load_past_record()

    def update_record_to_gcp(self, content: dict) -> None:
        with open("secret.json") as fin:
            cfg = json.load(fin)

        bucket_name = "leetcode-notion-db"
        bucket = storage.Client().get_bucket(bucket_name)

        if cfg["mode"] == "deploy":
            gcp_pth = "past_record.json"
        else:
            gcp_pth = "test.json"

        blob = bucket.blob(gcp_pth)
        blob.upload_from_string(
            data=json.dumps(content, ensure_ascii=False),
            content_type="application/json",
        )
        return

    @staticmethod
    def load_past_record():
        bucket_name = "leetcode-notion-db"
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.get_blob("past_record.json")
        fileData = json.loads(blob.download_as_string())
        return fileData

    @staticmethod
    def load_past_record_from_file():
        with open("past_record.json") as fin:
            past_record = json.load(fin)
        return past_record
