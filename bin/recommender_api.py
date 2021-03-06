#!/usr/bin/env python
import webapp2
from csrec.Recommender import Recommender

"""
Usage:
python recommender_api.py

Start a webapp for testing the recommender.

"""


engine = Recommender()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Cold Start Recommender v. ' + str(csrec.__version__))

class InsertRating(webapp2.RequestHandler):
    """
    e.g.:
    curl -X POST  'localhost:8081/insertrating?item=Book1&user=User1&rating=4'
    """
    def post(self):
        global engine
        user = self.request.get('user')
        item = self.request.get('item')
        rating = self.request.get('rating')
        engine.insert_rating(user, item, rating)

class InsertItem(webapp2.RequestHandler):
    """
    e.g.:
    curl -X POST  'localhost:8081/insertitem?id=Book1&author=TheAuthor&cathegory=Horror'
    """
    def post(self):
        global engine
        item = {}
        for i in self.request.params.items():
            item[i[0]] = i[1]
        #self.response.write(item)
        engine.insert_item(item, _id='id')
        

class Recommend(webapp2.RequestHandler):
    """
    curl -X GET  'localhost:8081/recommend?user=User1'
    """
    def get(self):
        global engine
        user = self.request.get('user')
        max_recs = self.request.get('max_recs', 10)
        fast = self.request.get('fast', False)
        self.response.write(engine.get_recommendations(user, max_recs=max_recs, fast=fast))

class Reconcile(webapp2.RequestHandler):
    def post(self):
        global engine
        old = self.request.get('old')
        new = self.request.get('new')
        engine.reconcile(old, new)

class Info(webapp2.RequestHandler):
    """
    curl -X GET  'localhost:8081/info?user=User1'
    """
    def get(self):
        global engine
        user = self.request.get('user')
        self.response.write(engine.get_user_info(user))
        

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/insertrating', InsertRating),
    ('/insertitem', InsertItem),
    ('/recommend', Recommend),
    ('/reconcile', Reconcile),
    ('/info', Info),
], debug=True)

def main():
    global engine
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8081')

if __name__ == '__main__':
    main()
