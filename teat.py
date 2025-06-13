import streamlit as st
import google.generativeai as genai
import os

# Set your Google API Key
GOOGLE_API_KEY = "AIzaSyAx4bAdsO3o41eCGiyKiZSgPjlPhNxNH9g"
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Streamlit UI
st.set_page_config(page_title="Trending Post Generator", page_icon="📲")
st.title("📈 Trending Post Generator with Gemini AI")

# Input
topic = st.text_input("Enter a Topic", placeholder="e.g. AI in Education")

# Platform dropdown
medium = st.selectbox("Select Platform", ["LinkedIn", "Instagram", "YouTube", "Twitter", "Threads"])

# Generate on button click
if st.button("Generate Content"):
    if topic.strip() == "":
        st.warning("Please enter a topic.")
    else:
        # Create a custom prompt
        prompt = f"""
        You're a trending social media strategist. Based on the topic "{topic}" and the platform "{medium}", 
        suggest:
        1. 3 trending post ideas with a title.
        2. A short caption for each.
        3. Relevant and catchy hashtags for each post.
        Present the result in bullet points.
        """

        # Get response from Gemini
        response = model.generate_content(prompt)
        st.success("Generated successfully!")
        st.markdown("### 🚀 Suggested Posts & Hashtags")
        st.write(response.text)
