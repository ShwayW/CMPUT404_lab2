from multiprocessing import Process
import socket
import sys

# create a tcp socket
def create_tcp_socket():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM means we want tcp socket
	except(socket.error, msg):
		print("failed to create socket")
		sys.exit()
	print("socket created successfully")
	return s

# get host info
def get_remote_ip(host):
	try:
		remote_ip = socket.gethostbyname(host)
	except socket.gaierror:
		print("failed to get remote ip")
		sys.exit()
	print("successfully got remote ip")
	return remote_ip

def send_data(serversocket, payload):
	try:
		serversocket.sendall(payload.encode())
	except socket.error:
		sys.exit()
	print("Payload sent successfully")

def client_action():
	host = "localhost"
	destination = 'www.google.com'
	payload = f"GET / HTTP/1.0\r\nHost: {destination}\r\n\r\n"
	port = 8001
	buffer_size = 4096
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s = create_tcp_socket()
		remote_ip = get_remote_ip(host)
		s.connect((remote_ip, port))
		print(f'Socket Connected to {host} on ip {remote_ip}')
		# send data and shut down
		send_data(s, payload)
		s.shutdown(socket.SHUT_WR)
		# continue to accept data until no more left
		full_data = b""
		while True:
			data = s.recv(buffer_size)
			if not data:
				break
			full_data += data
		print(str(full_data))
	print("client closed")

def main():
	clients = [];
	n = 10 # number of clients
	for i in range(n):
		p = Process(target = client_action)
		clients.append(p)
		p.start()
	for i in range(len(clients)):
		p = clients.pop()
		print(len(clients))
		p.join()
		

if __name__ == "__main__":
	main()

