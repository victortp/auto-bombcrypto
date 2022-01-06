from src.detection import Detection
from src.login import Login
from src.controls import Controls
from src.hero import Hero
from src.bcoin import Bcoin
from src.logger import Logger
from time import time, sleep


#### DO NOT CHANGE ABOVE THIS LINE ####

# ACTIONS COOLDOWN IN MINUTES
SEND_HEROES_TO_WORK = 10
REFRESH_HEROES_POSITION = 3
LOG_BCOIN = 30
CHECK_CONNECTION = 1/60

# MISCELLANEOUS
SEND_ALL_HEROES_TO_WORK = False  # True = yes | False = no
SAVE_LOG_TO_FILE = True  # True = yes | False = no
RANDOMIZE_MOUSE_MOVEMENT = True  # True = yes | False = no

#### DO NOT CHANGE BELOW THIS LINE ####

logger = Logger(SAVE_LOG_TO_FILE)
detection = Detection()
controls = Controls(RANDOMIZE_MOUSE_MOVEMENT)
login = Login(detection, controls, logger)
hero = Hero(detection, controls, logger, SEND_ALL_HEROES_TO_WORK)
bcoin = Bcoin(detection, controls, logger)

last_execution = {
    'is_connected': 0,
    'start': 0,
    'send_to_work': 0,
    'refresh': 0,
    'bcoin': 0,
    'new_map': 0
}

state = {
    'SIGNING_IN': 0,
    'WORKING': 1,
    'REFRESHING': 2,
    'BCOIN': 3,
    'SEND_TO_WORK': 4
}

last_successful_execution = 0
started_at = 0
is_logged_in = False
current_state = None


def update_last_execution(feature, success=True):
    now = time()
    last_execution[feature] = now

    if success is True:
        last_successful_execution = now


def reset_last_execution():
    for key, _ in last_execution.items():
        last_execution[key] = 0


def main():
    welcome_message()
    logger.log('Starting', 0)
    started_at = time()

    current_state = state['SIGNING_IN']

    while True:
        now = time()

        # check if the game is connected
        is_connected = login.is_connected()

        update_last_execution('is_connected')

        if not is_connected:
            # sign in the game
            logger.log('Disconnected, signing in', 0)
            signed_in = login.sign_in()

            logger.log(
                f'{"Signed in" if signed_in else "Did not sign in"}', 1)

            reset_last_execution()

            if not signed_in:
                continue

        if current_state == state['SIGNING_IN']:
            # start adventure mode after signing in
            logger.log('Starting adventure mode', 0)
            started = hero.start()

            current_state = state['WORKING']

            update_last_execution('start', started)
            continue

        if now - last_execution['send_to_work'] > SEND_HEROES_TO_WORK * 60 and current_state != state['SIGNING_IN']:
            # look for heroes available to work
            logger.log('Looking for heroes available to work', 0)
            current_state = state['SEND_TO_WORK']
            sent_to_work = hero.send_to_work()
            current_state = state['WORKING']

            update_last_execution('send_to_work', sent_to_work)
            continue

        if now - last_execution['refresh'] > REFRESH_HEROES_POSITION * 60 and current_state != state['SIGNING_IN']:
            # refresh heroes position on the map
            logger.log('Refreshing heroes position on the map', 0)
            current_state = state['REFRESHING']
            updated = hero.refresh_heroes_position()
            current_state = state['WORKING']

            update_last_execution('refresh', updated)
            continue

        if now - last_execution['bcoin'] > LOG_BCOIN * 60 and current_state == state['WORKING']:
            # logs current bc value
            logger.log('Saving current Bcoin amount in the chest', 0)
            current_state = state['BCOIN']
            logged = bcoin.log_current_bc()
            current_state = state['WORKING']

            update_last_execution('bcoin', logged)
            continue

        if now - last_execution['new_map'] > 5 and current_state != state['SIGNING_IN']:
            result = hero.new_map()

            if result:
                logger.log("Map finished", new_map=True)

            update_last_execution('bcoin', result)
            continue

        if now - last_successful_execution > 3 * 60 and last_successful_execution != 0 or now - started_at > 60 * 60:
            # try to sign in again when the last successful execution was
            # performed over 3 minutes or 60 minutes has passed since login
            current_state = state['SIGNING_IN']
            login.sign_in()

            started_at = time()
            continue

        sleep(1)


def welcome_message():
    message = '''\t\t           _..._
        \t         .'     '.      _
        \t        /    .-""-\   _/ \\
        \t      .-|   /:.   |  |   |
        \t      |  \  |:.   /.-'-./
        \t      | .-'-;:__.'    =/
        \t      .'=  *=|     _.='
        \t     /   _.  |    ;
        \t    ;-.-'|    \   |
        \t   /   | \    _\  _\\
        \t   \__/'._;.  ==' ==\\
        \t            \    \   |
        \t            /    /   /
        \t            /-._/-._/
        \t            \   `\  \\
        \t             `-._/._/
        ____________________________________________________
        | If you like this project and want to support it, |
        |                  send me a tip                   |
        |                                                  |
        |                 BCOIN, BNB, BUSD                 |
        |    0xAD9069Aa7F18b1Fb7c9c6123a8083F0df4B53dDf    |
        |                                                  |
        |                     PAYPAL                       |
        |           https://bityli.com/8BIzysR             |
        |__________________________________________________|'''

    print(message)
    sleep(3)


if __name__ == '__main__':
    main()
