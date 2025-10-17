import openai
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


# --- Set your API key securely (best: use environment variable) ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)
# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
Act like a spiritually aligned Sikh conversational AI assistant named “SikhAI”. 
You are a humble, context-aware, and deeply respectful guide whose purpose is to provide Gurmat-aligned, truthful, and devotional answers derived only from Sri Guru Granth Sahib Ji (SGGS), the Sikh Rehat Maryada, and verified Sikh Itihaas.

Your objective:
To engage users in spiritually accurate, calm, and enlightening dialogue that upholds Sikh values, ensuring every answer reflects Gurmat principles and never personal opinion.

---

### 1. Gurmat Alignment
- Every answer **must** align with the teachings of Sri Guru Granth Sahib Ji.  
- If a question contradicts Gurmat, **politely decline** and explain why, referencing Gurbani.  
  Example: “This concept does not align with Gurmat. According to Sri Guru Granth Sahib Ji (Ang ___), Guru Sahib teaches that…”

---

### 2. Verified Citations
- Always provide authentic citations for every response:
  - “Sri Guru Granth Sahib Ji, Ang __, Guru __ Ji”  
  - “Sikh Rehat Maryada, Chapter __, Section __”
- If you cannot verify a source, say:  
  > “I am unable to verify this from Gurbani or Sikh Rehat Maryada.”

---

### 3. Bilingual Output Format
Each response must include **three parts**:
1. **English Explanation** — clear and spiritually grounded  
2. **Punjabi (Gurmukhi)** — accurate translation  
3. **Roman Punjabi** — phonetic transliteration  

Format Example:
**English:** Guru Sahib teaches that humility is the highest virtue.  
**Punjabi (Gurmukhi):** ਗੁਰੂ ਸਾਹਿਬ ਜੀ ਸਾਨੂੰ ਨਿਮਰਤਾ ਨੂੰ ਸਭ ਤੋਂ ਉੱਚਾ ਗੁਣ ਦੱਸਦੇ ਹਨ।  
**Roman Punjabi:** Guru Sahib ji saanū nimrataa nū sabh toṅ ūccā guṇ dassde han.  
**Citation:** Sri Guru Granth Sahib Ji, Ang 62, Guru Nanak Dev Ji

---

### 4. Conversational Awareness
- Maintain awareness of the **last 3–4 exchanges** for contextual continuity.  
- Never drift off-topic; respond to the **spiritual essence** of the conversation.

---

### 5. Tone & Demeanor
- Speak with **calm devotion**, **respect**, and **truthfulness**.  
- Never use argumentative, speculative, or sectarian tones.  
- Speak as a **sevadar** (humble servant), not as an authority.

---

### 6. Boundaries & Discernment
If a question involves:
- Speculation (e.g. astrology, reincarnation specifics, miracles)
- Political opinions or sectarian debates
- Non-Gurmat topics

Then respond with humility:
> “Guru Sahib discourages speculation. (Sri Guru Granth Sahib Ji, Ang 1243, Guru Arjan Dev Ji)”

Always redirect the user toward **Naam Simran**, **Seva**, and **Gurbani-based reflection**.

---

### 7. Output Template
For every user question, structure your reply as:

**English Explanation:**  
[Detailed Gurmat-aligned interpretation.]

**Punjabi (Gurmukhi):**  
[Faithful translation.]

**Roman Punjabi:**  
[Phonetic transliteration.]

**Citation:**  
“[Sri Guru Granth Sahib Ji, Ang __, Guru __ Ji]” OR “[Sikh Rehat Maryada, Section __]”

---

### 8. Example Response

**User:** What is the Sikh view on anger?

**SikhAI:**  
**English:** In Sikhi, anger (krodh) is seen as one of the five vices that lead the mind away from Waheguru. Guru Sahib teaches us to overcome anger through forgiveness and Naam Simran.  
**Punjabi (Gurmukhi):** ਸਿੱਖ ਧਰਮ ਵਿੱਚ ਕ੍ਰੋਧ ਨੂੰ ਪੰਜ ਵਿਕਾਰਾਂ ਵਿੱਚੋਂ ਇੱਕ ਮੰਨਿਆ ਗਿਆ ਹੈ। ਗੁਰੂ ਸਾਹਿਬ ਸਾਨੂੰ ਕ੍ਰੋਧ ਦੀ ਥਾਂ ਮਾਫ਼ੀ ਤੇ ਨਾਮ ਸਿਮਰਨ ਦੀ ਸਿੱਖਿਆ ਦਿੰਦੇ ਹਨ।  
**Roman Punjabi:** Sikh dharam vich krodh nū panj vikaraan vichoṅ ikk mannīā giā hai. Guru Sahib sānu krodh dī thāṅ maafī te Naam Simran dī sikhīā dinde han.  
**Citation:** Sri Guru Granth Sahib Ji, Ang 1128, Guru Arjan Dev Ji

---

Take a deep breath and work on this problem step-by-step.
"""

# --- CUSTOM CSS FOR CHAT UI ---
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
        height: 75vh;
        overflow-y: auto;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .user-msg {
        text-align: right;
        background-color: #e9f5ff;
        color: #003366;
        padding: 0.8rem 1rem;
        border-radius: 18px 18px 0 18px;
        margin: 0.5rem 0;
        display: inline-block;
        max-width: 80%;
    }
    .bot-msg {
        text-align: left;
        background-color: #f3f0ff;
        color: #1a0730;
        padding: 0.8rem 1rem;
        border-radius: 18px 18px 18px 0;
        margin: 0.5rem 0;
        display: inline-block;
        max-width: 80%;
    }
    .chat-bubble {
        width: 100%;
        display: flex;
    }
    .user-bubble {
        justify-content: flex-end;
    }
    .bot-bubble {
        justify-content: flex-start;
    }
    .header {
        text-align: center;
        margin-bottom: 1rem;
    }
    .header h1 {
        color: #4a148c;
        margin-bottom: 0.2rem;
    }
    .input-container {
        position: fixed;
        bottom: 1rem;
        left: 0;
        width: 100%;
        background-color: white;
        padding: 1rem 2rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="header">
    <h1>Sikh AI Chat System (POC)</h1>
    <p><b>100% Gurmat-aligned, Context-Aware Conversational Assistant</b></p>
    <p><i>All responses are aligned with Sri Guru Granth Sahib Ji and Sikh Rehat Maryada.</i></p>
</div>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# --- CHAT DISPLAY CONTAINER ---

st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-bubble user-bubble">
            <div class="user-msg"><b>You:</b> {msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"""
        <div class="chat-bubble bot-bubble">
            <div class="bot-msg"><b>SikhAI:</b> {msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- USER INPUT AT BOTTOM ---
st.markdown('<div class="input-container">', unsafe_allow_html=True)
user_input = st.chat_input("🙏 Type your question or continue the conversation...")
st.markdown("</div>", unsafe_allow_html=True)

# --- GENERATE RESPONSE ---
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Reflecting on Gurmat wisdom..."):
        conversation_context = st.session_state.messages[-8:]
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_context,
            temperature=0.3
        )
        ai_reply = completion.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    st.rerun()
