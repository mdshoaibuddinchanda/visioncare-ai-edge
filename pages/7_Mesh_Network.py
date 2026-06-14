"""
Mesh Network Simulation for Peer-to-Peer Database Sync.
"""
import streamlit as st
import time
from utils.styles import load_css, section_header, info_message

def show():
    load_css()
    
    st.markdown('<div class="main-header" style="font-family:monospace; text-transform:uppercase;">[MODULE 05] LOCAL MESH NETWORK (P2P)</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header" style="font-family:monospace;">> OFFLINE WEBRTC CRDT SYNCHRONIZATION</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("""
    <div class="card" style="border-left: 4px solid #00ffcc; padding: 1.5rem; background-color: #0a0a0a;">
        <h4 style="margin-top:0; color:#00ffcc; font-family:monospace;">[SYS] NETWORK STATUS: DISCONNECTED</h4>
        <p style="font-family:monospace; color:#888; font-size:0.9rem;">
            This terminal initializes the discovery protocol (mDNS) across the local subnet. 
            When active, Edge Terminals will automatically negotiate secure WebRTC data channels 
            and exchange SQLite CRDT (Conflict-free Replicated Data Type) deltas to ensure 
            100% data parity across the clinic without internet access.
        </p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    if st.button("[>] INITIATE LOCAL NODE DISCOVERY", use_container_width=True, type="primary"):
        terminal_container = st.empty()
        
        # Sequence of terminal lines and their delays
        sequence = [
            ("> Broadcasting mDNS discovery packets on subnet 192.168.1.x...", 0.6),
            ("> Listening for ACK...", 0.8),
            ("<span style='color:#00ffcc;'>[+] Found Node: CLINIC-STATION-B (192.168.1.104)</span>", 0.4),
            ("<span style='color:#00ffcc;'>[+] Found Node: CLINIC-STATION-C (192.168.1.112)</span>", 0.5),
            ("> Establishing secure WebRTC data channels via DTLS/SRTP...", 0.9),
            ("<span style='color:#00ffcc;'>[OK] Encrypted Handshake Successful (AES-256).</span>", 0.6),
            ("> Calculating SQLite CRDT Deltas (Vector Clock Comparison)...", 1.1),
            ("> Resolving distributed database conflicts...", 0.7),
            ("<span style='color:#ff9800;'>[SYNC] Transmitting 4 local telemetry logs to peers...</span>", 0.5),
            ("<span style='color:#00ffcc;'>[+] Pulled 14 new patient telemetry logs from MESH network.</span>", 0.8),
            ("<span style='color:#00ffcc;'>[OK] LOCAL DATABASE FULLY SYNCHRONIZED.</span>", 0.2),
        ]
        
        output_html = "<div class='card' style='background-color:#000; border: 1px solid #333; font-family:monospace; font-size:0.9rem; padding: 1rem;'>"
        
        for text, delay in sequence:
            output_html += f"<div style='margin-bottom:0.4rem;'>{text}</div>"
            terminal_container.markdown(output_html + "<span class='blink'>_</span></div>", unsafe_allow_html=True)
            time.sleep(delay)
            
        # Final render without blinking cursor
        terminal_container.markdown(output_html + "</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("[SYS] MESH NETWORK ESTABLISHED. Background syncing active.")
        
    st.markdown("""
    <div class="footer" style="margin-top: 3rem;">
        V2 Architecture Protocol | © VisionCare AI
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()
