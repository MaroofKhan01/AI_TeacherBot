# TeacherBot (Multilingual, Teacher-Style Chatbot)

A simple AI-powered chatbot that:
- Understands input in multiple languages (tested with **English**, **Hindi**, **Telugu**).
- Responds **in the same language** as the input.
- Gives **teacher-like**, structured answers (definitions, explanations, examples).
- Offers a **CLI** and a **Streamlit web UI**.

> Backend options:
> 1) **OpenAI API** (recommended if you have a key)  
> 2) **Local Transformers** (no key needed; downloads a small model on first run)

---

## 🧩 Project Structure

```
.
├── app_streamlit.py      # Streamlit web UI
├── cli_chat.py           # Command-line interface
├── teacher_bot.py        # Core logic (language detect + response generation)
├── prompts.py            # Prompt template
├── requirements.txt      # Python deps
└── README.md             # This file
```

---

## ⚙️ Setup

### 1) Create a virtual environment (optional but recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) (Optional) Set OpenAI API key
If you want to use the OpenAI backend, set your key:
```bash
# Windows (Powershell)
$env:OPENAI_API_KEY="YOUR_KEY"
# macOS/Linux
export OPENAI_API_KEY="YOUR_KEY"
```

> If no key is set, the app falls back to a local Transformers model.

---

## ▶️ Run the Chatbot

### Option A: Streamlit Web App
```bash
streamlit run app_streamlit.py
```
Then open the local URL it prints (usually http://localhost:8501).

### Option B: CLI
```bash
python cli_chat.py
```

---

## 🌍 Supported Languages
- English (en)
- Hindi (hi)
- Telugu (te)

The bot auto-detects input language and replies in the same language. It *also* works with many other languages, but quality may vary with the local model.

---

## 🧠 How it Works (Short)
1. Detects the language using `langdetect`.
2. Crafts a **teacher-style** prompt (definition → explanation → examples).
3. Uses either:
   - **OpenAI** (if `OPENAI_API_KEY` is set), or
   - **Local Transformers** (`google/flan-t5-small`) as a fallback.
4. Ensures output is **structured** and **in the same language**.

---

## 🧪 Sample Prompts to Try
- English: "Explain photosynthesis to a 10-year-old."
- Hindi: "एंटीबायोटिक रेसिस्टेंस क्या है? उदाहरण दें।"
- Telugu: "న్యూటన్ రెండవ నియమాన్ని సులువుగా వివరించండి ఉదాహరణలతో."

---

## 🚀 Optional: Deploy
- **Streamlit Cloud**: Push to GitHub → “New app” → pick `app_streamlit.py`.
- **Railway/Render**: Standard Python web app; add `streamlit run app_streamlit.py` as the start command.

---

## 🙌 Notes
- First run with Transformers downloads a small model (~300MB). One-time.
- Outputs are non-deterministic; you can tweak temperature/max tokens in UI.
- If you want a bigger local model, switch from `flan-t5-small` to `flan-t5-base` in `teacher_bot.py`.

