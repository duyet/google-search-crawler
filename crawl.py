from google import search
import pandas as pd 
import os
import json

df = pd.read_csv('comscore_gender.csv')
domains = df.domain.tolist()

for u in domains:
	save_to = 'results/%s.json' % u
	if not os.path.isfile(save_to):
		print("Start %s ..." % u)
		result = []
		for data in search('site:%s' % u, tld='com.vn', lang='vi', stop=40):
			result.append(data)
		with open(save_to, 'wb') as f:
			f.write(json.dumps(result))
			print "Done! Sato %s rows to %s" % (len(result), save_to)