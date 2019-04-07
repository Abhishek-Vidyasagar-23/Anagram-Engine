import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb


from myuser import MyUser

import os
from itertools import  combinations

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

def sorting(userWord):
   ordered = ''.join(sorted(userWord))
   return ordered

def subSort(word):
    listWord = list(word)
    word_keys = []
    for i in range(3,len(word)+1):
        temp=(["".join(c)for c in combinations(word,i)])
        for c in temp:
            word_keys.append(c)

    return word_keys




class SubAnagram(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()

        resultList = []

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

        wordList = self.request.get('wordList')


        wordSorted = sorting(wordList)
        resultList = []

        subList=subSort(wordSorted)
        for key in subList:
            w_key = ndb.Key('Anagram_engine', user.user_id() + key)
            my_word = w_key.get()

            if my_word != None:
                resultList.extend(my_word.wordList)

        user = users.get_current_user()
        my_user_key = ndb.Key('MyUser', user.user_id())
        my_user = my_user_key.get()



        template_values = {

            'user': user,
            'anagram_count': my_user.anagram_count,
            'word_count': my_user.word_count,
            'resultList': resultList
        }


        template = JINJA_ENVIRONMENT.get_template('subAnagram.html')
        self.response.write(template.render(template_values))

    def post(self):
            self.response.headers['Content - Type'] = 'text / html'
            action = self.request.get('button')
            user = users.get_current_user()

            if action == 'Check':

                wordList = self.request.get('wordList')
                self.redirect('/subAnagram?wordList='+wordList)





