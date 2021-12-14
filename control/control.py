from ..model import model
from ..view import view

class AbstractSubject(object):
    def register(self, listener):
        raise NotImplementedError("Must subclass me")
 
    def deregister(self, listener):
        raise NotImplementedError("Must subclass me")
 
    def notify_viewer(self, event):
        raise NotImplementedError("Must subclass me")
 
ChatbotDB = model.Modeler()

class Controller(AbstractSubject):
    def __init__(self):
        self.listeners = []
        self.data = None

    def do_something_1(self, raw_data):
        self.data = raw_input('Enter something to do:')
        return self.data

    def do_something_2(self):
        self.data = raw_input('Enter something to do:')
        return self.data

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
    action = m_Controller.do_something_1(raw_data)
    m_Controller.notify_viewers(action)

    return

def update_leaderboard():

    m_Controller = Controller()
    m_Viewer = view.Viewer(m_Controller)

    raw_data = ChatbotDB.query_daily_notion()
    action = m_Controller.do_something_2(raw_data)
    m_Controller.notify_viewers(action)
    return

def daily_update():
    # query self db
    # query notion api
    # implement this in model 

    # instantiate view
    # register view to this process(controller)
    # do this for check duplicate and daily leaderboard
    
    check_duplicate()
    update_leaderboard()

    return