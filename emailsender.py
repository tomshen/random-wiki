from google.appengine.api import mail
from wikiscraper import getRandomArticleData

def sendConfirmationEmail(to_addr):
	if to_addr != "":
		from_addr = "daily@random-wiki.appspotmail.com"

		data = getRandomArticleData()
		subject = 'You\'ve been subscribed to receive daily random Wikipedia articles'
		body = 'You should receive new articles every morning at 5 am, EST.'
		body += '\nTo unsubscribe, go to http://random-wiki.appspot.com/unsubscribe?email=' + to_addr

		mail.send_mail(from_addr, to_addr, subject, body)

def sendRandomWikipediaArticleTo(to_addr):
	if to_addr != "":
		from_addr = "daily@random-wiki.appspotmail.com"

		data = getRandomArticleData()
		subject = 'Daily Random Wikipedia Article: \"' + data['title'] + '\"'
		body = data['info'].decode('UTF-8') + '\n\nFor more information go to: ' + data['url']
		body += '\nTo unsubscribe, go to http://random-wiki.appspot.com/unsubscribe?email=' + to_addr

		mail.send_mail(from_addr, to_addr, subject, body)