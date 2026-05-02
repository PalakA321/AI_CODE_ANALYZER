RULES = [

    # ══════════════════════════════════════════════════════════════
    # CATEGORY 1: SECURITY (HIGH severity)
    # ══════════════════════════════════════════════════════════════

    {
        "id": 1,
        "pattern": "eval(",
        "severity": "HIGH",
        "message": "eval() is dangerous — can execute any code injected by user!",
        "category": "Security",
        "fix": "Remove eval(). Use ast.literal_eval() for safe evaluation of literals."
    },
    {
        "id": 2,
        "pattern": "exec(",
        "severity": "HIGH",
        "message": "exec() is a serious security risk — executes arbitrary code!",
        "category": "Security",
        "fix": "Remove exec(). Use proper function calls or logic instead."
    },
    {
        "id": 3,
        "pattern": "password",
        "severity": "HIGH",
        "message": "Hardcoded password detected — never store passwords in code!",
        "category": "Security",
        "fix": "Use environment variables: import os; password = os.environ.get('PASSWORD')"
    },
    {
        "id": 4,
        "pattern": "secret",
        "severity": "HIGH",
        "message": "Hardcoded secret detected — store secrets in environment variables!",
        "category": "Security",
        "fix": "Use: import os; secret = os.environ.get('SECRET_KEY')"
    },
    {
        "id": 5,
        "pattern": "api_key",
        "severity": "HIGH",
        "message": "Hardcoded API key in code — this is a security vulnerability!",
        "category": "Security",
        "fix": "Use: api_key = os.environ.get('API_KEY') and store in .env file"
    },
    {
        "id": 6,
        "pattern": "pickle.load(",
        "severity": "HIGH",
        "message": "pickle.load() can execute malicious code from untrusted files!",
        "category": "Security",
        "fix": "Use json.load() for safe data loading instead of pickle."
    },
    {
        "id": 7,
        "pattern": "shell=True",
        "severity": "HIGH",
        "message": "subprocess with shell=True allows command injection attacks!",
        "category": "Security",
        "fix": "Use shell=False and pass command as a list: subprocess.run(['ls', '-la'], shell=False)"
    },
    {
        "id": 8,
        "pattern": "__import__(",
        "severity": "HIGH",
        "message": "Dynamic import with __import__() can be a security risk!",
        "category": "Security",
        "fix": "Use importlib.import_module() or regular static imports instead."
    },

    # ══════════════════════════════════════════════════════════════
    # CATEGORY 2: COMMON STUDENT BUGS (MEDIUM severity)
    # ══════════════════════════════════════════════════════════════

    {
        "id": 9,
        "pattern": "except:",
        "severity": "MEDIUM",
        "message": "Bare except: catches everything including system exits — too broad!",
        "category": "Bug",
        "fix": "Catch specific exceptions: except ValueError: or except TypeError:"
    },
    {
        "id": 10,
        "pattern": "except Exception:",
        "severity": "LOW",
        "message": "Too broad exception — catches almost every error, hides real bugs",
        "category": "Bug",
        "fix": "Catch the specific exception you expect, e.g., except ZeroDivisionError:"
    },
    {
        "id": 11,
        "pattern": "open(",
        "severity": "MEDIUM",
        "message": "File opened without 'with' — file may not close properly on error!",
        "category": "Bug",
        "fix": "Use: with open('file.txt', 'r') as f:  — this auto-closes the file"
    },
    {
        "id": 12,
        "pattern": "global ",
        "severity": "MEDIUM",
        "message": "Global variable usage — makes code hard to test and debug",
        "category": "Best Practice",
        "fix": "Pass the variable as a function parameter instead of using global."
    },
    {
        "id": 13,
        "pattern": "while True:",
        "severity": "MEDIUM",
        "message": "Infinite loop detected — make sure there is a break condition!",
        "category": "Bug",
        "fix": "Add a break statement or use a proper loop condition: while count < limit:"
    },
    {
        "id": 14,
        "pattern": "time.sleep(",
        "severity": "MEDIUM",
        "message": "time.sleep() blocks the entire program — bad for performance!",
        "category": "Performance",
        "fix": "Consider using async/await or threading for non-blocking delays."
    },
    {
        "id": 15,
        "pattern": "assert ",
        "severity": "MEDIUM",
        "message": "assert is disabled in optimized Python (-O flag) — not safe for validation!",
        "category": "Bug",
        "fix": "Use: if not condition: raise ValueError('message') instead of assert"
    },
    {
        "id": 16,
        "pattern": "import *",
        "severity": "MEDIUM",
        "message": "Wildcard import pollutes namespace and causes name conflicts!",
        "category": "Best Practice",
        "fix": "Import only what you need: from math import sqrt, pi"
    },
    {
        "id": 17,
        "pattern": "input(",
        "severity": "MEDIUM",
        "message": "User input used directly — always validate before processing!",
        "category": "Security",
        "fix": "Validate input: val = input('Enter: '); if not val.isdigit(): raise ValueError"
    },
    {
        "id": 18,
        "pattern": "/ 0",
        "severity": "HIGH",
        "message": "Division by zero detected — this will crash your program!",
        "category": "Bug",
        "fix": "Add check: if divisor != 0: result = num / divisor"
    },
    {
        "id": 19,
        "pattern": "int(input(",
        "severity": "MEDIUM",
        "message": "Direct int(input()) will crash if user types non-number!",
        "category": "Bug",
        "fix": "Wrap in try-except: try: val = int(input('Enter: ')) except ValueError: print('Not a number!')"
    },
    {
        "id": 20,
        "pattern": "float(input(",
        "severity": "MEDIUM",
        "message": "Direct float(input()) crashes on non-numeric input!",
        "category": "Bug",
        "fix": "Wrap in try-except: try: val = float(input()) except ValueError: ..."
    },

    # ══════════════════════════════════════════════════════════════
    # CATEGORY 3: BEST PRACTICES / CODE QUALITY
    # ══════════════════════════════════════════════════════════════

    {
        "id": 21,
        "pattern": "== None",
        "severity": "LOW",
        "message": "'== None' comparison — use identity check instead",
        "category": "Best Practice",
        "fix": "Replace 'x == None' with 'x is None'"
    },
    {
        "id": 22,
        "pattern": "== True",
        "severity": "LOW",
        "message": "'== True' is redundant — use the boolean value directly",
        "category": "Best Practice",
        "fix": "Replace 'if x == True:' with 'if x:'"
    },
    {
        "id": 23,
        "pattern": "== False",
        "severity": "LOW",
        "message": "'== False' is redundant — use 'not' instead",
        "category": "Best Practice",
        "fix": "Replace 'if x == False:' with 'if not x:'"
    },
    {
        "id": 24,
        "pattern": "print(",
        "severity": "LOW",
        "message": "print() in code — use logging module for production output",
        "category": "Best Practice",
        "fix": "Use: import logging; logging.info('message') instead of print()"
    },
    {
        "id": 25,
        "pattern": "TODO",
        "severity": "LOW",
        "message": "TODO comment found — incomplete code!",
        "category": "Code Quality",
        "fix": "Complete the TODO before submitting or deploying code."
    },
    {
        "id": 26,
        "pattern": "pass",
        "severity": "LOW",
        "message": "Empty 'pass' block — is this intentional? Empty blocks can hide bugs",
        "category": "Code Quality",
        "fix": "Add proper logic or raise NotImplementedError('Not implemented yet')"
    },
    {
        "id": 27,
        "pattern": "range(len(",
        "severity": "LOW",
        "message": "range(len(list)) is not Pythonic — use enumerate() instead",
        "category": "Best Practice",
        "fix": "Replace with: for i, item in enumerate(my_list):"
    },
    {
        "id": 28,
        "pattern": "x = x + 1",
        "severity": "LOW",
        "message": "Use shorthand operator — x += 1 is cleaner and more Pythonic",
        "category": "Best Practice",
        "fix": "Replace 'x = x + 1' with 'x += 1'"
    },
    {
        "id": 29,
        "pattern": "if len(",
        "severity": "LOW",
        "message": "Avoid 'if len(x) > 0' — in Python just use 'if x:'",
        "category": "Best Practice",
        "fix": "Replace 'if len(my_list) > 0:' with 'if my_list:'"
    },
    {
        "id": 30,
        "pattern": "type(",
        "severity": "LOW",
        "message": "Using type() for type check — use isinstance() instead",
        "category": "Best Practice",
        "fix": "Replace 'type(x) == int' with 'isinstance(x, int)' — supports inheritance too"
    },

    # ══════════════════════════════════════════════════════════════
    # CATEGORY 4: PERFORMANCE ISSUES
    # ══════════════════════════════════════════════════════════════

    {
        "id": 31,
        "pattern": "+ str(",
        "severity": "LOW",
        "message": "String concatenation with + is slow — use f-strings instead",
        "category": "Performance",
        "fix": "Use f-string: f'Hello {name}' instead of 'Hello ' + str(name)"
    },
    {
        "id": 32,
        "pattern": ".append(",
        "severity": "LOW",
        "message": "Repeated append in loop — consider list comprehension for better speed",
        "category": "Performance",
        "fix": "Use list comprehension: result = [process(x) for x in items]"
    },
    {
        "id": 33,
        "pattern": "not in range(",
        "severity": "LOW",
        "message": "'not in range()' is O(n) — direct comparison is O(1) and faster",
        "category": "Performance",
        "fix": "Replace 'x not in range(0, 100)' with 'not (0 <= x < 100)'"
    },
    {
        "id": 34,
        "pattern": "sorted(sorted(",
        "severity": "MEDIUM",
        "message": "Double sorting detected — unnecessary duplicate operation!",
        "category": "Performance",
        "fix": "Sort only once with correct key: sorted(data, key=lambda x: x['name'])"
    },
    {
        "id": 35,
        "pattern": "dict()",
        "severity": "LOW",
        "message": "dict() constructor is slower — use {} literal instead",
        "category": "Performance",
        "fix": "Replace dict() with {} for empty dict, or {'key': value} directly"
    },

    # ══════════════════════════════════════════════════════════════
    # CATEGORY 5: STUDENT-SPECIFIC MISTAKES
    # ══════════════════════════════════════════════════════════════

    {
        "id": 36,
        "pattern": "def function(",
        "severity": "LOW",
        "message": "Generic function name 'function' — use a descriptive name!",
        "category": "Code Quality",
        "fix": "Name functions by what they do: def calculate_sum() or def get_user_data()"
    },
    {
        "id": 37,
        "pattern": "lst[len(lst)]",
        "severity": "HIGH",
        "message": "Index out of range! Last valid index is len(lst)-1, not len(lst)",
        "category": "Bug",
        "fix": "Use lst[-1] to get last element safely"
    },
    {
        "id": 38,
        "pattern": "self.self.",
        "severity": "HIGH",
        "message": "Double self.self — this is a logic error in a class!",
        "category": "Bug",
        "fix": "Use just self.attribute, not self.self.attribute"
    },
    {
        "id": 39,
        "pattern": "n == 0\n    return",
        "severity": "LOW",
        "message": "Possible missing base case in recursion — check carefully!",
        "category": "Bug",
        "fix": "Make sure recursion base case handles all edge cases including n < 0"
    },
    {
        "id": 40,
        "pattern": "my_list = list",
        "severity": "MEDIUM",
        "message": "Shadowing built-in 'list' — this replaces Python's built-in!",
        "category": "Bug",
        "fix": "Use a specific name: student_list = [], item_list = []"
    },
    {
        "id": 41,
        "pattern": "my_dict = dict",
        "severity": "MEDIUM",
        "message": "Shadowing built-in 'dict' — this replaces Python's built-in!",
        "category": "Bug",
        "fix": "Use a specific name: user_dict = {}, data_map = {}"
    },
    {
        "id": 42,
        "pattern": "str = ",
        "severity": "HIGH",
        "message": "Shadowing built-in 'str' — breaks all string operations in this scope!",
        "category": "Bug",
        "fix": "Use a different variable name: name_str, text_value, etc."
    },
    {
        "id": 43,
        "pattern": "list = ",
        "severity": "HIGH",
        "message": "Shadowing built-in 'list' — breaks all list() calls in this scope!",
        "category": "Bug",
        "fix": "Use a different variable name: my_items, data_list, etc."
    },
    {
        "id": 44,
        "pattern": "def __init__(self, self",
        "severity": "HIGH",
        "message": "Incorrect __init__ signature — self should not appear twice!",
        "category": "Bug",
        "fix": "Correct format: def __init__(self, param1, param2):"
    },
    {
        "id": 45,
        "pattern": "elif True:",
        "severity": "MEDIUM",
        "message": "'elif True:' is always True — use 'else:' instead",
        "category": "Bug",
        "fix": "Replace 'elif True:' with 'else:'"
    },

    # ══════════════════════════════════════════════════════════════
    # CATEGORY 6: COMMON LOGIC ERRORS
    # ══════════════════════════════════════════════════════════════

    {
        "id": 46,
        "pattern": "if x = ",
        "severity": "HIGH",
        "message": "Assignment '=' inside if condition — use '==' for comparison!",
        "category": "Bug",
        "fix": "Change 'if x = value' to 'if x == value'"
    },
    {
        "id": 47,
        "pattern": "except:\n    continue",
        "severity": "MEDIUM",
        "message": "Silently continuing after exception — error hidden from user!",
        "category": "Bug",
        "fix": "Log the error before continuing: logging.warning(f'Skipping: {e}')"
    },
    {
        "id": 48,
        "pattern": "import os, sys",
        "severity": "LOW",
        "message": "Multiple imports on one line — separate for readability (PEP8)",
        "category": "Best Practice",
        "fix": "Put each import on its own line: import os  (newline)  import sys"
    },
    {
        "id": 49,
        "pattern": "return True\n    return False",
        "severity": "LOW",
        "message": "Returning True/False separately — simplify with direct boolean return",
        "category": "Best Practice",
        "fix": "Simplify: return condition  instead of if condition: return True; return False"
    },
    {
        "id": 50,
        "pattern": "bare_except",
        "severity": "MEDIUM",
        "message": "Custom bare_except pattern — always use specific exception types!",
        "category": "Bug",
        "fix": "Use specific exceptions: except (ValueError, TypeError) as e:"
    },
]


def detect_bugs(code):
    bugs = []
    lines = code.split('\n')

    for line_number, line in enumerate(lines, start=1):
        for rule in RULES:
            if rule["pattern"].lower() in line.lower():
                bugs.append({
                    "line": line_number,
                    "code": line.strip(),
                    "severity": rule["severity"],
                    "message": rule["message"],
                    "category": rule["category"],
                    "fix": rule.get("fix", "Review this line manually.")
                })

    return bugs


def get_bug_summary(bugs):
    summary = {
        "total": len(bugs),
        "high": len([b for b in bugs if b["severity"] == "HIGH"]),
        "medium": len([b for b in bugs if b["severity"] == "MEDIUM"]),
        "low": len([b for b in bugs if b["severity"] == "LOW"])
    }
    return summary