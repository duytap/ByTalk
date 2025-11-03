import socket, threading, sys
from cryptography.fernet import Fernet

def key_from_pass(password: str):
    import base64, hashlib
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def send(sock, f):
    try:
        while True:
            msg = input("> ")
            if msg.strip().lower() == "exit": break
            sock.send(f.encrypt(msg.encode()))
    except: pass
    finally:
        sock.close(); sys.exit(0)

def recv(sock, f):
    try:
        while True:
            data = sock.recv(4096)
            if not data: break
            print("\nPeer:", f.decrypt(data).decode(), "\n> ", end="")
    except: pass
    finally:
        sock.close(); sys.exit(0)

def host(port, f):
    s = socket.socket()
    s.bind(("0.0.0.0", port))
    s.listen(1)
    print(f"waitting for connection at {socket.gethostbyname(socket.gethostname())}:{port}")
    conn, addr = s.accept()
    print("connected to", addr)
    threading.Thread(target=recv, args=(conn,f), daemon=True).start()
    send(conn,f)

def connect(ip, port, f):
    s = socket.socket()
    s.connect((ip, port))
    print("connected to host.")
    threading.Thread(target=recv, args=(s,f), daemon=True).start()
    send(s,f)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("How to use:\n host:   python bytalk.py host [port]\n client: python bytalk.py connect <ip> [port]")
        sys.exit(0)

    mode = sys.argv[1]
    port = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 9999
    password = input("Type password: ")
    f = Fernet(key_from_pass(password))

    if mode == "host":
        host(port,f)
    elif mode == "connect" and len(sys.argv) >= 3:
        connect(sys.argv[2],port,f)
    else:
        print("syntac error")

