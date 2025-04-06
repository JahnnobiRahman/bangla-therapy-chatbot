import streamlit as st
import requests
from datetime import datetime
import time

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def query_llm(prompt):
    try:
        # Add timeout to the request
        response = requests.post(
            "http://192.168.0.125:1234/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "llama-3.2-3b-instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": f"""আপনি একজন সহানুভূতিশীল বাংলা থেরাপিস্ট।
আমার প্রশ্ন: {prompt}"""
                    }
                ],
                "temperature": 0.5
            },
            timeout=30  # 30 seconds timeout
        )

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"❌ API ত্রুটি: {response.status_code} - {response.text}"

    except requests.Timeout:
        return "❌ সময় শেষ হয়ে গেছে। অনুগ্রহ করে আবার চেষ্টা করুন।"
    except requests.ConnectionError:
        return "❌ সার্ভারে সংযোগ করতে পারছি না। অনুগ্রহ করে নিশ্চিত করুন যে LM Studio চালু আছে।"
    except Exception as e:
        return f"❌ ত্রুটি:\n{e}"

# Page configuration
st.set_page_config(
    page_title="বাংলা থেরাপি চ্যাটবট",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
    .stMarkdown {
        font-family: 'SolaimanLipi', Arial, sans-serif;
    }
    .stSpinner > div {
        border-top-color: #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    if st.button("🗑️ Clear chat history"):
        st.session_state.messages = []
        st.rerun()
    
    # Server status indicator
    try:
        requests.get("http://192.168.0.125:1234/v1/models", timeout=5)
        st.success("✅ সার্ভার আছে ভাই")
    except:
        st.error("❌ সার্ভার নাই ভাই")

# Main content
st.title("🧠 বাংলা থেরাপি চ্যাটবট 🤖💬")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message["timestamp"])

# Chat input
if prompt := st.chat_input("✍️ কি ভাবেন? আমার সাথে কথা বলেন..."):
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(datetime.now().strftime("%H:%M"))

    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("⏳ ওয়েট, ভাবতে দেন..."):
            start_time = time.time()
            response = query_llm(prompt)
            end_time = time.time()
            
            st.markdown(response)
            st.caption(f"{datetime.now().strftime('%H:%M')} • {end_time - start_time:.1f} সেকেন্ড")
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().strftime("%H:%M")
            })

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and llama-3.2-3b-instruct")
