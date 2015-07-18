import cherrypy
import requests
import json

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
    def search(self):
        # meters = float(miles) * 1609.34
        # url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=30.638088,-96.370452&radius={}&types=restaurant&key={}'.format(meters, API_KEY)
        url = 'http://localhost:5588/results'
        response = requests.get(url)
        results = json.loads(response.text)['results']
        for result in results:
            name = result['name']
            address = result['vicinity']
            yield '{}: {} </br>'.format(name, address)

    @cherrypy.expose
    def results(self):
        with open('results.json', encoding='utf-8') as data_file:
            data = json.loads(data_file.read())
        return json.dumps(data)

cherrypy.config.update({'server.socket_port': 5588})
cherrypy.quickstart(HelloWorld())
