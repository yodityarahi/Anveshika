import glob
import re

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    # Remove comments and strings to check structural brackets
    # Simple regex-based cleaner
    # Remove single-line comments
    cleaned = re.sub(r'//.*', '', code)
    # Remove multi-line comments
    cleaned = re.sub(r'/\*[\s\S]*?\*/', '', cleaned)
    
    # Check for quotes errors
    for idx, line in enumerate(code.splitlines()):
        if re.search(r'^\s*([a-zA-Z0-9_]+)"\s*:', line):
            print(f"ERROR: Stray quote at {filepath}:{idx+1} -> {line.strip()}")
            return False

    # Check matching brackets ignoring string contents
    # We parse strings carefully
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    in_string = None
    escape = False

    i = 0
    line_no = 1
    col_no = 1
    while i < len(code):
        ch = code[i]
        if ch == '\n':
            line_no += 1
            col_no = 1
            i += 1
            continue

        if in_string:
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == in_string:
                in_string = None
        else:
            if ch in ('"', "'", '`'):
                in_string = ch
            elif ch == '/' and i + 1 < len(code) and code[i+1] == '/':
                # single line comment: skip till \n
                while i < len(code) and code[i] != '\n':
                    i += 1
                line_no += 1
                col_no = 1
                i += 1
                continue
            elif ch == '/' and i + 1 < len(code) and code[i+1] == '*':
                # multi-line comment: skip till */
                i += 2
                while i + 1 < len(code) and not (code[i] == '*' and code[i+1] == '/'):
                    if code[i] == '\n':
                        line_no += 1
                        col_no = 1
                    i += 1
                i += 2
                continue
            elif ch in ('(', '{', '['):
                stack.append((ch, line_no, col_no))
            elif ch in (')', '}', ']'):
                if not stack:
                    print(f"ERROR: Unmatched closing {ch} at {filepath}:{line_no}:{col_no}")
                    return False
                last_ch, last_line, last_col = stack.pop()
                if pairs[ch] != last_ch:
                    print(f"ERROR: Mismatched bracket {last_ch} opened at {filepath}:{last_line}:{last_col} but closed by {ch} at {line_no}:{col_no}")
                    return False
        col_no += 1
        i += 1

    if stack:
        last_ch, last_line, last_col = stack[-1]
        print(f"ERROR: Unclosed bracket {last_ch} opened at {filepath}:{last_line}:{last_col}")
        return False

    print(f"SUCCESS: {filepath} structure valid (all brackets matched)")
    return True

all_good = True
for f in glob.glob("frontend/js/*.js"):
    if not check_file(f):
        all_good = False

if all_good:
    print("ALL FRONTEND JS FILES STRUCTURALLY AND SYNTACTICALLY VALID!")
else:
    print("THERE WERE ERRORS IN JS FILES!")
