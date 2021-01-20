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
		host = "localhost"
		destination = 'www.google.com'
		payload = f"GET / HTTP/1.0\r\nHost: {destination}\r\n\r\n"
		port = 8001
		buffer_size = 4096

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
	except Exception as e:
		print(e)
	finally:
		# always close at the end
		s.close()
		print("client closed")

if __name__ == "__main__":
	main()

