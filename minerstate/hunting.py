from minerstate import state
import winkey
import screen
import datetime
import time


class _CompareArmy(state.SubState):
    def __init__(self, hunter):
        state.SubState.__init__(self, hunter)
        self.done = False

    def do(self, event):
        return True

    def check(self, event):
        if screen.army_is_back(self.get_hunter().get_capture, event):
            self.done = True
        winkey.send_key(winkey.VK_CODE['esc'])
        time.sleep(1)
        return True

    def next(self):
        if self.done:
            return None
        return _ClickForCheckArmy(self.get_hunter())


class _ClickForCheckArmy(state.SubState):
    def __init__(self, hunter):
        state.SubState.__init__(self, hunter)

    def do(self, event):
        winkey.send_key(winkey.VK_CODE['m'])
        return True

    def check(self, event):
        if screen.is_area_popup(event):
            time.sleep(1)
            return True
        return False

    def next(self):
        return _CompareArmy(self.get_hunter())


class _SetMine(state.SubState):
    def __init__(self, hunter):
        state.SubState.__init__(self, hunter)

    def do(self, event):
        if screen.is_mine_found(event):
            winkey.send_key(winkey.VK_CODE['h'])
        else:
            winkey.send_key(winkey.VK_CODE['d'])
            time.sleep(1)
            return False
        return True

    def check(self, event):
        if screen.is_search_popup(event):
            return True
        return False

    def next(self):
        return _ClickForCheckArmy(self.get_hunter())


class _PointToMine(state.SubState):
    def __init__(self, hunter):
        state.SubState.__init__(self, hunter)

    def do(self, event):
        winkey.send_key(winkey.VK_CODE['q'])
        return True

    def check(self, event):
        if screen.is_search_popup(event):
            return True
        return False

    def next(self):
        return _SetMine(self.get_hunter())


class _Attack(state.SubState):
    def __init__(self, hunter):
        state.SubState.__init__(self, hunter)
        self.set_mine = False
        self.defeat_popup = False

    def do(self, event):
        time.sleep(1)
        winkey.send_key(winkey.VK_CODE['z'])
        time.sleep(1)
        winkey.send_key(winkey.VK_CODE['x'])
        self.get_hunter().set_hunting_start()
        return True

    def check(self, event):
        if self.defeat_popup and not screen.is_defeat_popup(event):
            return True
        elif screen.is_defeat_popup(event):
            print("DEFEAT POPUP")
            self.defeat_popup = True
        elif self.get_hunter().is_hunting_timeout():
            print("HUNTING TIMEOUT")
            return True
        return False

    def next(self):
        return _PointToMine(self.get_hunter())


class _CheckTarget(state.SubState):
    index = 0
    def __init__(self, hunter):
        state.SubState.__init__(self, hunter)
        self.can_defeat = False
        self.set_mine = False
        self.go_attack = False
        self.pressed = False

    def do(self, event):
        type = screen.get_target_type(event)
        if type == -1:
            return False

        self.can_defeat = self.get_hunter().can_defeat(type)
        if self.can_defeat:
            winkey.send_key(winkey.VK_CODE['y'])  # TODO: change to attack key
            self.go_attack = True
            self.pressed = True
        else:
            winkey.send_key(winkey.VK_CODE['g'])  # TODO: change to next
            self.pressed = True
        return True

    def check(self, event):
        if self.pressed:
            if not screen.is_target_screen(event):
                self.pressed = False
            return False

        if self.can_defeat:
            if screen.dispatch_army_popup(event):
                return True

            return False
        else:
            # no more
            print("SAVE", _CheckTarget.index)
            #event.save('test_' + str(_CheckTarget.index) + '.png')
            _CheckTarget.index += 1
            if screen.is_no_more_target(event):
                print("NO MORE TARGET")
                self.set_mine = True
                return True
            elif screen.is_target_screen(event):
                print("GO TO TARGET SCREEM")
                return True

        return False

    def next(self):
        if self.set_mine:
            return _PointToMine(self.get_hunter())
        elif self.go_attack:
            return _Attack(self.get_hunter())

        return _CheckTarget(self.get_hunter())


class _NextTarget(state.SubState):
    def __init__(self, hunter):
        state.SubState.__init__(self, hunter)
        self.set_mine = False

    def do(self, event):
        winkey.send_key(winkey.VK_CODE['n'])
        return True

    def check(self, event):
        if screen.is_no_more_target(event):
            self.set_mine = True
            return True
        elif screen.is_target_screen(event):
            return True

        return False

    def next(self):
        if self.set_mine:
            return _PointToMine(self.get_hunter())
        return _CheckTarget(self.get_hunter())


class _SetTarget(state.SubState):
    def __init__(self, hunter):
        state.SubState.__init__(self, hunter)

    def do(self, event):
        if screen.is_target_found(event):
            winkey.send_key(winkey.VK_CODE['j'])
        else:
            winkey.send_key(winkey.VK_CODE['d'])
            time.sleep(1)
            return False
        return True

    def check(self, event):
        if screen.is_search_popup(event):
            return True
        return False

    def next(self):
        return _NextTarget(self.get_hunter())


class _CaptureArea(state.SubState):
    def __init__(self, player):
        state.SubState.__init__(self, player)

    def do(self, event):
        # Capture 1st
        self.get_hunter().set_capture(screen.capture_primary_army(event))
        winkey.send_key(winkey.VK_CODE['0'])
        return True

    def check(self, event):
        if screen.is_search_popup(event):
            return True
        return False

    def next(self):
        return _SetTarget(self.get_player())


class _ClickArea(state.SubState):
    def __init__(self, hunter):
        state.SubState.__init__(self, hunter)

    def do(self, event):
        winkey.send_key(winkey.VK_CODE['m'])
        return True

    def check(self, event):
        if screen.is_area_popup(event):
            return True
        return False

    def next(self):
        return _CaptureArea(self.get_hunter())


class _Search(state.SubState):
    def __init__(self, hunter):
        state.SubState.__init__(self, hunter)

    def do(self, event):
        now = datetime.datetime.now()
        weather_start = now.replace(hour=22, minute=30, second=0, microsecond=0)
        weather_end = now.replace(hour=22, minute=40, second=0, microsecond=0)

        new_day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        new_day_end = now.replace(hour=0, minute=10, second=0, microsecond=0)

        if weather_start < now < weather_end:
            print("WAIT WEATHER")
            time.sleep(5)
            return False
        elif new_day_start < now < new_day_end:
            print("WAIT NEWDAY")
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
        return _ClickArea(self.get_hunter())


class Hunting(state.State):
    def __init__(self, hunter):
        state.State.__init__(self, hunter)
        self.set_status(_Search(hunter))

    def is_waiting(self):
        return False

    def on_event(self, event):
        next_status = self.get_status().on_event(event)
        if next_status:
            self.set_status(next_status)
            print("State %s%s" % (str(self), str(self.get_status())))
            return self
        else:
            return None