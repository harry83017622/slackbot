import json
class ClientInfo():
    def __init__(self) -> None:
        # read client db
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
        pass

    def _load_daily_record() -> dict:
        with open("daily_record.json","r") as f:
            content = json.load(f)
        