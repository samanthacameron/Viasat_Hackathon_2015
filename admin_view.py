import cherrypy
import os, os.path
from database import session

class Admin(object):

    @cherrypy.expose
    def index(self):
        yield 'This is the admin view'

    @cherrypy.expose
    def restraunts:
    	yield ''

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
            }
    }
    cherrypy.config.update({'server.socket_port': 5588})
    cherrypy.quickstart(Admin(), '/', conf)
