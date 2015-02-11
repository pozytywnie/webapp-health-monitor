_registered_actions = set()


def register(action_class):
    _registered_actions.add(action_class)


def get_actions():
    return list(_registered_actions)


class Action:
    def run(self, verification_suit_result):
        raise NotImplementedError()
