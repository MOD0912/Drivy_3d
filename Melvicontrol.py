import socket
import threading
import time
import queue

HOST = "0.0.0.0"   # listen on all interfaces
PORT = 9999        # pick a port that's open on your machine
CALLBACK_PORT = 5003 # Port for receiving events from the remote controller

# Target (socket_client_test.py)
TARGET_IP = "127.0.0.1"
TARGET_PORT = 5002

# Queue to store incoming events for main.py to process
event_queue = queue.Queue()

def get_events():
    """Returns a list of all pending events."""
    events = []
    try:
        while True:
            events.append(event_queue.get_nowait())
    except queue.Empty:
        pass
    return events

def start_event_listener():
    """Starts a server to listen for events from socket_client_test.py."""
    def listener_loop():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("0.0.0.0", CALLBACK_PORT))
                s.listen()
                print(f"Melvicontrol Callback Listener on port {CALLBACK_PORT}")
                while True:
                    conn, _ = s.accept()
                    with conn:
                        data = conn.recv(1024).decode(errors='ignore').strip()
                        if data:
                            print(f"Received Event: {data}")
                            event_queue.put(data)
            except Exception as e:
                print(f"Callback Listener Failed: {e}")

    t = threading.Thread(target=listener_loop, daemon=True)
    t.start()

start_event_listener() # Auto-start listener on import

def send_to_target(cmd):
    """Connects to socket_client_test.py and sends the command."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((TARGET_IP, TARGET_PORT))
            s.sendall(cmd.encode('utf-8'))
    except Exception as e:
        print(f"Failed to forward to target: {e}")

def drive_up():
    print("drive_up() called -> Forwarding UP")
    send_to_target("UP")

def drive_down():
    print("drive_down() called -> Forwarding DOWN")
    send_to_target("DOWN")

def drive_left():
    print("drive_left() called -> Forwarding LEFT")
    send_to_target("LEFT")

def drive_right():
    print("drive_right() called -> Forwarding RIGHT")
    send_to_target("RIGHT")

def stop():
    print("stop() called -> Forwarding STOP")
    send_to_target("STOP")

def run_self_test():
    """Tests all functions sequentially with more power and duration."""
    print("--- STARTING SELF TEST (Ensure socket_client_test.py is running) ---")
    time.sleep(2)
    
    # Drive UP - Spam to accelerate
    print("Accelerating UP...")
    for _ in range(5): # Spam 10 times to reach max speed
        drive_up()
        time.sleep(0.05)
    time.sleep(3) # Drive for 3 seconds at high speed
    
    time.sleep(1)
    
    # Drive LEFT
    print("Accelerating LEFT...")
    for _ in range(10):
        drive_left()
        time.sleep(0.05)
    time.sleep(3)
    time.sleep(1)
    
    # Drive RIGHT
    print("Accelerating RIGHT...")
    for _ in range(20):
        drive_right()
        time.sleep(0.05)
    time.sleep(3)
    stop()
    time.sleep(1)
    
    # Drive DOWN
    print("Accelerating DOWN...")
    for _ in range(5):
        drive_down()
        time.sleep(0.05)
    time.sleep(3)
    stop()
    
    print("--- SELF TEST COMPLETE ---")


def handle_command(cmd):
    """Map text command to drive functions."""
    cmd = cmd.strip().upper()
    if cmd in ("UP", "FORWARD"):
        drive_up()
        return "OK\n"
    if cmd in ("DOWN", "BACK", "BACKWARD"):
        drive_down()
        return "OK\n"
    if cmd in ("LEFT",):
        drive_left()
        return "OK\n"
    if cmd in ("RIGHT",):
        drive_right()
        return "OK\n"
    if cmd in ("STOP",):
        stop()
        return "OK\n"
    return "UNKNOWN COMMAND\n"

def client_thread(conn, addr):
    with conn:
        print("Connected:", addr)
        buffer = b""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buffer += data
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                cmd = line.decode(errors="ignore")
                resp = handle_command(cmd)
                try:
                    conn.sendall(resp.encode())
                except Exception:
                    pass
        print("Disconnected:", addr)

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    try:
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=client_thread, args=(conn, addr), daemon=True)
            t.start()
    finally:
        s.close()

if __name__ == "__main__":
    run_self_test()

    start_server()