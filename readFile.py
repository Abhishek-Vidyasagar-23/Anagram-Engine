import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

from add_anagram import addAnagram
from anagram_engine import Anagram_engine
from myuser import MyUser

import os


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

def sort(n):
   ordered = ''.join(sorted(n))
   return ordered

class ReadFile(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content - Type'] = 'text / html'
        message= "Welome to upload the file"
        template_values={
            'message': message
        }

        template= JINJA_ENVIRONMENT.get_template('readFile.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content - Type'] = 'text / html'
        action= self.request.get('button')

        user= users.get_current_user()
        my_user_key= ndb.Key('MyUser',user.user_id())
        my_user= my_user_key.get()

        file=self.request.get('uploadFile')

        if action=='Upload':
            openFile= open(file)
            readLine= openFile.readline()
            while readLine:
                word=(readLine.strip('\n\r')).lower()
                wordSorted= sort(word)
                wordLength = len(word)
                anagram_key = user.user_id() + wordSorted

                lexicography = ndb.Key(Anagram_engine, anagram_key)
                retrievedWord=lexicography.get()

                if retrievedWord==None:

                    wordInfo = Anagram_engine(id=anagram_key, wordSorted=wordSorted.lower(), wordLength=wordLength,
                                                  email=user,
                                                  wordCount=1)
                    anagram_count = my_user.anagram_count + 1
                    word_count = my_user.word_count + 1

                    my_user = MyUser(id=user.user_id(), name=user.email(), anagram_count=anagram_count,
                                         word_count=word_count)

                    my_user.put()

                    wordInfo.wordList.append(word)

                    wordInfo.put()
                    self.redirect('/')

                else:
                        wordCounter = len(retrievedWord.wordList) + 1
                        retrievedWord.wordCount = wordCounter
                        retrievedWord.wordList.append(word)
                        retrievedWord.put()
                        word_count = my_user.word_count + 1
                        anagram_count = my_user.anagram_count
                        my_user = MyUser(id=user.user_id(), name=user.email(), anagram_count=anagram_count,
                                         word_count=word_count)

                        my_user.put()

                readLine = openFile.readline()


            openFile.close()

        template_values={
            'message': 'File uploaded successfully'
        }

        template= JINJA_ENVIRONMENT.get_template('readFile.html')
        self.response.write(template.render(template_values))













