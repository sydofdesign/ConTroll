import streamlit as st
import google.generativeai as genai
from PIL import Image

# הגדרות דף
st.set_page_config(page_title="ConTroll", page_icon="logoCT.png", layout="centered")

# טעינת CSS
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass

local_css("style.css")

# אתחול Session State
if 'lang' not in st.session_state: st.session_state.lang = 'Hebrew'
if 'persona' not in st.session_state: st.session_state.persona = "The Savage"

# הגדרת AI (תיקון 404 סופי)
API_KEY = "AIzaSyC1JvhUdZZxelkH09dDLl6b8HaEQTqK89A"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# מילון תרגומים
translations = {
    'Hebrew': {
        'dir': 'rtl', 'align': 'right',
        'persona_h': 'בחירת פרסונה',
        'level_h': 'רמת תגובה',
        'context_label': 'קונטקסט (איך זה התחיל?)',
        'context_ph': 'למשל: ויכוח על ... / סרטון על ...',
        'link_label': 'קישור לפוסט (... Facebook, X, Instagram)',
        'link_ph': 'קישור לפוסט יעזור להבנת הקונטקסט טוב יותר',
        'file_label': 'יש לכם צילום מסך? עלו לכאן זה יעזור להבנת הסיטואציה',
        'troll_label': 'מה הטרול כתב?',
        'troll_ph': 'הדביקו כאן את התגובה המטופשת שלהם',
        'target_lang': 'שפת התגובה המבוקשת',
        'fire_btn': 'צור תגובה 🪄',
        'levels': ["תהיה עדין", "תהיה נוקשה", "תהיה אטומי", "תהיה ציני", "תהיה רציני"],
        'langs': ["English", "עברית", "ערבית", "הולנדית", "רוסית"]
    },
    'English': {
        'dir': 'ltr', 'align': 'left',
        'persona_h': 'Select Persona',
        'level_h': 'Response Level',
        'context_label': 'Context (How did it start?)',
        'context_ph': 'e.g., Argument about...',
        'link_label': 'Link to post...',
        'link_ph': 'Link will help...',
        'file_label': 'Have a screenshot? Upload here',
        'troll_label': 'What did the troll write?',
        'troll_ph': 'Paste response here',
        'target_lang': 'Target Language',
        'fire_btn': 'Generate Response 🪄',
        'levels': ["Be Mild", "Be Tough", "Be Atomic", "Be Savage", "Be Serious"],
        'langs': ["English", "Hebrew", "Arabic", "Dutch", "Russian"]
    }
}

t = translations[st.session_state.lang]

# בחירת שפה - בראש הדף
col_s1, col_s2 = st.columns([5,1])
with col_s2:
    st.session_state.lang = st.selectbox("", ["Hebrew", "English"], label_visibility="collapsed")

# לוגו
st.image("logoCT.png", width=150)

# --- 1. בחירת פרסונה (Carousel) ---
st.markdown(f"<h2 style='text-align: center;'>{t['persona_h']}</h2>", unsafe_allow_html=True)

personas = [
    {"id": "The Historian", "name": "הפרופסור", "desc": "הסבר על הפרסונה"},
    {"id": "The Proud Zionist", "name": "הציוני על מלא", "desc": "הסבר על הפרסונה"},
    {"id": "The Theological Glitch", "name": "התיאולוג", "desc": "הסבר על הפרסונה"},
    {"id": "The Savage", "name": "הציני והעוקצני", "desc": "הסבר על הפרסונה"},
    {"id": "The Nazi Hunter", "name": "צייד הנאצים", "desc": "הסבר על הפרסונה"},
    {"id": "The Mirror Troll", "name": "הטרול הנגדי", "desc": "הסבר על הפרסונה"}
]

# יצירת הקרוסלה ב-HTML/CSS בצורה שלא תשבר
persona_html = '<div class="persona-scroll-container">'
for p in personas:
    is_active = "active-circle" if st.session_state.persona == p['id'] else "inactive-circle"
    persona_html += f'''
    <div class="persona-item">
        <div class="circle-box {is_active}">דמות</div>
        <div class="persona-name">{p['name']}</div>
        <div class="persona-desc">{p['desc']}</div>
    </div>
    '''
persona_html += '</div>'
st.markdown(persona_html, unsafe_allow_html=True)

# בחירת פרסונה מאחורי הקלעים
selected_p = st.selectbox("p_hidden", [p['id'] for p in personas], label_visibility="collapsed")
st.session_state.persona = selected_p

# --- 2. רמת תגובה ---
st.markdown(f"<h2 style='text-align: center;'>{t['level_h']}</h2>", unsafe_allow_html=True)
level = st.radio("level", t['levels'], horizontal=True, label_visibility="collapsed")

# --- 3. שדות קלט ---
st.markdown(f"<p class='input-label'>{t['context_label']}</p>", unsafe_allow_html=True)
context = st.text_input("ctx", placeholder=t['context_ph'], label_visibility="collapsed")

st.markdown(f"<p class='input-label'>{t['link_label']}</p>", unsafe_allow_html=True)
link = st.text_input("link", placeholder=t['link_ph'], label_visibility="collapsed")

st.markdown(f"<p class='input-label'>{t['file_label']}</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("file", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

st.markdown(f"<p class='input-label'>{t['troll_label']}</p>", unsafe_allow_html=True)
troll_text = st.text_area("troll", placeholder=t['troll_ph'], label_visibility="collapsed")

# --- 4. שפת תגובה ---
st.markdown(f"<p style='text-align: center; font-weight: bold;'>{t['target_lang']}</p>", unsafe_allow_html=True)
target_lang = st.radio("lang", t['langs'], horizontal=True, label_visibility="collapsed")

# --- 5. כפתור שיגור ---
if st.button(t['fire_btn'], use_container_width=True):
    if troll_text:
        with st.spinner("Processing..."):
            try:
                prompt = f"Act as {st.session_state.persona}. Tone: {level}. Lang: {target_lang}. Troll text: {troll_text}."
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([prompt, img])
                else:
                    response = model.generate_content(prompt)
                st.success(response.text)
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("<br><p style='text-align: center; opacity: 0.5;'>AM YISRAEL CHAI IL</p>", unsafe_allow_html=True)
