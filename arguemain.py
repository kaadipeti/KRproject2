class AF:
    def __init__(self, arguments=None, attack_relations=None):
        self.args = dict() if arguments is None else arguments
        self.ar = list() if attack_relations is None else attack_relations
        self.check_extentions()

    def check_extentions(self):
        self.check_conflict_free()
        self.admissible()
        self.preferred()
        self.complete()
        self.grounded()


    def check_conflict_free(self):
        # Helper functions
        def check_next_level(level):
            new_sets = set()
            for cf in level:
                for arg in set(self.args).difference(cf):
                    new = cf.union(arg)
                    if conflict_free(new):
                        new_sets.add(new)
            return new_sets

        def extend_and_add_set(cf, new_sets):
            for arg in set(self.args).difference(cf):
                new = cf.union(arg)
                if conflict_free(new):
                    new_sets.add(new)

        def conflict_free(set_):
            for a in set_:
                for b in set_:
                    if [a, b] in self.ar:
                        return False
            return True

        self.cf = {frozenset()}
        level = self.cf
        while len(level) > 0:
            level = check_next_level(level)
            self.cf = self.cf.union(level)

    def admissible(self):
        admissible_arguments = set()

        for argument in self.cf:
            if argument.issubset(self.defended(argument)):
                admissible_arguments.add(argument)

        self.admi = admissible_arguments

    def preferred(self):
        max_length = 0
        preferred_arguments = set()

        for argument in self.admi:
            argument_length = len(argument)
            if argument_length > max_length:
                max_length = argument_length
                preferred_arguments = {argument}
            elif argument_length == max_length:
                preferred_arguments.add(argument)

        self.pref = preferred_arguments

    def complete(self):
        complete_arguments = set()

        for argument in self.cf:
            if argument == self.defended(argument):
                complete_arguments.add(argument)

        self.comp = complete_arguments

    def grounded(self):
        grounded_arguments = set()

        for argument in self.comp:
            is_subset = all(argument.issubset(other) for other in self.comp)
            if is_subset:
                grounded_arguments.add(argument)

        self.grnd = grounded_arguments

    def defended(self, set_):
        attacks = self.get_attacks(set_)

        def is_defended(item):
            for a, b in self.ar:
                if b == item and a not in attacks:
                    return False
            return True

        return {e for e in self.args if is_defended(e)}

    def get_attacks(self, set_):
        attacks = []
        for a, b in self.ar:
            if a in set_:
                attacks.append(b)
        return attacks

    def credulous_acceptance(self, argument, semantics='pref'):
        accepted_arguments = set()
        for arg in getattr(self, semantics):
            accepted_arguments.update(arg)

        if argument in accepted_arguments:
            return 'Credulous Acceptance: True'
        else:
            return 'Credulous Acceptance: False'


if __name__ == "__main__":
    import json
    from sys import argv

    try:
        af_file = json.load(open(argv[1]))
        if argv[2] not in af_file['Arguments']:
            print("Invalid argument. Please enter a valid argument.")
            print("Available arguments:")
            print(af_file['Arguments'])
        else:
            for _ in range(1000):
                af = AF(arguments=af_file['Arguments'], attack_relations=af_file['Attack Relations'])
                result = af.credulous_acceptance(argv[2], semantics=argv[3]) if len(
                    argv) > 3 else af.credulous_acceptance(argv[2])
            print(result)
    except (IndexError, FileNotFoundError):
        print("Invalid input. Please use:\tpython argumentation.py file argument semantic")