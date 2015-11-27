#! /usr/bin/python
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor
import sys, urllib2, requests, json, thread, threading
from bs4 import BeautifulSoup
from clint.textui import progress

pre = 'http://www.watchop.se/'

class DownloadThread(threading.Thread):
	def __init__(self, link):
		threading.Thread.__init__(self)
		self.link = link
	def run(self):
		self.res = requests.get(self.link)
		self.url_soup = BeautifulSoup(self.res.text)
		try:
			self.result = self.url_soup.find_all('iframe')[1]
		except:
			self.link = self.link + '-english-sub'
			self.res = requests.get(self.link)
			self.url_soup = BeautifulSoup(self.res.text)
			self.result = self.url_soup.find_all('iframe')[1]

		self.link = 'http://www.watchop.se/' + self.result['src']
		self.res = requests.get(self.link)
		self.url_soup = BeautifulSoup(self.res.text)
		self.result = self.url_soup.find_all('script')[2]
		self.result = str(self.result)
		self.result = self.result.replace('<script type="text/javascript">', ' ')
		self.result = self.result.replace('</script>', ' ')
		self.temp = self.result.split('sources: [')[1]
		self.data = self.temp.split("},")[0] + '}'
		self.a = self.data.split(',')[0]
		self.a = self.a.replace("{", "")
		self.a = self.a.replace('"', '')
		self.dlink = self.a.strip().split()[1]
		self.r = requests.get(self.dlink, stream=True)
		self.total_length = int(self.r.headers.get('content-length'))
		self.f = open(dest + str(epno) + '.mp4', 'wb')
		for self.chunk in progress.bar(self.r.iter_content(chunk_size=1024), expected_size=(self.total_length/1024) + 1): 
			if self.chunk:
				self.f.write(self.chunk)

length = range(int(sys.argv[1]), int(sys.argv[2])+1)
dest = ' '.join(sys.argv[3:]) + '/'
print 'Will Download into %s' % dest
if len(length) < 5:
	for epno in length:
		print 'Downloading ', epno
		link = pre + '/view/one-piece-episode-' + str(epno+0)
		threadi = DownloadThread(link)
		threadi.start()
		threadi.join()	
		print 'Downloaded ', epno
else:
	for epno in range(int(sys.argv[1]), int(sys.argv[2])+1, 5):
		threads = []
		for i in range(0, 5):
			if i > length[-1]:
				continue
			print 'Downloading ', epno+i
			link = pre + '/view/one-piece-episode-' + str(epno+0)
			threadi = DownloadThread(link)
			threads.append(threadi)
		print threads
		for i in threads:
			i.start()
		for i in threads:
			i.join()
		print 'Downloaded '
