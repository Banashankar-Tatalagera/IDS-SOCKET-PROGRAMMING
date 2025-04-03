import socket
import threading
import time

# IDS Configuration
BLOCK_THRESHOLD = 10  # Max allowed requests in 5 seconds
BLOCK_TIME = 10  # Block duration in seconds

request_counts = {}  # Tracks requests per IP
blocked_ips = {}  # Stores blocked IPs with unblock timestamps
server_socket = None
running = False  # Controls server state

def detect_attack(client_socket, client_address, data):
    ip = client_address[0]

    # Check if IP is blocked
    if ip in blocked_ips and time.time() < blocked_ips[ip]:
        print(f"🚫 [BLOCKED] Dropping connection from {ip}.")
        client_socket.close()
        return

    # Unblock IP if time has passed
    if ip in blocked_ips and time.time() > blocked_ips[ip]:
        del blocked_ips[ip]

    # Track incoming requests
    if ip not in request_counts:
        request_counts[ip] = []
    
    request_counts[ip].append(time.time())

    # Keep only the last 5 seconds of request history
    request_counts[ip] = [t for t in request_counts[ip] if time.time() - t < 5]

    # Attack Detection
    if data == "SYN_FLOOD":
        print(f"⚠️ 🔃 SYN Flood detected from {ip}! 🌊")
    elif data == "UDP_FLOOD":
        print(f"⚠️ 📤📥 UDP Flood detected from {ip}! 🌊")
    elif data == "ICMP_FLOOD":
        print(f"⚠️ 📡💬 ICMP Ping Flood detected from {ip}! 🌊")

    # Detect DoS attack (too many requests in 5 seconds)
    elif len(request_counts[ip]) > BLOCK_THRESHOLD:
        print(f"🚨 [ALERT] DoS attack detected from {ip}! 🚀 Blocking for {BLOCK_TIME} seconds.")
        blocked_ips[ip] = time.time() + BLOCK_TIME
    else:
        print(f"✅ [INFO] Connection from {ip} accepted. 🔗")

    client_socket.close()

def start_server(host="0.0.0.0", port=9999):
    """Starts IDS server and listens for connections"""
    global server_socket, running
    running = True

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"🎯 [*] IDS Server started on {host}:{port}. Type 'stop' to shut down.")

    while running:
        try:
            server_socket.settimeout(1)  # Avoid blocking on accept
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024).decode('utf-8').strip()
            thread = threading.Thread(target=detect_attack, args=(client_socket, client_address, data))
            thread.start()
        except socket.timeout:
            continue
        except Exception as e:
            if running:
                print(f"⚠️ [ERROR] {e}")

def stop_server():
    """Stops the IDS server"""
    global running, server_socket
    running = False
    if server_socket:
        server_socket.close()
    print("🛑 [*] IDS Server stopped.")

def main():
    """Main function to control the IDS server"""
    while True:
        cmd = input("\n💻 Enter command (start/stop/exit): ").strip().lower()
        if cmd == "start":
            if not running:
                threading.Thread(target=start_server, daemon=True).start()
            else:
                print("🔄 [*] Server is already running.")
        elif cmd == "stop":
            stop_server()
        elif cmd == "exit":
            stop_server()
            print("👋 Exiting IDS. Stay secure!")
            break
        else:
            print("❌ [!] Invalid command. Use 'start', 'stop', or 'exit'.")

if __name__ == "__main__":
    main()
