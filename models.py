from google.appengine.ext import db

class Link(db.Model):
    """Models a unique tutorial link submission."""
    url = db.LinkProperty()
    heading = db.StringProperty(indexed=False)
    description = db.TextProperty()
    stars = db.IntegerProperty(default=0)
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def is_starred(cla):
        return 1

class Tag(db.Model):
    """Models tags for a URL."""
    tag = db.StringProperty()
    link = db.ReferenceProperty(Link, collection_name='tags')

class Star(db.Model):
    """Models stars for a URL."""
    author = db.UserProperty()
    link = db.ReferenceProperty(Link, collection_name='starred')

    @classmethod
    def count_upvotes(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)



