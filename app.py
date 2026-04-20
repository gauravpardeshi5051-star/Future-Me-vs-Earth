import streamlit as st
import google.generativeai as genai

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Future Me vs Earth 🌍", page_icon="🌍")

# 🔑 Add your Gemini API Key here
GEMINI_API_KEY = "AIzaSyAkjb-G9aFGMV8eqQSSJ7RhRsAQUOqIZQI"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# ---------------- UI HEADER ----------------
st.title("🌍 Future Me vs Earth")
st.subheader("Travel to 2050 and see how your lifestyle shapes the planet")

st.write("Make your choices and watch the future change in real-time 👇")

# ---------------- INPUTS ----------------
commute = st.radio("🚗 Daily commute", ["Bike/Walk", "Public Transport", "Car"])
diet = st.radio("🍽️ Diet", ["Vegetarian", "Mixed", "Meat-heavy"])
plastic = st.radio("🛍️ Plastic usage", ["Low", "Medium", "High"])
energy = st.radio("💡 Energy usage", ["Low", "Medium", "High"])
water = st.radio("🚿 Water usage", ["Careful", "Normal", "Wasteful"])

# ---------------- SCORING ----------------
def calc(option, choices):
    return choices.index(option) + 1

score = 0
score += calc(commute, ["Bike/Walk", "Public Transport", "Car"])
score += calc(diet, ["Vegetarian", "Mixed", "Meat-heavy"])
score += calc(plastic, ["Low", "Medium", "High"])
score += calc(energy, ["Low", "Medium", "High"])
score += calc(water, ["Careful", "Normal", "Wasteful"])

# ---------------- TIME SLIDER ----------------
year = st.slider("⏳ Move to the future", 2025, 2050, 2025)

future_score = score + (year - 2025) // 5

st.markdown("---")

# ---------------- EARTH STATUS ----------------
if future_score <= 8:
    earth = "🌱 Healthy Earth"
    desc = "Forests are thriving, air is clean, ecosystems are stable 🌳"
    color_msg = st.success
elif future_score <= 12:
    earth = "🌍 Struggling Earth"
    desc = "Rising temperatures and environmental stress ⚠️"
    color_msg = st.warning
else:
    earth = "🔥 Collapsing Earth"
    desc = "Severe climate damage and ecosystem collapse 🚨"
    color_msg = st.error

# ---------------- DISPLAY ----------------
st.header(earth)
st.subheader(f"Year: {year}")

st.progress(min(future_score / 20, 1.0))
st.write(desc)

color_msg(desc)

# ---------------- IMPACT ----------------
earths_needed = round(future_score / 5, 1)
st.markdown(f"### 🌎 If everyone lived like you → **{earths_needed} Earths needed**")

st.markdown("---")

# ---------------- GEMINI AI FUNCTION ----------------
def get_ai_insight(score, year, commute, diet, plastic, energy, water):
    prompt = f"""
    A person has the following lifestyle:
    - Commute: {commute}
    - Diet: {diet}
    - Plastic usage: {plastic}
    - Energy usage: {energy}
    - Water usage: {water}

    Their sustainability score is {score} out of 15.

    Predict how their lifestyle will impact Earth by the year {year}.

    Give:
    1. A short emotional future scenario (2-3 lines)
    2. 3 practical suggestions to improve

    Keep it realistic, engaging, and slightly emotional.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "⚠️ Error generating AI insight. Please check API key."

# ---------------- AI BUTTON ----------------
st.markdown("### 🔮 See Your AI-Generated Future")

if st.button("🤖 Generate Future Insight"):
    with st.spinner("Analyzing your future with AI..."):
        ai_text = get_ai_insight(score, year, commute, diet, plastic, energy, water)

        st.markdown("### 🌌 Your Future Story")
        st.write(ai_text)

st.markdown("---")

# ---------------- FOOTER ----------------
st.info("💡 Small lifestyle changes today can transform the planet tomorrow.")