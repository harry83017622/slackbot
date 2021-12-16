import datetime
import requests

class Modeler:
    def __init__(self,auth) -> None:
        self.auth = auth

    def query_daily_notion(self) -> object:
        '''
        return today update articles and their authors from notion api
        '''
        auth = self.auth
        # print(auth.__dict__)
        def query_notion():
            date = (datetime.datetime.utcnow()-datetime.timedelta(days=1)
                    ).replace(microsecond=0).isoformat()+'.000Z'
            # date = date[:11]+'18:00:00.000Z'
            query = {
                "filter": {
                    "property": "Last Edited Time",
                    "date": {
                        "on_or_after": date
                    }
                }
            }

            header = {"Authorization": auth._secret_key,
                        "Notion-Version": "2021-05-13"}
            response = requests.post(
                auth.base_url + auth._database_id + "/query", headers=header, json=query)
            return response
            

        return query_notion()

    def article_count(self,nums:list) -> list:
        '''
        input article number
        output count of articles
        '''
        auth = self.auth
        ret = []
        for num in nums:
            query = {
                "filter": {
                    "property": "題號",
                    "number": {
                        "equals": num
                    }
                }
            }

            header = {"Authorization": auth._secret_key,
                        "Notion-Version": "2021-05-13"}
            response = requests.post(
                auth.base_url + auth._database_id + "/query", headers=header, json=query)

            ret.append(len(response.json()["results"]))
        return ret

    def query_past_record(self) -> dict:
        '''
        return query of articles(key) and author(value) from local db 
        '''
        return dict

    def update_record(self,content:dict) -> None:
        return