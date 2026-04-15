import streamlit as st
import google.generativeai as genai

# פונקציה לטעינת CSS מקובץ חיצוני
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.set_page_config(page_title="ConTroll - Anti-Troll Defense", page_icon="🛡️")

# טעינת הסטייל
try:
    local_css("style.css")
except:
    pass # למקרה שהקובץ עדיין לא עלה

# הגדרות עיצוב (Custom CSS) משופרות לנגישות וחווית משתמש
st.set_page_config(page_title="ConTroll - Anti-Troll Defense", page_icon="🛡️")

st.markdown(f"""
    <style>
    /* רקע כהה מאוד לניגודיות מקסימלית */
    .stApp {{
        background-color: #0B0E14;
    }}
    
    /* כותרת ראשית בטורקיז - לוגו */
    h1 {{
        color: #5BF0E0 !important;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
    }}
    
    /* טקסט לבן וקריא */
    .stMarkdown, p, label {{
        color: #FFFFFF !important;
    }}

    /* עיצוב כפתור - כחול עמוק עם טקסט לבן (נגישות גבוהה) */
    .stButton>button {{
        background-color: #2E35C2 !important;
        color: #FFFFFF !important;
        border-radius: 12px;
        border: 2px solid #5BF0E0;
        width: 100%;
        height: 3.5em;
        font-size: 1.1rem;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(46, 53, 194, 0.3);
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        background-color: #5BF0E0 !important;
        color: #0B0E14 !important; /* טקסט כהה על רקע בהיר ב-Hover */
        border: 2px solid #FFFFFF;
        transform: translateY(-2px);
    }}

    /* תיבות טקסט עם מסגרת עדינה */
    .stTextArea textarea {{
        background-color: #161B22 !important;
        color: #FFFFFF !important;
        border: 2px solid #2E35C2 !important;
        border-radius: 10px;
    }}
    
    /* התאמת צבעים לתיבת הבחירה */
    div[data-baseweb="select"] {{
        background-color: #161B22 !important;
        border-radius: 10px;
    }}

    /* עיצוב תיבת התוצאה */
    .stSuccess {{
        background-color: #161B22 !important;
        color: #5BF0E0 !important;
        border: 1px solid #5BF0E0 !important;
        border-right: 5px solid #5BF0E0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# כותרת
st.title("🛡️ ConTroll")
st.markdown("<p style='text-align: center; font-size: 1.2rem; opacity: 0.8;'>Anti-Troll Intelligence System</p>", unsafe_allow_html=True)

# API Setup
API_KEY = "AIzaSyC1JvhUdZZxelkH09dDLl6b8HaEQTqK89A" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Personas
PERSONAS = {
    "The Savage (הציני)": "Witty, cynical, biting sarcasm. Focus on economic/logical failure.",
    "The Historian (הפרופסור)": "Academic, factual, corrects lies about Israel's history.",
    "The Theological Glitch (התיאולוג)": "Uses Islamic sources to prove Jewish land rights."
}

# UI Layout
troll_input = st.text_area("הדבק את תגובת הטרול:", placeholder="What did they say?", height=120)

col1, col2 = st.columns(2)
with col1:
    persona_name = st.selectbox("בחר פרסונה:", list(PERSONAS.keys()))
with col2:
    intensity = st.select_slider("רמת חריפות:", options=["Low", "Medium", "Atomic"])

if st.button("NEUTRALIZE TROLL 🚀"):
    if troll_input:
        with st.spinner('Calculating laser trajectory...'):
            system_prompt = PERSONAS[persona_name]
            full_prompt = f"System: {system_prompt}\nIntensity: {intensity}\nTroll: {troll_input}\nResponse (English/Hebrew):"
            try:
                response = model.generate_content(full_prompt)
                st.markdown("### 🎯 Result:")
                st.success(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Input required.")

st.markdown("<br><hr><p style='text-align: center; color: #5BF0E0; font-weight: bold;'>AM YISRAEL CHAI 🇮🇱</p>", unsafe_allow_html=True)
