#!/usr/bin/python
#-*- encoding: utf-8 -*-
import socket

class MirrorClient:
	"A client for the mirror server."

	def __init__(self, server, port):
		"Connect to the given mirror server."
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((server, port))

	def mirror(self, s):
		if len(s) == 0:
			return "Please input something."

		"Sends the given string to the server, and prints the response."
		if s[-1] != '\n':
			s += '\r\n'
		self.socket.send(s)

		#Read server response in chunks until we get a newline; that
		#indicates the end of the response.
		buf = []
		input = ''

		while not '\n' in input:
			try:
				input = self.socket.recv(1024)
				buf.append(input)
			except socket.error:
				break
			return ''.join(buf)[:-1]

	def close(self):
		self.socket.send('\r\n') #We don't want to mirror anything else.
		self.socket.close()

if __name__ == '__main__':
	import sys
	if len(sys.argv) < 3:
		print 'Usage: %s [hostname] [port number]' % sys.argv[0]
		sys.exit(1)
	hostname = sys.argv[1]
	port = int(sys.argv[2])
	m = MirrorClient(hostname, port)
	while 1:
		msg = raw_input('Enter String: ')
		print m.mirror(msg)
	m.close()
