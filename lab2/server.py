import socket
import threading
import selectors
import json
import time
import types
from datetime import datetime, timedelta

from constants import PORT, HOST, MSG_LENGTH, FORMAT, TIMER_SECS


sel = selectors.DefaultSelector()
CLIENTS_SOCKETS = []
CLIENTS_CONNECTIONS = []
timer_first_connection = None


def handle_connection(sock):
    conn, addr = sock.accept()  # Should be ready to read
    # print(f'Client connection from: {addr}')
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, msg=b'')
    events = selectors.EVENT_READ
    sel.register(conn, events, data=data)
    CLIENTS_SOCKETS.append(conn)
    return f'[CONNECTION] {addr} connected on {datetime.now()}'


def service_operation(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(MSG_LENGTH)  # Should be ready to read
        # if recv_data:
        #     data.msg += recv_data
            # recv_data = sock.recv(MSG_LENGTH)
        recv_data = json.loads(recv_data.decode(FORMAT))
        data.id = recv_data['client_id']
        print(f'received: {recv_data}')

    # if mask & selectors.EVENT_WRITE:
    #     if data.out:
    #         clients_data = json.dumps({
    #             'client_id': data.id,
    #             'timer_date': timer_first_connection.strftime('%H:%M:%S.%f'),
    #             'clients_connections': CLIENTS_CONNECTIONS
    #         }).encode(FORMAT)
    #         sock.sendall(clients_data)
    #         data.out = False
    #         print("Closing connection to", data.addr)
    #         sel.unregister(sock)
    #         sock.close()
    


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print("[LISTENING] Server on", (HOST, PORT))
server.setblocking(False)
sel.register(server, selectors.EVENT_READ, data=None)

i = 0
while True:
    timeout = None
    if timer_first_connection:
        timeout = (
            timedelta(seconds=TIMER_SECS) - (datetime.now() - timer_first_connection)
        ).seconds
        if timeout > TIMER_SECS:
            timeout = 0.0
    
    events = sel.select(
        timeout=timeout
    )
    
    # print(events, len(CLIENTS_SOCKETS))
    if not events:
        print('okey')
        clients_data = {
            'clients_connections': CLIENTS_CONNECTIONS,
            'timer_date': timer_first_connection.strftime('%H:%M:%S.%f'),
        }
        for client in CLIENTS_SOCKETS:
            client.sendall(json.dumps(
                clients_data
            ).encode(FORMAT))
            sel.unregister(client)
            client.close()
            CLIENTS_SOCKETS.remove(client)
    else:
        for key, mask in events:
            # print(key.data, mask)
            if key.data is None:
                # print(f'receiving: {i}')
                i+=1
                CLIENTS_CONNECTIONS.append(handle_connection(key.fileobj))
                if not timer_first_connection:
                    timer_first_connection = datetime.now()
            else:
                service_operation(key, mask)
