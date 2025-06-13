import streamlit as st
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os

# Set Gemini API key directly
GOOGLE_API_KEY = "AIzaSyAx4bAdsO3o41eCGiyKiZSgPjlPhNxNH9g"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize Gemini model (fixed model name)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# Initialize DuckDuckGo search tool
search_tool = DuckDuckGoSearchResults()

# Streamlit UI
st.set_page_config(page_title="Trending Post Generator", page_icon="🔍")
st.title("🚀 Trending Post Generator using Gemini & DuckDuckGo")

# Input
topic = st.text_input("Enter a Topic", placeholder="e.g. AI in Education")

# Dropdown
medium = st.selectbox("Select Platform", ["LinkedIn", "Instagram", "YouTube", "Twitter", "Threads"])

# On Submit
if st.button("Generate Trending Posts"):
    if topic.strip() == "":
        st.warning("Please enter a topic.")
    else:
        # Use LangChain-style invocation
        results = search_tool.invoke(f"{topic} site:{medium.lower()}.com")

        # Format search results
        results_text = ""
        for i, result in enumerate(results[:5], 1):
            title = result.get("title", "No title")
            link = result.get("link", "")
            results_text += f"{i}. [{title}]({link})\n"

        # Create prompt for Gemini
        prompt = ChatPromptTemplate.from_template("""
        Based on the topic "{topic}" and the platform "{medium}", here are some trending posts:
        {results}
        Generate relevant and catchy hashtags for these posts.
        """)

        chain = prompt | llm
        output = chain.invoke({
            "topic": topic,
            "medium": medium,
            "results": results_text
        })

        # Output in UI
        st.success("Trending content & hashtags generated successfully!")
        st.markdown("### 🔗 Trending Posts")
        st.markdown(results_text, unsafe_allow_html=True)

        st.markdown("### 🔥 Suggested Hashtags")
        st.write(output.content)
