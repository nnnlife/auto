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


def occasion_exist(img):
    if screen.is_weather(current_screen):
        winkey.send_key(winkey.VK_CODE['w'])
        time.sleep(3)
        return True
    elif screen.is_reward(current_screen):
        winkey.send_key(winkey.VK_CODE['f'])
        time.sleep(3)
        return True

    return False


def is_hunting_available(h):
    now = datetime.datetime.now()
    # earlier 10 min than normal
    weather_start = now.replace(hour=22, minute=20, second=0, microsecond=0)
    weather_end = now.replace(hour=22, minute=40, second=0, microsecond=0)

    # earlier 10 min than normal
    new_day_start = now.replace(hour=23, minute=50, second=0, microsecond=0)
    new_day_end = now.replace(hour=0, minute=10, second=0, microsecond=0)

    if weather_start < now < weather_end:
        print("WAIT WEATHER")
        time.sleep(5)
        return False
    elif new_day_start < now < new_day_end:
        print("WAIT NEWDAY")
        time.sleep(5)
        return False

    if (datetime.datetime.now() - h.get_last_no_ticket_time()).total_seconds() > 60 * 30:
        return True
    return False


# TODO: 황건 모집령 다 썼을 경우 에러 처리

if __name__ == '__main__':
    win = windep.WinDep()
    army = checkarmy.CheckArmy()
    miners = []
    hunt = None
    players = [player.Player((6, 2)), player.Player((5,4))]

    BLOCK_HUNTING = False
    hunter = hunter.Hunter([3])  # ['infantry', 'archer', 'knight', 'tank']

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
                            time.sleep(random.randint(10, 20))
            else:
                time.sleep(0.1)
