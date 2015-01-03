from google.appengine.ext import db, ndb

class Greeting(ndb.Model):
    """Models an individual Guestbook entry."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class Link(db.Model):
    """Models a unique tutorial link submission."""
    url = db.LinkProperty()
    heading = db.StringProperty(indexed=False)
    description = db.TextProperty()
    upvotes = db.IntegerProperty(default=0)
    downvotes = db.IntegerProperty(default=0)
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class Tag(db.Model):
    """Models tags for a URL."""
    tag = db.StringProperty()
    link = db.ReferenceProperty(Link)


class Upvote(db.Model):
    """Models upvotes for a URL."""
    author = db.UserProperty()
    link = db.ReferenceProperty(Link)


class Downvote(db.Model):
    """Models downvotes for a URL."""
    author = db.UserProperty()
    link = db.ReferenceProperty(Link)

