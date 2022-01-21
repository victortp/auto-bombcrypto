from src.detection import Detection
from src.login import Login
from src.controls import Controls
from src.hero import Hero
from src.bcoin import Bcoin
from src.logger import Logger
from src.context import Context
from time import sleep
import sys


#### DO NOT CHANGE ABOVE THIS LINE ####

# ACTIONS COOLDOWN IN MINUTES
SEND_HEROES_TO_WORK = 10
REFRESH_HEROES_POSITION = 3
LOG_BCOIN = 30
CHECK_CONNECTION = 1/60

# MISCELLANEOUS
# True = yes | False = no
SEND_ALL_HEROES_TO_WORK = False
# True = yes | False = no
SAVE_LOG_TO_FILE = True
# True = yes | False = no
RANDOMIZE_MOUSE_MOVEMENT = True
# Number of attempts to complete each step of the login proccess
LOGIN_STEP_ATTEMPTS = 20

#### DO NOT CHANGE BELOW THIS LINE ####
DEBUG = False

logger = Logger(SAVE_LOG_TO_FILE)
detection = Detection()
controls = Controls(RANDOMIZE_MOUSE_MOVEMENT)
login = Login(detection, controls, logger, LOGIN_STEP_ATTEMPTS)
hero = Hero(detection, controls, logger, SEND_ALL_HEROES_TO_WORK)
bcoin = Bcoin(detection, controls, logger)
win = None
ctx = []


if sys.platform in ['linux', 'linux2']:
    from src.window_linux import WindowLinux
    win = WindowLinux()
elif sys.platform in ['Windows', 'win32', 'cygwin']:
    from src.window import Window
    win = Window()


def main():
    welcome_message()

    windows = win.get_windows('Bombcrypto')

    for w in windows:
        c = Context()
        ctx.append(c)

    logger.log(f' Starting', 0)

    for c in ctx:
        c.failed_attempts = 0
        c.update_last_execution('started_at')

    while True:
        for index, c in enumerate(ctx):
            if DEBUG:
                print(c)
                c.debug()

            if c.has_elapsed('last_successful_execution', 3 * 60) or c.has_elapsed('started_at', 60 * 60) or c.failed_attempts > 5:
                # try to sign in again when the last successful execution was
                # performed over 3 minutes or 60 minutes has passed since login

                win.activate_window(windows[index])

                logger.log(f'-=[{index + 1}]=- Reloading the game', 0)
                c.set_state(c.states.SIGNING_IN)
                login.sign_in()

                c.reset_last_execution()
                c.update_last_execution('started_at')

                continue

            if c.has_elapsed('check_connection', CHECK_CONNECTION * 60):
                # check if the game is connected

                win.activate_window(windows[index])

                is_connected = login.is_connected()

                c.update_last_execution('check_connection')

                if not is_connected:
                    # sign in the game
                    c.set_state(c.states.SIGNING_IN)
                    logger.log(
                        f'-=[{index + 1}]=- Disconnected, signing in', 0)
                    signed_in = login.sign_in()

                    logger.log(
                        f'{"Signed in" if signed_in else "Did not sign in"}', 1)

                    c.reset_last_execution()
                    c.update_last_execution('started_at')

                    if signed_in is False:
                        continue

            if c.state_equals(c.states.SIGNING_IN):
                # start treasure hunt after signing in

                win.activate_window(windows[index])

                logger.log(f'-=[{index + 1}]=- Starting treasure hunt', 0)
                started = hero.start()

                if started:
                    c.failed_attempts = 0
                    logger.log(f'-=[{index + 1}]=- Started treasure hunt', 1)
                    c.set_state(c.states.WORKING)
                    c.update_last_execution('start', started)
                else:
                    c.failed_attempts += 1
                    logger.log(
                        f'-=[{index + 1}]=- Could not start treasure hunt', 1)

                continue

            if c.has_elapsed('send_to_work', SEND_HEROES_TO_WORK * 60) and not c.state_equals(c.states.SIGNING_IN):
                # look for heroes available to work

                win.activate_window(windows[index])

                logger.log(
                    f'-=[{index + 1}]=- Looking for heroes available to work', 0)
                c.set_state(c.states.SEND_TO_WORK)
                sent_to_work = hero.send_to_work()

                if sent_to_work:
                    c.failed_attempts = 0
                    logger.log(
                        f'-=[{index + 1}]=- All available heroes sent to work', 1)
                    c.set_state(c.states.WORKING)
                    c.update_last_execution('send_to_work', sent_to_work)
                else:
                    c.failed_attempts += 1
                    logger.log(
                        f'-=[{index + 1}]=- Could not send heroes to work', 1)

                continue

            if c.has_elapsed('refresh', REFRESH_HEROES_POSITION * 60) and c.state_equals(c.states.WORKING):
                # refresh heroes position on the map

                win.activate_window(windows[index])

                logger.log(
                    f'-=[{index + 1}]=- Refreshing heroes position on the map', 0)
                c.set_state(c.states.REFRESHING)
                refreshed = hero.refresh_heroes_position()

                if refreshed:
                    c.failed_attempts = 0
                    logger.log(
                        f'-=[{index + 1}]=- Refreshed heroes position', 1)
                    c.set_state(c.states.WORKING)
                    c.update_last_execution('refresh', refreshed)
                else:
                    c.failed_attempts += 1
                    logger.log(
                        f'-=[{index + 1}]=- Could not refresh heroes position', 1)

                continue

            if c.has_elapsed('bcoin', LOG_BCOIN * 60) and c.state_equals(c.states.WORKING):
                # logs current bc value

                win.activate_window(windows[index])

                logger.log(
                    f'-=[{index + 1}]=- Saving current Bcoin amount in the chest', 0)
                c.set_state(c.states.BCOIN)
                logged = bcoin.log_current_bc()

                if logged:
                    c.failed_attempts = 0
                    logger.log(f'-=[{index + 1}]=- Saved Bcoin amount', 1)
                    c.set_state(c.states.WORKING)
                    c.update_last_execution('bcoin', logged)
                else:
                    c.failed_attempts += 1
                    logger.log(
                        f'-=[{index + 1}]=- Could not save Bcoin amount', 1)

                continue

            if c.has_elapsed('new_map', 5) and not c.state_equals(c.states.SIGNING_IN):
                win.activate_window(windows[index])

                result = hero.new_map()

                if result:
                    logger.log("Map finished", new_map=True)

                c.update_last_execution('new_map', result)

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
