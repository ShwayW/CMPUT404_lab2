import requests
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

def main():
	try:
		host = "www.google.com"
		port = 80
		payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
		buffer_size = 4096
		# create socket
		s = create_tcp_socket()
		# get the remote IP address
		remote_ip = get_remote_ip(host)
		# connect to the remote ip through port
		s.connect((remote_ip, port))
		print(f'Socket Connected to {host} on ip {remote_ip}')

		# send data and shut down
		send_data(s, payload)

		# continue to accept data until no more left
		full_data = b""
		while True:
			data = s.recv(buffer_size)
			if not data:
				break
			full_data += data
		print(full_data)
	except Exception as e:
		print(e)
	finally:
		# always close at the end
		s.close()

if __name__ == "__main__":
	main()

