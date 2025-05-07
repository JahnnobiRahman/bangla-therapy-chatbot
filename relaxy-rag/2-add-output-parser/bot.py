import streamlit as st
import requests
from datetime import datetime
import time
import os
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema #added output parser and response schema


# Page setup
st.set_page_config(page_title="বাংলা থেরাপি চ্যাটবট", page_icon="🧠", layout="wide")

# Sidebar setup
with st.sidebar:
    st.title("⚙️ Settings")

    # Show current working directory
    cwd = os.getcwd()
    
    st.markdown("📁 **Current Working Directory:**")
    st.code(cwd)

    file_path = os.path.join(cwd, "/Users/jahnnobirahman/Desktop/python/allcode/projects/l01/relaxy-rag/therapy_knowledge.txt")
    st.markdown("📄 **Trying to load file from:**")
    st.code(file_path)

    # Load the file and preview
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            docs = f.readlines()
            st.session_state.documents = docs
            st.success("✅ File loaded successfully!")
            st.markdown("📄 Preview of file:")
            st.code("".join(docs[:5]), language="text")
    except Exception as e:
        st.error(f"❌ File loading failed:\n{e}")

    # Server status check
    try:
        requests.get("http://192.168.0.104:1235/v1/models", timeout=5)
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

# Context retrieval function
def retrieve_context(user_prompt):
    keywords = user_prompt.lower().split()
    relevant = [doc for doc in st.session_state.documents if any(word in doc.lower() for word in keywords)]
    return "\n".join(relevant[:3])


#  Structured output schema
response_schemas = [
    ResponseSchema(name="problem", description="ইউজারের মূল সমস্যা"),
    ResponseSchema(name="suggestion", description="সাইকোলজিস্টের পরামর্শ")
]
parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = parser.get_format_instructions()

#  Query the local LLM (Qwen 1.5 - 1.8B) with context
def query_llm(user_prompt):
    try:
        context = retrieve_context(user_prompt)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "আপনি একজন সহানুভূতিশীল বাংলা থেরাপিস্ট। নিচে কিছু কনটেক্সট দেয়া হলো:\n{context}"),
            ("user", "{question}")
        ])
        final_prompt = prompt_template.format(context=context, question=user_prompt)

        response = requests.post(
            "http://192.168.0.104:1235/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "Qwen1.5-1.8B-Chat-GGUF",
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
        return "❌ সময় শেষ ভাইয়া।"
    except requests.ConnectionError:
        return "❌ সার্ভারে সংযোগ পাইনা। LM Studio চালু আছে কিনা দ্যাখ?।"
    except Exception as e:
        return f"❌ ত্রুটি:\n{e}"

#  Main content
st.title("🧠 বাংলা থেরাপি চ্যাটবট 🤖💬")

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message["timestamp"])

# Chat input from user
if prompt := st.chat_input("✍️ কি ভাবেন? আমার সাথে কথা বলেন..."):
    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%H:%M")
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(datetime.now().strftime("%H:%M"))

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("⏳ ভাবছি..."):
            start_time = time.time()
            response = query_llm(prompt)
            end_time = time.time()

            st.markdown(response)
            st.caption(f"{datetime.now().strftime('%H:%M')} • {end_time - start_time:.1f} সেকেন্ড")

            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().strftime("%H:%M")
            })

#  Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit + Qwen1.5-1.8B-Chat-GGUF + LangChain")
