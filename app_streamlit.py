import streamlit as st
from teacher_bot import TeacherBot, BotConfig

st.set_page_config(page_title="TeacherBot (Multilingual)", page_icon="🎓", layout="centered")

st.title("🎓 TeacherBot — Multilingual, Teacher-Style Chatbot")
st.write("Understands your question and teaches back in the **same language** (English/Hindi/Telugu).")

with st.sidebar:
    st.header("Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.05)
    max_new_tokens = st.slider("Max new tokens", 64, 1024, 512, 32)
    top_p = st.slider("Top-p", 0.1, 1.0, 0.9, 0.05)
    st.caption("Backend auto-selects: OpenAI if API key is set, else local Transformers (Flan-T5).")

config = BotConfig(temperature=temperature, max_new_tokens=max_new_tokens, top_p=top_p)
bot = TeacherBot(config)

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_area("Ask me anything (try English/Hindi/తెలుగు):", height=120, placeholder="e.g., एंटीबायोटिक रेसिस्टेंस क्या है? / న్యూటన్ రెండవ నియమం ఏమిటి?")
go = st.button("Teach me")

if go and user_input.strip():
    resp = bot.answer(user_input)
    st.session_state.history.append({
        "user": user_input,
        "lang": resp["language"]["name"],
        "backend": resp["backend"],
        "answer": resp["answer"]
    })

for turn in st.session_state.history[::-1]:
    with st.container(border=True):
        st.markdown(f"**You** ({turn['lang']}): {turn['user']}")
        st.markdown(f"**TeacherBot** ({turn['backend']}):")
        st.write(turn["answer"])
