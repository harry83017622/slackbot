class Viewer(object):
    def __init__(self, controller):
        controller.register(self)
 
    def notify(self, event):
        print("received event", event)