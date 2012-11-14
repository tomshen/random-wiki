#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2
from HTMLParser import HTMLParser

url = 'http://en.wikipedia.org/w/index.php?title=Special:Random&printable=yes'

def getRandomArticleData():
	return scrapePage(url)

def scrapePage(url):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	html = opener.open(url).read().decode('UTF-8')
	html = html[:html.index('</p>')]
	scraper = WikiPageScraper()
	scraper.feed(html)
	data = scraper.getData()
	scraper.close()
	return data

class WikiPageScraper(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.data = {}
		self.data['title'] = ""
		self.data['info'] = ""
		self.data['url'] = ""
		self.foundTitle = False
		self.foundInfo = False
		self.done = False

	def handle_starttag(self, tag, attrs):
		if tag == 'link' and len(attrs) == 3 and attrs[0][1] == 'edit':
			url = attrs[2][1]
			self.data['url'] = 'http://en.wikipedia.org/wiki/' + url[url.index('=')+1:url.index('&')]
		if not self.done:
			if tag == 'title':
				self.foundTitle = True
			elif tag == 'p':
				self.foundInfo = True

	def handle_endtag(self, tag):
		if self.foundTitle:
			self.foundTitle = False
		if tag == 'p' and self.foundInfo:
			self.foundInfo = False
			self.done = True
			
	def handle_data(self, data):
		if self.foundTitle:
			i = data.find(' - Wikipedia, the free encyclopedia')
			if i != -1:
				self.data['title'] = data[:i]
			else:
				self.data['title'] = data
		if self.foundInfo:
			try:
				self.data['info'] += data.encode('UTF-8')
			except:
				pass
		
	def getData(self):
		self.data['info'] = self.data['info'].strip()
		return self.data