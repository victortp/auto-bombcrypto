from src.detection import Detection
from src.login import Login
from src.controls import Controls
from src.hero import Hero
from src.bcoin import Bcoin
from src.logger import Logger
from src.context import Context
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
DEBUG = False

logger = Logger(SAVE_LOG_TO_FILE)
detection = Detection()
controls = Controls(RANDOMIZE_MOUSE_MOVEMENT)
login = Login(detection, controls, logger)
hero = Hero(detection, controls, logger, SEND_ALL_HEROES_TO_WORK)
bcoin = Bcoin(detection, controls, logger)
ctx = Context()


def main():
    welcome_message()

    logger.log('Starting', 0)

    ctx.update_last_execution('started_at')

    while True:
        if DEBUG:
            ctx.debug()

        # check if the game is connected
        is_connected = login.is_connected()

        ctx.update_last_execution('is_connected')

        if not is_connected:
            # sign in the game
            ctx.set_state(ctx.states.SIGNING_IN)
            logger.log('Disconnected, signing in', 0)
            signed_in = login.sign_in()

            logger.log(
                f'{"Signed in" if signed_in else "Did not sign in"}', 1)

            ctx.reset_last_execution()

            if signed_in is False:
                continue

        if ctx.state_equals(ctx.states.SIGNING_IN):
            # start adventure mode after signing in
            logger.log('Starting adventure mode', 0)
            started = hero.start()

            ctx.set_state(ctx.states.WORKING)
            ctx.update_last_execution('start', started)

            continue

        if ctx.has_elapsed('send_to_work', SEND_HEROES_TO_WORK * 60) and not ctx.state_equals(ctx.states.SIGNING_IN):
            # look for heroes available to work
            logger.log('Looking for heroes available to work', 0)
            ctx.set_state(ctx.states.SEND_TO_WORK)
            sent_to_work = hero.send_to_work()
            ctx.set_state(ctx.states.WORKING)

            ctx.update_last_execution('send_to_work', sent_to_work)

            continue

        if ctx.has_elapsed('refresh', REFRESH_HEROES_POSITION * 60) and ctx.state_equals(ctx.states.SIGNING_IN):
            # refresh heroes position on the map
            logger.log('Refreshing heroes position on the map', 0)
            ctx.set_state(ctx.states.REFRESHING)
            updated = hero.refresh_heroes_position()
            ctx.set_state(ctx.states.WORKING)

            ctx.update_last_execution('refresh', updated)

            continue

        if ctx.has_elapsed('bcoin', LOG_BCOIN * 60) and ctx.state_equals(ctx.states.WORKING):
            # logs current bc value
            logger.log('Saving current Bcoin amount in the chest', 0)
            ctx.set_state(ctx.states.BCOIN)
            logged = bcoin.log_current_bc()
            ctx.set_state(ctx.states.WORKING)

            ctx.update_last_execution('bcoin', logged)

            continue

        if ctx.has_elapsed('new_map', 5) and ctx.state_equals(ctx.states.SIGNING_IN):
            result = hero.new_map()

            if result:
                logger.log("Map finished", new_map=True)

            ctx.update_last_execution('new_map', result)

            continue

        if ctx.has_elapsed('last_successful_execution', 3 * 60) or ctx.has_elapsed('started_at', 60 * 60):
            # try to sign in again when the last successful execution was
            # performed over 3 minutes or 60 minutes has passed since login
            logger.log('Reloading the game', 0)
            ctx.set_state(ctx.states.SIGNING_IN)
            login.sign_in()

            ctx.reset_last_execution()
            ctx.update_last_execution('started_at')

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
