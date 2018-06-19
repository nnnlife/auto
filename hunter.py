import datetime
import numpy as np
import os


class Hunter:
    mine = np.load('data' + os.sep + 'mine.npy')
    target = np.load('data' + os.sep + 'target.npy')
    no_more = np.load('data' + os.sep + 'no_more.npy')
    tt = ['infantry', 'archer', 'knight', 'tank']
    types = [np.load('data' + os.sep + tt[0] + '.npy'),
             np.load('data' + os.sep + tt[1] + '.npy'),
             np.load('data' + os.sep + tt[2] + '.npy'),
             np.load('data' + os.sep + tt[3] + '.npy')]

    def __init__(self, win_types):
        self.hunting_start_time = None
        self.capture = None
        self.win_types = win_types

    def reset(self):
        self.hunting_start_time = None
        self.capture = None
        return self

    def can_defeat(self, type):
        for i in self.win_types:
            if type == i:
                return True
        return False

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