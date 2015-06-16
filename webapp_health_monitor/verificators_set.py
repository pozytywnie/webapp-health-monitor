import collections


class VerificatorsSet(object):
    def __init__(self):
        self._untagged_verificators_classes = set()
        self._tagged_verificators_classes = collections.defaultdict(list)

    def register(self, verificator_class, tags=()):
        if tags:
            for tag in tags:
                self._tagged_verificators_classes[tag].append(verificator_class)
        else:
            self._untagged_verificators_classes.add(verificator_class)

    def get_verificators(self, tags=()):
        verificator_classes = set()
        if tags:
            for tag in tags:
                verificator_classes.update(self._tagged_verificators_classes[tag])
        else:
            verificator_classes.update(self._untagged_verificators_classes)
            for tagged_verificator_classes in self._tagged_verificators_classes.values():
                verificator_classes.update(tagged_verificator_classes)

        return [verificator_class() for verificator_class in
                sorted(verificator_classes, key=str)]
