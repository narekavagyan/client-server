import json
import logging
import socket
import threading
import uuid

logging.basicConfig(filename="out.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

HOST = "127.0.0.1"
IDENTIFIER_PORT = 8000
MESSAGE_PORT = 8001

CLIENTS = {}


def manage_identifier_client(conn, addr):
    with conn:
        logger.info(f"New identifier connection {addr}")
        data = conn.recv(1024)
        if data:
            identifier = data.decode()
            code = str(uuid.uuid4())
            CLIENTS[identifier] = code
            conn.sendall(code.encode())


def manage_message_client(conn, addr):
    with conn:
        logger.info(f"New message connection {addr}")
        data = conn.recv(1024)
        if data:
            data = json.loads(data.decode())
            identifier = data.get("identifier")
            if CLIENTS.get(identifier) == data.get("code"):
                CLIENTS.pop(identifier)
                logger.info(f"Message from client {addr}({identifier=}):  {data.get('message')}")
            else:
                logger.info(f"Invalid code from connection {addr}: {identifier=}")
                conn.sendall("Invalid code".encode())
            conn.close()


def run_identifier_server():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, IDENTIFIER_PORT))
            s.listen()
            conn, addr = s.accept()
            threading.Thread(target=manage_identifier_client, args=(conn, addr)).start()


def run_message_server():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, MESSAGE_PORT))
            s.listen()
            conn, addr = s.accept()
            threading.Thread(target=manage_message_client, args=(conn, addr)).start()


threading.Thread(target=run_identifier_server).start()
threading.Thread(target=run_message_server).start()
