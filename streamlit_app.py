import streamlit as st
import requests
import pyttsx3
import speech_recognition as sr
from datetime import datetime

API_URL = "http://127.0.0.1:5000"

# ============================================================================
# PAGE CONFIG & STYLING
# ============================================================================
st.set_page_config(
    page_title="🏠 AI Smart Voice Home",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# ============================================================================
# CUSTOM CSS - CLEAN, MINIMAL, MODERN DESIGN
# ============================================================================
st.markdown("""
    <style>
    /* Global Styling */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Soft cream background */
    .main {
        background-color: #f9f8f6;
        min-height: 100vh;
        padding: 1.5rem;
    }
    
    /* Main container */
    .main .block-container {
        max-width: 900px;
        margin: 0 auto;
    }
    
    /* Minimal Header */
    .header-minimal {
        text-align: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e9e7e0;
    }
    
    .header-minimal h1 {
        font-size: 1.8rem;
        font-weight: 600;
        color: #4a4a4a;
        letter-spacing: 1px;
        margin: 0;
    }
    
    /* Large Mic Button */
    .mic-button-wrapper {
        display: flex;
        justify-content: center;
        margin: 2rem 0 3rem 0;
    }
    
    .mic-button {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        border: none;
        background: linear-gradient(135deg, #7ec8c2 0%, #a8d8d8 100%);
        color: white;
        font-size: 4rem;
        cursor: pointer;
        box-shadow: 0 10px 30px rgba(126, 200, 194, 0.3);
        transition: all 0.3s ease;
        font-weight: 700;
    }
    
    .mic-button:hover {
        transform: scale(1.1);
        box-shadow: 0 15px 40px rgba(126, 200, 194, 0.4);
    }
    
    .mic-button:active {
        transform: scale(0.95);
    }
    
    .mic-label {
        text-align: center;
        font-size: 0.95rem;
        color: #6b6b6b;
        font-weight: 600;
        margin-top: 1rem;
        letter-spacing: 0.5px;
    }
    
    /* Device Grid */
    .device-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
        margin: 3rem 0;
    }
    
    .device-item {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #f0ede6;
        transition: all 0.3s ease;
    }
    
    .device-item:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }
    
    /* Device Header */
    .device-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .device-icon-large {
        font-size: 2.5rem;
        line-height: 1;
    }
    
    .device-label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #4a4a4a;
    }
    
    /* Toggle Switch Container */
    .toggle-switches {
        display: flex;
        gap: 0.8rem;
        justify-content: flex-start;
    }
    
    /* Custom Toggle Buttons */
    .toggle-btn {
        flex: 1;
        padding: 0.7rem 1rem;
        border: none;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .toggle-on {
        background: linear-gradient(135deg, #7ec8c2 0%, #a8d8d8 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(126, 200, 194, 0.3);
    }
    
    .toggle-on:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(126, 200, 194, 0.4);
    }
    
    .toggle-off {
        background: #e9e7e0;
        color: #8b8b8b;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    .toggle-off:hover {
        background: #ddd9d0;
        transform: translateY(-2px);
    }
    
    /* Override Streamlit Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #7ec8c2 0%, #a8d8d8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.7rem 1rem !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 12px rgba(126, 200, 194, 0.3) !important;
        width: auto !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(126, 200, 194, 0.4) !important;
    }
    
    /* Status Indicator */
    .status-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 0.5rem;
        vertical-align: middle;
    }
    
    .status-dot.active {
        background-color: #7ec8c2;
        box-shadow: 0 0 8px rgba(126, 200, 194, 0.5);
    }
    
    .status-dot.inactive {
        background-color: #cbd5e0;
    }
    
    .status-text {
        font-size: 0.85rem;
        color: #8b8b8b;
        font-weight: 600;
    }
    
    /* History Section */
    .history-section {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 3rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #f0ede6;
    }
    
    .history-title {
        font-size: 1rem;
        font-weight: 700;
        color: #4a4a4a;
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }
    
    .history-item {
        padding: 1rem;
        background: #f9f8f6;
        border-radius: 10px;
        margin-bottom: 0.8rem;
        border-left: 3px solid #7ec8c2;
        font-size: 0.9rem;
        color: #6b6b6b;
    }
    
    .history-item:last-child {
        margin-bottom: 0;
    }
    
    .history-cmd {
        font-weight: 600;
        color: #4a4a4a;
        margin-bottom: 0.3rem;
    }
    
    .history-response {
        font-size: 0.85rem;
        color: #8b8b8b;
    }
    
    .history-time {
        font-size: 0.75rem;
        color: #b3b3b3;
        margin-top: 0.4rem;
    }
    
    /* Responsive Grid */
    @media (max-width: 768px) {
        .device-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .mic-button {
            width: 120px;
            height: 120px;
            font-size: 3rem;
        }
        
        .header-minimal h1 {
            font-size: 1.5rem;
        }
    }
    
    /* Text Styling */
    h1, h2, h3 {
        color: #4a4a4a;
    }
    
    p {
        color: #6b6b6b;
        line-height: 1.6;
    }
    
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def speak(text: str):
    """Convert text to speech"""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

def detect_wakeup_word(audio) -> bool:
    """Check if audio contains 'HEY BOSS'"""
    try:
        r = sr.Recognizer()
        text = r.recognize_google(audio).upper()
        return "HEY BOSS" in text or ("HEY" in text and "BOSS" in text)
    except Exception:
        return False

def get_device_emoji(device_name):
    """Get emoji for device"""
    emojis = {
        "light": "💡",
        "fan": "🌀",
        "tv": "📺",
        "ac": "❄️"
    }
    return emojis.get(device_name.lower(), "⚙️")


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "devices" not in st.session_state:
    st.session_state.devices = {}

if "theme" not in st.session_state:
    st.session_state.theme = "light"

# ============================================================================
# MAIN UI - CLEAN & MINIMAL LAYOUT
# ============================================================================

# Minimal Header
st.markdown("""
    <div class="header-minimal">
        <h1>🏠 SMART HOME</h1>
    </div>
""", unsafe_allow_html=True)

# Large Microphone Button
st.markdown("""
    <div class="mic-button-wrapper">
        <button class="mic-button" onclick="document.querySelector('[data-testid=stButton]').click()" title="Press to listen">🎤</button>
    </div>
    <div class="mic-label">TAP TO SPEAK</div>
""", unsafe_allow_html=True)

# Hidden button that triggers on click
col_mic = st.columns([1])[0]
with col_mic:
    listen_btn = st.button("", key="listen_main")

# Listening for voice
if listen_btn:
    st_placeholder = st.empty()
    try:
        st_placeholder.info("🎤 Listening... Say a command!")
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source, timeout=10)
        
        st_placeholder.info("🔄 Processing...")
        
        text = r.recognize_google(audio)
        st_placeholder.success(f"✅ {text}")
        
        response = requests.post(f"{API_URL}/process_command", json={"command": text})
        data = response.json()
        result = data.get("result", "Command processed")
        
        st_placeholder.success(f"✨ {result}")
        speak(result)
        
        st.session_state.history.insert(0, {
            "command": text,
            "response": result,
            "time": datetime.now().strftime("%H:%M")
        })
        
    except sr.UnknownValueError:
        st_placeholder.error("❌ Could not understand audio. Please try again.")
    except sr.RequestError:
        st_placeholder.error("❌ Internet connection required.")
    except Exception as e:
        st_placeholder.error(f"❌ Error: {str(e)}")

# Device Grid
st.markdown('<div class="device-grid">', unsafe_allow_html=True)

try:
    devices_response = requests.get(f"{API_URL}/states")
    devices_data = devices_response.json().get("devices", {})
    
    for device_name, status in devices_data.items():
        device_emoji = get_device_emoji(device_name)
        is_on = status == "ON"
        status_dot_class = "active" if is_on else "inactive"
        
        st.markdown(f"""
            <div class="device-item">
                <div class="device-header">
                    <div class="device-icon-large">{device_emoji}</div>
                    <div>
                        <div class="device-label">{device_name.title()}</div>
                        <div class="status-text">
                            <span class="status-dot {status_dot_class}"></span>
                            {status}
                        </div>
                    </div>
                </div>
                <div class="toggle-switches" id="{device_name}_toggles">
                    <!-- Buttons will be placed here by Streamlit -->
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # ON/OFF buttons
        col_on, col_off = st.columns(2, gap="small")
        
        with col_on:
            on_btn = st.button(
                "ON",
                key=f"on_{device_name}",
                use_container_width=True,
                help=f"Turn on {device_name.title()}"
            )
            if on_btn:
                try:
                    requests.post(f"{API_URL}/process_command", json={"command": f"turn {device_name} on"})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        
        with col_off:
            off_btn = st.button(
                "OFF",
                key=f"off_{device_name}",
                use_container_width=True,
                help=f"Turn off {device_name.title()}"
            )
            if off_btn:
                try:
                    requests.post(f"{API_URL}/process_command", json={"command": f"turn {device_name} off"})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

except Exception as e:
    st.error(f"Connection error: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# History Section
if st.session_state.history:
    st.markdown("""
        <div class="history-section">
            <div class="history-title">📜 Recent Commands</div>
    """, unsafe_allow_html=True)
    
    for item in st.session_state.history[:5]:
        st.markdown(f"""
            <div class="history-item">
                <div class="history-cmd">🎤 {item['command']}</div>
                <div class="history-response">✅ {item['response']}</div>
                <div class="history-time">⏰ {item['time']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e9e7e0; color: #999;">
        <p style="font-size: 0.85rem;">Voice-Controlled Smart Home • Powered by Flask & Streamlit</p>
    </div>
""", unsafe_allow_html=True)
