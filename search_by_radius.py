import cherrypy
import requests
import json
import oauth2
import os
from database import *

# API_KEY = 'AIzaSyCY0yYTShIG54l8rUPNUOsl3Jm7NdWtXBQ'
API_HOST = 'http://api.yelp.com/v2/search/?'
CONSUMER_KEY = 'bH-ntL7Nv-iUC7mndRvujw'
CONSUMER_SECRET = 'B-Br6RdJJpyMZAwYAmoKPisv-Cw'
TOKEN = 'ugQuBYYmoJBNcnBDpVrVO2HiPpMyahmZ'
TOKEN_SECRET = 'ljnrQcblPl7yHbuQebRoqhvlRoI'


class RestaurantSearch(object):

    @cherrypy.expose
    def index(self):
        yield '''<html>
                <head>
                    <link href="/static/css/stylesearch.css" rel="stylesheet">
                </head>
                '''
        yield '''<body>
                <form action="search">
                <fieldset>
                <legend>Polling:</legend>
                Location:<br>
                <input type="text" name="location" value="Bryan, TX"> <br>
                Radius in Miles:<br>
                <input type="text" name="miles" value="5"> <br>
                Category:<br>
                <input type="radio" name="category" value="bbq">Barbecue<br>
                <input type="radio" name="category" value="pizza">Pizza<br>
                <input type="radio" name="category" value="burgers">Burgers<br>
                <br><br>
                <input type="submit" value="Submit"></fieldset>
                </form></body>'''

    @cherrypy.expose
    def search(self, location='Bryan, TX', miles=5, category='bbq'):
        yield '''<html>
        <head>
            <link href="/static/css/stylesearch.css" rel="stylesheet">
          </head>
        '''
        # START USING YELP API

        meters = float(miles) * 1609.34
        consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        oauth_request = oauth2.Request(method="GET", url=API_HOST, parameters=None)

        oauth_request.update(
            {
                'oauth_nonce': oauth2.generate_nonce(),
                'oauth_timestamp': oauth2.generate_timestamp(),
                'oauth_token': TOKEN,
                'oauth_consumer_key': CONSUMER_KEY,
                'location': location,
                'category_filter': category,
                'radius_filter': meters
            }
        )
        token = oauth2.Token(TOKEN, TOKEN_SECRET)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
        # url = oauth_request.to_url()

        # END USING YELP API

        # USING LOCAL RESULTS

        if category == 'bbq':
            url = 'http://localhost:5588/results?category=barbecue'
        elif category == 'pizza':
            url = 'http://localhost:5588/results?category=burgers'
        elif category == 'burgers':
            url = 'http://localhost:5588/results?category=burgers'
        else:
            yield 'Please input a valid category'

        response = requests.get(url)
        restaurants = json.loads(response.text)['businesses']
        for restaurant in restaurants:
            name = restaurant['name']
            name.replace("'", "")
            full_address = restaurant['location']['display_address']
            address = ""
            rating = restaurant['rating_img_url']
            yield'{}<br>'.format(name)
            for field in full_address:
                yield'{}<br>'.format(field)
                address += field + ' '

            yield '<a href="http://localhost:5588/add?name={}&address={}&category={}">Add</a>'.format(name, address, category)

            yield '<br>'
            yield '<img src="{}"></img></br>'.format(rating)
            yield '<br>'

    @cherrypy.expose
    def add(self, name, address, category):
        new_rest = Restaurant(name=name, address=address, category=category, votes=0)
        session.add(new_rest)
        session.commit()
        yield 'Restaurant Added'

    @cherrypy.expose
    def results(self, category):
        if category == 'burgers':
            with open('burgers.json') as data_file:
                data = json.loads(data_file.read())
            return json.dumps(data)
        elif category == 'barbecue':
            with open('barbecue.json') as data_file:
                data = json.loads(data_file.read())
            return json.dumps(data)
        elif category == 'pizza':
            with open('pizza.json') as data_file:
                data = json.loads(data_file.read())
            return json.dumps(data)

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
cherrypy.quickstart(RestaurantSearch(), '/', conf)
