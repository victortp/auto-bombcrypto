from time import time


class State:
    SIGNING_IN = 0
    WORKING = 1
    REFRESHING = 2
    BCOIN = 3
    SEND_TO_WORK = 4


class Context:
    state = None
    states = None

    last_execution = {
        'is_connected': 0,
        'start': 0,
        'send_to_work': 0,
        'refresh': 0,
        'bcoin': 0,
        'new_map': 0,
        'started_at': 0,
        'last_successful_execution': 0
    }

    def __init__(self):
        self.states = State()
        self.state = self.states.SIGNING_IN

    def update_last_execution(self, feature, success=True):
        now = time()
        self.last_execution[feature] = now

        if success is True:
            self.last_execution['last_successful_execution'] = now

    def reset_last_execution(self):
        for key, _ in self.last_execution.items():
            self.last_execution[key] = 0

    def has_elapsed(self, feature, minutes):
        now = time()

        result = now - self.last_execution[feature] > minutes

        return result

    def state_equals(self, feature):
        result = self.state == feature

        return result

    def set_state(self, feature):
        self.state = feature

    def debug(self):
        now = time()
        for key, value in self.last_execution.items():
            print(f'{key}: {now - value if now - value != now else 0}s')


if __name__ == '__main__':
    ctx = Context()
    print(ctx.states.SIGNING_IN)
