from time import sleep


class Login:
    detection = None
    controls = None
    logger = None
    attempts = None

    def __init__(self, detection, controls, logger, attempts=10):
        self.detection = detection
        self.controls = controls
        self.logger = logger
        self.attempts = attempts

    def is_connected(self):
        screenshot = self.detection.get_screenshot()
        # check if connect wallet button is visible on the screen
        connect_button = self.detection.find_on_screen(
            self.detection.images['connect-wallet'], screenshot)

        if len(connect_button) > 0:
            return False

        # check if error message box is visible on the screen
        error_messagebox = self.detection.find_on_screen(
            self.detection.images['error'], screenshot)

        if len(error_messagebox) > 0:
            return False

        # check if bombcrypto logo is visible on the screen
        logo = self.detection.find_on_screen(
            self.detection.images['bomb-logo'], screenshot)

        if len(logo) > 0:
            return False

        return True

    def move_to_game_window(self):
        corner = self.detection.find_on_screen(
            self.detection.images['game-corner'])

        if len(corner) == 0:
            return False

        self.controls.mouse_click(corner[0])
        return True

    def sign_in(self):
        self.move_to_game_window()
        self.controls.reload_page()
        sleep(2)

        connect_button = self.detection.find_on_screen(
            self.detection.images['connect-wallet'], attempts=self.attempts)

        if len(connect_button) > 0:
            self.controls.mouse_click(connect_button[0])

        sign_button = self.detection.find_on_screen(
            self.detection.images['sign'], attempts=self.attempts)

        if len(sign_button) > 0:
            self.controls.mouse_click(sign_button[0])

        treasure_hunt = self.detection.find_on_screen(
            self.detection.images['treasure-hunt-icon'], attempts=self.attempts)

        if len(treasure_hunt) == 0:
            return False

        return True
