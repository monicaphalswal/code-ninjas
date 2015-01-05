from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class DeleteCronTask(webapp.RequestHandler):
    def get(self):
        # do something