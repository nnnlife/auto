import windep
import miner
import time
import player
import screen
import winkey
import random
from minerstate import checkarmy


if __name__ == '__main__':
    win = windep.WinDep()
    army_check = False
    army = None
    startup = True
    miners = []
    players = [player.Player((6, 2)), player.Player((4,5))]

    while True:
        current_screen = win.capture()
        waiting_exist = False
        #current_screen.save('archer.png')
        #exit(0)
        if army_check:
            army = army.on_event(current_screen)

            if not army:
                miners = []
                army_check = False
                for p in players:
                    p.player_waiting_reset()
                    miners.append(miner.Miner(p, screen.army_exists(current_screen,
                                                                    p.base_area())))
                winkey.send_key(winkey.VK_CODE['esc'])
                time.sleep(1)
                winkey.send_key(winkey.VK_CODE['esc'])
                time.sleep(1)
                if not startup:
                    print("SLEEP")
                    time.sleep(random.randint(10, 20))
                startup = False
            continue

        if screen.is_weather(current_screen):
            winkey.send_key(winkey.VK_CODE['w'])
            time.sleep(3)
        elif screen.is_reward(current_screen):
            winkey.send_key(winkey.VK_CODE['f'])
            time.sleep(3)
        elif startup:
            army_check = True
            army = checkarmy.CheckArmy()
            continue

        for m in miners:
            if not m.is_waiting():
                m.next(current_screen)

        for m in miners:
            if m.is_waiting():
                m.next(current_screen)
                waiting_exist = True
                break

        if not waiting_exist:
            army_check = True
            army = checkarmy.CheckArmy()

        time.sleep(0.1)
