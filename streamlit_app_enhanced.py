import streamlit as st
import requests
import pyttsx3
import speech_recognition as sr

API_URL = "http://127.0.0.1:5000"


def speak(text: str):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass


def detect_wakeup_word(audio) -> bool:
    """Check if audio contains the wake-up word 'HEY BOSS'"""
    try:
        r = sr.Recognizer()
        text = r.recognize_google(audio).upper()
        return "HEY BOSS" in text or ("HEY" in text and "BOSS" in text)
    except Exception:
        return False


st.set_page_config(page_title="AI Smart Voice Home", layout="wide", initial_sidebar_state="collapsed")

# Enhanced CSS styling
st.markdown("""
    <style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .header-container h1 {
        margin: 0;
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .header-container p {
        margin: 0.8rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 300;
    }
    
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .card h2 {
        color: #333;
        margin-top: 0;
        margin-bottom: 1.5rem;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .device-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.8rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .device-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
    }
    
    .device-card.off {
        background: linear-gradient(135deg, #e0e0e0 0%, #bdbdbd 100%);
        opacity: 0.75;
    }
    
    .device-icon {
        font-size: 3rem;
        margin-bottom: 0.8rem;
        display: block;
    }
    
    .device-name {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    
    .device-status {
        font-size: 0.95rem;
        opacity: 0.92;
        font-weight: 500;
    }
    
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }
    
    .history-item {
        padding: 1rem;
        border-left: 3px solid #667eea;
        background: #f8f9ff;
        border-radius: 5px;
        margin-bottom: 0.8rem;
    }
    
    .history-time {
        color: #667eea;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .history-command {
        color: #333;
        font-weight: 500;
        margin: 0.3rem 0;
    }
    
    .history-response {
        color: #666;
        font-size: 0.9rem;
        margin: 0.3rem 0 0 0;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .listening-animation {
        animation: pulse 1.5s infinite;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <h1>🏠 Smart Voice Home</h1>
        <p>✨ AI-Powered Voice Control Assistant ✨</p>
    </div>
""", unsafe_allow_html=True)

# Theme toggle
with st.sidebar:
    st.header("⚙️ Settings")
    theme_choice = st.selectbox("🌓 Theme", ["Light", "Dark"], index=0)
    st.session_state.theme = theme_choice
    st.markdown("---")
    st.markdown("**About**")
    st.markdown("Wake word: **HEY BOSS**")
    st.markdown("Devices: Light, Fan, TV, AC")

# Apply dark theme CSS if selected
if st.session_state.theme == "Dark":
    st.markdown('''
        <style>
        .main { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important; color: #e6eef6 !important; }
        .card { background: #0f3460 !important; color: #e6eef6 !important; border-color: rgba(255,255,255,0.1) !important; }
        .card h2 { color: #e6eef6 !important; }
        .device-card { box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6) !important; }
        .history-item { background: #16213e !important; border-left-color: #e94560 !important; }
        .history-time { color: #e94560 !important; }
        .history-command { color: #e6eef6 !important; }
        .history-response { color: #bbb !important; }
        </style>
    ''', unsafe_allow_html=True)

if "recognized" not in st.session_state:
    st.session_state.recognized = ""
if "states" not in st.session_state:
    try:
        resp = requests.get(f"{API_URL}/states", timeout=2)
        st.session_state.states = resp.json()
    except Exception:
        st.session_state.states = {"light": "OFF", "fan": "OFF", "tv": "OFF", "ac": "OFF"}
if "listening_mode" not in st.session_state:
    st.session_state.listening_mode = False
if "history" not in st.session_state:
    st.session_state.history = []
if "theme" not in st.session_state:
    st.session_state.theme = "Light"


def add_history(command: str, response: str):
    from datetime import datetime
    st.session_state.history.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "command": command, "response": response})


