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

    def _create_daily_record_template(self, key_date):

        daily_record_template = {
            key_date: {
                "content": {
                    # "name" : [
                    #         # question_title,
                    #         # question_title
                    #     ]
                    #
                },
                "ttl": -1
            }
        }
        return daily_record_template

    def _load_daily_record(self) -> dict:
        content = {}
        try:
            with open("daily_record.json", "r") as f:
                content = json.load(f)
        except:
            pass
        return content

    def _load_user_record(self) -> dict:
        content = {}
        try:
            with open("user_record.json", "r") as f:
                content = json.load(f)
        except:
            pass
        return content

    # user.push(record={date:record})
    def push(self, record: dict) -> None:
        print(record)
        '''
        record = {
            date : {
                "name":"",
                "question":[
                    # question_title
                ]
            }
        }


        daily_record_template = {
            date:{
                "content" : {
                    # "name" : [
                    #         # question_title,
                    #         # question_title
                    #     ]
                    # 
                },
                "ttl" : -1
            }
        }
        '''
        # try:
        key_date = list(record.keys())[0]
        push_name = record[key_date]["name"]
        push_question = record[key_date]["question"]

        single_daily_record = self.daily_record.get(
            key_date, 
            self._create_daily_record_template(key_date))
        # print("single_daily_record.keys() = ",single_daily_record.keys())

        # print("single_daily_record[key_date] = ",single_daily_record[key_date])
        
        content = single_daily_record[key_date]["content"]
        if push_name not in list(content.keys()):
            content[push_name] = push_question
        else:
            content[push_name] += push_question
            

        single_daily_record[key_date]["content"] = content
        self.daily_record[key_date] = single_daily_record
        # print(self.daily_record)
        # except:
        #     print("len of record is 0")
        return
