"""Evaluate arithmetic expressions using two explicit stack instances."""
from pathlib import Path
import re
import sys

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError('Cannot pop an empty stack')
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError('Cannot peek an empty stack')
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)

TOKEN_PATTERN = re.compile(r'\s*(\d+(?:\.\d+)?|\.\d+|[()+*/-])')
PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, 'u+': 3, 'u-': 3}


def tokenize(expression):
    tokens = []
    position = 0
    while position < len(expression):
        if expression[position:].strip() == '':
            break
        match = TOKEN_PATTERN.match(expression, position)
        if not match:
            raise ValueError(f'Invalid character at position {position + 1}')
        tokens.append(match.group(1))
        position = match.end()
    if not tokens:
        raise ValueError('Empty expression')
    return tokens


def evaluate(expression):
    values, operators = Stack(), Stack()

    def apply_operator():
        op = operators.pop()
        if op in ('u+', 'u-'):
            if len(values) < 1:
                raise ValueError('Missing operand')
            value = values.pop()
            values.push(value if op == 'u+' else -value)
            return
        if len(values) < 2:
            raise ValueError('Missing operand')
        right, left = values.pop(), values.pop()
        if op == '+': result = left + right
        elif op == '-': result = left - right
        elif op == '*': result = left * right
        elif op == '/':
            if right == 0:
                raise ZeroDivisionError('Division by zero')
            result = left / right
        else: raise ValueError('Unknown operator')
        values.push(result)

    expecting_value = True
    for token in tokenize(expression):
        if token not in ('(', ')', '+', '-', '*', '/'):
            if not expecting_value:
                raise ValueError('Missing operator')
            values.push(float(token))
            expecting_value = False
        elif token == '(':
            if not expecting_value:
                raise ValueError('Missing operator before parenthesis')
            operators.push(token)
        elif token == ')':
            if expecting_value:
                raise ValueError('Missing value before closing parenthesis')
            while not operators.is_empty() and operators.peek() != '(':
                apply_operator()
            if operators.is_empty():
                raise ValueError('Unmatched closing parenthesis')
            operators.pop()
            expecting_value = False
        else:
            if expecting_value:
                if token not in ('+', '-'):
                    raise ValueError('Operator missing left operand')
                operators.push('u+' if token == '+' else 'u-')
                continue
            while (not operators.is_empty() and operators.peek() != '('
                   and PRECEDENCE[operators.peek()] >= PRECEDENCE[token]):
                apply_operator()
            operators.push(token)
            expecting_value = True
    if expecting_value:
        raise ValueError('Incomplete expression')
    while not operators.is_empty():
        if operators.peek() == '(':
            raise ValueError('Unmatched opening parenthesis')
        apply_operator()
    if len(values) != 1:
        raise ValueError('Invalid expression')
    return values.pop()


def format_result(value):
    return str(int(value)) if value.is_integer() else format(value, '.12g')


def process_file(input_path='input.txt', output_path='output.txt'):
    source = Path(input_path)
    if not source.is_file():
        raise FileNotFoundError(f'Input file not found: {source}')
    lines = source.read_text(encoding='utf-8').splitlines(keepends=True)
    output = []
    for line_number, line in enumerate(lines, 1):
        content = line.rstrip('\r\n')
        ending = line[len(content):]
        if not content.strip() or re.fullmatch(r'\s*-{3,}\s*', content):
            output.append(line)
            continue
        try:
            output.append(format_result(evaluate(content)) + ending)
        except (ValueError, ZeroDivisionError, IndexError) as error:
            output.append(f'ERROR (line {line_number}): {error}' + ending)
    Path(output_path).write_text(''.join(output), encoding='utf-8')
    return output


if __name__ == '__main__':
    try:
        input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.txt'
        results = process_file(input_file, output_file)
        print(f'Processed {len(results)} lines. Results saved to {output_file}')
    except (OSError, UnicodeError) as error:
        print(f'File error: {error}', file=sys.stderr)
        sys.exit(1)
