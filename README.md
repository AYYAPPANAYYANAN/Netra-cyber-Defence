# 🛡️ Netra: Cyber Defense (Project AXON)

**Netra: Cyber Defense** (also known as Project AXON) is a gamified, AI-powered Security Operations Center (SOC) dashboard built with Streamlit. It simulates an advanced national defense portal, featuring real-time IP tracking, AI-driven dark web content classification, hardware supply chain auditing, and visual forensics.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-F9AB00.svg)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)

---

## ✨ Core Features

### 👁️ AI Cyber: Visual & Hardware Forensics
* **Image Forensics:** Analyzes uploaded images or live camera captures for AI generation signatures and hidden steganographic payloads (LSB).
* **Silicon-Watch (Supply Chain Auditor):** Scans Hardware Bills of Materials (BOM) to detect restricted or high-risk hardware vendors (e.g., Huawei, ZTE, Hikvision) to ensure compliance with security protocols.

### 🦅 Cyber Patrol Command Center
* **Dark Web Crawler:** Simulates interception of `.onion` traffic and uses an integrated NLP model (`facebook/bart-large-mnli`) to classify payloads as cyber threats, illegal marketplaces, or neutral communications.
* **Geo-Spatial Intel:** Visualizes regional threat activity nodes across the globe on an interactive map.
* **Global IP Trace:** Tracks and triangulates suspicious IP addresses in real-time using external geolocation APIs.

### 👨‍💻 Citizen SOC
* **Zero-Trust Identity Vault:** A simulated secure gateway for agent authentication.
* **Liar Firewall:** A regex-based firewall designed to detect and block malicious prompt injections (e.g., "ignore all previous instructions") and system probes.
* **APK Analyzer:** A quarantine zone for static analysis of mobile application packages.

### 🎮 Gamified Agent HUD
* **Agent Progression:** Tracks user actions in a local SQLite database (`sentinai_soc.db`) to award XP, leveling up users from "Novice" to "Cyber Commander."
* **Live System Pulse:** A dynamic sidebar HUD displaying simulated network latency, threat vectors, and real-time UTC sync.

---

## 🚀 Installation & Setup

**1. Clone the repository**

``bash
git clone [https://github.com/yourusername/netra-cyber-defense.git](https://github.com/yourusername/netra-cyber-defense.git)
cd netra-cyber-defense

### 2. Create a virtual environment ###
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

### 3. Install dependencies
Create a requirements.txt file with the following packages, or install them directly:

Bash
pip install streamlit supabase requests beautifulsoup4 transformers pandas Pillow torch torchvision torchaudio
(Note: PyTorch is required to run the Hugging Face Transformers pipeline).

### 4. Run the application

Bash
streamlit run app.py
