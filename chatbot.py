from auth import Auth
from user import User
import requests
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import datetime
import utils


class chatBot(Auth):
    def __init__(self):
        super().__init__()
        self._load_slack_token()
        self._client = WebClient(token=self._slack_token)
        self._user = User()
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
        
        secret_key = self._secret_key
        header = {"Authorization": secret_key,
                    "Notion-Version": "2021-05-13"}
        response = requests.post(
            self.base_url + self._database_id + "/query", headers=header, json=query)
        if response.status_code == 200:
            # print(response.json()["results"][0])
            self.valid_cnt, self.duplicate_articles = self.filter_query_results(
                date, response.json()["results"])
            # self._response = len(response.json()["results"])
            # print(response.json()["results"])
            return
        else:
            print("bad request response")
    
    '''
    case 1: new article
        update db and post cnt++
    case 2: old article but new author
        detect duplicated article
        update db and post cnt++ 
    case 3: old article and not new author
        detect duplicated article
        pass
    '''

    def filter_query_results(self, date, results):
        user_db_date = datetime.datetime.utcnow().replace(
                    microsecond=0).isoformat()[:10]
        # print(results)
        cnt = 0
        notion_question_id_to_idx, data_results = utils.load_notion_db_from_gcp()
        duplicate_articles = []
        for i in results:
            t = i['properties']['Last Edited Time']['last_edited_time']
            # remove articles with empty title
            if i['properties']['Problem']['title'] == []:
                continue
            else:
                print(i['properties']['Last Edited Time']['last_edited_time'])
                # pass if time before utc+8 00:00
                if int(t[8:10]) == int(date[8:10]) and int(t[11:13]) < int(date[11:13]):
                    i['properties']['Problem']['title'][0]['plain_text']
                    print('wrong time')

                else:
                    # get author info
                    try:
                        author = [j['name'] for j in i['properties']['Person']['people']]
                    except:
                        author = []

                    # detect duplicated articles
                    # if i['properties']['題號']['number'] in notion_question_id_to_idx:
                    if notion_question_id_to_idx.get(i['properties']['題號']['number'],None):
                        # check author
                        db_idx = notion_question_id_to_idx[i['properties']['題號']['number']]
                        
                        # review old articles
                        if author==data_results[db_idx]["people"]:
                            continue
                        else:
                            # response 1 author and not equal to db
                            if len(author)==1:
                                duplicate_articles.append(
                                    " ".join(author)+" please merge "+str(i['properties']['題號']['number']))
                            # update in old article
                            else:

                                # push new author to leaderboard db
                                for new_author in author:
                                    
                                    if new_author in data_results[db_idx]["people"]:
                                        continue
                                    self._user.push(
                                        record = { 
                                            user_db_date : {
                                                "name" : new_author,
                                                "question" : [i['properties']['題號']['number']]
                                            }
                                        }
                                    )
                                
                                # check_diff = set(author)-set(data_results[db_idx]["people"])
                                
                                
                                
                                # intercept origin author and new author

                                data_results[db_idx]["people"]=author
                    else:
                        
                        # create new author here 


                        for new_author in author:
                            self._user.push(
                                record = { 
                                    user_db_date : {
                                        "name" : new_author,
                                        "question" : [i['properties']['題號']['number']]
                                    }
                                }
                            )





                        data_results.append({
                            "題號": i['properties']['題號']['number'],
                            "people": author
                        })

                    print(i['properties']['Problem']['title'][0]['plain_text'])
                    cnt += 1
            print('---------------------------------------------------')
        # response.json()["results"][4]['properties']['Last Edited Time']['last_edited_time']
        print('total valid articles = {}'.format(cnt))
        print(self._user.daily_record)
        # utils.upload_gcloud_bucket(data_results)
        return cnt, duplicate_articles

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
            if self.valid_cnt == 0:
                result = self._client.chat_postMessage(
                    channel=self.channel_id,
                    # blocks=blocks,
                    text="There is no new article updated today! You guys suck..."
                    # You could also use a blocks[] array to send richer content
                )
                # Print result, which includes information about the message (like TS)
                # print(result)
            else:
                date = datetime.datetime.utcnow().replace(
                    microsecond=0).isoformat()[:10]

                result = self._client.chat_postMessage(
                    channel=self.channel_id,
                    # blocks=blocks,
                    text="Total {} articles were updated on {}".format(
                        self.valid_cnt, date)
                    # You could also use a blocks[] array to send richer content
                )

                blocks_head= [
                    {
                        "type": "divider"
                    },
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Daily Ranking",
                            "emoji": True
                        }
                    }
                ]
                blocks_body = []
                # print(self._user.daily_record)
                # print(date)
                for writer, nums in self._user.daily_record[date][date]["content"].items():
                    print(writer,nums)
                    nums = [str(i) for i in nums]
                    stars = ":star:"*len(nums)
                    question_name = "\n".join(nums)
                    blocks_body.append(
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*{writer}*\n{stars}\n {question_name}"
                            }
                        }
                    )
                # blocks_body=[
                    
                #     {
                #         "type": "section",
                #         "text": {
                #             "type": "mrkdwn",
                #             "text": "*user_name_2*\n:star::star:\n question_name_1 \n question_name_2"
                #         }
                #     }
                # ]

                blocks_end =[
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*~Now move your ass and start coding~* :cat: <https://leetcode.com/|Leetcode>"
                        }
                    }
                ]
                blocks = blocks_head+blocks_body+blocks_end
                
                result = self._client.chat_postMessage(
                    channel=self.channel_id,
                    blocks=blocks
                    # You could also use a blocks[] array to send richer content
                )

                # Print result, which includes information about the message (like TS)
                # print(result)
                duplicate_articles = "  ".join(self.duplicate_articles)
                if duplicate_articles == "":
                    pass
                    # result = self._client.chat_postMessage(
                    #     channel=self.channel_id,
                    #     # blocks=blocks,
                    #     text="There is no duplicated article updated today. Good Job! Guys~"
                    #     # You could also use a blocks[] array to send richer content
                    # )
                    # # Print result, which includes information about the message (like TS)
                    # print(result)
                else:
                    result = self._client.chat_postMessage(
                        channel=self.channel_id,
                        # blocks=blocks,
                        text=duplicate_articles
                        # You could also use a blocks[] array to send richer content
                    )
                    # Print result, which includes information about the message (like TS)
                    # print(result)

        except SlackApiError as e:
            print(f"Error: {e}")
