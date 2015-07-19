import cherrypy
import os
import os.path
from database import *
from svg.charts.pie import Pie
import requests
import datetime

abbrevs = {'bbq': 'Barbecue', 'pizza': 'Pizza', 'burgers': 'Burgers', 'cajun': 'Cajun',
           'mexican': 'Mexican', 'italian': 'Italian', 'japanese': 'Japanese'}


class Poll(object):

    def __init__(self):
        self.uname = ""
        self.voteCount = 0
        self.going = 0

    @cherrypy.expose
    def index(self, username=""):
        yield '''<html>
        <head>
            <link href="/static/css/style.css" rel="stylesheet">
            <title>Polling App</title>
          </head>
        '''
        yield '''<h1>YOU HAVE BEEN INVITED TO LUNCH!</h1> '''
        yield '''<h2>Please enter your username and choose an option</h2></br>'''
        yield '''
        <form action="search">
        <div id="s">User Name: <input id="un" type="text" name="uname" value="%s"></br>''' % username
        yield '''</div><div id="o"><label for="optout" >
        <input type="radio" name="opt" value="3" checked="checked"/>Take me to submit my vote.
        </label></br>
        <label for="optout">
        <input type="radio" name="opt" value="1"/>I don't want to go
        </label></br>
        <label for="optout">
        <input type="radio" name="opt" value="2"/>I want to go but don't want to vote.
        </label></div></br>'''

        yield '''<button id="login" type="submit" >Login</button></form>'''
        
    @cherrypy.expose
    def timer(self,time):
        time = int(time)
        yield 'Current time: {}</br>'.format(str(datetime.datetime.now()))
        newtime = datetime.datetime.now() + datetime.timedelta(minutes=time)
        newtime = newtime.strftime('%I:%M')
        yield 'End Time: {}'.format(str(newtime))

    @cherrypy.expose
    def search(self, uname, opt):
        yield '''<html>
        <head>
            <link href="/static/css/style.css" rel="stylesheet">
            <title>Poll</title>
          </head>
        '''
        yield '<body>'
        match = 0
        for row in session.query(User):
            if uname == row.username:
                match = 1
        if match == 0:
            yield '''USERNAME NOT RECOGNIZED'''
            opt = "0"
            yield '</br> <a href = "/">Return To Login</a>'
        # no vote but going
        if opt == "2":

            userobject = session.query(User)

            userobject = userobject.filter(User.username == uname)
            for o in userobject:

                if o.voted == 1:
                    self.voteCount = self.voteCount - 1
                    o.voted = 0

                    restobject = session.query(Restaurant)
                    restobject = restobject.filter(Restaurant.id == o.rest_id)
                    for p in restobject:
                        p.votes = p.votes - 1
                        session.commit()
                    o.rest_id = None
                    session.commit()
                else:
                    self.going = self.going + 1
            yield '''Vote is Not Counted But {} Is Going'''.format(uname)
            yield '</br> <a href = "/poll">Return To Login</a>'

        # not going
        elif opt == "1":
            userobject = session.query(User)
            userobject = userobject.filter(User.username == uname)
            for o in userobject:
                if o.voted == 1:
                    self.voteCount = self.voteCount - 1
                    self.going = self.going - 1
                    o.voted = 0
                    restobject = session.query(Restaurant)
                    restobject = restobject.filter(Restaurant.id == o.rest_id)
                    for p in restobject:
                        p.votes = p.votes - 1
                        session.commit()
                    o.rest_id = None
                    session.commit()

            objects = session.query(User)
            objects = objects.filter(User.username == uname)
            yield '{} is not going to lunch'.format(uname)
            yield '</br> <a href = "/poll">Return To Login</a>'
        # option 3 is new person going
        elif opt == "3":
            self.uname = uname
            objects = session.query(User)
            objects = objects.filter(User.username == self.uname)
            for o in objects:
                if o.voted == 1:
                    opt = "4"
                else:
                    self.voteCount = self.voteCount + 1

                    yield'''
                        <legend>What is your Restaurant of choice?</legend>

                        <form action="submit">'''
                    yield '<div id=polllist>'
                    for row in session.query(Restaurant):

                        yield'''<label for="restId">
                            <input type="radio" name="restId" value="%s" id="Poll_0" />
                            %s
                         </label></br>''' % (str(row.id), row.name)
                    yield '</div>'
                    yield '''<button type="submit">Vote</button>'''
                    self.going = self.going + 1
        # option 4 is changed
        if opt == "4":
            yield'''
                <legend>What is your Restaurant of choice?</legend>

                <form action="submit">'''
            yield '<div id=polllist>'
            previouslySelected = session.query(User)
            previouslySelected = previouslySelected.filter(User.username == uname)
            for o in previouslySelected:
                prev = o.rest_id
            for row in session.query(Restaurant):
                if prev == row.id:
                    yield'''<label for="restId">
                    <input type="radio" name="restId" value="%s" id="Poll_0" checked="checked" />
                    %s
                    </label></br>''' % (str(row.id), row.name)
                    row.votes = row.votes - 1
                else:
                    yield'''<label for="restId">
                        <input type="radio" name="restId" value="%s" id="Poll_0" />
                        %s
                     </label></br>''' % (str(row.id), row.name)
                    self.going = self.going + 1
            yield '</div>'
            yield '''<button type="submit">Vote</button>'''
        yield '</body>'

    @cherrypy.expose
    def reset(self):
        yield '<head><title>Votes Reset</title></head>'
        for restaurant in session.query(Restaurant):
            restaurant.votes = 0
        for user in session.query(User):
            user.voted = 0
            user.rest_id = None
        for row in session.query(Restaurant):
            session.delete(row)
        for row in session.query(User):
            session.delete(row)
        session.commit()
        cherrypy.session['message'] = "Database cleared"

    @cherrypy.expose
    def submit(self, restId):
        yield '<head><title>Results</title></head>'
        restobjects = session.query(Restaurant)
        restobjects = restobjects.filter(Restaurant.id == int(restId))
        rvoteCount = 0
        for restaurant in session.query(Restaurant):
            rvoteCount += restaurant.votes
        uvoteCount = 0
        for user in session.query(User):
            uvoteCount += int(user.voted)
        if rvoteCount == 0:
            if uvoteCount - 1 != rvoteCount:
                for o in restobjects:
                    o.votes = o.votes + 1
        else:
            if uvoteCount != rvoteCount:
                for o in restobjects:
                    o.votes = o.votes + 1
        userobjects = session.query(User)
        userobjects = userobjects.filter(User.username == self.uname)
        for o in userobjects:
            for t in restobjects:
                restaurantId = t.id
            o.rest_id = restaurantId
            o.voted = 1
        session.commit()
        yield requests.get('http://localhost:5588/poll/results').text

    @cherrypy.expose
    def results(self):
        yield '''Number of People Going: %s</br>''' % str(self.going)
        yield '''Number of Votes: %s</br>''' % str(self.voteCount)
        yield '''
        <table border="1" style="width:100%"> <tr>
            <th>Name</th>
            <th>Address</th>
            <th>Category</th>
            <th>Votes</th>
        </tr>
'''
        totalVotes = 0
        for restaurant in session.query(Restaurant):
            totalVotes += restaurant.votes
        for restaurant in session.query(Restaurant):
            yield '''<tr> <td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
            ''' % (restaurant.name, restaurant.address, abbrevs[restaurant.category], str(restaurant.votes))
        yield '</table>'
        fields = []
        votes = []
        for restaurant in session.query(Restaurant):
            fields.append(restaurant.name)
            votes.append(restaurant.votes)
        try:
            graph = Pie(dict(
                height=500, width=500, fields=fields))
            graph.add_data({"data": votes, "title": "Lunch Votes"})
            yield graph.burn()
        except:
            yield '</br>There is no data yet.'

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
    cherrypy.quickstart(Poll(), "/", conf)
