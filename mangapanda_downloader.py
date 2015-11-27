#! /usr/bin/python
'''

Script By : Aadesh 
Download manga from MangaPanda:

Link format:
http://www.mangapanda.com/naruto/684/2

multithreaded program, each thread will download one page.

1. take series name
2. take lower, upper limit of episods
3. iterate through episodes and download each to new dir using multiple threads

'''

from bs4 import BeautifulSoup
import urllib
import os
import sys
import thread
import threading
import time

class DownloadThread(threading.Thread):
	def __init__(self, epno, pageno):
		threading.Thread.__init__(self)
		self.epno = epno
		self.pageno = pageno
	def run(self):
		if(self.pageno != 1):
			link = 'http://www.mangapanda.com/' + series + '/' + str(self.epno) + '/' + str(self.pageno)
		else:
			link = 'http://www.mangapanda.com/' + series + '/' + str(self.epno)
		
		dir_link = os.getcwd() + '/' + str(self.epno)
	
		try :  
			if not os.path.exists(dir_link):
				print "making dir", dir_link		
				os.makedirs(dir_link)
		except :
			pass
		
		file_link = dir_link + '/' + str(self.pageno) + '.jpg'

		try:
			url_response = urllib.urlopen(link).read()
	        url_soup = BeautifulSoup(url_response)
		except:
			return

		if not url_soup.find_all('img'):
			return
		else:
			for comiclink in url_soup.find_all('img',{'id':'img'}):	
			      	time.sleep(1)
				reallink = comiclink['src']
				if not os.path.exists(file_link):
					print "downloading " , self.epno, self.pageno
               		         	image_response = urllib.urlopen(reallink).read()
 					with open (file_link,"wb") as data:				
						data.write(image_response)
				else:
					return
		#print "exiting thread ", self.pageno

def download_episode(epno):
	#link = 'http://www.mangapanda.com/' + series + '/' + str(epno)
	#create threads for each page
	print "downloading episode", epno
	threads = []
	for i in range(1, 21):
		threadi = DownloadThread(epno, i)
		threads.append(threadi)
	for i in range(0, 20):
		threads[i].start()
	for i in range(0, 20):
		threads[i].join()
	print "exiting episode", epno

print "I will download Manga for you, in this directory\n"
series = raw_input("Enter series name(eg. naruto)\n")
lower, upper = raw_input("Enter Episodes range to download (e.g. 1 700)\n").split()
lower = int(lower)
upper = int(upper)
for no in range(lower, upper+1):
	download_episode(no)
