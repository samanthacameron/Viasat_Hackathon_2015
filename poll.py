import cherrypy
import os
import os.path
from database import *
from svg.charts.pie import Pie
import requests

abbrevs = {'bbq': 'Barbecue', 'pizza': 'Pizza', 'burgers': 'Burgers', 'cajun': 'Cajun',
           'mexican': 'Mexican', 'italian': 'Italian', 'japanese': 'Japanese'}


class Poll(object):

    def __init__(self):
        self.uname = ""
        self.voteCount = 0
        self.going = 0

    @cherrypy.expose
    def index(self):
        yield '''<html>
        <head>
            <link href="/static/css/style.css" rel="stylesheet">
          </head>
        '''
        yield '''<p>Congratulations! You have been invited to lunch!</br>Please enter a username and an option.</p></br>'''
        yield '''
        <form action="search">
        User Name: <input type="text" name="uname"></br>'''
        yield '''<label for="optout">
                <input type="radio" name="opt" value="1"/>I don't want to go
             </label></br>'''
        yield '''<label for="optout">
                <input type="radio" name="opt" value="2"/>I want to go but don't want to vote.
             </label></br>'''
        yield '''<label for="optout" >
                <input type="radio" name="opt" value="3" checked="checked"/>Take me to submit my vote.
             </label></br>'''
        yield '''<label for="optout">
                <input type="radio" name="opt" value="4"/>Change my vote.
             </label></br>'''
        yield '''<button type="submit">Login</button></form>'''
        yield '<a href = http://localhost:5588/poll/reset>Clear the poll.</a></html>'

    # needed for colin's management
    @cherrypy.expose
    def poll(self, uname, opt):

        yield '''
        <form action="search">
        ZipCode: <input type="text" name="zip">
        <select name="radius">
              <option value="5">5 miles</option>
              <option value="10">10 miles</option>
              <option value="20">20 miles</option>
        </select>

        <button type="submit">Search</button>
        </form>
            '''

    @cherrypy.expose
    def search(self, uname, opt):
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
            self.going = self.going + 1
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
            yield '''Vote is Not Counted But {} Is Going'''.format(uname)
            yield '</br> <a href = "/">Return To Login</a>'

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
            yield '</br> <a href = "/">Return To Login</a>'
        # option 4 is changed
        elif opt == "4":
            yield'''
                <legend>What is your Restaurant of choice?</legend>

                <form action="results">'''
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
            yield '''<button type="submit">Vote</button>'''

        # option 3 is new person going
        elif opt == "3":
            self.uname = uname
            objects = session.query(User)
            objects = objects.filter(User.username == self.uname)
            for o in objects:
                if o.voted == 1:
                    yield '''YOU HAVE ALREADY VOTED XD'''
                else:
                    self.voteCount = self.voteCount + 1

                    yield'''
                        <legend>What is your Restaurant of choice?</legend>

                        <form action="submit">'''
                    for row in session.query(Restaurant):

                        yield'''<label for="restId">
                            <input type="radio" name="restId" value="%s" id="Poll_0" />
                            %s
                         </label></br>''' % (str(row.id), row.name)
                    yield '''<button type="submit">Vote</button>'''
                    self.going = self.going + 1

    @cherrypy.expose
    def reset(self):
        for restaurant in session.query(Restaurant):
            restaurant.votes = 0
        for user in session.query(User):
            user.voted = 0
            user.rest_id = None
        session.commit()
        yield '''CLEARED'''

    @cherrypy.expose
    def submit(self, restId):
        restobjects = session.query(Restaurant)
        restobjects = restobjects.filter(Restaurant.id == int(restId))
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
