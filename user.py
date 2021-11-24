import json
import datetime

class User():
    def __init__(self) -> None:
        # read client db
        self.daily_record = self._load_daily_record()
        self.user_record = self._load_user_record()
        '''
        daily_record = {
            date:{
                record : [
                    {
                        name:"Lee",
                        question:[
                            question_title,
                            question_title
                        ]
                    },
                    {
                        name:"YL",
                        question:[
                            question_title
                        ]
                    }
                ]
                ttl : int
            }
        }


        user_record = {
            name:{
                "last_update_time": int
            }
        }
        '''
    def _create_daily_record_template(self):
        date = datetime.datetime.utcnow().replace(
                    microsecond=0).isoformat()[:10]
        daily_record_template = {
            date:{
                "record" : [
                    {
                        "name":"",
                        "question":[
                            # question_title,
                            # question_title
                        ]
                    },
                    # {
                    #     "name":"",
                    #     "question":[
                    #         # question_title
                    #     ]
                    # }
                ],
                "ttl" : -1
            }
        }
        return daily_record_template
        

    def _load_daily_record(self) -> dict:
        content = {}
        try:
            with open("daily_record.json","r") as f:
                content = json.load(f)
        except:
            pass
        return content

    def _load_user_record(self) -> dict:
        content = {}
        try:
            with open("user_record.json","r") as f:
                content = json.load(f)
        except:
            pass
        return content
    
    def push(self, record: dict) -> None:
        return