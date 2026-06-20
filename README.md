AI Code Analyzer

A web-based code analysis tool that reviews code automatically using Machine Learning. Paste any code and get instant feedback across three areas: bug detection, complexity analysis, and an ML-based code quality classifier.
This was a team project — forked here from the original repo by nahidaa-parbeen, built collaboratively. I contributed to development alongside my teammate.

What it does
Bug Detection — scans code line-by-line against 50 rules across security, bug, best-practice, performance, and code-quality categories, each with a severity level and auto-fix suggestion
Complexity Analysis — calculates time and space complexity, plus an overall quality score
ML Classifier — a trained Naive Bayes model predicts whether code is "Good" or "Needs Improvement," with a confidence percentage

Tech stack


-Python, Flask (backend)
-Scikit-learn — Multinomial Naive Bayes + TF-IDF for the classifier
-HTML, CSS, JavaScript (frontend)
-Supports analysis for Python, JavaScript, Java, C++, SQL

Model performance
Evaluated with 5-fold stratified cross-validation on 151 multi-language code samples — 85.4% accuracy, 88.5% F1 score.
Running locally

bashgit clone https://github.com/PalakA321/AI_CODE_ANALYZER.git
cd AI_CODE_ANALYZER
pip install -r requirements.txt
python app.py
Then open http://localhost:5000.

Contributors
nahidaa-parbeen
Palak Agrawal
