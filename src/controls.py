import pyautogui
import math
from random import random, randint


class Controls:
    randomize_mouse_movement = None

    def __init__(self, randomize_mouse_movement=True):
        self.randomize_mouse_movement = randomize_mouse_movement
        pyautogui.FAILSAFE = False

    def mouse_click(self, rectangle):
        self.mouse_move(rectangle)
        pyautogui.click()

    def mouse_move(self, rectangle):
        click_pos = self.get_click_position(rectangle)
        speed = self.get_mouse_speed(click_pos)
        easing = self.get_mouse_easing()
        pyautogui.moveTo(click_pos[0], click_pos[1],
                         speed, easing)

    def mouse_drag(self, drag_from, drag_to):
        self.mouse_move(drag_from)
        pyautogui.dragTo(drag_to[0], drag_to[1],
                         self.get_mouse_speed(self.get_click_position(drag_from)) + 3, button='left')

    def get_click_position(self, rectangle):
        x, y, w, h = rectangle

        return ((int(x+w/2), int(y+h/2)))

    def get_mouse_speed(self, click_pos):
        x, y = click_pos
        mouse_x, mouse_y = pyautogui.position()
        distance = math.sqrt(math.pow((x-mouse_x), 2)+math.pow((y-mouse_y), 2))
        speed = distance / 500 / (random() * 2)
        speed = 1 * random() * 2 if speed > 1 else speed
        return speed

    def get_mouse_easing(self):
        if not self.randomize_mouse_movement:
            return pyautogui.easeOutQuad

        l = [pyautogui.easeInQuad, pyautogui.easeOutQuad,
             pyautogui.easeInOutQuad, pyautogui.easeInBounce, pyautogui.easeInElastic]

        return l[randint(0, len(l) - 1)]

    def reload_page(self):
        pyautogui.hotkey('ctrl', 'f5')
