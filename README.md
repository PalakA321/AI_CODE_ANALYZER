# AI_CODE_ANALYZER
A web-based AI Code Analyzer that automatically reviews code using Machine Learning. Built with Python, Flask, and Scikit-learn.
What It Does
Paste any code and get instant analysis across three ML modules:

Bug Detection — Scans code line by line against 50 rules across Security, Bug, Best Practice, Performance, and Code Quality categories. Each bug comes with a severity level (HIGH / MEDIUM / LOW) and an auto-fix suggestion.
Complexity Analysis — Calculates Time Complexity (O(1) to O(2^n)) and Space Complexity using our own formula. Also gives a Quality Score out of 100.
ML Classifier — A trained Naive Bayes model predicts whether the submitted code is "Good Code" or "Needs Improvement" with a confidence percentage.
Chat with Code — Ask questions about your code after analysis.


Supported Languages
Python, JavaScript, Java, C++, SQL

ML Model Performance
Evaluated using 5-Fold Stratified Cross-Validation on 151 multilanguage code samples:
MetricScoreAccuracy85.43%Precision81.73%Recall96.59%F1 Score88.54%
Training dataset: 88 Good Code examples + 63 Bad Code examples across all 5 supported languages.

Project Structure
CodeML-Analyzer/
├── app.py                  # Flask backend — main server
├── requirements.txt        # Python dependencies
├── ml/
│   ├── bug_detector.py     # 50 rule-based detection rules + auto-fix
│   ├── complexity.py       # Time & space complexity analyzer
│   └── classifier.py       # Naive Bayes ML classifier
└── templates/
│   └── index.html          # Frontend UI
└── static/
    ├── style.css            # Styling
    └── script.js            # Frontend logic, language detection

How to Run Locally
1. Clone the repository
bashgit clone https://github.com/your-username/AI_CODE_ANALYZER.git
cd AI_CODE_ANALYZER
2. Install dependencies
bashpip install -r requirements.txt
3. Run the server
bashpython app.py
4. Open in browser
http://localhost:5000

How It Works
Bug Detector
Checks every line of code against 50 patterns organized into 6 categories:
CategoryExamplesSecurityeval(), exec(), hardcoded passwords, api_key, shell=TrueBugBare except, open() without with, while True without breakBest Practice== None, == True, range(len()), type() instead of isinstance()PerformanceString concatenation in loops, double sorting, repeated appendStudent Mistakesint(input()) crash, list/dict shadowing, index out of rangeCode QualityTODO, pass, generic function names, dead code
Complexity Analyzer
Counts loops, nesting levels, and recursive calls to determine:
Time ComplexityDetected WhenO(1)No loops, no recursionO(log n)Binary search pattern, mid variable, divide-and-conquerO(n)Single loopO(n log n)Recursive + divide patternO(n²)2 nested loopsO(n³)3 nested loopsO(2^n)Multiple recursive calls without memoization (e.g. naive Fibonacci)
Space Complexity is separately calculated based on data structures (lists, dicts, sets) and recursion depth.
ML Classifier

Algorithm: Multinomial Naive Bayes (alpha = 0.3)
Feature Extraction: TF-IDF Vectorizer (3000 features, n-gram range 1–3, sublinear TF)
Dataset: 151 manually curated samples across Python, JavaScript, Java, C++, SQL
Evaluation: 5-Fold Stratified Cross-Validation


Features

Language mismatch detection — warns if you paste C++ code in Python tab
Empty code check — clear error message if editor is empty
Auto-fix suggestions — each detected bug comes with how to fix it
Selective analysis — enable/disable individual modules via checkboxes
Chat interface — ask questions about your code after analysis
Fully offline — no external APIs, all analysis runs locally


Tech Stack
LayerTechnologyBackendPython 3, FlaskMLScikit-learn (Naive Bayes, TF-IDF)FrontendHTML, CSS, JavaScriptDataManually created dataset
