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

# --- ניהול מצב (Session State) ---
if 'lang' not in st.session_state:
    st.session_state.lang = 'Hebrew'
if 'history' not in st.session_state:
    st.session_state.history = []
if 'persona' not in st.session_state:
    st.session_state.persona = "The Savage (הציני)"

# --- מילון תרגומים ---
translations = {
    'Hebrew': {
        'dir': 'rtl', 'align': 'right',
        'select_persona': 'בחירת פרסונה',
        'response_level': 'רמת תגובה',
        'mild': 'עדין', 'spicy': 'חריף', 'atomic': 'אטומי',
        'target_lang': 'שפת התגובה המבוקשת',
        'context_label': 'קונטקסט (איך זה התחיל?)',
        'context_ph': 'למשל: ויכוח על המצור ב-X',
        'link_label': 'קישור לפוסט (Facebook, X, Instagram...)',
        'link_ph': 'הדביקו כאן את הלינק לפוסט',
        'troll_label': 'מה הטרול כתב?',
        'troll_ph': 'הדביקו כאן את התגובה...',
        'upload_label': 'העלה צילום מסך (אופציונלי)',
        'fire_btn': 'שגר הגנה! 🚀',
        'history_title': 'הטרלות אחרונות',
        'chosen_label': 'נבחר:',
        'analyzing': 'מנתח ומייצר תגובה...',
        'input_error': 'נא להזין את תגובת הטרול.',
        'result_title': '🎯 התוצאה:',
        'copy_tip': '💡 העתק את הטקסט למעלה והדבק אותו בתגובה.'
    },
    'English': {
        'dir': 'ltr', 'align': 'left',
        'select_persona': 'Select Persona',
        'response_level': 'Response Level',
        'mild': 'Mild', 'spicy': 'Spicy', 'atomic': 'Atomic',
        'target_lang': 'Target Response Language',
        'context_label': 'Context (How did it start?)',
        'context_ph': 'e.g., Argument about the blockade on X',
        'link_label': 'Link to post (Facebook, X, Instagram...)',
        'link_ph': 'Paste the URL here',
        'troll_label': 'What did the troll write?',
        'troll_ph': 'Paste the comment here...',
        'upload_label': 'Upload screenshot (Optional)',
        'fire_btn': 'FIRE DEFENSE! 🚀',
        'history_title': 'Recent ConTrolls',
        'chosen_label': 'Selected:',
        'analyzing': 'Analyzing and generating...',
        'input_error': 'Please enter the troll\'s text.',
        'result_title': '🎯 Result:',
        'copy_tip': '💡 Copy the text above and paste it.'
    }
}

# בורר שפת ממשק
col_lang_1, col_lang_2 = st.columns([4, 1])
with col_lang_2:
    st.session_state.lang = st.selectbox(
        "UI Lang", ["Hebrew", "English"], 
        index=0 if st.session_state.lang == 'Hebrew' else 1,
        label_visibility="collapsed"
    )

t = translations[st.session_state.lang]

