import streamlit as st
import google.generativeai as genai
import os

# Set Gemini API Key
GOOGLE_API_KEY = "AIzaSyAx4bAdsO3o41eCGiyKiZSgPjlPhNxNH9g"
genai.configure(api_key=GOOGLE_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash-lite")

# Streamlit UI
st.set_page_config(page_title="Trending Post Generator", page_icon="📲")
st.title("📈 Trending Post Generator with Gemini AI")

# Input fields
topic = st.text_input("Enter a Topic", placeholder="e.g. AI in Education")
medium = st.selectbox("Select Platform", ["LinkedIn", "Instagram", "YouTube", "Twitter", "Threads"])

# Button to generate
if st.button("Generate Content"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        prompt = f"""
        You're a social media content strategist. Based on the topic "{topic}" and platform "{medium}", generate:
        - 3 trending post ideas (short titles)
        - A short caption for each
        - Relevant, popular hashtags for each
        Format it clearly and engagingly.
        """

        try:
            response = model.generate_content(prompt)
            st.success("Content generated successfully!")
            st.markdown("### 🚀 Suggested Posts & Hashtags")
            st.write(response.text)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
