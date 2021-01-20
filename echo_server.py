from multiprocessing import Process
import socket
import time
import sys

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		s.bind((HOST, PORT))
		s.listen(2)
		while True:
			conn, addr = s.accept()
			print("Connected by", addr)

			full_data = conn.recv(BUFFER_SIZE)
			print(full_data)
			time.sleep(0.5)
			conn.sendall(full_data)
			conn.close()

if __name__ == "__main__":
	main()