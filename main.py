#!/usr/bin/env python
import jinja2
import os
import webapp2
from google.appengine.ext import db
from emailsender import sendRandomWikipediaArticleTo, sendConfirmationEmail

# loads framework for HTML templates
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(
	[os.path.dirname(__file__), '/templates']))

class Subscriber(db.Model):
	emailAddress = db.StringProperty()
	
class DailyEmailSender(webapp2.RequestHandler):
	def get(self):
		subs = Subscriber.all()
		for sub in subs:
			sendRandomWikipediaArticleTo(sub.emailAddress)

class SubscriptionHandler(webapp2.RequestHandler):
	def post(self):
		to_addr = self.request.get('signup-email')
		sub = Subscriber(emailAddress = to_addr)
		sub.put()
		sendConfirmationEmail(to_addr)
		template = jinja_environment.get_template('templates/sub.html')
		self.response.out.write(template.render())

class UnsubscriptionHandler(webapp2.RequestHandler):
	def get(self):
		emailAddress = self.request.get('email')
		subs = Subscriber.all()
		subs.filter("emailAddress = ", emailAddress)
		for sub in subs:
			sub.delete()
		template = jinja_environment.get_template('templates/unsub.html')
		self.response.out.write(template.render())

class MainHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('templates/index.html')
		self.response.out.write(template.render())

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/subscribe', SubscriptionHandler),
	('/unsubscribe', UnsubscriptionHandler),
	('/mail/daily', DailyEmailSender)
	], debug=True)
