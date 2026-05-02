# =============================================
# FLASK APP - Our Web Server
# This connects all the ML modules together
# =============================================

from flask import Flask, request, jsonify, render_template
from ml.bug_detector import detect_bugs, get_bug_summary
from ml.complexity import analyze_complexity
from ml.classifier import classify_code

app = Flask(__name__)

# ===== HOME PAGE =====
@app.route('/')
def home():
    return render_template('index.html')

# ===== MAIN ANALYZE API =====
@app.route('/analyze', methods=['POST'])
def analyze():
    """
    This endpoint analyzes the given code
    It uses three ML models together
    Performs selective analysis based on checkbox options
    """

    # Get code and options from frontend
    data = request.get_json()
    code = data.get('code', '')
    language = data.get('language', 'Python')

    # Checkbox options — default True if not provided
    run_bug      = data.get('run_bug', True)
    run_complex  = data.get('run_complex', True)
    run_security = data.get('run_security', True)
    run_ml       = data.get('run_ml', True)

    if not code:
        return jsonify({"error": "Code is empty!"}), 400

    # ===== SELECTIVE ML MODELS =====

    # 1. Bug detection (run only if checkbox is selected)
    if run_bug or run_security:
        bugs = detect_bugs(code)
        bug_summary = get_bug_summary(bugs)

        # If only security is selected, filter only security-related bugs
        if not run_bug and run_security:
            bugs = [b for b in bugs if b['category'] == 'Security']
            bug_summary = get_bug_summary(bugs)
    else:
        bugs = []
        bug_summary = {"total": 0, "high": 0, "medium": 0, "low": 0}

    # 2. Complexity analysis
    if run_complex:
        complexity = analyze_complexity(code)
    else:
        complexity = {
            "total_lines": 0, "code_lines": 0, "comment_lines": 0,
            "function_count": 0, "class_count": 0, "loop_count": 0,
            "condition_count": 0, "max_nesting": 0, "complexity_score": 0,
            "quality_score": 0, "time_complexity": "N/A",
            "space_complexity": "N/A", "recursive_calls": 0,
            "data_structures_used": 0
        }

    # 3. ML Classification
    if run_ml:
        classification = classify_code(code)
    else:
        classification = {
            "quality": "N/A",
            "confidence": 0,
            "score": 0
        }

    # ===== RETURN RESULT =====
    return jsonify({
        "bugs": bugs,
        "bug_summary": bug_summary,
        "complexity": complexity,
        "classification": classification,
        "language": language,
        "modules_run": {
            "bug": run_bug,
            "security": run_security,
            "complexity": run_complex,
            "ml": run_ml
        }
    })

# ===== START SERVER =====
if __name__ == '__main__':
    print("Starting server...")
    print("Open in browser: http://localhost:5000")
    app.run(debug=True)