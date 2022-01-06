from datetime import datetime
import cv2 as cv
from pathlib import Path


class Logger:
    save_to_file = None

    def __init__(self, save_to_file=True):
        self.save_to_file = save_to_file

        Path("log/images").mkdir(parents=True, exist_ok=True)

    def timestamp(self, slash_separator=True, only_date=False):
        now = datetime.now()
        if only_date:
            format = '%d-%m-%Y'
        else:
            format = '%d/%m/%Y %H:%M:%S' if slash_separator else '%d.%m.%Y %H.%M.%S'

        date_time = now.strftime(format)

        return date_time

    def save_log(self, text, bcoin=False, new_map=False):
        prefix = 'BCOIN ' if bcoin else 'MAP ' if new_map else ''
        path_to_file = Path(
            './log').joinpath(f'{prefix}{self.timestamp(only_date=True)}.txt')
        file = open(str(path_to_file), 'a', encoding='utf-8')
        file.write(f'{text}\n')

    def log(self, message, level=0, bcoin=False, new_map=False):
        indent = ''
        for i in range(level):
            indent += '\t'

        log_message = f'[{self.timestamp()}] {indent}{message}'
        print(log_message)
        self.save_log(log_message)

        if bcoin:
            self.save_log(log_message, bcoin=bcoin)
        elif new_map:
            self.save_log(log_message, new_map=new_map)

    def log_image(self, image, filename):
        cv.imwrite(
            str(Path(
                './log/images').joinpath(f'{self.timestamp(False)} - {filename}.jpg')), image)
