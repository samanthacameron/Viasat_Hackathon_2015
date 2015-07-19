import cherrypy
import requests
import json
import oauth2
import os
from database import *
from poll import Poll
import datetime

# API_KEY = 'AIzaSyCY0yYTShIG54l8rUPNUOsl3Jm7NdWtXBQ'
API_HOST = 'http://api.yelp.com/v2/search/?'
CONSUMER_KEY = 'bH-ntL7Nv-iUC7mndRvujw'
CONSUMER_SECRET = 'B-Br6RdJJpyMZAwYAmoKPisv-Cw'
TOKEN = 'ugQuBYYmoJBNcnBDpVrVO2HiPpMyahmZ'
TOKEN_SECRET = 'ljnrQcblPl7yHbuQebRoqhvlRoI'

category_names = {'None': 'None', 'bbq': 'Barbecue', 'pizza': 'Pizza', 'burgers': 'Burgers', 'cajun': 'Cajun',
                  'mexican': 'Mexican', 'italian': 'Italian', 'japanese': 'Japanese'}


class RestaurantSearch(object):

    def __init__(self):
        self.poll = Poll()
        self.STARTIME = datetime.datetime.now()
        self.T = 0
        self.ENDTIME = (datetime.datetime.now() + datetime.timedelta(minutes=self.T)).strftime('%I:%M:%S %p')

    @cherrypy.expose
    def index(self):
        yield '''<html>
        <head>
            <link href="/static/css/style.css" rel="stylesheet">
            <title>Polling App</title>
          </head>
        '''
        yield '''
        <h1>POLLING APP</h1>
        <h2>Choose an option below</h2>
        <div id="c"><form action = search_entry><button id="sel" type="submit" >Search for restaurants to add to the poll</button></form></br>'''
        yield '''<form action = "invite"><button id="sel" type="submit" >Invite members</button></form></br>'''
        yield '''<form action = "poll"><button id="sel" type="submit" >Join current poll</button></form></br>'''
        yield '''<form action = "poll/results"><button id="sel" type="submit" >View current poll results</button></form></br>'''
        yield '''<form action = "poll/reset"><button id="sel" type="submit" >Done with the poll, reset it</button></form></br>'''
        yield '''<form action = "timer">Minutes: <input id="un" type="number" name="minutes"><button type="submit">Start Timer</button></br>End Time: {}</form></div>'''.format(str(self.ENDTIME))

        if('message' in cherrypy.session):
            message = cherrypy.session['message']
            yield '<div id= flash>'
            yield message
            yield '<div>'
            del cherrypy.session['message']

    @cherrypy.expose
    def timer(self, minutes):
        self.T = int(minutes)
        self.ENDTIME = (datetime.datetime.now() + datetime.timedelta(minutes=self.T)).strftime('%I:%M:%S %p')

        # currentTime = datetime.datetime.now().strftime('%I:%M:%S %p')
        # yield 'Current time: {}</br>'.format(str(currentTime))
        # newtime = datetime.datetime.now() + datetime.timedelta(minutes=time)
        # newtime = newtime.strftime('%I:%M:%S %p')
        # yield 'End Time: {}'.format(str(newtime))
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def search_entry(self):
        yield '''<html>
                <head>
                    <link href="/static/css/style.css" rel="stylesheet">
                    <title>Search for a restaurant</title>
                </head>
                '''
        if('message' in cherrypy.session):
            message = cherrypy.session['message']
            yield '<div id= flash>'
            yield message
            yield '<div>'
            del cherrypy.session['message']
        yield '''<body>
                <form action="search">
                <fieldset>
                <legend>Polling:</legend>
                Name (Optional):<br>
                <input type="text" name="name" value=""> <br>
                Location:<br>
                <input type="text" name="location" value="Bryan, TX"> <br>
                Radius in Miles:<br>
                <input type="text" name="miles" value="5"> <br>
                Category:<br>'''
        for key in category_names:
            yield '<input type="radio" name="category" value="%s">%s<br>' % (key, category_names[key])
        yield '''<br><br>
                <input type="submit" value="Submit"></fieldset>
                </form></body>'''
        yield '</br> <a href = "/">Home</a>'

    @cherrypy.expose
    def search(self, name=None, location='Bryan, TX', miles=5, category=None):
        yield '''<html>
        <head>
            <link href="/static/css/style.css" rel="stylesheet">
            <title>Search Results</title>
          </head>
        '''
        yield '<body>'
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
                'radius_filter': meters
            }
        )
        if category is not None:
            oauth_request['category_filter'] = category
        if name is not None:
            oauth_request['term'] = name
        token = oauth2.Token(TOKEN, TOKEN_SECRET)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
        url = oauth_request.to_url()

        # END USING YELP API

        # USING LOCAL RESULTS

        # if category == 'bbq':
        #     url = 'http://localhost:5588/results?category=barbecue'
        # elif category == 'pizza':
        #     url = 'http://localhost:5588/results?category=burgers'
        # elif category == 'burgers':
        #     url = 'http://localhost:5588/results?category=burgers'

        response = requests.get(url)
        restaurants = json.loads(response.text)['businesses']
        for restaurant in restaurants:
            name = restaurant['name']
            name = sanitize(name)

            if(session.query(Blacklist).get(name) is not None):
                continue

            yield '<div id=rest>'

            full_address = restaurant['location']['display_address']
            address = ""
            rating = restaurant['rating_img_url']
            yield'<div id=name>{}</div>'.format(name.encode('utf-8'))

            yield '<div id=address>'
            for field in full_address:
                yield'{}<br>'.format(field)
                address += field + ' '
            yield '</div>'

            yield '<a href="http://localhost:5588/add?name={}&address={}&category={}" class="addpoll">Add to Poll</a>'.format(name.encode('utf-8'), address, category)
            yield '<br>'
            yield '<img src="{}"></img></br>'.format(rating)
            yield '<br>'

            yield '</div>'
        yield '</body>'

    @cherrypy.expose
    def add(self, name, address, category):
        yield '<head><title>Restaurant Added</title></head>'
        restaurantmatch = session.query(Restaurant).filter(Restaurant.name == name).first()
        if restaurantmatch is None:
            new_rest = Restaurant(name=name, address=address, category=category, votes=0)
            session.add(new_rest)
            session.commit()
            cherrypy.session['message'] = 'Restaurant Added'
        else:
            cherrypy.session['message'] = 'This restaurant is already in the poll'
        raise cherrypy.HTTPRedirect('/search_entry')

    # @cherrypy.expose
    # def results(self, category):
    #     if category == 'burgers':
    #         with open('burgers.json') as data_file:
    #             data = json.loads(data_file.read())
    #         return json.dumps(data)
    #     elif category == 'barbecue':
    #         with open('barbecue.json') as data_file:
    #             data = json.loads(data_file.read())
    #         return json.dumps(data)
    #     elif category == 'pizza':
    #         with open('pizza.json') as data_file:
    #             data = json.loads(data_file.read())
    #         return json.dumps(data)

    @cherrypy.expose
    def invite(self):
        yield '''<html>
        <head>
            <link href="/static/css/style.css" rel="stylesheet">
            <title>Invite a colleague</title>
          </head>
        '''
        yield '<body>'
        yield '<form action="invited">'
        for person in session.query(UserList):
            name = person.username
            yield '<div id=user>'
            yield '''
             <input type="checkbox" name="person" value="%s">%s
            ''' % (name, name)
            yield '<br>'
            yield '</div>'
        yield 'Other:<br><input type ="field", name="new_person" value><br><br>'
        yield '<input type="submit" value="Submit">'
        yield '</form>'
        yield '</body>'

    @cherrypy.expose
    def invited(self, **args):
        yield '<head><title>Invited</title></head>'
        message = ""
        if 'new_person' in args:
            new_name = args['new_person']
            if(new_name != ""):
                if(session.query(UserList).get(new_name) is None):
                    new_person = UserList(username=new_name)
                    session.add(new_person)
                    session.commit
                if(session.query(User).get(new_name) is None):
                    new_user = User(username=new_name, voted=0)
                    session.add(new_user)
                    session.commit()
                yield new_name
                message += new_name + ", "
                # yield '<br>'

        if 'person' in args:
            names = args['person']
            if not isinstance(names, list):
                names = [names]
            for name in names:
                yield name
                if(session.query(User).get(name) is None):
                    new_user = User(username=name, voted=0)
                    session.add(new_user)
                    session.commit()
                # yield '<br>'
                message += name + ", "
            # yield 'Invited'
        message += "Invited"
        cherrypy.session['message'] = message

        raise cherrypy.HTTPRedirect('/')


def sanitize(s):
    s = s.replace("'", "")
    s = s.replace("&", "and")
    s = s.replace("?", "")
    s = s.replace("%", "")
    return s

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
