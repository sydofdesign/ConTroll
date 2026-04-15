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

# אתחול Session State
if 'history' not in st.session_state:
    st.session_state.history = []
if 'lang' not in st.session_state:
    st.session_state.lang = 'Hebrew'
if 'persona' not in st.session_state:
    st.session_state.persona = "The Savage (הציני)"

# --- מילון תרגומים ---
translations = {
    'Hebrew': {
        'dir': 'rtl',
        'align': 'right',
        'select_persona': 'בחירת פרסונה',
        'response_level': 'רמת תגובה',
        'context_label': 'קונטקסט (איך זה התחיל / על מה הוויכוח?)',
        'context_ph': 'למשל: ויכוח על המצור ב-X',
        'troll_label': 'מה הטרול כתב?',
        'troll_ph': 'הדביקו כאן את התגובה המטופשת שלהם',
        'upload_label': 'העלה צילום מסך של הוויכוח (אופציונלי)',
        'fire_btn': 'שגר הגנה! 🚀',
        'history_title': 'הטרלות אחרונות',
        'chosen_label': 'נבחר:',
        'analyzing': 'מנתח את הטרול...',
        'input_error': 'נא להזין את תגובת הטרול.',
        'result_title': '🎯 התוצאה:',
        'copy_tip': '💡 העתק את הטקסט למעלה והדבק אותו בתגובה.'
    },
    'English': {
        'dir': 'ltr',
        'align': 'left',
        'select_persona': 'Select Persona',
        'response_level': 'Response Level',
        'context_label': 'Context (How did it start?)',
        'context_ph': 'e.g., Argument about the blockade on X',
        'troll_label': 'What did the troll write?',
        'troll_ph': 'Paste their stupid comment here...',
        'upload_label': 'Upload a screenshot (Optional)',
        'fire_btn': 'FIRE DEFENSE! 🚀',
        'history_title': 'Recent ConTrolls',
        'chosen_label': 'Selected:',
        'analyzing': 'Analyzing troll...',
        'input_error': 'Please enter the troll\'s text.',
        'result_title': '🎯 Result:',
        'copy_tip': '💡 Copy the text above and paste it back.'
    }
}

t = translations[st.session_state.lang]

# --- הגדרת AI ---
API_KEY = "AIzaSyC1JvhUdZZxelkH09dDLl6b8HaEQTqK89A" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# הגדרת הפרסונות
PERSONAS = {
    "The Savage (הציני)": "You are a witty, cynical Israeli expert. Destroy trolls with biting sarcasm.",
    "The Historian (הפרופסור)": "Expert in history. Correct lies with cold, hard facts about Israel.",
    "The Theological Glitch (התיאולוג)": "Expert in Islam. Use Islamic sources to prove Jewish land rights."
}

# --- ממשק המשתמש ---

# בורר שפה (Language Switcher)
col_lang_1, col_lang_2 = st.columns([4, 1])
with col_lang_2:
    st.session_state.lang = st.selectbox("", ["Hebrew", "English"], label_visibility="collapsed")

# לוגו
st.image("logoCT.png", width=180)

# 1. בחירת פרסונה
st.markdown(f"<h2 style='text-align: center;'>{t['select_persona']}</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="persona-card">Image</div>', unsafe_allow_html=True)
    if st.button("The Savage", use_container_width=True):
        st.session_state.persona = "The Savage (הציני)"
with col2:
    st.markdown('<div class="persona-card">Image</div>', unsafe_allow_html=True)
    if st.button("The Historian", use_container_width=True):
        st.session_state.persona = "The Historian (הפרופסור)"
with col3:
    st.markdown('<div class="persona-card">Image</div>', unsafe_allow_html=True)
    if st.button("The Theology", use_container_width=True):
        st.session_state.persona = "The Theological Glitch (התיאולוג)"

st.markdown(f"<p style='text-align: center; color: #2E35C2;'>{t['chosen_label']} <b>{st.session_state.persona}</b></p>", unsafe_allow_html=True)

# 2. רמת תגובה
st.markdown(f"<h2 style='text-align: center;'>{t['response_level']}</h2>", unsafe_allow_html=True)
intensity = st.radio("", ["Mild", "Spicy", "Atomic"], horizontal=True, label_visibility="collapsed")

# 3. קונטקסט ותוכן
st.markdown("---")
st.markdown(f"<p style='text-align: {t['align']}; font-weight: bold;'>{t['context_label']}</p>", unsafe_allow_html=True)
context_input = st.text_input("", placeholder=t['context_ph'], label_visibility="collapsed")

st.markdown(f"<p style='text-align: {t['align']}; font-weight: bold;'>{t['troll_label']}</p>", unsafe_allow_html=True)
troll_input = st.text_area("", placeholder=t['troll_ph'], label_visibility="collapsed", height=100)

uploaded_file = st.file_uploader(t['upload_label'], type=['png', 'jpg', 'jpeg'])

# שליטה על כיווניות התיבה דרך CSS דינמי
st.markdown(f"<style>textarea, input {{ direction: {t['dir']}; text-align: {t['align']}; }}</style>", unsafe_allow_html=True)

# כפתור שיגור
if st.button(t['fire_btn'], key="fire"):
    if troll_input:
        with st.spinner(t['analyzing']):
            try:
                prompt_content = [f"Persona: {st.session_state.persona}, Intensity: {intensity}, Context: {context_input}, Troll text: {troll_input}. Generate response in {st.session_state.lang}:"]
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    prompt_content.append(img)
                
                response = model.generate_content(prompt_content)
                final_text = response.text
                
                st.markdown("---")
                st.markdown(f"### {t['result_title']}")
                st.success(final_text)
                st.info(t['copy_tip'])
                st.session_state.history.insert(0, {"troll": troll_input, "response": final_text})
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning(t['input_error'])

# 4. ארכיון
if st.session_state.history:
    st.markdown("---")
    st.markdown(f"<h2 style='text-align: center;'>{t['history_title']}</h2>", unsafe_allow_html=True)
    for i, item in enumerate(st.session_state.history[:5]):
        with st.expander(f"Log {i+1}: {item['troll'][:30]}..."):
            st.write(item['response'])

st.markdown("<br><p style='text-align: center; color: #2E35C2;'>AM YISRAEL CHAI 🇮🇱</p>", unsafe_allow_html=True)
