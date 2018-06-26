import windep
import miner
import time
import player
import screen
import winkey
import hunter
import random
import datetime
from minerstate import checkarmy
from minerstate import hunting
import eventtime


def occasion_exist(img):
    now = datetime.datetime.now()
    castle_time = now.replace(hour=22, minute=00, second=0, microsecond=0)
    is_in_castle_time = abs((now - castle_time).total_seconds()) < 10 * 60

    if screen.is_weather(img):  # 22:30, 24:00 short
        winkey.send_key(winkey.VK_CODE['l'])
        time.sleep(3)
        return True
    elif screen.is_reward(img):  # RANDOM
        winkey.send_key(winkey.VK_CODE['f'])
        time.sleep(3)
        return True
    elif is_in_castle_time and screen.is_castle_summary(img):     # 22:00
        winkey.send_key(winkey.VK_CODE['k'])
        time.sleep(3)
        return True

    return False


def is_hunting_available(h):
    if eventtime.is_event_time():
        return False

    if datetime.datetime.now().hour is not h.get_last_no_ticket_time().hour:
        return True

    return False


if __name__ == '__main__':
    win = windep.WinDep()
    army = checkarmy.CheckArmy()
    miners = []
    hunt = None
    players = [player.Player((5, 2)), player.Player((1,3))]

    BLOCK_HUNTING = False
    hunter = hunter.Hunter([0, 3])  # ['infantry', 'archer', 'knight', 'tank']

    while True:
        current_screen = win.capture()
        waiting_exist = False

        if occasion_exist(current_screen):
            continue

        for m in miners:
            if m.is_waiting():
                waiting_exist = True
                m.next(current_screen)
                break

        if waiting_exist:    # startup
            time.sleep(0.1)
        elif hunt is not None:
            hunt = hunt.on_event(current_screen)
        else:
            army = army.on_event(current_screen)
            if not army:
                army = checkarmy.CheckArmy()
                winkey.send_key(winkey.VK_CODE['esc'])
                time.sleep(1)
                winkey.send_key(winkey.VK_CODE['esc'])
                time.sleep(1)

                if len(miners) is 0:
                    for p in players:
                        miners.append(miner.Miner(p, screen.army_exists(current_screen,
                                                                        p.base_area())))
                else:
                    found = False
                    for i, p in enumerate(players):
                        if screen.army_exists(current_screen, p.base_area()):
                            p.player_waiting_reset()
                            miners[i].set_wait_status(p)
                            found = True

                    if not found:
                        if not BLOCK_HUNTING and is_hunting_available(hunter):
                            print("START HUNTING")
                            hunt = hunting.Hunting(hunter.reset())
                            time.sleep(0.1)
                        else:
                            print("SLEEP")
                            if not eventtime.is_event_time():
                                time.sleep(5)
                                winkey.send_key(winkey.VK_CODE['o'])
                                time.sleep(5)
                                current_screen = win.capture()
                                if screen.is_time_reward(current_screen):
                                    winkey.send_key(winkey.VK_CODE['r'])
                                    time.sleep(6)
                                    winkey.send_key(winkey.VK_CODE['r'])
                                    time.sleep(5)
                                    winkey.send_key(winkey.VK_CODE['o'])
                                else:
                                    winkey.send_key(winkey.VK_CODE['o'])

                            time.sleep(random.randint(10, 20))
            else:
                time.sleep(0.1)
