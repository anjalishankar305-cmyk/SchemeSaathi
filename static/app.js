/**
 * SchemeSaathi - Client Application
 * Handles Multilingual UI rendering, Web Speech API (STT & TTS),
 * RAG Chat, Deterministic Eligibility, and Notice Explanation.
 */

let currentLang = "en";
let recognition = null;
let isListening = false;
let currentUtterance = null;
let selectedFile = null;

const LANG_VOICE_MAP = {
  en: "en-IN",
  hi: "hi-IN",
  kn: "kn-IN",
  ta: "ta-IN"
};

document.addEventListener("DOMContentLoaded", () => {
  initLanguage();
  initTabs();
  initSpeechRecognition();
  initChat();
  initEligibility();
  initNotice();
  checkHealth();
});

// 1. Language & Localization
function initLanguage() {
  const langSelect = document.getElementById("langSelect");
  langSelect.addEventListener("change", (e) => {
    currentLang = e.target.value;
    updateUILanguage(currentLang);
  });
  updateUILanguage(currentLang);
}

function updateUILanguage(lang) {
  const t = LOCALES[lang] || LOCALES.en;

  // Header & Navigation
  document.getElementById("appTitle").textContent = t.appTitle;
  document.getElementById("appTagline").textContent = t.tagline;
  document.getElementById("tabAskBtn").textContent = t.tabAsk;
  document.getElementById("tabEligibilityBtn").textContent = t.tabEligibility;
  document.getElementById("tabNoticeBtn").textContent = t.tabNotice;

  // Chat Tab
  document.getElementById("chatInput").placeholder = t.chatPlaceholder;
  document.getElementById("sendBtnText").textContent = t.sendBtn;
  document.getElementById("micBtnText").textContent = t.micReady;
  document.getElementById("quickQuestionsTitle").textContent = t.quickQuestionsTitle;
  renderQuickQuestions(t.quickQuestions);

  // Eligibility Tab
  document.getElementById("eligibilityTitle").textContent = t.eligibilityTitle;
  document.getElementById("eligibilitySubtitle").textContent = t.eligibilitySubtitle;
  document.getElementById("lblAge").textContent = t.lblAge;
  document.getElementById("lblGender").textContent = t.lblGender;
  document.getElementById("optFemale").textContent = t.optFemale;
  document.getElementById("optMale").textContent = t.optMale;
  document.getElementById("optOther").textContent = t.optOther;
  document.getElementById("lblState").textContent = t.lblState;
  document.getElementById("lblIncome").textContent = t.lblIncome;
  document.getElementById("lblOccupation").textContent = t.lblOccupation;
  document.getElementById("optFarmer").textContent = t.optFarmer;
  document.getElementById("optStudent").textContent = t.optStudent;
  document.getElementById("optSelfEmployed").textContent = t.optSelfEmployed;
  document.getElementById("optSalaried").textContent = t.optSalaried;
  document.getElementById("optHomemaker").textContent = t.optHomemaker;
  document.getElementById("optRetired").textContent = t.optRetired;
  document.getElementById("optUnemployed").textContent = t.optUnemployed;
  document.getElementById("lblCategory").textContent = t.lblCategory;
  document.getElementById("optGen").textContent = t.optGen;
  document.getElementById("optOBC").textContent = t.optOBC;
  document.getElementById("optSC").textContent = t.optSC;
  document.getElementById("optST").textContent = t.optST;
  document.getElementById("lblOwnsLand").textContent = t.lblOwnsLand;
  document.getElementById("lblRationCard").textContent = t.lblRationCard;
  document.getElementById("optNone").textContent = t.optNone;
  document.getElementById("optBPL").textContent = t.optBPL;
  document.getElementById("optAAY").textContent = t.optAAY;
  document.getElementById("optAPL").textContent = t.optAPL;
  document.getElementById("lblTaxPayer").textContent = t.lblTaxPayer;
  document.getElementById("lblPuccaHouse").textContent = t.lblPuccaHouse;
  document.getElementById("lblLPG").textContent = t.lblLPG;
  document.getElementById("btnCheckAll").textContent = t.btnCheckAll;
  document.getElementById("btnReset").textContent = t.btnReset;

  // Notice Tab
  document.getElementById("noticeTitle").textContent = t.noticeTitle;
  document.getElementById("noticeSubtitle").textContent = t.noticeSubtitle;
  document.getElementById("dragDropText").textContent = t.dragDropText;
  document.getElementById("btnUpload").textContent = t.btnUpload;
  document.getElementById("btnCamera").textContent = t.btnCamera;
  document.getElementById("btnExplain").textContent = t.btnExplain;

  // Footer & Privacy
  document.getElementById("privacyBanner").textContent = t.privacyBanner;
  document.getElementById("disclaimer").textContent = t.disclaimer;
}

