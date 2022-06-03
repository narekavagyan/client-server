import json
import socket
import uuid

HOST = "127.0.0.1"
IDENTIFIER_PORT = 8000
MESSAGE_PORT = 8001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, IDENTIFIER_PORT))
    identifier = str(uuid.uuid4())
    s.sendall(identifier.encode())
    data = s.recv(1024)
    code = data.decode()
    s.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, MESSAGE_PORT))

    data = {
        "identifier": identifier,
        "code": code,
        "message": "Hello"
    }

    s.sendall(json.dumps(data).encode())

    data = s.recv(1024)
    code = data.decode()
    s.close()
