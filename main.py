import requests
import json
import sys
from os import listdir
from os.path import isfile, join

from Imagelib import *
from AI import *

baseurl = 'http://localhost:10000'
command = ['start','train','test']

if len(sys.argv)==2 and sys.argv[1] not in command:
	print "Usage : python {0} COMMAND".format(sys.argv[0])
	print "init  - Set inital learning data"
	print "train - OCR challenge with training"
	print "test  - OCR challenge"
	sys.exit(-1)

if len(sys.argv)==1:
	IA = AI()
else:
	IA = AI(sys.argv[1])

with requests.Session() as s:
	r = s.post(baseurl + '/start')
	url = baseurl + r.text

	path = './data/nums/'
	for stage in range(1,101):
		extract_number(url)
		result = ''
		
		files = sorted([int(f.split('.')[0]) for f in listdir(path)])
	
		for fidx in files:
			result += str(int(IA.OCR(path+'{0}.png'.format(fidx))[0][0]))
		
		print "stage {0} - OCR result : {1}".format(stage,result)

		r = s.post(baseurl + '/check', data={'ans' : result})
		if stage == 100:
		url = json.loads(r.text)['url']
		url = baseurl + url

	print r.text 

