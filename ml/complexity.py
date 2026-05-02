def analyze_complexity(code):
    lines = code.split('\n')

    total_lines = len(lines)
    code_lines = len([l for l in lines if l.strip() != ''])
    comment_lines = len([l for l in lines
                         if l.strip().startswith('#')
                         or l.strip().startswith('//')
                         or l.strip().startswith('/*')])
    function_count = len([l for l in lines
                          if l.strip().startswith('def ')
                          or 'function ' in l
                          or l.strip().startswith('void ')
                          or l.strip().startswith('public ')
                          or l.strip().startswith('private ')])
    class_count = len([l for l in lines
                       if l.strip().startswith('class ')])

    loop_count = len([l for l in lines
                      if l.strip().startswith('for ')
                      or l.strip().startswith('while ')
                      or 'for(' in l or 'for (' in l
                      or 'while(' in l or 'while (' in l])

    condition_count = len([l for l in lines
                           if l.strip().startswith('if ')
                           or l.strip().startswith('elif ')
                           or 'if(' in l or 'if (' in l])

    # Count nested loops (lines inside multiple loops)
    nested_loop_depth = 0
    current_depth = 0
    for line in lines:
        stripped = line.strip()
        is_loop = (stripped.startswith('for ') or stripped.startswith('while ')
                   or 'for(' in stripped or 'for (' in stripped
                   or 'while(' in stripped or 'while (' in stripped)
        if is_loop:
            current_depth += 1
            nested_loop_depth = max(nested_loop_depth, current_depth)
        if stripped in ('}', '') and current_depth > 0:
            current_depth = max(0, current_depth - 1)

    max_nesting = 0
    for line in lines:
        if line.strip():
            spaces = len(line) - len(line.lstrip())
            nesting = spaces // 4
            max_nesting = max(max_nesting, nesting)

    # Recursive calls detection
    recursive_calls = 0
    multi_recursive = False  # True if function calls itself 2+ times (e.g. fib)
    func_names = []
    for l in lines:
        s = l.strip()
        if s.startswith('def ') and '(' in s:
            func_names.append(s.split('(')[0].replace('def ', '').strip())
    for fname in func_names:
        calls_in_line = 0
        for l in lines:
            if fname + '(' in l and not l.strip().startswith('def '):
                recursive_calls += 1
                count = l.count(fname + '(')
                if count >= 2:
                    multi_recursive = True

    # Log detection (binary search / divide-and-conquer patterns)
    has_log = any(
        'mid' in l or '// 2' in l or '>> 1' in l or '/2' in l
        or 'divide' in l.lower() or 'binary' in l.lower()
        for l in lines
    )

    # ── TIME COMPLEXITY (Full range) ──────────────────────────────
    complexity_score = (
        loop_count * 3 +
        condition_count * 2 +
        max_nesting * 4 +
        function_count * 1
    )

    if loop_count == 0 and recursive_calls == 0:
        time_complexity = "O(1) — Constant"
    elif recursive_calls > 0 and has_log:
        time_complexity = "O(log n) — Logarithmic (divide & conquer / binary search)"
    elif loop_count == 1 and max_nesting <= 1 and recursive_calls == 0:
        if has_log:
            time_complexity = "O(log n) — Logarithmic"
        else:
            time_complexity = "O(n) — Linear"
    elif (multi_recursive or recursive_calls >= 2) and loop_count == 0 and not has_log:
        time_complexity = "O(2^n) — Exponential (multiple recursive calls, no memoization)"
    elif recursive_calls > 0 and loop_count <= 1:
        time_complexity = "O(n log n) — Linearithmic (recursive with divide)"
    elif loop_count == 2 and max_nesting <= 2:
        if has_log:
            time_complexity = "O(n log n) — Linearithmic (loop + log operation)"
        else:
            time_complexity = "O(n²) — Quadratic"
    elif loop_count == 3 or (loop_count == 2 and max_nesting > 2):
        time_complexity = "O(n³) — Cubic"
    elif loop_count > 3:
        time_complexity = "O(n^k) — Polynomial (k = " + str(loop_count) + " nested levels)"
    elif recursive_calls > 0 and loop_count == 0:
        time_complexity = "O(2^n) — Exponential (plain recursion without memoization)"
    else:
        time_complexity = "O(n²) — Quadratic"

    # ── SPACE COMPLEXITY ──────────────────────────────────────────
    list_count = sum(1 for l in lines if '= []' in l or '= list(' in l
                     or 'new ArrayList' in l or 'vector<' in l)
    dict_count = sum(1 for l in lines if '= {}' in l or '= dict(' in l
                     or 'new HashMap' in l or 'unordered_map' in l)
    set_count  = sum(1 for l in lines if '= set(' in l or 'new HashSet' in l)
    dp_count   = sum(1 for l in lines if 'dp' in l and ('= [' in l or '= {' in l))

    total_structures = list_count + dict_count + set_count

    if dp_count > 0 and loop_count >= 2:
        space_complexity = "O(n²) — Quadratic (2D DP table)"
    elif dp_count > 0:
        space_complexity = "O(n) — Linear (1D DP array)"
    elif recursive_calls > 0 and loop_count >= 2:
        space_complexity = "O(n²) — Quadratic (recursion stack + nested loops)"
    elif recursive_calls > 0 and has_log:
        space_complexity = "O(log n) — Logarithmic (divide & conquer call stack)"
    elif recursive_calls > 0:
        space_complexity = "O(n) — Linear (recursive call stack)"
    elif total_structures == 0:
        space_complexity = "O(1) — Constant (no extra data structures)"
    elif total_structures == 1:
        space_complexity = "O(n) — Linear (1 growing data structure)"
    elif total_structures >= 2:
        space_complexity = "O(n) — Linear (multiple structures, same asymptotic order)"
    else:
        space_complexity = "O(1) — Constant"

    # ── QUALITY SCORE ─────────────────────────────────────────────
    quality_score = 100
    if comment_lines == 0:
        quality_score -= 20
    if function_count == 0 and code_lines > 10:
        quality_score -= 15
    if max_nesting > 4:
        quality_score -= 20
    if loop_count > 5:
        quality_score -= 10
    if recursive_calls > 0 and function_count == 0:
        quality_score -= 10
    if total_structures > 5:
        quality_score -= 5
    quality_score = max(0, quality_score)

    return {
        "total_lines": total_lines,
        "code_lines": code_lines,
        "comment_lines": comment_lines,
        "function_count": function_count,
        "class_count": class_count,
        "loop_count": loop_count,
        "condition_count": condition_count,
        "max_nesting": max_nesting,
        "complexity_score": complexity_score,
        "quality_score": quality_score,
        "time_complexity": time_complexity,
        "space_complexity": space_complexity,
        "recursive_calls": recursive_calls,
        "data_structures_used": total_structures
    }