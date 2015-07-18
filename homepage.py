import cherrypy
import requests

API_KEY = 'AIzaSyCY0yYTShIG54l8rUPNUOsl3Jm7NdWtXBQ'


class HelloWorld(object):

    @cherrypy.expose
    def index(self):
        yield '''<form action="search">
                <fieldset>
                <legend>Polling:</legend>
                Radius in Miles:<br>
                <input type="text" name="miles" value="">
                <br><br>
                <input type="submit" value="Submit"></fieldset>
                </form>'''

    @cherrypy.expose
    def search(self, miles):
        meters = float(miles) * 1609.34
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=30.638088,-96.370452&radius={}&types=restaurant&key={}'.format(meters, API_KEY)
        restaurants = requests.get(url)
        yield restaurants.text


cherrypy.config.update({'server.socket_port': 5588})
cherrypy.quickstart(HelloWorld())
