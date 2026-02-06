# AI Smart Voice-Controlled Home Assistant (Simulated)

This project simulates a voice-controlled home assistant for Light, Fan, TV, and AC without any hardware. It captures voice via your computer microphone, recognizes speech, parses intent, simulates device control, and provides voice feedback.

Features
- Record voice from microphone (button in Streamlit UI)
- Speech-to-text using Google's recognition via `SpeechRecognition`
- Intent parsing (turn on / turn off + appliance detection)
- Simulated device states (in-memory)
- Text-to-speech feedback using `pyttsx3`
- Flask backend API and Streamlit frontend

Requirements (Windows)
- Python 3.8+
- Install dependencies:

```powershell
pip install pipwin
pipwin install pyaudio
pip install -r requirements.txt
```

Run the backend and frontend

1. Start the Flask backend (in a terminal):

```powershell
python "C:/Users/munni/OneDrive/Desktop/smart voice home/app.py"
```

2. In another terminal, start the Streamlit UI:

```powershell
streamlit run "C:/Users/munni/OneDrive/Desktop/smart voice home/streamlit_app.py"
```

Usage
- Open the Streamlit URL (usually http://localhost:8501).
- Click "Start Listening" and speak a command such as "Turn on the light".
- Click "Send to Assistant" to forward the recognized text to the backend.
- The app will display the updated state and speak a confirmation.

Notes
- Speech recognition uses Google's web API (internet required). For an entirely local transcription, integrate Whisper models.
- `PyAudio` installation on Windows works best via `pipwin` (included in instructions).
- If TTS doesn't play, ensure sound output is configured on your machine.
