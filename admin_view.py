import cherrypy
import os, os.path
from database import session

class Admin(object):

    @cherrypy.expose
    def index(self):
        yield 'This is the admin view'

    @cherrypy.expose
    def restaurants(self):
        restaurants = session.query("SELECT * FROM restaurants;")
        for rest in restaurants:
            yield rest
        yield ''

    @cherrypy.expose
    def createpoll(self):
        yield ''

    @cherrypy.expose
    def blacklist(self):
        yield ''

    @cherrypy.expose
    def favorites(self):
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
