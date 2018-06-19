import enum


class Action(enum.Enum):
    DO, CHECK, DONE = range(3)


class State:
    def __init__(self, player):
        self.player = player
        self.status = None

    def get_player(self):
        return self.player

    def set_status(self, substate):
        self.status = substate

    def get_status(self):
        return self.status

    def on_event(self):
        pass

    def is_waiting(self):
        return False

    def check_status(self):
        pass

    def __repr(self):
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__


class SubState:
    def __init__(self, player):
        self.player = player
        self.step = Action.DO

    def do(self, event):
        return False

    def check(self, event):
        return False

    def next(self):
        return self

    def get_player(self):
        return self.player

    def get_hunter(self):
        return self.player

    def go_to_do(self):
        self.step = Action.DO

    def on_event(self, event):
        if self.step is Action.DO:
            if self.do(event):
                self.step = Action.CHECK
        elif self.step is Action.CHECK:
            if self.check(event):
                self.step = Action.DONE

        if self.step is Action.DONE:
            return self.next()

        return self

    def __repr(self):
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__