# Main layout
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 🎤 Voice Command")
    
    btn_col = st.columns([1])[0]
    with btn_col:
        if st.button("🎙️ START LISTENING", use_container_width=True, key="listen_btn"):
            st.session_state.listening_mode = True
    
    if st.session_state.listening_mode:
        st.info("🔊 Waiting for 'HEY BOSS'...")
        try:
            with st.spinner("👂 Listening..."):
                r = sr.Recognizer()
                with sr.Microphone() as mic:
                    audio = r.listen(mic, phrase_time_limit=5)
                
                if detect_wakeup_word(audio):
                    st.success("✅ Wake-up word detected!")
                    speak("Ready to control your home boss")
                    st.success("🎯 READY TO CONTROL YOUR HOME")
                    st.info("🎙️ Listening for command...")
                    
                    with st.spinner("👂 Listening for command..."):
                        with sr.Microphone() as mic:
                            command_audio = r.listen(mic, phrase_time_limit=5)
                        text = r.recognize_google(command_audio)
                        st.session_state.recognized = text
                        st.success(f"✅ Command: **{text}**")
                        add_history(text, "(processing)")
                else:
                    st.warning("⚠️ Wake-up word not detected. Say 'HEY BOSS' to activate!")
                    st.session_state.listening_mode = False
        
        except sr.UnknownValueError:
            st.warning("⚠️ Could not understand audio. Please try again.")
            st.session_state.listening_mode = False
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.session_state.listening_mode = False
    
    st.text_area("📝 Recognized Command", value=st.session_state.recognized, height=100, disabled=True, key="cmd_display")
    
    if st.session_state.recognized and not st.session_state.recognized.startswith("("):
        with st.spinner("⏳ Processing..."):
            try:
                resp = requests.post(f"{API_URL}/process_command", json={"command": st.session_state.recognized}, timeout=5)
                data = resp.json()
                message = data.get("message") or "Command processed"
                st.success(message)
                st.session_state.states = data.get("states", st.session_state.states)
                spoken = data.get("spoken") or message
                speak(spoken)
                add_history(st.session_state.recognized, message)
                st.session_state.listening_mode = False
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)


with col_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 💡 Appliance Control")
    
    device_info = {
        "light": ("💡", "Light"),
        "fan": ("🌀", "Fan"),
        "tv": ("📺", "TV"),
        "ac": ("❄️", "AC")
    }
    
    col1, col2 = st.columns(2)
    
    devices_list = list(st.session_state.states.items())
    for idx, (device, state) in enumerate(devices_list):
        col = col1 if idx % 2 == 0 else col2
        emoji, name = device_info.get(device, ("❓", device.capitalize()))
        
        with col:
            status_color = "🟢 ON" if state == "ON" else "⚫ OFF"
            st.markdown(f"""
                <div class="device-card {'off' if state == 'OFF' else ''}">
                    <span class="device-icon">{emoji}</span>
                    <div class="device-name">{name}</div>
                    <div class="device-status">{status_color}</div>
                </div>
            """, unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns(2, gap="small")
            with btn_col1:
                if st.button("✅ ON", key=f"on_{device}", use_container_width=True):
                    try:
                        resp = requests.post(f"{API_URL}/process_command", json={"command": f"turn on the {device}"}, timeout=5)
                        data = resp.json()
                        st.session_state.states = data.get("states", st.session_state.states)
                        message = data.get("message", f"{name} turned ON")
                        speak(message)
                        add_history(f"turn on the {device}", message)
                        st.success(f"✅ {message}")
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            with btn_col2:
                if st.button("❌ OFF", key=f"off_{device}", use_container_width=True):
                    try:
                        resp = requests.post(f"{API_URL}/process_command", json={"command": f"turn off the {device}"}, timeout=5)
                        data = resp.json()
                        st.session_state.states = data.get("states", st.session_state.states)
                        message = data.get("message", f"{name} turned OFF")
                        speak(message)
                        add_history(f"turn off the {device}", message)
                        st.success(f"✅ {message}")
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    st.divider()
    
    st.markdown("## 🕘 Recent Activity")
    if len(st.session_state.history) == 0:
        st.info("No commands yet. Start by clicking 'START LISTENING'!")
    else:
        for item in st.session_state.history[:6]:
            st.markdown(f"""
                <div class="history-item">
                    <div class="history-time">⏱️ {item['time']}</div>
                    <div class="history-command">💬 {item['command']}</div>
                    <div class="history-response">📢 {item['response']}</div>
                </div>
            """, unsafe_allow_html=True)

    if st.button("🔄 Refresh Status", use_container_width=True, key="refresh_btn"):
        try:
            resp = requests.get(f"{API_URL}/states", timeout=2)
            st.session_state.states = resp.json()
            st.success("✅ Status refreshed")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #666;">
    <h3>📋 Quick Guide</h3>
    <p><strong>1.</strong> Click "🎙️ START LISTENING" button</p>
    <p><strong>2.</strong> Say "HEY BOSS" to wake up</p>
    <p><strong>3.</strong> Give your command (e.g., "Turn on the light")</p>
    <p style="margin-top: 1.5rem; font-size: 0.9rem; opacity: 0.8;">
    🔊 AI Smart Voice Home v3.0 | Wake-word: HEY BOSS | Powered by Flask + Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
