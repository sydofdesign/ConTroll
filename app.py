import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- פונקציות עזר וטעינת CSS ---
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

# הגדרות דף
st.set_page_config(page_title="ConTroll", page_icon="logoCT.png", layout="centered")
local_css("style.css")

# אתחול היסטוריה ב-Session State
if 'history' not in st.session_state:
    st.session_state.history = []
if 'persona' not in st.session_state:
    st.session_state.persona = "The Savage (הציני)"

# --- הגדרת AI ---
API_KEY = "AIzaSyC1JvhUdZZxelkH09dDLl6b8HaEQTqK89A" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- ממשק המשתמש ---

# לוגו
st.image("logoCT.png", width=180)

# 1. בחירת פרסונה
st.markdown("<h2 style='text-align: center;'>בחירת פרסונה</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

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

st.markdown(f"<p style='text-align: center; color: #2E35C2;'>נבחר: <b>{st.session_state.persona}</b></p>", unsafe_allow_html=True)

# 2. רמת תגובה
st.markdown("<h2 style='text-align: center;'>רמת תגובה</h2>", unsafe_allow_html=True)
intensity = st.radio("", ["תהיה עדין", "תהיה נוקשה", "תהיה אטומי"], horizontal=True, label_visibility="collapsed")

# 3. קונטקסט ותוכן (הפיצ'ר החדש)
st.markdown("---")
st.markdown("<p style='text-align: right; font-weight: bold;'>קונטקסט (איך זה התחיל / על מה הוויכוח?)</p>", unsafe_allow_html=True)
context_input = st.text_input("", placeholder="למשל: ויכוח על המצור ב-X", label_visibility="collapsed")

st.markdown("<p style='text-align: right; font-weight: bold;'>מה הטרול כתב?</p>", unsafe_allow_html=True)
troll_input = st.text_area("", placeholder="הדביקו כאן את התגובה...", label_visibility="collapsed", height=100)

uploaded_file = st.file_uploader("העלה צילום מסך של הוויכוח (אופציונלי)", type=['png', 'jpg', 'jpeg'])

# כפתור שיגור
if st.button("שגר הגנה! 🚀", key="fire"):
    if troll_input:
        with st.spinner('מכין תשובה קטלנית...'):
            try:
                # בניית הפרומפט עם הקונטקסט
                prompt_content = [f"Persona: {st.session_state.persona}, Intensity: {intensity}, Context: {context_input}, Troll text: {troll_input}. Write a response:"]
                
                # אם הועלתה תמונה, ה-AI ינתח אותה
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    prompt_content.append(img)
                
                response = model.generate_content(prompt_content)
                final_text = response.text
                
                # הצגת התוצאה
                st.markdown("### 🎯 התוצאה:")
                st.success(final_text)
                
                # שמירה להיסטוריה
                st.session_state.history.insert(0, {"troll": troll_input, "response": final_text})
                
            except Exception as e:
                st.error(f"שגיאה: {e}")
    else:
        st.warning("נא להזין את תגובת הטרול.")

# 4. ארכיון הטרלות (הפיצ'ר החדש)
if st.session_state.history:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>הטרלות אחרונות</h2>", unsafe_allow_html=True)
    for i, item in enumerate(st.session_state.history[:5]): # מציג 5 אחרונות
        with st.expander(f"הטרלה {i+1}: {item['troll'][:30]}..."):
            st.write(f"**הטרול כתב:** {item['troll']}")
            st.write(f"**ConTroll ענה:** {item['response']}")

# פוטר
st.markdown("<br><p style='text-align: center; color: #2E35C2;'>AM YISRAEL CHAI 🇮🇱</p>", unsafe_allow_html=True)
