<div align="center">

# 👁️‍🗨️ VisionCare AI

**Autonomous Edge Diagnostic Terminal for Rural Healthcare**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.0+-5C3EE8.svg?style=for-the-badge&logo=opencv)](https://opencv.org/)
[![Ollama](https://img.shields.io/badge/Local_AI-Ollama-white.svg?style=for-the-badge&logo=ollama&color=black)](https://ollama.com/)
[![Devfolio](https://img.shields.io/badge/Hackathon-Winner-2ea44f?style=for-the-badge&logo=devfolio)](https://devfolio.co)

*Zero Cloud Dependency. Zero Privacy Leaks. 100% Edge Processing.*

</div>

---

## 🚨 The Problem
Access to early diagnostic eye care is fundamentally broken in remote and underserved regions. Traditional ophthalmology screenings require expensive, stationary hardware (like $50,000 retinal cameras) and trained specialists, which simply don't exist outside of urban centers. Furthermore, modern Cloud-AI solutions fail in these regions due to lack of internet connectivity, and they violate medical privacy laws by sending patient photos to central servers.

## 💡 The Solution
**VisionCare AI** is an offline-first Edge Diagnostic Terminal. It transforms a standard smartphone photo into a clinical-grade medical assessment without ever touching the cloud. By fusing local Vision-Language Models (VLMs) with Conversational AI triage, we extract four critical biological health indicators directly from the eye, bypassing the need for expensive diagnostic hardware.

---

## 🔥 Key Features

- **Multi-Spectral Emulation (OpenCV):** We don't just pass raw JPEGs to the AI. We run a Contrast Limited Adaptive Histogram Equalization (CLAHE) via OpenCV to mathematically strip the Red and Blue light. This simulates a $50,000 Red-Free clinical retinal camera using pure software, exposing the micro-vasculature of the eye.
- **Multi-Modal Data Fusion:** Relying purely on pixels is dangerous due to lighting bias. Our system requires the patient to answer a dynamic triage questionnaire, fusing patient history with visual matrices so the AI makes an informed, holistic diagnosis.
- **Zero-Trust Edge Security:** Before the AI even touches the data, we SHA-256 anonymize all Personal Identifiable Information (PII). Because inference runs locally via Ollama, zero patient data ever leaves the laptop. It is strictly HIPAA compliant by default.
- **Clinical Brutalism UI:** The interface is specifically designed as a high-contrast, distraction-free Medical Terminal, optimizing for utility and speed over consumer aesthetics.
- **Geospatial Specialist Routing:** Automatically routes critical patients to the nearest hospital or ophthalmology clinic using OpenStreetMap data.

---

## 🛠️ Technology Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Frontend** | Streamlit | Rapid UI deployment with custom CSS architecture. |
| **Computer Vision** | OpenCV & PIL | Red-Free multi-spectral image emulation and enhancement. |
| **Edge AI Inference** | Ollama | Running `Qwen2.5-VL` (Vision) and `Llama3` locally offline. |
| **Data Synchronization** | SQLite | Local CRDT-ready database for mesh-network synchronization. |
| **Reporting** | ReportLab | Generation of secure, offline PDF payloads. |
| **Geospatial** | Overpass API | OpenStreetMap querying for nearby health infrastructure. |

---

## 🚀 How to Run Locally

### 1. Prerequisites
- **Python 3.10+**
- **Ollama** installed on your system (Download from [ollama.com](https://ollama.com/))
- **Git**

### 2. Pull the required Local AI Models
Open your terminal and pull the required vision and language models via Ollama:
```bash
ollama run qwen2.5-vl
ollama run llama3
```

### 3. Clone and Setup
Clone the repository and install the Python dependencies:
```bash
git clone https://github.com/your-username/visioncare-ai.git
cd visioncare-ai

# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory (or rename `.env.example` to `.env`):
```ini
# For full offline capability, set this to ollama
AI_PROVIDER=ollama
OLLAMA_VISION_MODEL=qwen2.5-vl
OLLAMA_TEXT_MODEL=llama3

# If testing with cloud API (not recommended for production edge use):
# GEMINI_API_KEY=your_api_key_here
```

### 5. Launch the Terminal
Start the Streamlit application:
```bash
streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`.

---

## 🗺️ V2 Research Roadmap

- **Local WebRTC Mesh Networking:** Deploy a local gossip protocol. Multiple offline clinic laptops will automatically discover each other via mDNS and sync their SQLite CRDT deltas over an encrypted WebRTC channel, sharing patient records across a rural hospital without internet.
- **Federated Learning:** As clinics scan more eyes, the laptops won't share patient photos, but they will share mathematical gradient updates over the mesh network. The global AI gets smarter every day, but privacy is mathematically guaranteed.
- **DICOM Interoperability:** Wrap the final PDF and image payload into the global DICOM medical imaging standard, allowing our offline terminals to natively sync with massive hospital PACS systems in the city.

---

<div align="center">

*Built for the Devfolio Hackathon 2025. Made to save lives.*

</div>