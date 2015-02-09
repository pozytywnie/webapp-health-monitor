_registered_verificators_classes = set()


def register(verificator_class):
    _registered_verificators_classes.add(verificator_class)


def get_verificators():
    return [verificator_class()
            for verificator_class in _registered_verificators_classes]
