from google.appengine.ext import ndb



class Anagram_engine(ndb.Model):
    wordList= ndb.StringProperty(repeated=True)
    wordCount= ndb.IntegerProperty()
    wordLength=ndb.IntegerProperty()
    wordSorted= ndb.StringProperty()
    subAnagram= ndb.StringProperty(repeated=True)

    email=ndb.UserProperty()