# הזרקת CSS לכיווניות
st.markdown(f"""
    <style>
    textarea, input {{ direction: {t['dir']} !important; text-align: {t['align']} !important; }}
    .stMarkdown p {{ text-align: {t['align']} !important; direction: {t['dir']} !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- הגדרת AI (תיקון גרסה ידני למניעת 404) ---
API_KEY = "AIzaSyC1JvhUdZZxelkH09dDLl6b8HaEQTqK89A"
genai.configure(api_key=API_KEY)

# יצירת המודל עם שם מפורש
model = genai.GenerativeModel('gemini-1.5-flash')

PERSONAS = {
    "The Savage (הציני)": "Witty, cynical, biting sarcasm. Focus on logic or national failure.",
    "The Historian (הפרופסור)": "Academic, factual, corrects lies with historical dates/facts.",
    "The Theological Glitch (התיאולוג)": "Expert in Islam. Uses Quranic verses like 5:21 to prove Jewish rights."
}

# --- ממשק המשתמש ---
st.image("logoCT.png", width=180)

# 1. פרסונה
st.markdown(f"<h2 style='text-align: center;'>{t['select_persona']}</h2>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="persona-card">Savage</div>', unsafe_allow_html=True)
    if st.button("The Savage", use_container_width=True): st.session_state.persona = "The Savage (הציני)"
with c2:
    st.markdown('<div class="persona-card">Historian</div>', unsafe_allow_html=True)
    if st.button("The Historian", use_container_width=True): st.session_state.persona = "The Historian (הפרופסור)"
with c3:
    st.markdown('<div class="persona-card">Theology</div>', unsafe_allow_html=True)
    if st.button("The Theology", use_container_width=True): st.session_state.persona = "The Theological Glitch (התיאולוג)"

st.markdown(f"<p style='text-align: center; color: #2E35C2;'>{t['chosen_label']} <b>{st.session_state.persona}</b></p>", unsafe_allow_html=True)

# 2. רמה
st.markdown(f"<h2 style='text-align: center;'>{t['response_level']}</h2>", unsafe_allow_html=True)
intensity_labels = [t['mild'], t['spicy'], t['atomic']]
intensity = st.radio("intensity", intensity_labels, horizontal=True, label_visibility="collapsed")

# 3. קונטקסט, לינק ותוכן
st.markdown("---")
st.markdown(f"<p style='text-align: {t['align']}; font-weight: bold;'>{t['context_label']}</p>", unsafe_allow_html=True)
context_input = st.text_input("ctx", placeholder=t['context_ph'], label_visibility="collapsed")

st.markdown(f"<p style='text-align: {t['align']}; font-weight: bold;'>{t['link_label']}</p>", unsafe_allow_html=True)
post_link = st.text_input("link", placeholder=t['link_ph'], label_visibility="collapsed")

st.markdown(f"<p style='text-align: {t['align']}; font-weight: bold;'>{t['troll_label']}</p>", unsafe_allow_html=True)
troll_input = st.text_area("troll", placeholder=t['troll_ph'], label_visibility="collapsed", height=100)

uploaded_file = st.file_uploader(t['upload_label'], type=['png', 'jpg', 'jpeg'])

# 4. שפת תגובה
st.markdown(f"<p style='text-align: center; margin-top:20px; font-weight: bold;'>{t['target_lang']}</p>", unsafe_allow_html=True)
target_lang = st.radio("target_lang", ["Hebrew", "English", "Arabic", "Russian"], horizontal=True, label_visibility="collapsed")

st.write("") 

if st.button(t['fire_btn'], key="fire"):
    if troll_input:
        with st.spinner(t['analyzing']):
            try:
                # בניית הפרומפט
                prompt = (
                    f"Instruction: {PERSONAS[st.session_state.persona]}. "
                    f"Intensity: {intensity}. Context: {context_input}. "
                    f"Troll text: {troll_input}. "
                    f"Target Language: {target_lang}."
                )
                
                # תמיכה בתמונה
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([prompt, img])
                else:
                    response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(f"### {t['result_title']}")
                st.success(response.text)
                st.session_state.history.insert(0, {"troll": troll_input, "response": response.text, "lang": target_lang})
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning(t['input_error'])

# 5. ארכיון
if st.session_state.history:
    st.markdown("---")
    st.markdown(f"<h2 style='text-align: center;'>{t['history_title']}</h2>", unsafe_allow_html=True)
    for i, item in enumerate(st.session_state.history[:5]):
        with st.expander(f"Log {i+1} ({item['lang']}): {item['troll'][:30]}..."):
            st.write(item['response'])

st.markdown("<br><p style='text-align: center; color: #2E35C2;'>AM YISRAEL CHAI 🇮🇱</p>", unsafe_allow_html=True)
