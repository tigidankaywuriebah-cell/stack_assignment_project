import tempfile
import unittest
from pathlib import Path
from stack_evaluator import Stack, evaluate, process_file

class StackTests(unittest.TestCase):
    def test_push_pop_peek(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        s.push(3)
        s.push(5)
        self.assertEqual(s.peek(), 5)
        self.assertEqual(s.pop(), 5)
        self.assertEqual(s.pop(), 3)
        self.assertTrue(s.is_empty())

    def test_empty_stack(self):
        s = Stack()
        with self.assertRaises(IndexError): s.pop()
        with self.assertRaises(IndexError): s.peek()

class ExpressionTests(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(evaluate('3 + 5 * 2'), 13)
        self.assertEqual(evaluate('((8 / 4) + 7 * 2)'), 16)
        self.assertEqual(evaluate('10 - (2 + 3) * 4'), -10)

    def test_unary_and_decimals(self):
        self.assertEqual(evaluate('-3 + 5 * (2 + 1)'), 12)
        self.assertEqual(evaluate('12 / 4 + 2.5'), 5.5)
        self.assertEqual(evaluate('2 * -3'), -6)
        self.assertEqual(evaluate('-(2 + 3)'), -5)

    def test_errors(self):
        for expression in ['(3 + 2', '2 +', '2 ** 3', '3 4', ')3(', '3 + a', '()']:
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError): evaluate(expression)
        with self.assertRaises(ZeroDivisionError): evaluate('8 / 0')

    def test_file_preserves_separators(self):
        with tempfile.TemporaryDirectory() as directory:
            input_file = Path(directory) / 'input.txt'
            output_file = Path(directory) / 'output.txt'
            input_file.write_text('3 + 5 * 2\n-----\n8 / 0\n', encoding='utf-8')
            process_file(input_file, output_file)
            self.assertEqual(output_file.read_text(), '13\n-----\nERROR (line 3): Division by zero\n')

if __name__ == '__main__':
    unittest.main()
