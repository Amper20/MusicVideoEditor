

class Event:

    def __init__(self, message, start_time, ch):
        self.message = message
        self.time = start_time
        self.channel = ch

    def __repr__(self):
        return "(" + str(self.time) + ", " + str(self.message) + ")"

    def __str__(self):
        return str(self.time) + " " + str(self.message)