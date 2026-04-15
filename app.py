import streamlit as st
import google.generativeai as genai

# --- פונקציות עזר וטעינת CSS ---
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

# הגדרות דף
st.set_page_config(
    page_title="ConTroll - Anti-Troll Defense", 
    page_icon="logoCT.png", 
    layout="centered"
)

# טעינת העיצוב מקובץ ה-CSS
local_css("style.css")

# --- הגדרת AI ---
API_KEY = "AIzaSyC1JvhUdZZxelkH09dDLl6b8HaEQTqK89A" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# הגדרת הפרסונות
PERSONAS = {
    "The Savage (הציני)": "You are a witty, cynical Israeli expert. Destroy trolls with biting sarcasm. Keep it short.",
    "The Historian (הפרופסור)": "Expert in history. Correct lies with cold, hard facts about Israel's history.",
    "The Theological Glitch (התיאולוג)": "Expert in Islam. Use Islamic sources like Quran 5:21 to prove the land belongs to Jews."
}

# --- ממשק המשתמש (UI) לפי התבנית ---

# לוגו מרכזי
col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
with col_l2:
    st.image("logoCT.png", use_container_width=True)

# 1. בחירת פרסונה
st.markdown("<h2 style='text-align: center;'>בחירת פרסונה</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# שימוש ב-Session State כדי לנהל בחירה יחידה של פרסונה
if 'persona' not in st.session_state:
    st.session_state.persona = "The Savage (הציני)"

with col1:
    st.markdown('<div class="persona-card">דמות</div>', unsafe_allow_html=True)
    if st.button("The Savage\n(הציני)", use_container_width=True):
        st.session_state.persona = "The Savage (הציני)"

with col2:
    st.markdown('<div class="persona-card">דמות</div>', unsafe_allow_html=True)
    if st.button("The Historian\n(הפרופסור)", use_container_width=True):
        st.session_state.persona = "The Historian (הפרופסור)"

with col3:
    st.markdown('<div class="persona-card">דמות</div>', unsafe_allow_html=True)
    if st.button("The Theological Glitch\n(התיאולוג)", use_container_width=True):
        st.session_state.persona = "The Theological Glitch (התיאולוג)"

st.markdown(f"<p style='text-align: center; color: #2E35C2; font-weight: bold;'>נבחר: {st.session_state.persona}</p>", unsafe_allow_html=True)

# 2. רמת תגובה
st.markdown("<h2 style='text-align: center;'>רמת תגובה</h2>", unsafe_allow_html=True)
intensity = st.radio(
    "", 
    ["תהיה עדין", "תהיה נוקשה", "תהיה אטומי"], 
    horizontal=True, 
    label_visibility="collapsed"
)

# 3. תיבת קלט
st.markdown("<p style='text-align: right; margin-bottom: 5px;'>מה הטרול כתב?</p>", unsafe_allow_html=True)
troll_input = st.text_area(
    "", 
    placeholder="הדביקו כאן את התגובה המטופשת שלהם", 
    label_visibility="collapsed",
    height=100
)

st.write("") # רווח

# כפתור שליחה מרכזי
if st.button("שגר הגנה! 🚀", key="fire"):
    if troll_input:
        with st.spinner('מנתח את הטרול...'):
            try:
                system_instruction = PERSONAS[st.session_state.persona]
                full_prompt = (
                    f"System: {system_instruction}\n"
                    f"Intensity: {intensity}\n"
                    f"Troll wrote: {troll_input}\n\n"
                    f"Response (English/Hebrew):"
                )
                response = model.generate_content(full_prompt)
                
                st.markdown("---")
                st.markdown("### 🎯 התוצאה:")
                st.success(response.text)
            except Exception as e:
                st.error(f"שגיאה: {e}")
    else:
        st.warning("נא להזין טקסט לפני השיגור.")

# פוטר
st.markdown("<br><hr><p style='text-align: center; color: #2E35C2; font-weight: bold;'>AM YISRAEL CHAI 🇮🇱</p>", unsafe_allow_html=True)
