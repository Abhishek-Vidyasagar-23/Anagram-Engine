from google.appengine.ext import ndb
from anagram_engine import Anagram_engine


class MyUser(ndb.Model):
    name= ndb.StringProperty()
    anagram_count= ndb.IntegerProperty()
    word_count= ndb.IntegerProperty()

