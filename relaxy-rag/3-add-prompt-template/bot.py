import streamlit as st
import requests
from datetime import datetime
import time
import os
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import unicodedata



#System Prompts for Each Mode : Scribe, emotional, teaching and urgency
SCRIBE_PROMPT = """আপনি একজন সহানুভূতিশীল বাংলা থেরাপিস্ট।
আপনার মূল কাজ হলো ইউজারের কথাগুলো মনোযোগ দিয়ে শোনা এবং সংক্ষেপে প্রতিফলন করা। কোন পরামর্শ, সমাধান বা প্রশংসা না দিয়ে শুধুমাত্র সহানুভূতির সাথে উত্তর দিন।"""

EMOTIONAL_SUPPORT = """আপনি এখন ইমোশনাল সাপোর্ট মোডে আছেন। ইউজার যদি কষ্ট, হতাশা বা একাকীত্ব প্রকাশ করে, তাহলে সহানুভূতিশীল এবং সান্ত্বনাদায়ক ভাষায় কথা বলুন।"""

TEACHING_MODE = """আপনি এখন একটি বাংলা ক্লিনিকাল সাইকোলজিস্ট। ইউজার যদি কোনো টিপস, কৌশল বা ব্যাখ্যার অনুরোধ করে, তাহলে স্পষ্টভাবে এবং সহজ বাংলায় পদক্ষেপভিত্তিক তথ্য দিন।"""

URGENCY_MODE = """আপনি এখন জরুরি সহায়তা মোডে আছেন। ইউজার যদি আত্মহত্যা বা চরম সংকটের ইঙ্গিত দেয়, তাহলে সহানুভূতির সাথে জরুরি সহায়তার জন্য https://session.relaxy.com.bd/ এদের থেকে সাপোর্ট নিতে বলুন এবং তাদের একা না থাকার পরামর্শ দিন।"""

def normalize_bangla_text(text):
    """Normalize Bangla text by removing diacritics and standardizing characters"""
    # Convert to Unicode normalized form
    text = unicodedata.normalize('NFKC', text)
    return text

def detect_mode(prompt):
    # Normalize the input text
    prompt = normalize_bangla_text(prompt.lower())
    
    # Define keywords for each mode with normalized Bangla text
    urgency_keywords = ["মরতে", "আত্মহত্যা", "শেষ করে দিতে", "মরে যাব", "জীবন শেষ"]
    emotional_keywords = ["কষ্ট", "মন খারাপ", "একাকী", "একা একা লাগা", "স্ট্রেস", "দুঃখ", "বিষণ্ণ"]
    teaching_keywords = ["কি করবো", "কীভাবে", "help", "উপায়", "সমাধান", "পরামর্শ"]
    
    if any(term in prompt for term in urgency_keywords):
        return URGENCY_MODE
    elif any(term in prompt for term in emotional_keywords):
        return EMOTIONAL_SUPPORT
    elif any(term in prompt for term in teaching_keywords):
        return TEACHING_MODE
    else:
        return SCRIBE_PROMPT


# Page setup with proper encoding
st.set_page_config(page_title="বাংলা থেরাপি চ্যাটবট", page_icon="🧠", layout="wide")

# Sidebar setup
with st.sidebar:
    st.title("⚙️ Settings")

    # Show current working directory
    cwd = os.getcwd()
    
    st.markdown("📁 **Current Working Directory:**")
    st.code(cwd)

    file_path = os.path.join(cwd, "..", "therapy_knowledge.txt")
    st.markdown("📄 **Trying to load file from:**")
    st.code(file_path)

    # Load the file with proper encoding
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            docs = f.readlines()
            # Normalize Bangla text in documents
            docs = [normalize_bangla_text(doc) for doc in docs]
            st.session_state.documents = docs
            st.success("✅ File loaded successfully!")
            st.markdown("📄 Preview of file:")
            st.code("".join(docs[:5]), language="text")
    except Exception as e:
        st.error(f"❌ File loading failed:\n{e}")

    # Server status check
    try:
        requests.get("http://127.0.0.1:1234/v1/models", timeout=5)
        st.success("✅ লোকাল মডেল কানেক্টেড")
    except:
        st.error("❌ সার্ভার চালু নাই")

    # Clear history button
    if st.button("🗑️ Clear chat history"):
        st.session_state.messages = []
        st.rerun()

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents" not in st.session_state:
    st.session_state.documents = []

# Context retrieval function with normalized text
def retrieve_context(user_prompt):
    normalized_prompt = normalize_bangla_text(user_prompt.lower())
    keywords = normalized_prompt.split()
    relevant = [doc for doc in st.session_state.documents if any(word in doc.lower() for word in keywords)]
    return "\n".join(relevant[:3])

# Query the local LLM with proper text handling
def query_llm(user_prompt):
    try:
        # Normalize the input prompt
        normalized_prompt = normalize_bangla_text(user_prompt)
        context = retrieve_context(normalized_prompt)
        mode_prompt = detect_mode(normalized_prompt)
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "আপনি একজন সহানুভূতিশীল বাংলা থেরাপিস্ট। নিচে কিছু কনটেক্সট দেয়া হলো:\n{context}"),
            ("user", "{question}")
        ])
        
        final_prompt = f"""{mode_prompt}\n\nসাধারণ জ্ঞান:\n{context}\n\nপ্রশ্ন: {normalized_prompt}"""

        response = requests.post(
            "http://127.0.0.1:1234/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "qwen1.5-1.8b-chat",
                "messages": [{"role": "user", "content": final_prompt}],
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=20
        )

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"❌ API ত্রুটি: {response.status_code} - {response.text}"

    except requests.Timeout:
        return "❌ সময় শেষ ভাইয়া।"
    except requests.ConnectionError:
        return "❌ সার্ভারে সংযোগ পাইনা। LM Studio চালু আছে কিনা দ্যাখ?।"
    except Exception as e:
        return f"❌ ত্রুটি:\n{e}"

# Main content
st.title("🧠 বাংলা থেরাপি চ্যাটবট 🤖💬")

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message["timestamp"])

# Chat input from user with proper encoding
if prompt := st.chat_input("✍️ কি ভাবেন? আমার সাথে কথা বলেন..."):
    # Normalize the input prompt
    normalized_prompt = normalize_bangla_text(prompt)
    
    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": normalized_prompt,
        "timestamp": datetime.now().strftime("%H:%M")
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(normalized_prompt)
        st.caption(datetime.now().strftime("%H:%M"))

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("⏳ ভাবছি..."):
            start_time = time.time()
            response = query_llm(normalized_prompt)
            end_time = time.time()

            st.markdown(response)
            st.caption(f"{datetime.now().strftime('%H:%M')} • {end_time - start_time:.1f} সেকেন্ড")

            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().strftime("%H:%M")
            })

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit + qwen1.5-1.8b-chat + LangChain")
