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
    def __init__(self):
        self.listeners = []
        self.data = None

    def filter_query_results(self, response):
        if response.status_code != 200:
            return "bad request response"

        # print(response.json()["results"])
        nums = [{num["properties"]["題號"]["number"]:num["properties"]["Person"]["people"]} for num in response.json()["results"]]
        return nums

    def do_something_2(self):
        # self.data = raw_input('Enter something to do:')
        # return self.data
        pass

    # Implement abstract Class AbstractSubject

    def register(self, listener):
        self.listeners.append(listener)
 
    def deregister(self, listener):
        self.listeners.remove(listener)
 
    def notify_viewers(self, event):
        for listener in self.listeners:
            listener.notify(event)


def check_duplicate(query_today=None):

    m_Controller = Controller()
    m_Viewer = view.Viewer(m_Controller)

    raw_data = ChatbotDB.query_daily_notion()
    nums_authors_map = m_Controller.filter_query_results(raw_data)
    
    articles = [list(tmp.keys())[0] for tmp in nums_authors_map]
    cnt_articles = ChatbotDB.article_count(articles)
    
    if not any(list(map(lambda x: x!=1,cnt_articles))):
        m_Controller.notify_viewers("Detect no duplicated article")
        return

    action = "Please merge the article with\n"
    for idx, cnt in enumerate(cnt_articles):
        if cnt != 1:
            article = articles[idx]
            
            author_list = [i["name"] for i in list(nums_authors_map[idx].values())[0]]
            arthors = ', '.join(author_list)
            action += f"question number: {article} and arthor: {arthors}\n"
    
    m_Controller.notify_viewers(action)
    return

# def update_leaderboard():

#     m_Controller = Controller()
#     m_Viewer = view.Viewer(m_Controller)

    
#     action = m_Controller.do_something_2(raw_data)
#     m_Controller.notify_viewers(action)
#     return

def daily_update():

    query_today = ChatbotDB.query_daily_notion()
    query_past = ChatbotDB.query_past_record()

    check_duplicate(query_today=query_today)
    # update_leaderboard()

    return