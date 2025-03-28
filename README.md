# বাংলা থেরাপি চ্যাটবট (Bangla Therapy Chatbot)

A Streamlit-based chatbot application that provides therapeutic conversations in Bangla using the Qwen1.5-1.8B-Chat-GGUF model through LM Studio.

## Features

- 💬 Interactive chat interface in Bangla
- 🧠 Powered by Qwen1.5-1.8B-Chat-GGUF model
- ⚡ Real-time responses
- 📱 Mobile-friendly design
- 🔄 Chat history persistence
- ⏱️ Response time tracking

## Prerequisites

- Python 3.7+
- LM Studio running locally with Qwen1.5-1.8B-Chat-GGUF model
- Required Python packages

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bangla-therapy-chatbot.git
cd bangla-therapy-chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3. Install required packages:
```bash
pip install streamlit requests
```

## Usage

1. Start LM Studio and load the Qwen1.5-1.8B-Chat-GGUF model
2. Run the Streamlit app:
```bash
streamlit run tryQwen.py
```

3. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Configuration

The app is configured to connect to LM Studio at `http://192.168.0.125:1234`. If your LM Studio is running on a different address, update the URL in `tryQwen.py`.

## License

MIT License 