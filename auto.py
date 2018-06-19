import windep
import miner
import time
import player
import screen
import winkey
import hunter
import random
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


def is_hunting_available():
    return True


if __name__ == '__main__':
    win = windep.WinDep()
    army = checkarmy.CheckArmy()
    miners = []
    hunt = None
    players = [player.Player((6, 2)), player.Player((4,5))]
    hunter = hunter.Hunter()

    while True:
        current_screen = win.capture()
        # current_screen.save('archer.png')
        # exit(0)
        waiting_exist = False
        hunting_exist = False

        if occasion_exist(current_screen):
            continue

        for m in miners:
            if m.is_waiting():
                waiting_exist = True
                m.next(current_screen)
                break

        if waiting_exist or hunting_exist:    # startup
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
                        print("SLEEP")
                        if is_hunting_available():
                            hunt = hunting.Hunting(hunter.reset())
                            time.sleep(0.1)
                        else:
                            time.sleep(random.randint(10, 20))
            else:
                time.sleep(0.1)
