#! /usr/bin/python
import sys, requests
from bs4 import BeautifulSoup
from clint.textui import progress

pre = 'http://www.watchop.se/'

def run(link):
	res = requests.get(link)
	url_soup = BeautifulSoup(res.text)
	try:
		result = url_soup.find_all('iframe')[1]
	except:
		link = link + '-english-sub'
		res = requests.get(link)
		url_soup = BeautifulSoup(res.text)
		result = url_soup.find_all('iframe')[1]

	link = 'http://www.watchop.se/' + result['src']
	res = requests.get(link)
	url_soup = BeautifulSoup(res.text)
	result = url_soup.find_all('script')[2]
	result = str(result)
	result = result.replace('<script type="text/javascript">', ' ')
	result = result.replace('</script>', ' ')
	temp = result.split('sources: [')[1]
	data = temp.split("},")[0] + '}'
	a = data.split(',')[0]
	a = a.replace("{", "")
	a = a.replace('"', '')
	dlink = a.strip().split()[1]
	r = requests.get(dlink, stream=True)
	total_length = int(r.headers.get('content-length'))
	f = open(dest + str(epno) + '.mp4', 'wb')
	for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
		if chunk:
			f.write(chunk)

dest = ' '.join(sys.argv[3:]) + '/'
print 'Will Download into %s' % dest
for epno in range(int(sys.argv[1]), int(sys.argv[2])+1):
	print 'Downloading ', epno
	link = pre + '/view/one-piece-episode-' + str(epno+0)
	run(link)