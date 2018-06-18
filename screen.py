import numpy as np
import cv2
from skimage.measure import compare_ssim


UNKNOWN = 0
OCCUPIED = 1
AVAILABLE = 2


def _check_area_with_color(img, area, red_r, green_r, blue_r, debug = False):
    """
    :param img: PIL Image
    :param area: (start x, start y, end x, end y)
    :param red_r: (red rgb range start, red rgb range end)
    :param green_r:
    :param blue_r:
    :return: Bool
    """
    np_arr = np.array(img)
    np_arr = np_arr[area[1]:area[3], area[0]:area[2], :]
    if debug:
        print(np_arr)

    for i, c in enumerate(np.nditer(np.array(np_arr))):
        if i % 3 is 0:  # red
            if red_r[1] < c or c < red_r[0]:
                if debug:
                    print("Red Fail %d %d %d" % (c, red_r[0], red_r[1]))
                return False
        elif (i + 2) % 3 is 0:  # green
            if green_r[1] < c or c < green_r[0]:
                return False
        elif (i + 3) % 3 is 0:  # blue
            if blue_r[1] < c or c < blue_r[0]:
                return False

    if debug:
        print("Return TRUE")
    return True


def is_search_popup(img):
    return _check_area_with_color(img, (4, 578, 151, 579),
                                  (23,23), (26,26), (31, 31))


def is_area_popup(img):
    black_header = _check_area_with_color(img, (20, 181, 200, 182),
                                          (20, 25), (20, 25), (20, 25))
    blue_button = _check_area_with_color(img, (427, 219, 500, 220),
                                         (104, 106), (141, 143), (183, 185))
    return black_header and blue_button


def is_checked_mine(img, player):
    occupied_mines = player.get_occupied_mine()
    xpos, ypos = fetch_pos_area_as_gray(img)

    for o in occupied_mines:
        (xscore, xdiff) = compare_ssim(xpos, o[1], full=True)
        (yscore, ydiff) = compare_ssim(ypos, o[2], full=True)
        print("XSCORE", xscore)
        print("YSCORE", yscore)
        if xscore > 0.8 and yscore > 0.8:
            return True

    return False


def is_occupied_mine(img, count = 0):
    icon_areas = [(389, 571, 393, 576 + 1), (394, 560, 395, 561 + 1),  # 5th
                  (335, 618, 340, 623 + 1), (360, 617, 362, 619 + 1),  # 4th
                  (267, 634, 273, 638 + 1),                            # 3rd
                  (182, 607, 201, 611 + 1),                            # 2nd
                  (137, 556, 140, 569 + 1)]                            # 1th
    result = OCCUPIED
    for area in icon_areas:
        if not _check_area_with_color(img, area,
                                      (200, 255), (200, 255), (200, 255)):
            if count is 0:
                print("UNKNOWN")
            result = UNKNOWN
            break

    if result is OCCUPIED:
        print("OCCUPIED")
        return OCCUPIED

    icon_areas = [(335, 620, 346, 623 + 1), (360, 617, 362, 619 + 1),  # 3rd
                  (268, 634, 273, 638 + 1),                            # 2nd
                  (190, 601, 194, 614 + 1)]                            # 1nd

    black_areas = [(184, 594, 198 + 1, 594 + 1),
                   (263, 614, 276 + 1, 614 + 1),
                   (341, 594, 352 + 1, 594 + 1)]

    result = AVAILABLE
    for area in icon_areas:
        if not _check_area_with_color(img, area,
                                      (200, 255), (200, 255), (200, 255)):
            if count is 0:
                print("UNKNOWN")
            result = UNKNOWN
            break

    for area in black_areas:
        if not _check_area_with_color(img, area,
                                      (15, 30), (15, 30), (15, 30)):
            result = UNKNOWN
            if count is 0:
                print("UNKNOWN")
            break

    if result is AVAILABLE:
        print("AVAILABLE")
        return AVAILABLE

    return UNKNOWN


def dispatch_army_popup(img):
    blue_area = _check_area_with_color(img, (132, 918, 213, 918 + 1),
                                       (125, 140), (160, 185), (195, 210))
    yellow_area = _check_area_with_color(img, (342, 918, 396, 918 + 1),
                                         (195, 210), (170, 190), (115, 135))

    return blue_area and yellow_area


def is_other_going(img):
    blue_area = _check_area_with_color(img, (110, 612, 167, 612 + 1),
                                       (125, 140), (160, 185), (195, 210))
    yellow_area = _check_area_with_color(img, (344, 612, 409, 612 + 1),
                                         (195, 210), (170, 190), (115, 135))

    return blue_area and yellow_area


def is_high_number(img):
    # 311, 393, 316, 401
    np_arr = np.array(img)
    np_arr = np_arr[393:401+1, 304:309+1, :]

    count = 0
    for i in range(402-393):
        for j in range(317-311):
            if np_arr[i][j][0] > 17 and np_arr[i][j][1] > 17 and np_arr[i][j][2] > 17:
                count += 1

    print("NUMBER COUNT:%d" % count)
    if count >= 20:
        return True

    return False


def is_weather(img):
    # 470, 259, 478 + 1, 266 + 1  r = 150, 250, g = 60, 90, b = 40, 50
    # 458, 247, 464 + 1, 250 + 1  r = 210, 230, g = 90, 105, b = 50, 65
    # 484, 250, 488 + 1, 252 + 1  r = 195, 230, g = 90, 105, b = 50, 65
    # 482, 271, 484 + 1, 273 + 1  r = 135, 150, g = 45, 60, b = 25, 35
    r1 = _check_area_with_color(img, (470, 259, 478+1, 266+1),
                                       (150, 250), (60, 90), (40, 50))
    r2 = _check_area_with_color(img, (458, 247, 464 + 1, 250 + 1),
                                (210, 230), (90, 105), (50, 65))
    r3 = _check_area_with_color(img, (484, 250, 488 + 1, 252 + 1),
                                (195, 230), (90, 105), (50, 65))
    r4 = _check_area_with_color(img, (482, 271, 484 + 1, 273 + 1),
                                (130, 150), (45, 60), (25, 35))

    return r1 and r2 and r3 and r4


def army_exists(img, index):
    y = 230 + 110 * index
    height = 11
    x = 187
    width = 2
    np_arr = np.array(img)
    np_arr = np_arr[y:y+height, x:x+width, :]
    for i in range(height):
        for j in range(width):
            if np_arr[i][j][0] > 200 and np_arr[i][j][1] > 200 and np_arr[i][j][2] > 200:
                print("ARMY EXIST")
                return True
    print("NO ARMY")
    return False


def is_reward(img):
    red = _check_area_with_color(img, (74, 633, 85 + 1, 649 + 1),
                                (200, 210), (60, 65), (50, 55))
    orange = _check_area_with_color(img, (71, 660, 81 + 1, 667 + 1),
                                 (200, 230), (145, 150), (60, 70))
    orange2 = _check_area_with_color(img, (236, 655, 248 + 1, 666 + 1),
                                    (200, 230), (145, 150), (60, 70))
    return red and orange and orange2


def fetch_pos_area_as_gray(img):
    np_arr = np.array(img)
    x_np_arr = np_arr[823:837+1, 225:239+1, :]
    y_np_arr = np_arr[823:837 + 1, 296:330 + 1, :]
    x_gray = cv2.cvtColor(x_np_arr, cv2.COLOR_BGR2GRAY)
    y_gray = cv2.cvtColor(y_np_arr, cv2.COLOR_BGR2GRAY)
    return x_gray, y_gray


