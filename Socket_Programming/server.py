# Data: csv file containing communications data between
# spacecrafts and ground stations
# This server serves clients data from the file: comm_data.csv

import socket
import _thread as thread
import os
import pandas as pd


SEPARATOR = "<SEPARATOR>"

cols = ['ipaddress', 'src', 'dest', 'message', 'timestamp', 'priority']
df = pd.DataFrame(columns=cols)

df.astype({'priority': int})
if(os.stat("communications_data.csv").st_size != 0):
    df = pd.read_csv('communications_data.csv')


# df.index += 1


def add_row(conn_socket, timestamp, src, dest, message,  priority, ipaddress):
    priority = int(priority)
    df.loc[len(df.index)] = [ipaddress, src,
                             dest, message, timestamp, priority]
    df.to_csv('communications_data.csv', index=False)
    # conn_socket.send(bytes(df.to_string(), 'utf-8'))
    conn_socket.send(b"Added Row Successfully")
    try:
        pass
    except:
        conn_socket.send(b"Operation failed")


HOST = socket.gethostname()
PORT = 1234
ADDR = (HOST, PORT)
CHUNK_SIZE = 1024
FORMAT = 'utf-8'


# Init socket obj
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to address
server.bind(ADDR)


def send_all(conn_socket):
    conn_socket.send(bytes(df.to_string(), FORMAT))


def send_range(conn_socket):

    pass


def send_timestamp_range(conn_socket, date):
    new_df = df.loc[df["timestamp"].str.startswith(date)]
    conn_socket.send(bytes(new_df.to_string(), FORMAT))


def send_priority(conn_socket, priority):
    priority = int(priority)
    new_df = df.loc[df["priority"] >= priority]
    conn_socket.send(bytes(new_df.to_string(), FORMAT))


def send_src(conn_socket, src):
    srcdatadf = df.loc[df["src"] == src]
    conn_socket.send(bytes(srcdatadf.to_string(), FORMAT))


def send_dst(conn_socket, dst):
    destdatadf = df.loc[df["dest"] == dst]
    conn_socket.send(bytes(destdatadf.to_string(), FORMAT))

# Method to serve data to client


def on_new_client(clientsocket, addr, host):
    while True:
        msg = clientsocket.recv(1024).decode()
        args = msg.split(SEPARATOR)

        if(args[0] == "-1"):
            break
        elif(args[0] == "0"):
            add_row(clientsocket, args[1], args[2],
                    args[3], args[4], args[5], args[6])
        elif(args[0] == "1"):
            send_all(clientsocket)
        elif(args[0] == "2"):
            send_timestamp_range(clientsocket, args[1])
        elif(args[0] == "3"):
            send_priority(clientsocket, args[1])
        elif(args[0] == "4"):
            send_src(clientsocket, args[1])
        elif(args[0] == "5"):
            send_dst(clientsocket, args[1])

    clientsocket.close()


def start():
    # Listen for connections
    server.listen()
    print('[SERVER] Listening on:', ADDR)

    while True:
        conn, addr = server.accept()
        thread.start_new_thread(on_new_client, (conn, addr, HOST))


print('[SERVER] Starting...')
start()
