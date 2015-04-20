import unittest
from server import execute_code

class TestExecuteCode(unittest.TestCase):

    def test_returns_correct_data_structure(self):
        code = 'print("foo")'
        data = execute_code(code=code)
        self.assertCountEqual(['stdout', 'stderr'], data.keys())

    def test_prints_to_stdout(self):
        code = 'print("foo")'
        data = execute_code(code=code)
        self.assertEqual('foo\n', data['stdout'])
        self.assertEqual('', data['stderr'])

    def test_wrong_print_syntax(self):
        code = 'print "foo"'
        data = execute_code(code=code)
        self.assertEqual('', data['stdout'])
        self.assertIn('SyntaxError', data['stderr'])
        import pdb; pdb.set_trace()  # XXX BREAKPOINT



if __name__ == '__main__':
    unittest.main()