function renderQuickQuestions(questions) {
  const container = document.getElementById("quickQuestionChips");
  container.innerHTML = "";
  questions.forEach(q => {
    const chip = document.createElement("button");
    chip.className = "q-chip";
    chip.textContent = q;
    chip.addEventListener("click", () => {
      document.getElementById("chatInput").value = q;
      handleSendMessage();
    });
    container.appendChild(chip);
  });
}

// 2. Navigation Tabs
function initTabs() {
  const tabs = ["tabAsk", "tabEligibility", "tabNotice"];
  tabs.forEach(tabId => {
    const btn = document.getElementById(`${tabId}Btn`);
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-view").forEach(v => v.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(`${tabId}View`).classList.add("active");
    });
  });
}

// 3. Web Speech Recognition (Speech to Text)
function initSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const micBtn = document.getElementById("micBtn");
  const micText = document.getElementById("micBtnText");

  if (!SpeechRecognition) {
    micBtn.title = "Speech recognition not supported in this browser";
    micBtn.style.opacity = "0.5";
    return;
  }

  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = () => {
    isListening = true;
    micBtn.classList.add("listening");
    const t = LOCALES[currentLang] || LOCALES.en;
    micText.textContent = t.micListening;
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById("chatInput").value = transcript;
    handleSendMessage();
  };

  recognition.onerror = (e) => {
    console.warn("Speech recognition error:", e.error);
    stopListening();
  };

  recognition.onend = () => {
    stopListening();
  };

  micBtn.addEventListener("click", () => {
    if (isListening) {
      recognition.stop();
    } else {
      recognition.lang = LANG_VOICE_MAP[currentLang] || "en-IN";
      try {
        recognition.start();
      } catch (err) {
        console.warn("Recognition start failed:", err);
      }
    }
  });
}

function stopListening() {
  isListening = false;
  const micBtn = document.getElementById("micBtn");
  const micText = document.getElementById("micBtnText");
  micBtn.classList.remove("listening");
  const t = LOCALES[currentLang] || LOCALES.en;
  micText.textContent = t.micReady;
}

// 4. Web Speech Synthesis (Text to Speech)
function speakText(text, buttonEl) {
  if (!("speechSynthesis" in window)) {
    alert("Speech synthesis is not supported in your browser.");
    return;
  }

  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    if (buttonEl) buttonEl.textContent = (LOCALES[currentLang] || LOCALES.en).speakBtn;
    return;
  }

  const cleanText = text.replace(/[*#_~`]/g, "");
  currentUtterance = new SpeechSynthesisUtterance(cleanText);
  currentUtterance.lang = LANG_VOICE_MAP[currentLang] || "en-IN";
  currentUtterance.rate = 0.95;

  if (buttonEl) {
    const t = LOCALES[currentLang] || LOCALES.en;
    buttonEl.textContent = t.stopSpeakBtn;
    currentUtterance.onend = () => {
      buttonEl.textContent = t.speakBtn;
    };
    currentUtterance.onerror = () => {
      buttonEl.textContent = t.speakBtn;
    };
  }

  window.speechSynthesis.speak(currentUtterance);
}

// 5. Chat Interface
function initChat() {
  const sendBtn = document.getElementById("sendBtn");
  const chatInput = document.getElementById("chatInput");

  sendBtn.addEventListener("click", handleSendMessage);
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  });
}

