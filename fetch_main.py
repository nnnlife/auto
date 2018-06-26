import numpy as np
from PIL import Image
import windep
from skimage.measure import compare_ssim
import time
import cv2
import os
import screen
import datetime

def png_to_np():
    im = Image.open('images' + os.sep + 'no_more.png')
    im = im.crop((132, 408, 408, 424))
     #im.save('test.png')
    current_arr = cv2.cvtColor(np.array(im), cv2.COLOR_BGR2GRAY)
    np.save('no_more.npy', current_arr)


def compare_test():
    while True:
        win = windep.WinDep()
        arr = np.load('data' + os.sep + 'no_more.npy')
        current_screen = win.capture()
        current_arr = np.array(current_screen)
        current_arr = current_arr[408:424, 132:408, :]

        current_arr = cv2.cvtColor(current_arr, cv2.COLOR_BGR2GRAY)

        (xscore, xdiff) = compare_ssim(current_arr, arr, full=True)
        print(xscore)
        time.sleep(1)


def save_slices():
    im = Image.open('targets.png')
    gap = (182 - 64)
    for i in range(4):
        s = im.crop((64 + gap*i, 648, 64 + gap*i + 52, 704))
        arr = cv2.cvtColor(np.array(s), cv2.COLOR_BGR2GRAY)
        np.save('test_' + str(i+1) + '.npy', arr)

    # 524 is end
    # search area : 64, 648, 524, 704


def save_area():
    im = Image.open('no_ticket_5.png')

    s = im.crop((137, 409, 367, 424))
    arr = cv2.cvtColor(np.array(s), cv2.COLOR_BGR2GRAY)
    np.save('no_ticket.npy', arr)


def template_match_test():
    mine = np.load('data' + os.sep + 'mine.npy')
    target = np.load('data' + os.sep + 'target.npy')
    win = windep.WinDep()

    while True:
        current_screen = win.capture()
        current_arr = np.array(current_screen)
        current_arr = current_arr[648:704, 64:524, :]
        current_arr = cv2.cvtColor(current_arr, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(current_arr, mine,
                            cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print("mine: ", min_val, max_val, min_loc, max_loc)
        res = cv2.matchTemplate(current_arr, target,
                                cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print("target: ", min_val, max_val, min_loc, max_loc)
        time.sleep(1)
        # 0.98

def fetch_type():
    t = ['infantry', 'archer', 'knight', 'tank']
    for i in range(4):
        im = Image.open('images' + os.sep + t[i] + '.png')
        arr = im.crop((254, 302, 283, 331))
        np_arr = cv2.cvtColor(np.array(arr), cv2.COLOR_BGR2GRAY)
        arr.save(t[i] + '.png')
        np.save(t[i] + '.npy', np_arr)


def capture(num, prefix, delay = 0):
    win = windep.WinDep()

    for i in range(num):
        current_screen = win.capture()
        current_screen.save(prefix + '_' + str(i+1) + '.png')
        time.sleep(delay)


def type_loop():
    tt = ['infantry', 'archer', 'knight', 'tank']
    type = []
    for t in tt:
        type.append(np.load('data' + os.sep + t + '.npy'))

    win = windep.WinDep()

    while True:
        current_screen = win.capture()
        new_c = current_screen.crop((254, 302, 283, 331))
        current_arr = cv2.cvtColor(np.array(new_c), cv2.COLOR_BGR2GRAY)
        for i in range(len(tt)):
            (score, diff) = compare_ssim(current_arr, type[i], full=True)
            print(tt[i], score)
        time.sleep(1)


def error_testing():
    im = Image.open('error2.png')
    print(screen.is_occupied_mine(im))
    print(screen.is_high_number(im))


def weather_check():
    im = Image.open('images' + os.sep + 'weather_2.png')
    print(screen.is_weather(im))


def is_castle_summary():
    im = Image.open('images' + os.sep + 'castle_result.png')
    print(screen.is_castle_summary(im))


def time_test():
    now = datetime.datetime.now()
    delta = datetime.timedelta(minutes=10)
    print(now - delta, now + delta)
    castle_time = now.replace(hour=22, minute=00, second=0, microsecond=0)
    print(abs((now - castle_time).total_seconds()))


def search_fail_test():
    im = Image.open('images' + os.sep + 'search_fail.png')
    print(screen.is_search_popup(im, True))


def capture_stress():
    win = windep.WinDep()

    while True:
        win.capture()


def castle_test():
    im = Image.open('castle_fail2_1.png')
    print(screen.is_castle_summary(im))


def time_test():
    now = datetime.datetime.now()
    print(now.hour, now.minute, now.second)


def is_time_reward():
    im = Image.open('time_reward_1.png')
    print(screen.is_time_reward(im))
    im = Image.open('none_reward_1.png')
    print(screen.is_time_reward(im))


def fetch_colors():
    win = windep.WinDep()
    red_min = 255
    red_max = 0
    blue_min = 255
    blue_max = 0
    green_min = 255
    green_max = 0
    while True:
        current_screen = win.capture()
        np_arr = np.array(current_screen)
        arr = np_arr[317:319 + 1, 319:322 + 1, :]

        for i, c in enumerate(np.nditer(arr)):
            if i % 3 is 0:  # red
                if c > red_max:
                    red_max = c
                if c < red_min:
                    red_min = c
            elif (i + 2) % 3 is 0:  # green
                if c > green_max:
                    green_max = c
                if c < green_min:
                    green_min = c

        print("R", red_min, red_max, "G", green_min, green_max, "B", blue_min, blue_max)

if __name__ == '__main__':
    #is_time_reward()
    #capture_stress()
    #search_fail_test()
    #time_test()
    #weather_check()
    #save_area()
    fetch_colors()
    #capture(1, 'time_r', 0)
    #error_testing()
    #png_to_np()
    #type_loop()
    #fetch_type()
    #compare_test()
    #save_slices()
    #template_match_test()
    #castle_test()
    #time_test()