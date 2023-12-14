class ArgumentationFramework:
    def __init__(self, arguments=None, attack_relations=None):
        self.args = dict() if arguments is None else arguments
        self.ar = list() if attack_relations is None else attack_relations
        self.find_extentions()
    
    def find_extentions(self):
        self.find_conflict_free()
        self.find_admissible()
        self.find_preferred()
        self.find_complete()
        self.find_grounded()
        self.find_stable()
    
    def find_conflict_free(self):
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
        
        # Iteratively add new elements to existing cf sets
        self.cf = {frozenset()}
        level = self.cf
        while len(level) > 0:
            level = check_next_level(level)
            self.cf = self.cf.union(level)
    
    def find_admissible(self):
        self.adm = {cf for cf in self.cf if cf.issubset(self.defended(cf))}

    def find_preferred(self):
        pref_len = len(max(self.adm, key=lambda x: len(x)))
        self.pref = {e for e in self.adm if len(e) == pref_len}
    
    def find_complete(self):
        self.comp = {cf for cf in self.cf if cf == self.defended(cf)}
    
    def find_grounded(self):
        self.grd = {c for c in self.comp if all([c.issubset(e) for e in self.comp])}
    
    def find_stable(self):
        def attacks(cf):
            attacks = self.get_attacks(cf)
            return all([a in attacks for a in set(self.args).difference(cf)])

        self.stb = {cf for cf in self.cf if attacks(cf)}

    def defended(self, set):
        attacks = self.get_attacks(set)
        def defends(item):
            return all([b != item or a in attacks for a, b in self.ar])
        
        return {e for e in self.args if defends(e)}
    
    def get_attacks(self, set):
        return [b for a, b in self.ar if a in set]

    def credulous_acceptance(self, argument, semantics='stb'):
        try: 
            return 'Yes' if argument in {a for arg in getattr(self, semantics) for a in arg} else 'No'
        except AttributeError:
            return 'Incorrect semantics provided. Available semantics: cf, adm, pref, comp, grd, stb'


if __name__ == "__main__":
    import json
    from sys import argv
    from datetime import datetime
    
    try:
        afd = json.load(open(argv[1]))
        start = datetime.now()
        for _ in range(1000):
            af = ArgumentationFramework(arguments=afd['Arguments'], attack_relations=afd['Attack Relations'])
            ans = af.credulous_acceptance(argv[2], semantics=argv[3]) if len(argv) > 3 else af.credulous_acceptance(argv[2])
        print(ans)
        print(f"Running time: {(datetime.now() - start).total_seconds()/1000:.3e}s")
    except (IndexError, FileNotFoundError):
        print("Invalid input. Call as:\n\tpython argumentation.py <file> <argument> <semantic|(optional)>")