import streamlit as st
import google.generativeai as genai

# --- פונקציות עזר ---

def local_css(file_name):
    """טעינת קובץ CSS חיצוני"""
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

# --- הגדרות דף ---
st.set_page_config(
    page_title="ConTroll - Anti-Troll Defense", 
    page_icon="logo.png", # האייקון בלשונית יהיה הלוגו שלך
    layout="centered"
)

# טעינת העיצוב (Light Mode שקידדנו ב-style.css)
local_css("style.css")

# --- הגדרת AI ---
# מפתח ה-API שלך
API_KEY = "AIzaSyC1JvhUdZZxelkH09dDLl6b8HaEQTqK89A" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # שימוש במודל עדכני ומהיר

# --- הגדרת הפרסונות ---
PERSONAS = {
    "The Savage (הציני האכזרי)": "You are a witty, cynical Israeli expert. Your goal is to destroy internet trolls with short, biting, and sarcastic comebacks. Focus on their lack of logic, economic failures, or personal obsession. Be extremely insulting but don't use forbidden curse words.",
    "The Historian (הפרופסור)": "You are an expert in history and geopolitics. Correct historical lies with cold, hard facts. Use terms like 'Indigenous' and mention that there was never a sovereign Palestinian state. Tone: academic, superior, and condescending.",
    "The Theological Glitch (התיאולוג)": "You are an expert in Islam. When a Muslim troll attacks Israel, use quotes from Islamic sources (like Surah 5:21) to prove the land belongs to Jews according to the Quran. Make them feel like they don't know their own religion."
}

# --- ממשק המשתמש (UI) ---

# הצגת הלוגו במרכז
col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 2, 1])
with col_logo_2:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.title("🛡️ ConTroll") # גיבוי למקרה שהקובץ לא נטען

st.markdown("<h3 style='text-align: center;'>Neutralize trolls with intelligence</h3>", unsafe_allow_html=True)

# תיבת קלט
troll_input = st.text_area(
    "מה הטרול כתב?", 
    placeholder="הדבק כאן את הטקסט המטופש שלהם...",
    height=150
)

# בחירת פרסונה ורמת חריפות בשורה אחת
col1, col2 = st.columns(2)
with col1:
    persona_name = st.selectbox("בחר כלי נשק:", list(PERSONAS.keys()))
with col2:
    intensity = st.select_slider(
        "רמת חריפות:", 
        options=["Low", "Medium", "Atomic"]
    )

st.write("") # רווח

# כפתור ההפעלה
if st.button("NEUTRALIZE TROLL 🚀"):
    if troll_input:
        with st.spinner('Calculating high-precision burn...'):
            try:
                # הכנת הפרומפט ל-AI
                system_instruction = PERSONAS[persona_name]
                full_prompt = (
                    f"System Instruction: {system_instruction}\n"
                    f"Intensity Level: {intensity}\n"
                    f"Troll's Comment: {troll_input}\n\n"
                    f"Response (English/Hebrew):"
                )
                
                # יצירת התשובה
                response = model.generate_content(full_prompt)
                
                # הצגת התוצאה
                st.markdown("---")
                st.markdown("### 🎯 ConTroll Result:")
                st.success(response.text)
                
                # טיפ למשתמש
                st.info("💡 העתק את הטקסט למעלה והדבק אותו בתגובה לטרול.")
                
            except Exception as e:
                st.error(f"שגיאה בחיבור ל-AI: {e}")
    else:
        st.warning("חביבי, אין תגובה - אין הגנה. הדבק טקסט קודם.")

# פוטר
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<p class='footer-text'>AM YISRAEL CHAI 🇮🇱</p>", unsafe_allow_html=True)
