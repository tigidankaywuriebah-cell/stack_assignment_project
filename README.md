# DCOMP320 — Stack-Based Mathematical Expression Evaluator

**Institution:** Limkokwing University of Creative Technology, Sierra Leone  
**Module:** DCOMP320 — Data Structures and Algorithm  
**Assignment:** Stacks Implementation  
**Student:** Tigidankay Wurie Bah 
**Student ID:** 905005471

## Overview
This Python program reads arithmetic expressions from `input.txt`, evaluates each using two stack objects, and writes results to `output.txt`. It preserves separator lines such as `-----` and blank lines.

## Requirements
Python 3.9 or later. No external packages required.

## Run
Open a terminal in this project directory and run:

```bash
python stack_evaluator.py
```

Optionally specify filenames:

```bash
python stack_evaluator.py input.txt output.txt
```

## Test

```bash
python -m unittest -v
```

## Input/output format
One arithmetic expression per line. Separator-only lines containing at least three hyphens are preserved unchanged. Supported operators are `+`, `-`, `*`, `/`, parentheses, decimals, and unary `+`/`-`. Each expression becomes one numerical result. Invalid expressions become an `ERROR (line N): ...` entry, and processing continues.

## Implementation
`Stack` provides `push`, `pop`, `peek`, and `is_empty`. Two stacks store numeric values and operators. Operators are applied according to precedence; parentheses control grouping. Time complexity is O(n) per expression and auxiliary space complexity is O(n).

## Assumptions and limitations
- Operators are standard arithmetic only; exponentiation, implicit multiplication, and variables are not supported.
- Division uses floating-point arithmetic and can have normal precision limitations.
- Errors are recorded as text rather than terminating the entire batch.
- Separator lines must contain three or more hyphens (with optional surrounding whitespace).

## Submission checklist
- [ ] Replace name and student ID in README and report
- [ ] Run program and verify output.txt
- [ ] Run tests and capture screenshot
- [ ] Add screenshots to report and print/bind
- [ ] Push repository to GitHub
- [ ] Invite lecturer as GitHub collaborator (obtain their GitHub username)
- [ ] Insert actual GitHub repository URL in report
