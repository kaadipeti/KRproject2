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
            for cf in level: extend_and_add_set(cf, new_sets)
            return new_sets

        def extend_and_add_set(cf, new_sets):
            for arg in set(self.args).difference(cf):
                new = cf.union(arg)
                if conflict_free(new):
                    new_sets.add(new)

        def conflict_free(set):
            return all([[a, b] not in self.ar for a in set for b in set])

        self.cf = {frozenset()}
        level = self.cf
        while len(level) > 0:
            level = check_next_level(level)
            self.cf = self.cf.union(level)

    def admissible(self):
        self.admi = {cf for cf in self.cf if cf.issubset(self.defended(cf))}

    def preferred(self):
        pref_len = len(max(self.admi, key=lambda x: len(x)))
        self.pref = {e for e in self.admi if len(e) == pref_len}

    def complete(self):
        self.comp = {cf for cf in self.cf if cf == self.defended(cf)}

    def grounded(self):
        self.grnd = {c for c in self.comp if all([c.issubset(e) for e in self.comp])}

    def defended(self, set):
        attacks = self.get_attacks(set)

        def defended_(item):
            return all([b != item or a in attacks for a, b in self.ar])

        return {e for e in self.args if defended_(e)}

    def get_attacks(self, set):
        return [b for a, b in self.ar if a in set]

    def credulous_acceptance(self, argument, semantics='pref'):
        return 'Credulous Acceptance: True' if argument in {a for arg in getattr(self, semantics) for a in arg} else 'Credulous Acceptance: False'


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