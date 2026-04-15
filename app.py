import streamlit as st
import google.generativeai as genai

# הגדרות עיצוב (Custom CSS) לפי המותג ConTroll
st.set_page_config(page_title="ConTroll - Anti-Troll Defense", page_icon="🛡️")

st.markdown(f"""
    <style>
    /* רקע כללי כהה */
    .stApp {{
        background-color: #0E1117;
    }}
    .main {{
        color: white;
    }}
    /* כותרת בצבע טורקיז */
    h1 {{
        color: #5BF0E0 !important;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    /* עיצוב כפתור בצבע כחול עם מסגרת טורקיז */
    .stButton>button {{
        background-color: #2E35C2 !important;
        color: white !important;
        border-radius: 10px;
        border: 2px solid #5BF0E0;
        width: 100%;
        height: 3em;
        font-weight: bold;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #5BF0E0 !important;
        color: #2E35C2 !important;
        border: 2px solid #2E35C2;
    }}
    /* עיצוב תיבת הטקסט */
    .stTextArea textarea {{
        background-color: #1A1C24 !important;
        color: #5BF0E0 !important;
        border: 1px solid #2E35C2 !important;
    }}
    /* עיצוב תיבות הבחירה */
    .stSelectbox div[data-baseweb="select"] {{
        background-color: #1A1C24 !important;
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# כותרת האפליקציה
st.title("🛡️ ConTroll")
st.markdown("<h3 style='text-align: center; color: white;'>מערכת הגנה תודעתית נגד טרולים</h3>", unsafe_allow_html=True)
st.write("")

# הגדרת ה-API שלך
API_KEY = "AIzaSyC1JvhUdZZxelkH09dDLl6b8HaEQTqK89A" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# הגדרת הפרסונות (הנשקים)
PERSONAS = {
    "The Savage (הציני האכזרי)": "You are a witty, cynical Israeli expert. Your goal is to destroy internet trolls with short, biting, and sarcastic comebacks. Focus on their lack of logic, economic failures, or personal obsession. Be extremely insulting but don't use forbidden curse words.",
    "The Historian (הפרופסור)": "You are an expert in history and geopolitics. Correct historical lies with cold, hard facts. Use terms like 'Indigenous' and mention that there was never a sovereign Palestinian state. Tone: academic, superior, and condescending.",
    "The Theological Glitch (התיאולוג)": "You are an expert in Islam. When a Muslim troll attacks Israel, use quotes from Islamic sources (like Surah 5:21) to prove the land belongs to Jews according to the Quran. Make them feel like they don't know their own religion."
}

# ממשק משתמש
troll_input = st.text_area("מה הטרול כתב?", placeholder="הדבק כאן את התגובה המעצבנת...", height=150)

col1, col2 = st.columns(2)
with col1:
    persona_name = st.selectbox("בחר כלי נשק:", list(PERSONAS.keys()))
with col2:
    intensity = st.select_slider("רמת חריפות:", options=["עדין", "חריף", "אטומי"])

st.write("")

if st.button("שגר הגנה! 🚀"):
    if troll_input:
        with st.spinner('מכייל קרני לייזר...'):
            system_prompt = PERSONAS[persona_name]
            # תרגום רמת החריפות לאנגלית עבור המודל
            intensity_map = {"עדין": "Mild and smart", "חריף": "Spicy and mean", "אטומי": "Atomic and devastating"}
            
            full_prompt = f"System Instruction: {system_prompt}\nResponse Intensity: {intensity_map[intensity]}\n\nTroll's comment: '{troll_input}'\n\nGenerate the ultimate response in English (unless the troll wrote in Hebrew, then answer in Hebrew):"
            
            try:
                response = model.generate_content(full_prompt)
                st.markdown("---")
                st.markdown("### 🎯 התגובה של ConTroll:")
                st.success(response.text)
                st.info("💡 העתק את הטקסט והדבק אותו בתגובה לטרול.")
            except Exception as e:
                st.error(f"אופס! יש שגיאה: {e}")
    else:
        st.warning("חביבי, שכחת להדביק את התגובה של הטרול!")

st.markdown("<br><br><hr><p style='text-align: center; color: gray;'>Powered by ConTroll AI | Stand with Israel 🇮🇱</p>", unsafe_allow_html=True)
