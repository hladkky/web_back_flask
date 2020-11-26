import socket
import json
import threading
from constants import PORT, HOST, MSG_LENGTH, FORMAT, NUM_OF_CLIENTS


def client_session(id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        # try:
        client.connect((HOST, PORT))
        message_structure = {
            'client_id': id,
            'text': f'I am client #_{id + 1}'
        }
        message = json.dumps(message_structure).encode(FORMAT)
        client.sendall(message)
        full_reply = b""
        reply = client.recv(MSG_LENGTH)
        while reply:
            full_reply += reply
            reply = client.recv(MSG_LENGTH)
        full_reply = json.loads(full_reply.decode(FORMAT))
        print(
            f'Client with id {id} has got information:',
            json.dumps(full_reply, indent=2)
        )
        # except:
        #     print(f'Client with id {id} has lost connection.')


for i in range(NUM_OF_CLIENTS):
    th = threading.Thread(target=client_session, args=(i,))
    th.start()
