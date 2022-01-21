from time import sleep


class Bcoin:
    detection = None
    controls = None
    logger = None

    def __init__(self, detection, controls, logger):
        self.detection = detection
        self.controls = controls
        self.logger = logger

    def log_current_bc(self):
        # TODO: adjust to be able to log for multiple accounts
        return True

        sleep(1)
        chest = self.detection.find_on_screen(
            self.detection.images['chest'], attempts=10)

        if len(chest) > 0:
            self.controls.mouse_click(chest[0])

        sleep(10)

        current_bc = self.detection.get_current_bc_value()

        if current_bc is not None:
            self.logger.log(f'Current bcoins: {current_bc[0]}', 1, bcoin=True)
            self.logger.log_image(current_bc[1], current_bc[0])

        x_button = self.detection.find_on_screen(
            self.detection.images['x'], attempts=10)

        if len(x_button) > 0:
            self.controls.mouse_click(x_button[0])

        return True if current_bc is not None else False
