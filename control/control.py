from collections import Counter
from model import model, auth
from view import view

import datetime

login = auth.Auth()
ChatbotDB = model.Modeler(login)

class AbstractSubject(object):
    def register(self, listener):
        raise NotImplementedError("Must subclass me")
 
    def deregister(self, listener):
        raise NotImplementedError("Must subclass me")
 
    def notify_viewer(self, event):
        raise NotImplementedError("Must subclass me")
 


class Controller(AbstractSubject):
    # public static class variable
    today_query = None
    past_record = None

    def __init__(self):
        self.listeners = []

    def filter_query_results(self, response):
        
        if response.status_code != 200:
            return "bad request response"

        if len(response.json()["results"])==0:
            return "no leetcoder today"

        # {question : authors} = {int: list(str)} only when authors exist
        nums = []
        for num in response.json()["results"]:
            if num["properties"]["Person"]["people"] and ("題號" in num["properties"].keys()):
                nums.append({num["properties"]["題號"]["number"]:num["properties"]["Person"]["people"]})
        Controller.today_query = nums
        return nums

    def count_user_points(self):
        user_points = Counter()
        today_query = Controller.today_query
        past_record = Controller.past_record

        if not today_query:
            return
        for idx, article in enumerate(today_query):
            today_article = list(article.keys())[0]
            # print(list(article.values())[0])
            author_list = [i["name"] for i in list(article.values())[0] if "name" in i.keys()]
            past_article = past_record.get(str(today_article))
            
            for author in author_list:
                if not past_article or (author not in past_article):
                    # print(past_article)
                    user_points[author] += 1
            

        return user_points

    # Implement abstract Class AbstractSubject

    def register(self, listener):
        self.listeners.append(listener)
 
    def deregister(self, listener):
        self.listeners.remove(listener)
 
    def notify_viewers(self, event):
        for listener in self.listeners:
            listener.notify(event)


def check_duplicate():

    m_Controller = Controller()
    m_Viewer = view.Viewer(m_Controller)

    raw_data = ChatbotDB.query_daily_notion()
    filter_result = m_Controller.filter_query_results(raw_data)

    if isinstance(filter_result,str):
        return m_Controller.notify_viewers(filter_result)
        
    articles = [list(tmp.keys())[0] for tmp in filter_result]
    cnt_articles = ChatbotDB.article_count(articles)
    
    if not any(list(map(lambda x: x!=1,cnt_articles))):
        return m_Controller.notify_viewers("Detect no duplicated article")
        

    action = "Please merge the article with\n"
    for idx, cnt in enumerate(cnt_articles):
        article = articles[idx]
        author_list = [i["name"] for i in list(filter_result[idx].values())[0]]
        if cnt != 1:
            arthors = ', '.join(author_list)
            action += f"question number: {article} and arthor: {arthors}\n"
            '''
            TODO
            Need to push warning articles in queue and check in daily
            '''

    m_Controller.notify_viewers(action)
    return

def update_leaderboard():

    m_Controller = Controller()
    m_Viewer = view.Viewer(m_Controller)
    past_record = ChatbotDB.query_past_record()
    Controller.past_record = past_record
    action = m_Controller.count_user_points()
    # action = len(past_record)
    m_Controller.notify_viewers(action)
    
    ChatbotDB.update_record({})
    return

def daily_update():

    check_duplicate()
    update_leaderboard()
    
    return