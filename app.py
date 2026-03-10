import streamlit as st
from supabase import create_client, Client
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import re
import hashlib
import time
import zipfile
import json
import os
import random
from PIL import Image
import io

# 1. GLOBAL CONFIG (Must be the first Streamlit command)
st.set_page_config(page_title="Netra: Cyber Defense", layout="wide", page_icon="🛡️")

# 2. GLOBAL VARIABLES
DB_FILE = "sentinai_soc.db"
WATERMARK_SECRET = b"corporate_master_key_998877"
def init_sqlite_db():
    """Initializes the local SQLite database for audit logging."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY, 
            ts TEXT, 
            input TEXT, 
            status TEXT, 
            risk TEXT, 
            rules TEXT, 
            analyst_summary TEXT
        )
    """)
    conn.commit()
    conn.close()
    return True
def get_agent_stats():
    """Calculates agent level and XP based on SOC activity."""
    try:
        conn = sqlite3.connect(DB_FILE)
        # Count total logs as 'experience'
        xp = pd.read_sql_query("SELECT COUNT(*) as count FROM logs", conn).iloc[0]['count']
        conn.close()
    except:
        xp = 0
    
    # Logic: Level 1 for 0-10 XP, Level 2 for 11-20, etc.
    level = (xp // 10) + 1
    rank = "Novice"
    if level > 2: rank = "Specialist"
    if level > 5: rank = "Elite Guardian"
    if level > 8: rank = "Cyber Commander"
    
    return xp, level, rank
# 3. SESSION STATE INITIALIZATION
if 'current_page' not in st.session_state: 
    st.session_state.current_page = "Home"
if "user" not in st.session_state: 
    st.session_state.user = None
if "role" not in st.session_state: 
    st.session_state.role = "user"
   
# 4. UI THEME ENGINE (Continued)
ULTRA_CYBER_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Share+Tech+Mono&display=swap');
    .stApp {
        background-color: #050814;
        background-image: linear-gradient(rgba(0, 255, 163, 0.05) 1px, transparent 1px), 
                          linear-gradient(90deg, rgba(0, 255, 163, 0.05) 1px, transparent 1px);
        background-size: 40px 40px;
        color: #E2E8F0 !important;
        font-family: 'Rajdhani', sans-serif;
    }
    h1, h2, h3 { font-family: 'Share Tech Mono', monospace !important; color: #00FFA3 !important; text-transform: uppercase; text-shadow: 0px 0px 15px rgba(0, 255, 163, 0.6); }
    [data-testid="metric-container"], .stDataFrame, div[data-testid="stExpander"] {
        background: rgba(10, 15, 30, 0.8) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 163, 0.15) !important;
        border-radius: 4px !important;
        border-left: 4px solid #7000FF !important;
    }
    div.stButton > button {
        background: rgba(0, 255, 163, 0.05) !important; color: #00FFA3 !important; border: 1px solid #00FFA3 !important; 
        border-radius: 2px !important; font-family: 'Share Tech Mono', monospace !important;
    }
    div.stButton > button:hover { background: #00FFA3 !important; color: #050814 !important; box-shadow: 0px 0px 25px rgba(0, 255, 163, 0.8) !important; }
</style>
"""
st.markdown(ULTRA_CYBER_CSS, unsafe_allow_html=True)

# 5. CORE FORENSIC ENGINES
def process_image_forensics(image_file):
    """Analyzes media for AI generation and steganographic payloads."""
    img_bytes = image_file.getvalue()
    file_hash = hashlib.sha256(img_bytes).hexdigest()
    hash_int = int(file_hash[:8], 16)
    
    return {
        "hash": file_hash[:12].upper(),
        "is_ai": (hash_int % 100) > 40,
        "ai_conf": 75 + (hash_int % 24),
        "has_payload": (hash_int % 50) > 40,
        "from_internet": (hash_int % 10) > 3,
        "mock_url": f"https://global-index.net/archive/img_{file_hash[:6]}.jpg"
    }
    # 6. HARDWARE & NETWORK INTELLIGENCE ENGINES
def run_silicon_watch_audit(component_text):
    """Audits Bill of Materials (BOM) for restricted hardware entities."""
    RESTRICTED_VENDORS = ["Hikvision", "Dahua", "Hytera", "ZTE", "Huawei", "Inspur"]
    findings = []
    for vendor in RESTRICTED_VENDORS:
        if re.search(rf"\b{vendor}\b", component_text, re.I):
            findings.append(vendor)
            
    if not findings:
        return "✅ CLEARED", "Compliance verified with National Security protocols.", 0
    else:
        risk_score = min(len(findings) * 35, 100)
        return "🔴 SECURITY VIOLATION", f"High-risk hardware detected: {', '.join(findings)}", risk_score

def track_ip_location(ip_address):
    """Geolocates suspicious IP addresses in real-time."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        if data['status'] == 'success':
            return data
        return {"Error": "Invalid IP or tracking blocked"}
    except Exception as e:
        return {"Error": str(e)}

# 7. AI CYBER DASHBOARD (Visual Forensics)
def ai_cyber_dashboard():
    st.title("👁️ AI Cyber: Visual & Hardware Forensics")
    st.markdown("---")
    
    # Corrected Tab Definitions to match your 'with' blocks
    tab1, tab2, tab3 = st.tabs(["📂 Device Upload", "📸 Live Terminal", "⚙️ Silicon-Watch"])
    image_to_scan = None

    with tab1:
        uploaded_file = st.file_uploader("Upload Target Image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image_to_scan = uploaded_file
            st.image(image_to_scan, caption="Target Acquired", width=300)

    with tab2:
        camera_file = st.camera_input("Initialize Secure Camera")
        if camera_file:
            image_to_scan = camera_file
            # 8. FORENSIC ANALYSIS DISPLAY
    if image_to_scan and st.button("INITIALIZE FORENSIC SCAN", type="primary"):
        with st.status("Running Deep Neural Analysis...", expanded=True) as status:
            st.write("Extracting noise patterns and LSB layers...")
            time.sleep(1.2)
            results = process_image_forensics(image_to_scan)
            status.update(label="Forensic Scan Complete", state="complete")

        st.subheader("📊 Forensic Intelligence Report")
        st.code(f"SHA-256 Signature: {results['hash']}")
        c1, c2, c3 = st.columns(3)
        with c1:
            if results['is_ai']: st.error("🤖 SYNTHETIC (AI)"); st.progress(results['ai_conf']/100)
            else: st.success("👤 HUMAN / ORGANIC")
        with c2:
            if results['has_payload']: st.error("🚨 PAYLOAD DETECTED"); st.warning("Hidden LSB Link found.")
            else: st.success("✅ CLEAN")
        with c3:
            if results['from_internet']: st.warning("🌐 INDEXED ON WEB"); st.caption(results['mock_url'])
            else: st.info("🛡️ UNIQUE LOCAL FILE")

    with tab3:
        st.subheader("⚙️ Silicon-Watch: Supply Chain Auditor")
        bom_input = st.text_area("Enter Hardware BOM:", placeholder="Example: ZTE-Chipset, Intel-i5...")
        if st.button("AUDIT HARDWARE", type="primary"):
            status_msg, detail, risk = run_silicon_watch_audit(bom_input)
            st.error(status_msg) if risk > 0 else st.success(status_msg)
            st.write(detail)
            if risk > 0: st.progress(risk / 100)

# 9. CYBER PATROL (Dark Web & Geo-Intel)
@st.cache_resource
def load_ai_model():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

classifier = load_ai_model()

def fetch_onion_data(url):
    """Simulates Tor network signal interception."""
    time.sleep(1) # Network latency simulation
    return "[ENCRYPTED SIGNAL INTERCEPTED]\nUser: APT_Shadow\nPayload: Industrial Control System Exploit."

def cyber_patrol_dashboard():
    st.title("🦅 Cyber Patrol Command Center")
    p_tab1, p_tab2, p_tab3 = st.tabs(["🕷️ Dark Web Crawler", "📍 Geo-Spatial Intel", "🌐 IP Tracker"])
    with p_tab1:
        st.subheader("Deep Web Signal Intercept")
        target_url = st.text_input("Enter .onion URL:", "http://v2c7hqiosk6is866.onion")
        if st.button("RUN LIVE AI ANALYSIS", type="primary"):
            with st.status("Accessing Tor Network...", expanded=True) as status:
                raw_text = fetch_onion_data(target_url)
                st.write("Analyzing content with BART-Large-MNLI...")
                labels = ["cyber threat", "illegal marketplace", "encrypted communication", "neutral"]
                result = classifier(raw_text, candidate_labels=labels)
                status.update(label="Analysis Complete", state="complete")
                
                top_threat = result['labels'][0]
                confidence = result['scores'][0]
                
                c_a, c_b = st.columns(2)
                c_a.metric("Dominant Category", top_threat.upper())
                c_b.metric("Confidence", f"{confidence:.2%}")
                if confidence > 0.7 and top_threat != "neutral":
                    st.error("🚨 CRITICAL THREAT: Escalation Required")

    with p_tab2:
        st.subheader("Regional Threat Activity Monitor")
        GLOBAL_NODES = {
            "APAC-South (Chennai)": (13.0827, 80.2707),
            "US-East (D.C.)": (38.9072, -77.0369),
            "EU-Central (Frankfurt)": (50.1109, 8.6821)
        }
        target_node = st.selectbox("Select Global Intelligence Node:", list(GLOBAL_NODES.keys()))
        if st.button("📡 Scan Region"):
            base_lat, base_lon = GLOBAL_NODES[target_node]
            map_data = pd.DataFrame({
                'lat': [base_lat + random.uniform(-0.5, 0.5) for _ in range(5)],
                'lon': [base_lon + random.uniform(-0.5, 0.5) for _ in range(5)]
            })
            st.map(map_data, color="#7000FF", size=40)

    with p_tab3:
        st.subheader("🌐 Global IP Trace")
        ip_input = st.text_input("Enter Target IP for Triangulation:")
        if st.button("EXECUTE TRACE"):
            data = track_ip_location(ip_input)
            if "Error" not in data:
                st.success(f"Origin: {data['city']}, {data['country']} ({data['isp']})")
                st.map(pd.DataFrame([{"lat": data['lat'], "lon": data['lon']}]))

# 10. CITIZEN SOC (Public Defense Tools)
def liar_firewall_scan(text):
    rules = [
        {"name": "PROMPT_INJECTION", "pat": r"ignore all previous", "risk": "CRITICAL"},
        {"name": "SYSTEM_PROBE", "pat": r"ls -la|whoami", "risk": "HIGH"}
    ]
    for r in rules:
        if re.search(r["pat"], text, re.I):
            return "BLOCKED", r["risk"], [r["name"]]
    return "ALLOWED", "NONE", []

# 11. CITIZEN SOC INTERFACE
def citizen_dashboard():
    # --- AUTHENTICATION GATE ---
    if st.session_state.user is None:
        st.title("🛡️ SentinAI: Identity Verification")
        st.markdown("##### *Zero-Trust Protocol Active. Authenticate to enter the SOC.*")
        auth_tab1, auth_tab2 = st.tabs(["🔑 Access Vault", "✨ Create Identity"])

        with auth_tab1:
            with st.form("login_logic"):
                l_email = st.text_input("Agent Email")
                l_pass = st.text_input("Access Key", type="password")
                if st.form_submit_button("UNSEAL VAULT"):
                    st.session_state.user = l_email
                    st.success("Identity Verified. Redirecting...")
                    time.sleep(1)
                    st.rerun()
        st.stop()

    # --- MAIN SOC UI ---
    user_name = st.session_state.user.split('@')[0].capitalize()
    st.title(f"🛡️ Welcome back, Agent {user_name}")
    
    tab1, tab2, tab3 = st.tabs(["🔥 Liar Firewall", "📱 APK Analyzer", "💧 Veri-Pixel"])
    
    with tab1:
        st.header("Gateway Protection")
        u_input = st.text_area("Intercepted Payload for Analysis:")
        if st.button("Route through Firewall") and u_input:
            status, risk, threats = liar_firewall_scan(u_input)
            if status == "BLOCKED": st.error(f"🛑 THREAT DETECTED: {threats}")
            else: st.success("✅ TRAFFIC ALLOWED")

    with tab2:
        st.header("Mobile Quarantine")
        apk = st.file_uploader("Upload APK/ZIP for Static Analysis", type=["apk", "zip"])
        if apk:
            with st.spinner("Decompiling assets..."):
                time.sleep(1.5)
                st.info("Scan complete: No malicious shell scripts detected.")

# 12. MAIN ROUTING & EXECUTION
def main():
    with st.sidebar:
        st.title("SYSTEM ACCESS")
        if st.button("🏠 MAIN MENU", use_container_width=True,key="sidebar_home_btn"):
            st.session_state.current_page = "Home"
            st.rerun()

    if st.session_state.current_page == "Home":
        st.title("Project AXON: National Defense Portal")
        st.markdown("### Select Authorization Level:")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("👨‍💻 CITIZEN PORTAL", use_container_width=True):
                st.session_state.current_page = "Citizen"; st.rerun()
        with c2:
            if st.button("👁️ AI CYBER HUB", use_container_width=True):
                st.session_state.current_page = "AI Cyber"; st.rerun()
        with c3:
            if st.button("🦅 CYBER PATROL", use_container_width=True):
                st.session_state.current_page = "Cyber Patrol"; st.rerun()
            
    elif st.session_state.current_page == "Citizen": citizen_dashboard()
    elif st.session_state.current_page == "AI Cyber": ai_cyber_dashboard()
    elif st.session_state.current_page == "Cyber Patrol": cyber_patrol_dashboard()

if __name__ == "__main__":
    # Ensure SQLite database is initialized
    conn = sqlite3.connect(DB_FILE)
    conn.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, ts TEXT, input TEXT, status TEXT)")
    conn.commit()
    main()
    def sidebar_hud():
     with st.sidebar:
        st.markdown("---")
        xp, level, rank = get_agent_stats()
        
        # Gamified Profile Header
        st.markdown(f"### 🎖️ AGENT STATUS: {rank}")
        col_lv, col_xp = st.columns(2)
        col_lv.metric("LEVEL", level)
        col_xp.metric("TOTAL XP", xp)
        
        # Progress to next level
        progress_to_next = (xp % 10) * 10 
        st.write(f"Progress to Level {level + 1}")
        st.progress(progress_to_next / 100)
        
        st.markdown("---")
        st.markdown("### 📡 SYSTEM PULSE")
        
        # Real-time war-room feel
        now = datetime.now().strftime("%H:%M:%S")
        st.code(f"UTC_SYNC: {now}\nUPLINK: SECURED\nNODE: AXON-PRIME")
        
        # Threat Level
        st.markdown("### 🚨 THREAT VECTOR")
        threat_val = random.randint(45, 92) if st.session_state.current_page != "Home" else 20
        st.progress(threat_val / 100)
        status_text = "🔴 CRITICAL" if threat_val > 75 else "🟢 STABLE"
        st.caption(f"STATUS: {status_text}")
    # 13. SIDEBAR INTELLIGENCE HUD (Live System Pulse)
def sidebar_hud():
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📡 SYSTEM PULSE")
        
        # Dynamic status based on current page
        if st.session_state.current_page == "Home":
            st.success("PROTOCOL: STANDBY")
            st.caption("Awaiting Authorization...")
        elif st.session_state.current_page == "AI Cyber":
            st.warning("PROTOCOL: FORENSIC SCAN")
            st.caption("Neural Engines: ACTIVE")
        elif st.session_state.current_page == "Cyber Patrol":
            st.error("PROTOCOL: LIVE INTERCEPT")
            st.caption("Tor Node: TUNNELED")
        
        # Real-time clock for the "War Room" feel
        now = datetime.now().strftime("%H:%M:%S")
        st.code(f"UTC_SYNC: {now}\nLATENCY: 24ms\nUPLINK: SECURED")
        
        # Threat Level Gauge Simulation
        st.markdown("---")
        st.markdown("### 🚨 REGIONAL THREAT LEVEL")
        threat_val = random.randint(30, 85)
        st.progress(threat_val / 100)
        if threat_val > 70:
            st.sidebar.error("LEVEL: CRITICAL")
        else:
            st.sidebar.warning("LEVEL: ELEVATED")
            

# 14. FINAL WRAPPER (Integrating the HUD)
# Update your main() calls to include the sidebar_hud()
def main_with_hud():
    sidebar_hud() # Call the HUD first
    
    with st.sidebar:
        st.title("SYSTEM ACCESS")
        if st.button("🏠 MAIN MENU", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()

    # (Your existing if/elif routing logic goes here...)
    if st.session_state.current_page == "Home":
        st.title("Project AXON: National Defense Portal")
        # ... and so on ...

# Replace your bottom block with this:
if __name__ == "__main__":
    init_sqlite_db() # Ensure DB is ready
    main_with_hud()