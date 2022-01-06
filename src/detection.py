import cv2 as cv
import numpy as np
from os import listdir
from os.path import isfile, join
from pyautogui import screenshot
from time import sleep


class Detection:
    images = {}
    number_images = {}

    def __init__(self):
        self.images = self.load_images()
        self.number_images = self.load_images('.\\images\\numbers')

    def load_images(self, dirname='.\\images\\'):
        files = [f for f in listdir(
            dirname) if isfile(join(dirname, f))]

        img = {}

        for file in files:
            img[file[:-4]] = cv.imread(join(dirname, file))

        return img

    def get_screenshot(self):
        img = screenshot()
        img = np.array(img)
        img = img[:, :, ::-1].copy()

        return img

    def find_on_screen(self, target, screenshot=None, threshold=0.7, attempts=1):
        if screenshot is None:
            screenshot = self.get_screenshot()

        result = cv.matchTemplate(
            screenshot, target, cv.TM_CCOEFF_NORMED)

        h, w, _ = target.shape

        locations = np.where(result >= threshold)
        rectangles = []
        for (x, y) in zip(*locations[::-1]):
            rectangles.append((x, y, w, h))

        if len(rectangles) > 0 or attempts == 1:
            return rectangles

        sleep(1)

        return self.find_on_screen(target, None, threshold, attempts=attempts-1)

    def get_current_bc_value(self, screenshot=None):
        if screenshot == None:
            screenshot = self.get_screenshot()

        matches = self.find_on_screen(self.images['bcoins'], screenshot)
        if len(matches) == 0 or matches is None:
            return None

        x, y, w, h = matches[0]
        cropped_img = screenshot[y+h:y+h+50, x-20:x+w+20]

        found_items = []
        for key, item in self.number_images.items():
            result = cv.matchTemplate(
                item, cropped_img, cv.TM_CCOEFF_NORMED)
            threshold = 0.95
            loc = np.where(result >= threshold)
            for pt in zip(*loc[::-1]):
                found_items.append(
                    {'char': key, 'xPos': pt[0]})

        found_items = sorted(found_items, key=lambda d: d['xPos'])
        bc_value = ''.join(str(x['char']) for x in found_items)

        return [bc_value, cropped_img]


if __name__ == '__main__':
    d = Detection()
    d.load_images('.\\images\\numbers')
