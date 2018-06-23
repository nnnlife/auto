from minerstate import state
import winkey
import screen
import time
import os
import datetime
from minerstate import gomining
import eventtime


_SCREEN_DIR = 'screen'


def _create_directory(p):
    if not os.path.exists(p):
        os.makedirs(p)


def get_screen_dir():
    dirpath = '.'
    screen_dir = dirpath + os.sep + _SCREEN_DIR
    _create_directory(screen_dir)
    return screen_dir + os.sep


class _CheckOtherGoing(state.SubState):
    def __init__(self, player):
        state.SubState.__init__(self, player)
        self.occupied = True

    def do(self, event):
        time.sleep(1.5)
        return True

    def check(self, event):
        if screen.is_other_going(event):
            winkey.send_key(winkey.VK_CODE['b'])
            self.get_player().add_occupied_mine()
            time.sleep(1.5)
        else:
            print("Good")
            event.save(get_screen_dir() + os.sep +
                       datetime.datetime.now().strftime('%Y%m%d_%H%M%S_Z') + '.png')
            self.occupied = False
            time.sleep(5)
        return True

    def next(self):
        if self.occupied:
            return _Search(self.get_player())
        else:
            return None


class _TryMining(state.SubState):
    def __init__(self, player):
        state.SubState.__init__(self, player)

    def do(self, event):
        winkey.send_key(winkey.VK_CODE['c'])
        return True

    def check(self, event):
        if screen.dispatch_army_popup(event):
            winkey.send_key(winkey.VK_CODE['z'])
            time.sleep(0.5)
            winkey.send_key(winkey.VK_CODE['x'])
            return True

        return False

    def next(self):
        return _CheckOtherGoing(self.get_player())


class _NextMine(state.SubState):
    def __init__(self, player):
        state.SubState.__init__(self, player)
        self.mine_available = False
        self.unknown_count = 0

    def do(self, event):
        self.get_player().increase_try_count()
        winkey.send_key(winkey.VK_CODE['n'])
        return True

    def check(self, event):
        result = screen.is_occupied_mine(event, self.unknown_count)
        # print("Result : %d" % result)
        if result is screen.UNKNOWN:
            time.sleep(0.05)
            self.unknown_count += 1
            if self.unknown_count > 3 and screen.is_search_popup(event):
                self.unknown_count = 0
                if self.get_player().get_try_count() is 0:
                    self.get_player().decrease_try_count()
                self.go_to_do()
            elif self.unknown_count > 20:
                self.unknown_count = 0
                if self.get_player().get_try_count() is 0:
                    self.get_player().decrease_try_count()
                self.mine_available = False
                return True
            return False
        elif result is screen.AVAILABLE and screen.is_high_number(event):
            self.unknown_count = 0
            if screen.is_checked_mine(event, self.get_player()):
                self.mine_available = False
            else:
                self.get_player().set_current_mine(screen.fetch_pos_area_as_gray(event))
                event.save(get_screen_dir() + os.sep +
                           datetime.datetime.now().strftime('%Y%m%d_%H%M%S_C') + '.png')
                self.mine_available = True
        else:
            self.unknown_count = 0
            self.mine_available = False
        return True

    def next(self):
        if self.mine_available:
            return _TryMining(self.get_player())
        return _Search(self.get_player())


class _SelectArea(state.SubState):
    def __init__(self, player):
        state.SubState.__init__(self, player)

    def do(self, event):
        winkey.send_key(winkey.VK_CODE['0'] + self.get_player().get_mine_area())
        return True

    def check(self, event):
        if screen.is_search_popup(event):
            return True
        return False

    def next(self):
        return _NextMine(self.get_player())


class _ClickArea(state.SubState):
    def __init__(self, player):
        state.SubState.__init__(self, player)

    def do(self, event):
        winkey.send_key(winkey.VK_CODE['m'])
        return True

    def check(self, event):
        if screen.is_area_popup(event):
            return True
        return False

    def next(self):
        return _SelectArea(self.get_player())


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
        if self.get_player().get_try_count() is 0:
            return _ClickArea(self.get_player())
        return _NextMine(self.get_player())


class WaitStatus(state.State):
    def __init__(self, player):
        state.State.__init__(self, player)
        self.set_status(_Search(player))
        self.last_state = ""

    def is_waiting(self):
        return True

    def on_event(self, event):
        next_status = self.get_status().on_event(event)
        if next_status:
            self.set_status(next_status)
            state = "State %s%s" % (str(self), str(self.get_status()))
            if self.last_state != state:
                print(state)
            self.last_state = state
            return self
        else:
            return gomining.GoMiningStatus(self.get_player())

