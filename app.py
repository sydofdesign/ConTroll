import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="ConTroll", page_icon="logoCT.png", layout="centered")

# פונקציית טעינת CSS
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except: pass

local_css("style.css")

# אתחול
if 'lang' not in st.session_state: st.session_state.lang = 'Hebrew'
if 'persona' not in st.session_state: st.session_state.persona = "The Savage"

# הגדרת AI
API_KEY = "AIzaSyC1JvhUdZZxelkH09dDLl6b8HaEQTqK89A"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# תרגומים
t = {
    'persona_h': 'בחירת פרסונה',
    'level_h': 'רמת תגובה',
    'context_label': 'קונטקסט (איך זה התחיל?)',
    'context_ph': 'למשל: ויכוח על...',
    'link_label': 'קישור לפוסט (...Facebook, X)',
    'link_ph': 'הדביקו לינק כאן',
    'file_label': 'יש לכם צילום מסך? עלו לכאן',
    'troll_label': 'מה הטרול כתב?',
    'troll_ph': 'הדביקו כאן את התגובה שלהם',
    'target_lang': 'שפת התגובה המבוקשת',
    'fire_btn': 'צור תגובה 🪄',
    'levels': ["תהיה עדין", "תהיה נוקשה", "תהיה אטומי", "תהיה ציני", "תהיה רציני"],
    'langs': ["English", "עברית", "ערבית", "הולנדית", "רוסית"]
}

# שפה ולוגו
st.selectbox("", ["Hebrew", "English"], key='lang_select', label_visibility="collapsed")
st.markdown('<div class="center-img">', unsafe_allow_html=True)
st.image("logoCT.png", width=120)
st.markdown('</div>', unsafe_allow_html=True)

# 1. פרסונות
st.markdown(f"## {t['persona_h']}")
personas = [
    {"id": "The Historian", "name": "הפרופסור"},
    {"id": "The Proud Zionist", "name": "הציוני על מלא"},
    {"id": "The Theological Glitch", "name": "התיאולוג"},
    {"id": "The Savage", "name": "הציני והעוקצני"},
    {"id": "The Nazi Hunter", "name": "צייד הנאצים"},
    {"id": "The Mirror Troll", "name": "הטרול הנגדי"}
]

cols = st.columns(6)
for i, p in enumerate(personas):
    with cols[i]:
        is_active = "active-circle" if st.session_state.persona == p['id'] else "p-circle"
        st.markdown(f'<div class="{is_active}">דמות</div>', unsafe_allow_html=True)
        if st.button(p['name'], key=p['id']):
            st.session_state.persona = p['id']
            st.rerun()

# 2. רמת תגובה
st.markdown(f"## {t['level_h']}")
level = st.radio("", t['levels'], horizontal=True, label_visibility="collapsed")

# 3. קלטים
st.markdown(f"**{t['context_label']}**")
context = st.text_input("ctx", placeholder=t['context_ph'], label_visibility="collapsed")

st.markdown(f"**{t['link_label']}**")
link = st.text_input("link", placeholder=t['link_ph'], label_visibility="collapsed")

st.markdown(f"**{t['file_label']}**")
uploaded_file = st.file_uploader("file", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

st.markdown(f"**{t['troll_label']}**")
troll_text = st.text_area("troll", placeholder=t['troll_ph'], label_visibility="collapsed")

# 4. שפה וכפתור
st.markdown(f"<p style='text-align:center'><b>{t['target_lang']}</b></p>", unsafe_allow_html=True)
target_lang = st.radio("lang", t['langs'], horizontal=True, label_visibility="collapsed")

if st.button(t['fire_btn'], use_container_width=True):
    if troll_text:
        with st.spinner("מייצר..."):
            try:
                res = model.generate_content(f"Persona {st.session_state.persona}, Tone {level}: {troll_text}")
                st.success(res.text)
            except Exception as e: st.error(str(e))
