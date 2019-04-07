import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

from subAnagram import  SubAnagram

from add_anagram import addAnagram
from anagram_engine import Anagram_engine
from myuser import MyUser
from readFile import ReadFile
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

def sorting(n):
   ordered = ''.join(sorted(n))
   return ordered

class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        if user== None:
            template_values = {
                'login_url': users.create_login_url(self.request.uri)
            }

            template = JINJA_ENVIRONMENT.get_template('mainpage_guest.html')
            self.response.write(template.render(template_values))
            return

        my_user_key = ndb.Key('MyUser', user.user_id())
        my_user = my_user_key.get()

        if my_user == None:
            my_user = MyUser(id=user.user_id(),name=user.email(),anagram_count=0,word_count=0)

            my_user.put()


        template_values = {
            'logout_url' : users.create_logout_url(self.request.uri),
            'user': user,
            'query':Anagram_engine.query().fetch(),
            'anagram_count': my_user.anagram_count,
            'word_count': my_user.word_count,

        }

        template = JINJA_ENVIRONMENT.get_template('mainpage.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content - Type'] = 'text / html'
        action = self.request.get('button')
        user=users.get_current_user()

        if action=='Search':
            wordList=self.request.get('wordList')
            wordSorted = sorting(wordList)

            user = users.get_current_user()
            my_user_key = ndb.Key('MyUser', user.user_id())
            my_user = my_user_key.get()



            if wordList== '':
                self.redirect('/')

            else:
                anagram_key = user.user_id() + wordSorted

                lexicography = ndb.Key(Anagram_engine, anagram_key)
                wordRetrieved = lexicography.get()
            template_values = {
                    'query': wordRetrieved,
                    'user': user,
                    'anagram_count': my_user.anagram_count,
                    'word_count': my_user.word_count,



                }

            template = JINJA_ENVIRONMENT.get_template('mainpage.html')
            self.response.write(template.render(template_values))








app = webapp2.WSGIApplication([
    ('/' , MainPage),
    ('/add_anagram',addAnagram),
    ('/readFile',ReadFile),
    ('/subAnagram',SubAnagram)


    ], debug=True)





