async function handleSendMessage() {
  const chatInput = document.getElementById("chatInput");
  const message = chatInput.value.trim();
  if (!message) return;

  chatInput.value = "";
  appendUserMessage(message);

  const botBubble = appendBotLoading();

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: message,
        language: currentLang
      })
    });

    if (!res.ok) {
      throw new Error(`Server returned ${res.status}`);
    }

    const data = await res.json();
    updateBotMessage(botBubble, data);
  } catch (err) {
    botBubble.innerHTML = `<div class="msg-text" style="color: #ef4444;">Could not fetch response (${err.message}). Please check network or try again.</div>`;
  }
}

function appendUserMessage(text) {
  const chatBox = document.getElementById("chatBox");
  const div = document.createElement("div");
  div.className = "message-bubble user-msg";
  div.innerHTML = `<div class="msg-text">${escapeHtml(text)}</div>`;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function appendBotLoading() {
  const chatBox = document.getElementById("chatBox");
  const div = document.createElement("div");
  div.className = "message-bubble bot-msg";
  div.innerHTML = `
    <div class="msg-header">
      <span>SchemeSaathi</span>
    </div>
    <div class="msg-text" style="display: flex; align-items: center; gap: 0.5rem;">
      <span class="spinner" style="border-top-color: var(--primary);"></span>
      <span>Finding verified rules and official guidelines...</span>
    </div>
  `;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
  return div;
}

function updateBotMessage(botBubble, data) {
  const t = LOCALES[currentLang] || LOCALES.en;
  let citationsHtml = "";
  if (data.citations && data.citations.length > 0) {
    citationsHtml = `
      <div class="citations-box">
        <div class="citations-title">${t.sourcesTitle}</div>
        <div>
          ${data.citations.map(c => `
            <a href="${c.link}" target="_blank" rel="noopener noreferrer" class="citation-pill">
              🔗 ${escapeHtml(c.scheme_name)} (${escapeHtml(c.section)})
            </a>
          `).join("")}
        </div>
      </div>
    `;
  }

  const formattedAnswer = formatMarkdown(data.answer);

  botBubble.innerHTML = `
    <div class="msg-header">
      <span>SchemeSaathi (${data.model_used || "AI Verified"})</span>
    </div>
    <div class="msg-text">
      ${formattedAnswer}
    </div>
    ${citationsHtml}
    <div class="msg-actions">
      <button class="speak-btn" onclick="speakText('${escapeAttr(data.answer)}', this)">
        ${t.speakBtn}
      </button>
    </div>
  `;

  const chatBox = document.getElementById("chatBox");
  chatBox.scrollTop = chatBox.scrollHeight;
}

// 6. Eligibility Form & Evaluation
function initEligibility() {
  const checkBtn = document.getElementById("btnCheckAll");
  const resetBtn = document.getElementById("btnReset");

  checkBtn.addEventListener("click", handleCheckEligibility);
  resetBtn.addEventListener("click", () => {
    document.getElementById("eligibilityForm").reset();
    document.getElementById("eligibilityResults").innerHTML = "";
  });
}

async function handleCheckEligibility() {
  const resultsContainer = document.getElementById("eligibilityResults");
  resultsContainer.innerHTML = `
    <div style="text-align: center; padding: 2rem;">
      <span class="spinner" style="border-top-color: var(--primary); width: 2rem; height: 2rem;"></span>
      <p style="margin-top: 0.5rem; color: var(--text-muted);">Evaluating your profile against all 13 verified welfare criteria...</p>
    </div>
  `;

  const profile = {
    age: parseInt(document.getElementById("inputAge").value) || null,
    gender: document.getElementById("inputGender").value || null,
    state: document.getElementById("inputState").value || null,
    annual_income: parseFloat(document.getElementById("inputIncome").value) || null,
    occupation: document.getElementById("inputOccupation").value || null,
    category: document.getElementById("inputCategory").value || null,
    owns_land: document.getElementById("inputOwnsLand").value === "yes" ? true : (document.getElementById("inputOwnsLand").value === "no" ? false : null),
    ration_card_type: document.getElementById("inputRationCard").value || null,
    has_ration_card: document.getElementById("inputRationCard").value !== "none",
    is_income_tax_payer: document.getElementById("inputTaxPayer").value === "yes" ? true : (document.getElementById("inputTaxPayer").value === "no" ? false : null),
    owns_pucca_house: document.getElementById("inputPuccaHouse").value === "yes" ? true : (document.getElementById("inputPuccaHouse").value === "no" ? false : null),
    has_lpg_connection: document.getElementById("inputLPG").value === "yes" ? true : (document.getElementById("inputLPG").value === "no" ? false : null),
    is_student: document.getElementById("inputOccupation").value === "student",
    is_domestic_electricity_consumer: true
  };

  try {
    const res = await fetch("/api/eligibility/find", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile: profile })
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    renderEligibilityResults(data.results);
  } catch (err) {
    resultsContainer.innerHTML = `<div style="color: #ef4444; padding: 1rem;">Failed to evaluate eligibility: ${err.message}</div>`;
  }
}

