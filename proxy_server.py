import socket
import time
import sys

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

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
		print("failed to send payload")
		sys.exit()
	print("Payload sent successfully")

def make_request(payload):
	# forwarding:
	ps = create_tcp_socket()
	ps_ip = get_remote_ip('www.google.com')
	ps.connect((ps_ip, 80))
	print(f'Proxy Socket Connected to {payload} on ip {ps_ip}')
	send_data(ps, payload.decode("utf-8"))
	# the data from google:
	full_data = b""
	while True:
		data = ps.recv(BUFFER_SIZE)
		if not data:
			break
		full_data += data
	ps.close()
	return full_data

def main():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# able to re-use the binding port
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		# bind to the host to its port
		s.bind((HOST, PORT))
		s.listen(2)
		while True:
			conn, addr = s.accept()
			print("Connected by", addr)
			full_data = b""
			while True:
				data = conn.recv(BUFFER_SIZE)
				if not data:
					break
				full_data += data
			result_data = make_request(full_data)
			conn.sendall(result_data)
			conn.close()
	except Exception as e:
		print(e)
	finally:
		s.close()

if __name__ == "__main__":
	main()