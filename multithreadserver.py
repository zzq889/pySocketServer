#!/usr/bin/python
#-*- encoding: utf-8 -*-

import socket
import threading
import SocketServer

class RequestHandler(SocketServer.StreamRequestHandler):
	"Handles one request to mirror some text."

	def handle(self):
		"""Read from StreamRequestHandler's provided rfile member,
		which contains the input from the client. Mirror the text
		and write it to the wfile member, which contains the output
		to be sent to the client."""
		l = True
		while l:
			l = self.rfile.readline().strip()
			if l:
				try:
					int(l)
					msg = l
					if len(msg) == 1:
						self.wfile.write(msg + '\n')
					while len(msg) > 1:
						sum = 0
						for x in list(msg):
							sum += int(x)
						msg = str(sum)
						self.wfile.write(msg + '\n')
				except:
					self.wfile.write('Sorry, cannot compute!\n')

if __name__ == '__main__':
	import sys
	if len(sys.argv) < 3:
		print 'Usage: %s [hostname] [port number]' % sys.argv[0]
		sys.exit(1)

	hostname = sys.argv[1]
	port = int(sys.argv[2])
	server = SocketServer.ThreadingTCPServer((hostname, port), RequestHandler)
	print " * Server Running On", hostname+":"+sys.argv[2]
	server.serve_forever()
