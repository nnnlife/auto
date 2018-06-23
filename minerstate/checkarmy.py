from minerstate import state
import winkey
import screen
import time
import datetime
import eventtime


class _ClickArea(state.SubState):
    def __init__(self, player):
        state.SubState.__init__(self, player)

    def do(self, event):
        winkey.send_key(winkey.VK_CODE['m'])
        time.sleep(1)  # to prevent empty string
        return True

    def check(self, event):
        if screen.is_area_popup(event):
            return True
        return False

    def next(self):
        return None


class _Search(state.SubState):
    def __init__(self, player):
        state.SubState.__init__(self, player)

    def do(self, event):
        if eventtime.is_event_time():
            time.sleep(5)
            return False
        else:
            winkey.send_key(winkey.VK_CODE['q'])
        return True

    def check(self, event):
        if screen.is_search_popup(event):
            return True
        return False

    def next(self):
        return _ClickArea(self.get_player())



class CheckArmy(state.State):
    def __init__(self):
        state.State.__init__(self, None)
        self.set_status(_Search(None))
        self.last_state = ""

    def on_event(self, event):
        next_status = self.get_status().on_event(event)
        if next_status:
            self.set_status(next_status)
            state = "State %s%s" % (str(self), str(self.get_status()))
            if self.last_state != state:
                print(state)
            self.last_state = state
            return self

        return None

