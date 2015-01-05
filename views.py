import os
import urllib

from google.appengine.api import users
from google.appengine.ext import db, ndb
from models import Link, Tag, Star
import jinja2
import webapp2
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(45)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+ '/templates/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class RanksPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        import urllib
        import json
        url = "http://codeforces.com/api/user.ratedList?activeOnly=true"
        codeforces_ratings = json.loads(urllib.urlopen(url).read())
        template_values = {
            'url_linktext': url_linktext,
            'url': url,
            'user':user,
            'codeforces_ratings':codeforces_ratings,
        }

        template = JINJA_ENVIRONMENT.get_template('ranks.html')
        self.response.write(template.render(template_values))


class MainPage(webapp2.RequestHandler):
    """
        Handler for the home page.
    """
    def get(self):
        links = db.Query(Link)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'links' : links,
            'user' : user,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class SubmitLink(webapp2.RequestHandler):
    """
        Handler to submit a new link.
    """
    def post(self):

        url = self.request.get("url")
        heading = self.request.get("heading")
        description = self.request.get("description")
        tags = self.request.get("tags")
        tags = tags.split(",")
        if url and heading and tags:
            p = Link(url = url,
                heading = heading,
                description = description,
                author = users.get_current_user(),
                )
            p.put()
            if p:
                link = p.key()
                for tag in tags:
                    tag = tag.replace (" ", "_")
                    q = Tag(link = link,
                            tag = tag,
                            )
                    q.put()
        self.redirect('/')

class StarLink(webapp2.RequestHandler):
    """
        Handler to star a link.
    """
    def post(self):
        import pdb
        link = self.request.get('link')
        author = users.get_current_user()
        link = Link.get_by_id(int(link))
        m = db.Query(Star)
        m.filter('link =', link).filter('author =', author)
        if author and link and not m:
            q = Star(link = link,
                author = author,
                )
            q.put()
        self.response.write('success')


class SingleLink(webapp2.RequestHandler):
    """
        Handler to dispaly a single link page.
    """
    def get(self, link_id):
        link = Link.get_by_id(int(link_id)) 
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            'url_linktext': url_linktext,
            'url': url,
            'user':user,
            'link':link,
        }

        template = JINJA_ENVIRONMENT.get_template('single_link.html')
        self.response.write(template.render(template_values))

class SingleTag(webapp2.RequestHandler):
    """
        Handler to dispaly a single tag page.
    """
    def get(self, tag_name):
        tags = db.GqlQuery("SELECT * FROM Tag WHERE tag = :tag_name", tag_name=tag_name)
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            'url_linktext': url_linktext,
            'url': url,
            'user':user,
            'tags':tags,
        }

        template = JINJA_ENVIRONMENT.get_template('single_tag.html')
        self.response.write(template.render(template_values))

class Tags(webapp2.RequestHandler):
    """
        Handler to dispaly all tags.
    """
    def get(self):
        tags = db.GqlQuery("SELECT distinct tag FROM Tag")
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            'url_linktext': url_linktext,
            'url': url,
            'user':user,
            'tags':tags,
        }

        template = JINJA_ENVIRONMENT.get_template('tags.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/__submitlink', SubmitLink),
    ('/__star', StarLink),
    ('/tags', Tags),
    (r'/link/(\d+)', SingleLink),
    (r'/tags/(\S+)', SingleTag),
], debug=True)