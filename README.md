# AI Call Bot

## Overview
This is an AI-powered Call Bot that utilizes Natural Language Processing (NLP) and Speech Recognition to understand and respond to voice interactions. It is designed to automate customer service calls, provide relevant responses, and improve user experience.

## Features
- Converts speech to text and text to speech.
- Uses NLP to understand user intent.
- Provides automated responses based on predefined rules or AI models.
- Supports multiple languages and accents.
- Logs and analyzes call interactions.

## Technologies Used
- **Python**
- **SpeechRecognition** (for speech-to-text conversion)
- **pyttsx3** (for text-to-speech conversion)
- **NLTK** / **spaCy** (for NLP processing)
- **Flask** (for API integration)
- **Twilio API** (for handling calls)

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-call-bot.git
cd ai-call-bot
```

### 2. Install Dependencies
Make sure you have Python 3.7+ installed. Then, install the required libraries:
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file and add your Twilio API keys:
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number
```

### 4. Run the Application
Start the AI Call Bot:
```bash
python app.py
```

## How It Works

### 1. Speech Processing (`speech_processing.py`)
- Captures voice input using `SpeechRecognition`.
- Converts speech to text.
- Uses NLP to analyze and extract intent.

### 2. Call Handling (`call_handler.py`)
- Receives incoming calls via Twilio API.
- Processes user input and generates responses.
- Sends responses as speech output.

### 3. AI Responses (`ai_responder.py`)
- Uses predefined rules or AI-based responses.
- Implements machine learning models for dynamic interaction.
- Supports multi-turn conversation flow.

### 4. Flask API (`app.py`)
- Provides an API to handle voice interactions.
- Logs call details for analytics.


