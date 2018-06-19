import datetime


class Hunter:
    def __init__(self):
        self.hunting_start_time = None
        self.capture = None

    def reset(self):
        self.hunting_start_time = None
        self.capture = None
        return self

    def set_hunting_start(self):
        self.hunting_start_time = datetime.datetime.now()

    def is_hunting_timeout(self):
        if (datetime.datetime.now() - self.hunting_start_time).total_seconds() > 60 * 10:
            self.hunting_start_time = None
            return True

        return False

    def set_capture(self, capture):
        self.capture = capture

    def get_capture(self):
        return self.capture