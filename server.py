"""
Code taken from: https://docs.python.org/2/library/asyncore.html#asyncore-example-basic-echo-server
Modified by Kyle Richelhoff
"""

import asyncore
import socket

class EchoHandler(asyncore.dispatcher_with_send):

	def handle_read(self):
		data = self.recv(8192)
		if data:
			formatted_data = data.strip()
			print("Got Message: {}".format(formatted_data))

			#Escape character closes the connection
			if formatted_data == chr(27):
				print("Closing connection.")
				self.close()
			else:
				self.send("{} {}\n".format(data.strip().encode("utf8"), "Kyle"))


class EchoServer(asyncore.dispatcher):

	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(5)

	def handle_accept(self):
		pair = self.accept()
		if pair is not None:
			sock, addr = pair
			handler = EchoHandler(sock)


if __name__ == "__main__":
	#Easier way to dispatch threads
	server = EchoServer('localhost', 9000)
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		print("Shutting down server...")

