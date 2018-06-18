from minerstate import state
import winkey
import screen
import time
import datetime

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
        now = datetime.datetime.now()
        weather_start = now.replace(hour=22, minute=30, second=0, microsecond=0)
        weather_end = now.replace(hour=22, minute=40, second=0, microsecond=0)

        new_day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        new_day_end = now.replace(hour=0, minute=10, second=0, microsecond=0)

        if weather_start < now < weather_end:
            print("CHECKARMY WAIT WEATHER")
            time.sleep(5)
            return False
        elif new_day_start < now < new_day_end:
            print("CHECKARMY WAIT NEWDAY")
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

    def on_event(self, event):
        next_status = self.get_status().on_event(event)
        if next_status:
            self.set_status(next_status)
            #print("State %s%s" % (str(self), str(self.get_status())))
            return self

        return None

