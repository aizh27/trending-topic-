import streamlit as st
from langchain.tools.ddg_search.tool import DuckDuckGoSearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os

# Set Gemini API key directly (avoid using .env as requested)
GOOGLE_API_KEY = "your_google_api_key_here"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# Initialize DuckDuckGo search tool
search = DuckDuckGoSearchResults()

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
        # Search using DuckDuckGo
        search_results = search.run(f"{topic} site:{medium.lower()}.com")  # returns list of dicts

        # Format search results
        results_text = ""
        for i, result in enumerate(search_results[:5], 1):
            title = result.get("title", "No title")
            link = result.get("link", "")
            results_text += f"{i}. [{title}]({link})\n"

        # Prompt template for Gemini
        prompt = ChatPromptTemplate.from_template("""
        Based on the topic "{topic}" and the platform "{medium}", here are some trending posts:
        {results}
        Generate relevant and catchy hashtags for these posts.
        """)
        
        chain = prompt | llm
        final_output = chain.invoke({
            "topic": topic,
            "medium": medium,
            "results": results_text
        })

        # Display Results
        st.success("Trending content & hashtags generated successfully!")
        st.markdown("### 🔗 Trending Posts")
        st.markdown(results_text, unsafe_allow_html=True)

        st.markdown("### 🔥 Suggested Hashtags")
        st.write(final_output.content)