function renderEligibilityResults(schemes) {
  const container = document.getElementById("eligibilityResults");
  container.innerHTML = "";
  const t = LOCALES[currentLang] || LOCALES.en;

  if (!schemes || schemes.length === 0) {
    container.innerHTML = "<p>No schemes evaluated.</p>";
    return;
  }

  schemes.forEach(s => {
    const card = document.createElement("div");
    card.className = `scheme-card ${s.status}`;

    let statusText = t.statusEligible;
    if (s.status === "needs_more_info") statusText = t.statusNeedsInfo;
    if (s.status === "not_eligible") statusText = t.statusNotEligible;

    let rulesHtml = "";
    if (s.passed_rules && s.passed_rules.length > 0) {
      rulesHtml += `
        <div class="rules-breakdown">
          <div class="rules-title" style="color: #166534;">${t.passedRulesTitle}</div>
          <ul class="rules-list">${s.passed_rules.map(r => `<li>${escapeHtml(r)}</li>`).join("")}</ul>
        </div>
      `;
    }

    if (s.failed_rules && s.failed_rules.length > 0) {
      rulesHtml += `
        <div class="rules-breakdown">
          <div class="rules-title" style="color: #991b1b;">${t.failedRulesTitle}</div>
          <ul class="rules-list">${s.failed_rules.map(r => `<li>${escapeHtml(r)}</li>`).join("")}</ul>
        </div>
      `;
    }

    if (s.missing_info && s.missing_info.length > 0) {
      rulesHtml += `
        <div class="rules-breakdown">
          <div class="rules-title" style="color: #92400e;">${t.missingInfoTitle}</div>
          <ul class="rules-list">${s.missing_info.map(m => `<li>${escapeHtml(m)}</li>`).join("")}</ul>
        </div>
      `;
    }

    let docsHtml = "";
    if (s.documents && s.documents.length > 0) {
      docsHtml = `
        <div class="docs-box">
          <strong>${t.requiredDocsTitle}</strong> ${s.documents.join(", ")}
        </div>
      `;
    }

    card.innerHTML = `
      <div class="scheme-header">
        <div>
          <div class="scheme-title">${escapeHtml(s.scheme_name)}</div>
          <div class="scheme-dept">${escapeHtml(s.dept)} (${escapeHtml(s.level)})</div>
        </div>
        <span class="status-badge ${s.status}">${statusText}</span>
      </div>
      <div style="font-size: 0.92rem; color: var(--text-main);">
        <strong>Benefits:</strong> ${escapeHtml(s.benefits)}
      </div>
      ${rulesHtml}
      ${docsHtml}
      <div class="scheme-actions">
        <a href="${s.apply_url}" target="_blank" rel="noopener noreferrer" class="apply-link">
          ${t.btnApplyNow}
        </a>
      </div>
    `;

    container.appendChild(card);
  });
}

