import unittest
import yaml
from argumentation import ArgumentationFramework


def setUpClassFactory(args, ar):
    @classmethod
    def setUpClass(self):
        self.af = ArgumentationFramework(args, ar)
        self.af.find_extentions()
    return setUpClass

def test_method_factory(exp, attr):
    def test_method(self):
        expected = exp
        actual = getattr(self.af, attr)
        self.assertCountEqual(expected, actual)
    return test_method


# Load test class descriptions
classes = yaml.safe_load(open('tests.yaml', 'r'))

# Generate and save test cases from descriptions
for cls in classes:
    globals()[cls['name']] =\
        type(cls['name'], (unittest.TestCase,), {
            'setUpClass': setUpClassFactory(cls['args'], cls['ar'])
        } | {
            meth: test_method_factory(eval(val['exp']), val['attr'])
            for meth, val in cls['methods'].items()
        })

if __name__ == "__main__":
    unittest.main()