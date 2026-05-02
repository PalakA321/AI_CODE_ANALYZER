/* =============================================
   CodeML Analyzer — Interactive Frontend
   ============================================= */

let selectedLanguage = "Python";
let lastData = null;
let currentTab = "overview";

// ---- PARTICLE BACKGROUND ----
(function () {
  const canvas = document.getElementById("bgCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  let W, H, particles;

  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  function createParticles() {
    particles = [];
    const count = Math.floor(W / 18);
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * W, y: Math.random() * H,
        r: Math.random() * 1.5 + 0.3,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        alpha: Math.random() * 0.4 + 0.1
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {
          ctx.beginPath();
          ctx.strokeStyle = `rgba(59,130,246,${0.05 * (1 - dist / 120)})`;
          ctx.lineWidth = 0.5;
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }
    particles.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(99,130,246,${p.alpha})`;
      ctx.fill();
    });
    requestAnimationFrame(draw);
  }

  resize(); createParticles(); draw();
  window.addEventListener("resize", () => { resize(); createParticles(); });
})();

// ---- TYPING EFFECT ----
(function () {
  const phrases = [
    "instant AI analysis",
    "real-time bug detection",
    "complexity breakdown",
    "security scanning",
    "ML classification"
  ];
  const el = document.getElementById("typeTarget");
  if (!el) return;
  let pi = 0, ci = 0, deleting = false;
  function type() {
    const phrase = phrases[pi];
    if (!deleting) {
      el.textContent = phrase.slice(0, ++ci);
      if (ci === phrase.length) { deleting = true; setTimeout(type, 1800); return; }
    } else {
      el.textContent = phrase.slice(0, --ci);
      if (ci === 0) { deleting = false; pi = (pi + 1) % phrases.length; setTimeout(type, 300); return; }
    }
    setTimeout(type, deleting ? 45 : 75);
  }
  setTimeout(type, 800);
})();

// ---- LINE NUMBERS ----
const codeInput = document.getElementById("codeInput");
const lineNums  = document.getElementById("lineNums");

function updateLineNums() {
  const lines = codeInput.value.split("\n").length;
  lineNums.textContent = Array.from({ length: lines }, (_, i) => i + 1).join("\n");
  lineNums.scrollTop = codeInput.scrollTop;
}

codeInput.addEventListener("input", updateLineNums);
codeInput.addEventListener("scroll", () => { lineNums.scrollTop = codeInput.scrollTop; });
codeInput.addEventListener("keydown", e => {
  if (e.key === "Tab") {
    e.preventDefault();
    const s = codeInput.selectionStart;
    codeInput.value = codeInput.value.slice(0, s) + "    " + codeInput.value.slice(codeInput.selectionEnd);
    codeInput.selectionStart = codeInput.selectionEnd = s + 4;
    updateLineNums();
  }
});
updateLineNums();

// ---- LANGUAGE SELECT ----
function selectLang(btn) {
  document.querySelectorAll(".ltab").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  selectedLanguage = btn.textContent;
}

// ---- TAB SWITCH ----
function switchTab(btn, tabName) {
  document.querySelectorAll(".rtab").forEach(t => t.classList.remove("active"));
  btn.classList.add("active");
  currentTab = tabName;
  if (lastData) showTab(tabName);
}

// ---- ANALYZE ----
async function analyzeCode() {
  const code = codeInput.value.trim();
  if (!code) {
    flash("Code editor is empty! Please paste your code first.");
    document.getElementById("resultBody").innerHTML = `
      <div class="empty-state">
        <div class="empty-spin-wrap">
          <svg class="empty-ring-outer" viewBox="0 0 100 100" width="100" height="100">
            <circle cx="50" cy="50" r="44" fill="none" stroke="#f87171" stroke-width="3.5"
              stroke-dasharray="80 197" stroke-linecap="round"/>
          </svg>
          <span class="empty-icon" style="color:#f87171">!</span>
        </div>
        <p class="empty-title" style="color:#f87171">No Code Found</p>
        <p class="empty-sub">Please paste your <strong>${selectedLanguage}</strong> code in the editor on the left, then click Analyze Code.</p>
      </div>`;
    return;
  }

  const btn = document.getElementById("analyzeBtn");
  btn.classList.add("loading"); btn.disabled = true;

  const resultBody = document.getElementById("resultBody");
  resultBody.innerHTML = `
    <div class="empty-state">
      <div style="width:50px;height:50px;border:3px solid #1a2d4a;border-top-color:#3b82f6;border-radius:50%;animation:spin 0.8s linear infinite;margin-bottom:12px"></div>
      <p class="empty-title">Analyzing your code...</p>
      <p class="empty-sub">Running ML models</p>
    </div>`;

  // Language mismatch detection
  const langPatterns = {
    "Python":     [/^def /, /^class /, /^import /, /^from .* import/, /print\(/, /:\s*$/m],
    "JavaScript": [/function\s+\w+/, /const |let |var /, /=>\s*{/, /console\.log/, /\.forEach\(/, /require\(/],
    "Java":       [/public (class|static|void)/, /System\.out\.print/, /new ArrayList/, /import java\./],
    "C++":        [/#include/, /using namespace/, /cout <</, /std::/, /int main\(/],
    "SQL":        [/SELECT .* FROM/i, /INSERT INTO/i, /CREATE TABLE/i, /UPDATE .* SET/i, /WHERE /i]
  };

  function detectLanguage(code) {
    let scores = {};
    for (const [lang, patterns] of Object.entries(langPatterns)) {
      scores[lang] = patterns.filter(p => p.test(code)).length;
    }
    return Object.entries(scores).sort((a, b) => b[1] - a[1])[0];
  }

  const [detectedLang, detectedScore] = detectLanguage(code);
  if (detectedScore > 0 && detectedLang !== selectedLanguage) {
    document.getElementById("resultBody").innerHTML = `
      <div class="rcard" style="border-color:#f87171">
        <div class="rcard-title" style="color:#f87171">Language Mismatch Detected</div>
        <p style="font-size:13px;color:#dce8f5;margin-bottom:12px">
          You selected <strong style="color:#60a5fa">${selectedLanguage}</strong> but the code looks like
          <strong style="color:#f87171">${detectedLang}</strong>.
        </p>
        <p style="font-size:12px;color:#8eaac8;margin-bottom:14px">
          Please either switch the language tab to <strong>${detectedLang}</strong>
          or paste the correct <strong>${selectedLanguage}</strong> code.
        </p>
        <div style="display:flex;gap:10px;flex-wrap:wrap">
          <button onclick="switchToDetected('${detectedLang}')"
            style="padding:8px 16px;background:rgba(248,113,113,0.15);border:1px solid #f87171;
            color:#f87171;border-radius:8px;cursor:pointer;font-size:12px;font-family:var(--mono)">
            Switch to ${detectedLang} and Analyze
          </button>

        </div>
      </div>`;
    btn.classList.remove("loading"); btn.disabled = false;
    return;
  }

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code,
        language: selectedLanguage,
        run_bug:      document.getElementById("chkBug").checked,
        run_complex:  document.getElementById("chkComplex").checked,
        run_security: document.getElementById("chkSec").checked,
        run_ml:       document.getElementById("chkML").checked
      })
    });
    lastData = await response.json();
    showTab(currentTab);
  } catch (error) {
    resultBody.innerHTML = `<div class="rcard"><p class="c-red">Error: ${error.message}</p></div>`;
  } finally {
    btn.classList.remove("loading"); btn.disabled = false;
  }
}

// ---- LANGUAGE MISMATCH HELPERS ----
function switchToDetected(lang) {
  document.querySelectorAll(".ltab").forEach(b => {
    if (b.textContent.trim() === lang) {
      b.click();
    }
  });
  analyzeCode();
}



// ---- SHOW TAB ----
function showTab(tabName) {
  const resultBody = document.getElementById("resultBody");
  if (!lastData) return;
  const d = lastData;

  // Show "disabled" message if this module was unchecked
  const skipMap = {
    bugs:       !document.getElementById("chkBug").checked,
    security:   !document.getElementById("chkSec").checked,
    complexity: !document.getElementById("chkComplex").checked,
    classifier: !document.getElementById("chkML").checked
  };
  if (skipMap[tabName]) {
    resultBody.innerHTML = `<div class="rcard" style="text-align:center;padding:30px">
      <p style="font-size:14px;color:#546e8a;margin-bottom:8px">This module was disabled</p>
      <p style="font-size:12px;color:#2e4f6e">Enable the checkbox and click Analyze Code again to see results.</p>
    </div>`;
    return;
  }

  if (tabName === "overview") {
    const qs = d.complexity.quality_score;
    const qColor = qs >= 70 ? "#34d399" : qs >= 40 ? "#fbbf24" : "#f87171";
    resultBody.innerHTML = `
      <div class="rcard" style="animation-delay:0s">
        <div class="rcard-title c-blue">Overview</div>
        <div class="mrow"><span class="mlabel">Language</span><span class="mvalue">${d.language}</span></div>
        <div class="mrow"><span class="mlabel">Total Lines</span><span class="mvalue">${d.complexity.total_lines}</span></div>
        <div class="mrow"><span class="mlabel">Code Lines</span><span class="mvalue">${d.complexity.code_lines}</span></div>
        <div class="mrow"><span class="mlabel">Functions</span><span class="mvalue">${d.complexity.function_count}</span></div>
        <div class="mrow"><span class="mlabel">Classes</span><span class="mvalue">${d.complexity.class_count}</span></div>
        <div class="mrow"><span class="mlabel">Bugs Found</span><span class="mvalue c-red">${d.bug_summary.total}</span></div>
        <div class="mrow"><span class="mlabel">ML Classification</span><span class="mvalue" style="color:${d.classification.quality==='Good Code'?'#34d399':'#f87171'}">${d.classification.quality}</span></div>
      </div>
      <div class="rcard" style="animation-delay:0.05s">
        <div class="rcard-title c-purple">Quality Score</div>
        <div class="score-big" style="background:linear-gradient(135deg,${qColor},#8b5cf6);-webkit-background-clip:text;background-clip:text">${qs}<span style="font-size:16px">/100</span></div>
        <div class="pbar-wrap"><div class="pbar-fill" style="width:${qs}%;background:linear-gradient(90deg,${qColor},#8b5cf6)"></div></div>
      </div>
      <div class="rcard" style="animation-delay:0.1s">
        <div class="rcard-title c-cyan">Bug Summary</div>
        <div class="mrow"><span class="mlabel">🔴 High Severity</span><span class="mvalue c-red">${d.bug_summary.high}</span></div>
        <div class="mrow"><span class="mlabel">🟡 Medium Severity</span><span class="mvalue c-yellow">${d.bug_summary.medium}</span></div>
        <div class="mrow"><span class="mlabel">🟢 Low Severity</span><span class="mvalue c-green">${d.bug_summary.low}</span></div>
      </div>`;

  } else if (tabName === "bugs") {
    const bugs = d.bugs;
    if (bugs.length === 0) {
      resultBody.innerHTML = `<div class="rcard"><div class="rcard-title c-green">Bug Detection</div><p style="color:#34d399;font-size:14px;text-align:center;padding:20px">No bugs detected!</p></div>`;
      return;
    }
    let html = `<div class="rcard" style="animation-delay:0s">
      <div class="rcard-title c-red">Bugs Found — ${bugs.length} issues</div>
      <div class="mrow"><span class="mlabel">High</span><span class="mvalue c-red">${d.bug_summary.high}</span></div>
      <div class="mrow"><span class="mlabel">Medium</span><span class="mvalue c-yellow">${d.bug_summary.medium}</span></div>
      <div class="mrow"><span class="mlabel">Low</span><span class="mvalue c-green">${d.bug_summary.low}</span></div>
    </div>`;
    bugs.forEach((bug, i) => {
      const bc = bug.severity === "HIGH" ? "badge-high" : bug.severity === "MEDIUM" ? "badge-medium" : "badge-low";
      html += `<div class="rcard" style="animation-delay:${(i+1)*0.05}s">
        <div style="display:flex;align-items:center;flex-wrap:wrap;gap:4px;margin-bottom:4px">
          <span class="badge ${bc}">${bug.severity}</span>
          <span class="bug-meta">Line ${bug.line} — ${bug.category}</span>
        </div>
        <p class="bug-msg">${bug.message}</p>
        <code class="bug-code">${escapeHtml(bug.code)}</code>
        ${bug.fix ? `<p style="margin-top:6px;font-size:12px;color:#34d399;background:rgba(52,211,153,0.08);padding:6px 10px;border-radius:6px;border-left:2px solid #34d399">Fix: ${bug.fix}</p>` : ''}
      </div>`;
    });
    resultBody.innerHTML = html;

  } else if (tabName === "complexity") {
    const c = d.complexity;
    resultBody.innerHTML = `
      <div class="rcard" style="animation-delay:0s">
        <div class="rcard-title c-cyan">Complexity Analysis</div>
        <div class="mrow"><span class="mlabel">Time Complexity</span><span class="mvalue c-cyan">${c.time_complexity}</span></div>
        <div class="mrow"><span class="mlabel">Space Complexity</span><span class="mvalue c-purple">${c.space_complexity}</span></div>
        <div class="mrow"><span class="mlabel">Loop Count</span><span class="mvalue">${c.loop_count}</span></div>
        <div class="mrow"><span class="mlabel">Conditions</span><span class="mvalue">${c.condition_count}</span></div>
        <div class="mrow"><span class="mlabel">Max Nesting</span><span class="mvalue">${c.max_nesting} levels</span></div>
        <div class="mrow"><span class="mlabel">Recursive Calls</span><span class="mvalue">${c.recursive_calls}</span></div>
        <div class="mrow"><span class="mlabel">Data Structures Used</span><span class="mvalue">${c.data_structures_used}</span></div>
        <div class="mrow"><span class="mlabel">Complexity Score</span><span class="mvalue c-yellow">${c.complexity_score}</span></div>
      </div>
      <div class="rcard" style="animation-delay:0.05s">
        <div class="rcard-title c-blue">Code Metrics</div>
        <div class="mrow"><span class="mlabel">Total Lines</span><span class="mvalue">${c.total_lines}</span></div>
        <div class="mrow"><span class="mlabel">Comment Lines</span><span class="mvalue">${c.comment_lines}</span></div>
        <div class="mrow"><span class="mlabel">Functions</span><span class="mvalue">${c.function_count}</span></div>
        <div class="mrow"><span class="mlabel">Classes</span><span class="mvalue">${c.class_count}</span></div>
      </div>`;

  } else if (tabName === "security") {
    const secBugs = d.bugs.filter(b => b.category === "Security");
    if (secBugs.length === 0) {
      resultBody.innerHTML = `<div class="rcard"><div class="rcard-title c-green">Security Scan</div><p style="color:#34d399;font-size:14px;text-align:center;padding:20px">No security issues found!</p></div>`;
      return;
    }
    let html = `<div class="rcard"><div class="rcard-title c-red">Security Issues — ${secBugs.length} found</div></div>`;
    secBugs.forEach((bug, i) => {
      html += `<div class="rcard" style="animation-delay:${i*0.05}s">
        <div style="display:flex;align-items:center;gap:4px;margin-bottom:4px;flex-wrap:wrap">
          <span class="badge badge-high">SECURITY</span>
          <span class="bug-meta">Line ${bug.line}</span>
        </div>
        <p class="bug-msg">${bug.message}</p>
        <code class="bug-code">${escapeHtml(bug.code)}</code>
        ${bug.fix ? `<p style="margin-top:6px;font-size:12px;color:#34d399;background:rgba(52,211,153,0.08);padding:6px 10px;border-radius:6px;border-left:2px solid #34d399">Fix: ${bug.fix}</p>` : ''}
      </div>`;
    });
    resultBody.innerHTML = html;

  } else if (tabName === "classifier") {
    const cl = d.classification;
    const isGood = cl.quality === "Good Code";
    const mainColor = isGood ? "#34d399" : "#f87171";
    const score = cl.score;
    resultBody.innerHTML = `
      <div class="rcard" style="animation-delay:0s">
        <div class="rcard-title c-purple">ML Classifier Result</div>
        <div style="text-align:center;padding:12px 0 6px">
          <div style="font-size:36px;font-weight:700;font-family:var(--mono);color:${mainColor};margin-bottom:4px">${isGood ? "✓" : "⚠"}</div>
          <div style="font-size:20px;font-weight:700;color:${mainColor}">${cl.quality}</div>
        </div>
        <div class="mrow"><span class="mlabel">Confidence</span><span class="mvalue">${cl.confidence}%</span></div>
        <div class="mrow"><span class="mlabel">Good Code Score</span><span class="mvalue c-green">${score}%</span></div>
        <div class="pbar-wrap" style="margin-top:10px">
          <div class="pbar-fill" style="width:${score}%;background:linear-gradient(90deg,${mainColor},#8b5cf6)"></div>
        </div>
        <p style="margin-top:12px;font-size:10px;color:var(--text-dim);text-align:center">
          Model: Naive Bayes + TF-IDF · Trained on 150+ code samples
        </p>
      </div>`;
  }
}

// ---- SMART CHATBOT ----
function sendChat() {
  const input = document.getElementById("chatInput");
  const question = input.value.trim();
  if (!question) return;

  addBubble(question, "user");
  input.value = "";

  if (!lastData) {
    addBubble("Please analyze your code first! Paste your code on the left and click <b>Analyze Code</b> — then I can answer all your questions. 😊", "ai");
    return;
  }

  const q = question.toLowerCase();
  const d = lastData;
  const c = d.complexity;
  const bugs = d.bugs;
  const qs = c.quality_score;

  // OPTIMIZE / IMPROVE
  if (q.includes("optim") || q.includes("improve") || q.includes("better") || q.includes("enhance") || q.includes("suggest") || q.includes("tip") || q.includes("help") || q.includes("fix") || q.includes("how")) {
    let tips = [];

    if (c.max_nesting > 3)
      tips.push("<b>Reduce deep nesting</b> — your max nesting depth is " + c.max_nesting + " levels. Anything beyond 3 makes code hard to read. Use early returns or extract helper functions.");

    if (c.loop_count > 3)
      tips.push("<b>Optimize your loops</b> — " + c.loop_count + " loops detected. Nested loops increase time complexity. Try list comprehensions or built-in functions like <code>map()</code> and <code>filter()</code>.");

    if (c.comment_lines === 0)
      tips.push("<b>Add comments</b> — there are no comments in your code! Write a brief description above each function explaining what it does. This greatly improves readability.");

    if (c.function_count === 0 && c.code_lines > 10)
      tips.push("<b>Break code into functions</b> — all your code is in one block. Separate concerns into named functions like <code>calculate()</code>, <code>display()</code>, <code>validate()</code>.");

    if (bugs.filter(b => b.severity === "HIGH").length > 0)
      tips.push("<b>Fix high severity bugs first</b> — " + bugs.filter(b => b.severity === "HIGH").length + " critical issue(s) found. Check the Bugs tab and resolve them immediately.");

    if (bugs.filter(b => b.category === "Best Practice").length > 0)
      tips.push("<b>Follow best practices</b> — for example, use <code>is None</code> instead of <code>== None</code>, and use variables directly instead of comparing to <code>True</code>.");

    if (c.function_count > 0 && c.comment_lines < c.function_count)
      tips.push("<b>Add docstrings</b> — add a docstring inside each function. Example: <code>\"\"\"Sorts the input list in ascending order.\"\"\"</code>");

    if (qs >= 80)
      tips.push("<b>Code is already quite good!</b> Score: " + qs + "/100. Focus on improving comments and error handling to reach a perfect score.");

    if (tips.length === 0)
      tips.push("<b>Great job! Code looks clean.</b> Score: " + qs + "/100 — no major issues found. Consider writing unit tests as the next step!");

    addBubble("<b>Here are ways to improve your code:</b><br><br>" + tips.join("<br><br>"), "ai");

  // BUGS
  } else if (q.includes("bug") || q.includes("error") || q.includes("issue") || q.includes("problem") || q.includes("wrong")) {
    if (bugs.length === 0) {
      addBubble("No bugs found! Your code appears to be bug-free. High: 0, Medium: 0, Low: 0. Excellent work!", "ai");
    } else {
      const highBugs = bugs.filter(b => b.severity === "HIGH");
      const medBugs  = bugs.filter(b => b.severity === "MEDIUM");
      let reply = `<b>${bugs.length} issue(s) detected:</b> ${d.bug_summary.high} High &nbsp; ${d.bug_summary.medium} Medium &nbsp; ${d.bug_summary.low} Low<br><br>`;
      if (highBugs.length > 0) {
        reply += "<b>Fix these first (HIGH priority):</b><br>";
        highBugs.slice(0, 2).forEach(b => { reply += `• Line ${b.line}: ${b.message}<br>`; });
      }
      if (medBugs.length > 0) {
        reply += "<br><b>Medium priority:</b><br>";
        medBugs.slice(0, 2).forEach(b => { reply += `• Line ${b.line}: ${b.message}<br>`; });
      }
      reply += "<br>Visit the <b>Bugs tab</b> for full details.";
      addBubble(reply, "ai");
    }

  // COMPLEXITY
  } else if (q.includes("complex") || q.includes("time") || q.includes("loop") || q.includes("nesting") || q.includes("slow") || q.includes("fast") || q.includes("performance")) {
    let reply = `<b>Complexity Report:</b><br><br>`;
    reply += `Time Complexity: <b>${c.time_complexity}</b><br>`;
    reply += `Space Complexity: <b>${c.space_complexity}</b><br>`;
    reply += `Loops: ${c.loop_count} &nbsp; | &nbsp; Conditions: ${c.condition_count}<br>`;
    reply += `Max Nesting Depth: ${c.max_nesting} levels<br><br>`;
    if (c.max_nesting > 4)
      reply += "Nesting is very deep! Each extra nesting level adds O(n) overhead. Refactor using helper functions to bring it under 3 levels.<br>";
    else if (c.loop_count >= 2)
      reply += "Multiple loops detected — check for any nested loops causing O(n²) complexity. Using a dictionary or set can often bring this down to O(n).<br>";
    else
      reply += "Complexity looks good! Code appears to be efficient.<br>";
    addBubble(reply, "ai");

  // SECURITY
  } else if (q.includes("security") || q.includes("safe") || q.includes("secure") || q.includes("vulnerable") || q.includes("password") || q.includes("hack")) {
    const secBugs = bugs.filter(b => b.category === "Security");
    if (secBugs.length === 0) {
      addBubble("<b>Security scan passed!</b> No security issues found. No hardcoded passwords, no <code>eval()</code>, no <code>exec()</code> detected. Your code looks safe!", "ai");
    } else {
      let reply = `<b>${secBugs.length} security issue(s) found — these must be fixed:</b><br><br>`;
      secBugs.forEach(b => { reply += `Line ${b.line}: ${b.message}<br>`; });
      reply += "<br><b>General security tips:</b><br>• Never store passwords in source code — use environment variables or a <code>.env</code> file<br>• Avoid <code>eval()</code> and <code>exec()</code> — they open the door to code injection attacks<br>• Avoid <code>import *</code> — always use specific imports";
      addBubble(reply, "ai");
    }

  // QUALITY / SCORE
  } else if (q.includes("quality") || q.includes("score") || q.includes("rating") || q.includes("marks") || q.includes("grade") || q.includes("good") || q.includes("bad")) {
    const grade = qs >= 80 ? "A — Excellent!" : qs >= 60 ? "B — Good, needs a bit more polish" : qs >= 40 ? "C — Average, several improvements required" : "D — Needs significant work";
    addBubble(`<b>Code Quality Report:</b><br><br>Quality Score: <b>${qs}/100</b><br>Grade: <b>${grade}</b><br>ML Classification: <b>${d.classification.quality}</b> (${d.classification.confidence}% confidence)<br><br>${qs < 60 ? "Try asking me <i>'how to improve'</i> for detailed, actionable suggestions!" : "Looking great! A few more refinements and it will be excellent."}`, "ai");

  // EXPLAIN CODE
  } else if (q.includes("explain") || q.includes("what does") || q.includes("describe") || q.includes("overview") || q.includes("summary")) {
    addBubble(`<b>Code Overview:</b><br><br>${c.total_lines} total lines<br>${c.function_count} function(s) defined<br>${c.class_count} class(es) found<br>Time complexity: ${c.time_complexity}<br>${bugs.length} potential issue(s) detected<br><br>Code is ${d.classification.quality === "Good Code" ? "generally clean and readable" : "in need of some improvements — check the Bugs tab"}`, "ai");

  // FUNCTIONS / CLASSES
  } else if (q.includes("function") || q.includes("def") || q.includes("method") || q.includes("class") || q.includes("structure")) {
    let reply = `<b>Code Structure:</b><br><br>Functions: <b>${c.function_count}</b><br>Classes: <b>${c.class_count}</b><br>`;
    if (c.function_count === 0 && c.code_lines > 8)
      reply += "<br><b>Tip:</b> Consider breaking your code into functions. This improves reusability and readability — one function, one responsibility is the golden rule.";
    else if (c.function_count > 0)
      reply += "<br>Good — you are using functions! Make sure each function name clearly describes what it does.";
    addBubble(reply, "ai");

  // HELLO
  } else if (q.includes("hi") || q.includes("hello") || q.includes("hey")) {
    addBubble("Hi! I'm your Code Analysis Assistant. Your code has been analyzed. You can ask me:<br><br>• <b>'How do I optimize my code?'</b><br>• <b>'What bugs were found?'</b><br>• <b>'Is my code secure?'</b><br>• <b>'What is my quality score?'</b><br>• <b>'Explain my code'</b>", "ai");

  // DEFAULT
  } else {
    const tips = [];
    if (d.bug_summary.high > 0) tips.push(`fix ${d.bug_summary.high} high-severity bug(s)`);
    if (c.max_nesting > 3) tips.push("reduce nesting depth");
    if (c.comment_lines === 0) tips.push("add comments");
    if (c.function_count === 0) tips.push("use functions");

    addBubble(`Here is a quick summary of your code:<br><br>Score: <b>${qs}/100</b> &nbsp;|&nbsp; Bugs: <b>${bugs.length}</b> &nbsp;|&nbsp; ML: <b>${d.classification.quality}</b><br><br>${tips.length > 0 ? "Recommended actions: " + tips.join(", ") + "." : "Code looks clean overall!"}<br><br>Try asking: <i>'how to optimize'</i>, <i>'what bugs'</i>, <i>'security check'</i>, or <i>'explain my code'</i>`, "ai");
  }
}

function addBubble(text, type) {
  const chat = document.getElementById("chatMessages");
  const div = document.createElement("div");
  div.className = `bubble ${type}`;
  div.innerHTML = `
    <div class="bubble-avatar">${type === "ai" ? "AI" : "U"}</div>
    <div class="bubble-content">${text}</div>`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function escapeHtml(s) {
  return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

function flash(msg) {
  const existing = document.querySelector(".flash-msg");
  if (existing) existing.remove();
  const el = document.createElement("div");
  el.className = "flash-msg";
  el.style.cssText = `position:fixed;top:80px;left:50%;transform:translateX(-50%);background:#1a2d4a;border:1px solid #3b82f6;color:#60a5fa;padding:10px 20px;border-radius:8px;font-size:13px;z-index:9999;font-family:var(--mono);animation:fadeSlide 0.3s ease`;
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 2500);
}

document.getElementById("chatInput").addEventListener("keypress", e => {
  if (e.key === "Enter") sendChat();
});
