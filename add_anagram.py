import os
import webapp2
import jinja2
from myuser import MyUser
from google.appengine.api import users
from google.appengine.ext import ndb
from anagram_engine import Anagram_engine

from itertools import combinations

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

def sort(n):
    listWord = list(n)
    ordered = ''.join(sorted(listWord))
    return ordered


class addAnagram(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        if user== None:
            template_values = {
                'login_url': users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('mainpage_guest.html')
            self.response.write(template.render(template_values))
            return
        template_values = {

            'logout_url': users.create_logout_url(self.request.uri),
            'running': "running"
        }
        template = JINJA_ENVIRONMENT.get_template('add_anagram.html')
        self.response.write(template.render(template_values))



    def post(self):
        self.response.headers['Content - Type'] = 'text / html'
        action = self.request.get('button')

        if action=='ADD WORD':
            wordList = self.request.get('wordList')
            wordLength = len(wordList)
            wordSorted = sort(wordList)
            # subWords= subAnagram(wordList)


            if wordList == '':
                self.redirect('/')

            else:
                user = users.get_current_user()
                anagram_key= user.user_id()+wordSorted

                lexicography = ndb.Key(Anagram_engine, anagram_key)
                wordRetrieved = lexicography.get()
                my_user_key = ndb.Key('MyUser', user.user_id())
                my_user = my_user_key.get()

                if wordRetrieved==None:
                    wordInfo = Anagram_engine(id=anagram_key, wordSorted=wordSorted.lower(), wordLength=wordLength, email=user,
                                       wordCount=1)
                    anagram_count= my_user.anagram_count+1
                    word_count= my_user.word_count+1

                    my_user = MyUser(id=user.user_id(), name=user.email(), anagram_count=anagram_count, word_count=word_count)

                    my_user.put()





                    wordInfo.wordList.append(wordList)

                    wordInfo.put()
                    self.redirect('/')

                else :
                    counter = len(wordRetrieved.wordList) + 1
                    wordRetrieved.wordCount = counter
                    wordRetrieved.wordList.append(wordList)
                    wordRetrieved.put()
                    word_count= my_user.word_count+1
                    anagram_count= my_user.anagram_count
                    my_user = MyUser(id=user.user_id(), name=user.email(), anagram_count=anagram_count, word_count=word_count)

                    my_user.put()
                    responseMessage = {
                        "message": " New Word is added to the anagram engine database. "
                    }
                    template = JINJA_ENVIRONMENT.get_template('add_anagram.html')
                    self.response.write(template.render(responseMessage))




















































