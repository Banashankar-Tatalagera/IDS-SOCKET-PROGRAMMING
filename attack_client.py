import socket
import time

def send_requests(target_ip, target_port, attack_type, rate=1):
    """Simulates network traffic based on attack type"""
    print(f"🚀 Sending {attack_type} traffic to {target_ip}:{target_port} at {rate} req/sec")
    
    for _ in range(20):  # Number of requests to send
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.send(attack_type.encode('utf-8'))
            s.close()
            print(f"✅ Sent {attack_type} request.")
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(1 / rate)  # Control request rate

if __name__ == "__main__":
    print("🌐 Welcome to IDS Traffic Simulator")
    
    target_ip = input("🎯 Enter IDS Server IP (e.g., 127.0.0.1 or 192.168.x.x): ")
    target_port = int(input("🎯 Enter IDS Server Port (default: 9999): "))

    print("\n🚦 Choose Traffic Type:")
    print("1️⃣ Normal Traffic (1 req/sec) 🟢")
    print("2️⃣ SYN Flood (10 req/sec) 🔃")
    print("3️⃣ UDP Flood (20 req/sec) 📤📥")
    print("4️⃣ ICMP Flood (15 req/sec) 📡💬")
    
    choice = input("🔽 Enter your choice (1-4): ")

    if choice == "1":
        print("🟢 Sending Normal Traffic...")
        send_requests(target_ip, target_port, "NORMAL", rate=1)
    elif choice == "2":
        print("🔃 Launching SYN Flood Attack...")
        send_requests(target_ip, target_port, "SYN_FLOOD", rate=10)
    elif choice == "3":
        print("📤📥 Launching UDP Flood Attack...")
        send_requests(target_ip, target_port, "UDP_FLOOD", rate=20)
    elif choice == "4":
        print("📡💬 Launching ICMP Flood Attack...")
        send_requests(target_ip, target_port, "ICMP_FLOOD", rate=15)
    else:
        print("❌ Invalid choice! Please enter a number between 1-4.")
