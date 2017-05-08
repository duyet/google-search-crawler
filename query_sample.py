from google import search
import pprint

KEYWORDS = 'duyetdev'

data = []
for d in search(KEYWORDS, tld='com.vn', lang='vi', stop=10):
	data.append(d)

print pprint.pprint(data)