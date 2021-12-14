class Viewer(object):
    def __init__(self, name, controller):
        self.name = name
        controller.register(self)
 
    def notify(self, event):
        print(self.name, "received event", event)