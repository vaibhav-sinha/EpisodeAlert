from bs4 import BeautifulSoup
import requests
import datetime
from datetime import date
import re
import sys
import signal

def handler(signum,frame):
	print("Dumping database to file and exiting.")
	f = open('db.dump.txt','w')
	for name,url in db.items():
		f.write(name + ' ' + url + '\n')
	f.close()
	exit(0)

signal.signal(signal.SIGINT,handler)

def check(name,url):
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)

	done = 0
	for node in soup.find_all('tr',attrs={'class':'vevent'}):
		#if node.find_next('td').find_next('td').string is None and not done:
		if not done:
			rd = (node.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('span').find_next('span').string)
			if rd:
				m = re.search('(\d+)-(\d+)-(\d+)',rd)
				if m:
					#continue
					k = datetime.date(int(m.group(1)),int(m.group(2)),int(m.group(3)))
					t = date.today()
					if k > t:
						print(name + ':' + k.strftime('%d/%m/%y'))
						done = 1
					if k== t:
						print(name + ':' + 'New Episode Today :)')
						done = 1
	if not done:
		print(name + ':' + 'Next episode info not available for this show')


db = {}
try:
	f = open('db.dump.txt','r')
	for line in f:
		l = line.split()
		db[l[0]] = l[1]
	f.close()
except (OSError,IOError) as e:
	print('No existing database. Looks like you are running the script for the first time')

print("Choose an option:\n 1.Add new show\n 2.Check the date of next episode\n 3.Remove a show\n 4.Get the list of shows\n 5.Exit")
while 1:
	opt = input('>')
	opt = int(opt)

	if opt == 1:
		name = input('Enter the name of the show: ')
		url = input('Enter the Wikipedia Episode List page URL for the show: ')
		db[name] = url
	elif opt == 2:
		for name,url in db.items():
			check(name,url)
	elif opt == 3:
		name = input('Enter the name of show to remove: ')
		del db[name]
	elif opt == 4:
		for key in db:
			print(key)
	elif opt == 5:
		f = open('db.dump.txt','w')
		for name,url in db.items():
			f.write(name + ' ' + url + '\n')
		f.close()
		exit(0)
	else:
		print("Invalid option. Try again.\n")