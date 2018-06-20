import numpy as np
from PIL import Image
import windep
from skimage.measure import compare_ssim
import time
import cv2
import os
import screen

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


if __name__ == '__main__':
    save_area()
    #capture(5, 'no_ticket', 0.1)
    #error_testing()
    #png_to_np()
    #type_loop()
    #fetch_type()
    #compare_test()
    #save_slices()
    #template_match_test()