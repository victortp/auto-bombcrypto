from time import sleep


class Hero:
    detection = None
    controls = None
    logger = None
    send_all = None

    def __init__(self, detection, controls, logger, send_all=False):
        self.detection = detection
        self.controls = controls
        self.logger = logger
        self.send_all = send_all

    def start(self):
        treasure_hunt = self.detection.find_on_screen(
            self.detection.images['treasure-hunt-icon'], attempts=10)

        if len(treasure_hunt) == 0:
            return False

        self.controls.mouse_click(treasure_hunt[0])

        return True

    def send_to_work(self):
        up_arrow = self.detection.find_on_screen(
            self.detection.images['up-arrow'], attempts=10)

        if len(up_arrow) > 0:
            self.controls.mouse_click(up_arrow[0])

        hero = self.detection.find_on_screen(
            self.detection.images['hero-icon'], attempts=10)

        if len(hero) > 0:
            self.controls.mouse_click(hero[0])

        # in account of possible lag
        sleep(5)

        if self.send_all:
            self.send_all_heroes()
        else:
            self.send_green_energy_heroes()

        # in account of possible lag
        sleep(3)

        x_button = self.detection.find_on_screen(
            self.detection.images['x'], attempts=10)

        if len(x_button) > 0:
            self.controls.mouse_click(x_button[0])

        down_arrow = self.detection.find_on_screen(
            self.detection.images['down-arrow'], attempts=10)

        if len(down_arrow) > 0:
            self.controls.mouse_click(down_arrow[0])

        # TODO check if all went fine and return
        return True

    def send_all_heroes(self):
        all_button = self.detection.find_on_screen(
            self.detection.images['all-button'], attempts=10)

        if len(all_button) > 0:
            self.controls.mouse_click(all_button[0])

    def send_green_energy_heroes(self):
        scroll_amount = 3
        while scroll_amount >= 0:
            green_bar = self.detection.find_on_screen(
                self.detection.images['green-bar'], threshold=0.9)

            if len(green_bar) > 0:
                work_btn = self.detection.find_on_screen(
                    self.detection.images['work'], threshold=0.9)

                if len(work_btn) > 0:
                    for gb in green_bar:
                        for wb in work_btn:
                            distance = abs(
                                (gb[1] + gb[3]/2) - (wb[1] + wb[3]/2))
                            if distance <= 10:
                                self.controls.mouse_click(wb)

            if scroll_amount > 0:
                vertical_bar = self.detection.find_on_screen(
                    self.detection.images['hero-list-vertical-bar'])

                if len(vertical_bar) == 0:
                    return False

                self.controls.mouse_drag(
                    vertical_bar[len(vertical_bar) - 1], vertical_bar[0])

            scroll_amount -= 1
            sleep(2)

    def refresh_heroes_position(self):
        x_button = self.detection.find_on_screen(
            self.detection.images['x'], attempts=2)

        if len(x_button) > 0:
            self.controls.mouse_click(x_button[0])

        go_back = self.detection.find_on_screen(
            self.detection.images['go-back-arrow'], attempts=10)

        if len(go_back) > 0:
            self.controls.mouse_click(go_back[0])

        self.start()

        # TODO check if all went fine and return
        return True
