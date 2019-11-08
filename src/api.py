import os, os.path
import cherrypy
import pandas as pd
from baseconv import base62

import mysql.connector

class Api(object):


	# Used to redirect users to long url
	@cherrypy.expose
	def default(self, *url_parts, **params):
		if len(url_parts) > 1:
			raise cherrypy.HTTPError(status=400)
		
		id = base62.decode(url_parts[0])

		cnx = mysql.connector.connect(host="172.17.0.2", user="url_shortner",passwd="pass",db="url_shortner")
		cursor = cnx.cursor(dictionary=True)
		cursor.execute("SELECT url FROM urls WHERE id='{0}'".format(id))
		result = cursor.fetchall()

		url = result[0]['url']
		proto = ''
		# For some reason without the protocal the redirection doesn't work properly.
		if 'http' not in url[0:4]:
			proto = 'http://'
		raise cherrypy.HTTPRedirect(proto+url,302)

	# Displays the form at '/'
	@cherrypy.expose
	def index(self):
		return open('index.html')

	# API call to get the short url
	@cherrypy.expose
	@cherrypy.tools.allow(methods=['POST'])
	def GenerateShortUrl(self, url):
		cnx = mysql.connector.connect(host="172.17.0.2", user="url_shortner",passwd="pass",db="url_shortner")
		cursor = cnx.cursor(dictionary=True)
		cursor.execute("INSERT INTO urls (hash, url) VALUES('','{0}')".format(url))
		id = cursor.lastrowid
		hash = base62.encode(id)
		cursor.execute("UPDATE urls SET hash='{0}' WHERE id='{1}'".format(hash,id))
		cnx.commit()
		cursor.close()
		cnx.close()
		return hash

	# API call for application health
	@cherrypy.expose
	@cherrypy.tools.allow(methods=['GET'])
	def health(self):
		return 'OK'


if __name__ == '__main__':
	config = {'server.socket_host': '0.0.0.0','server.socket_port': 8888}
	cherrypy.config.update(config)
	cherrypy.quickstart(Api())