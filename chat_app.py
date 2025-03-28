import streamlit as st
import requests

# Query function for LM Studio (chat-completion)
def query_llm(prompt):
    try:
        response = requests.post(
            "http://192.168.0.125:1234/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": "mistral-7b-instruct-v0.3",
                "messages": [
                    {
                        "role": "user",
                        "content": f"""আপনি একজন সহানুভূতিশীল বাংলা থেরাপিস্ট।
আমার প্রশ্ন: {prompt}"""
                    }
                ],
                "temperature": 0.7
            }
        )

        if response.status_code != 200:
            return f"⚠️ সার্ভার ত্রুটি (status code: {response.status_code})\n\n{response.text}"

        data = response.json()

        if "choices" not in data:
            return f"⚠️ 'choices' পাওয়া যায়নি:\n\n{data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ ত্রুটি ঘটেছে:\n\n{e}"

# Streamlit UI
st.title("🧠 বাংলা থেরাপি চ্যাটবট 🤖💬")

user_input = st.text_input("আপনার কথা লিখুন", key="user_input_main")

if user_input:
    response = query_llm(user_input)
    st.write("🧠 থেরাপিস্ট: " + response)
