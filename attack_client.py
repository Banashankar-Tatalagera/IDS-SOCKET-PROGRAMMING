import socket
import time
import streamlit as st
import threading

def send_requests(target_ip, target_port, attack_type, rate=1):
    """Simulates network traffic based on attack type"""
    st.write(f"🚀 Sending {attack_type} traffic to {target_ip}:{target_port} at {rate} req/sec")
    
    for _ in range(20):  # Number of requests to send
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.send(attack_type.encode('utf-8'))
            s.close()
            st.write(f"✅ Sent {attack_type} request.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        time.sleep(1 / rate)  # Control request rate

def main():
    st.title("IDS Traffic Simulator")
    
    target_ip = st.text_input("🎯 Enter IDS Server IP", "127.0.0.1")
    target_port = st.number_input("🎯 Enter IDS Server Port", min_value=1, max_value=65535, value=9999)
    
    st.subheader("🚦 Choose Traffic Type:")
    attack_type = st.selectbox("Select Attack Type", ["Normal Traffic", "SYN Flood", "UDP Flood", "ICMP Flood"])
    
    rate = 1
    if attack_type == "SYN Flood":
        rate = 10
    elif attack_type == "UDP Flood":
        rate = 20
    elif attack_type == "ICMP Flood":
        rate = 15
    
    if st.button("Start Attack"):
        threading.Thread(target=send_requests, args=(target_ip, target_port, attack_type.upper().replace(" ", "_"), rate), daemon=True).start()
        st.success(f"Started {attack_type} attack on {target_ip}:{target_port}")

if __name__ == "__main__":
    main()