// 7. Notice Explainer
function initNotice() {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("noticeFileInput");
  const cameraInput = document.getElementById("cameraInput");
  const btnExplain = document.getElementById("btnExplain");

  dropzone.addEventListener("click", () => fileInput.click());
  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.style.borderColor = "var(--primary)";
  });
  dropzone.addEventListener("dragleave", () => {
    dropzone.style.borderColor = "var(--primary-light)";
  });
  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.style.borderColor = "var(--primary-light)";
    if (e.dataTransfer.files.length > 0) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  cameraInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  document.getElementById("btnUpload").addEventListener("click", (e) => {
    e.stopPropagation();
    fileInput.click();
  });

  document.getElementById("btnCamera").addEventListener("click", (e) => {
    e.stopPropagation();
    cameraInput.click();
  });

  btnExplain.addEventListener("click", handleExplainNotice);
}

function handleFileSelected(file) {
  selectedFile = file;
  const preview = document.getElementById("filePreview");
  preview.style.display = "flex";
  document.getElementById("fileNameDisplay").textContent = `Selected: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
  document.getElementById("btnExplain").disabled = false;
}

async function handleExplainNotice() {
  if (!selectedFile) return;

  const btnExplain = document.getElementById("btnExplain");
  const outputBox = document.getElementById("noticeOutput");
  const t = LOCALES[currentLang] || LOCALES.en;

  btnExplain.disabled = true;
  btnExplain.innerHTML = `<span class="spinner"></span> ${t.explainingText}`;
  outputBox.style.display = "block";
  outputBox.innerHTML = `<p style="color: var(--text-muted);">${t.explainingText}</p>`;

  const formData = new FormData();
  formData.append("file", selectedFile);
  formData.append("language", currentLang);

  try {
    const res = await fetch("/api/explain-notice", {
      method: "POST",
      body: formData
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    outputBox.innerHTML = `
      <div style="margin-bottom: 0.75rem; font-weight: 600; color: var(--text-muted);">
        Notice Explanation (${data.model_used || "AI Verified"}):
      </div>
      <div>${formatMarkdown(data.explanation)}</div>
      <div class="notice-warning">
        <strong>⚠️ ${t.noticeWarningTitle}</strong> ${escapeHtml(data.warning || "")}
      </div>
      <div style="margin-top: 1rem;">
        <button class="speak-btn" onclick="speakText('${escapeAttr(data.explanation)}', this)">
          ${t.speakBtn}
        </button>
      </div>
    `;
  } catch (err) {
    outputBox.innerHTML = `<p style="color: #ef4444;">Error processing notice: ${err.message}</p>`;
  } finally {
    btnExplain.disabled = false;
    btnExplain.textContent = t.btnExplain;
  }
}

// 8. Health Check
async function checkHealth() {
  try {
    const res = await fetch("/health");
    const data = await res.json();
    const banner = document.getElementById("demoBanner");
    if (!data.gemini_api_key_configured) {
      banner.style.display = "flex";
    } else {
      banner.style.display = "none";
    }
  } catch (err) {
    console.warn("Health check error:", err);
  }
}

// Utility Helpers
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function escapeAttr(str) {
  if (!str) return "";
  return String(str)
    .replace(/\\/g, "\\\\")
    .replace(/'/g, "\\'")
    .replace(/"/g, "&quot;")
    .replace(/\n/g, " ");
}

function formatMarkdown(text) {
  if (!text) return "";
  let html = escapeHtml(text);
  // Bold
  html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  // Bullet points
  html = html.replace(/^[•\-\*]\s+(.*)$/gm, "<li>$1</li>");
  html = html.replace(/(<li>.*<\/li>)/s, "<ul>$1</ul>");
  // Line breaks
  html = html.replace(/\n\n/g, "</p><p>");
  html = html.replace(/\n/g, "<br>");
  return `<p>${html}</p>`;
}
