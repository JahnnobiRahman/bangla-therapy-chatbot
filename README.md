# বাংলা থেরাপি চ্যাটবট (Bangla Therapy Chatbot)

A Streamlit-based chatbot application that provides therapeutic conversations in Bangla using the llama-3.2-3b-instruct model through LM Studio.

## Features

- 💬 Interactive chat interface in Bangla
- 🧠 Powered by llama-3.2-3b-instruct model
- ⚡ Real-time responses
- 📱 Mobile-friendly design
- 🔄 Chat history persistence
- ⏱️ Response time tracking
- 🎨 Beautiful and intuitive UI
- 🔍 Server status monitoring

## Prerequisites

- Python 3.7+
- LM Studio running locally with llama-3.2-3b-instruct model
- Required Python packages

## Installation

1. Clone the repository:
```bash
git clone https://github.com/JahnnobiRahman/bangla-therapy-chatbot.git
cd bangla-therapy-chatbot
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start LM Studio and load the llama-3.2-3b-instruct model
2. Run the Streamlit app:
```bash
streamlit run relaxy-rag/final_bot.py
```

3. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Configuration

The app is configured to connect to LM Studio at `http://192.168.0.125:1234`. If your LM Studio is running on a different address, update the URL in `relaxy-rag/final_bot.py`.

## Project Structure

```
bangla-therapy-chatbot/
├── relaxy-rag/           # Main application directory
│   └── final_bot.py      # Main Streamlit application
├── chatbot/              # Additional chatbot components
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Features in Detail

- **Bengali Language Support**: Fully supports Bengali language input and output
- **Real-time Chat**: Instant responses with response time tracking
- **Session Management**: Chat history is maintained during the session
- **Server Status**: Real-time monitoring of LM Studio server status
- **Clean UI**: Modern and responsive design with Bengali font support
- **Error Handling**: Graceful handling of connection issues and timeouts

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License 
