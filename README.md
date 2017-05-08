# google-search-crawler
Input list of keywords, crawler top (url, title, description) data from Google Search.


```python
from google import search

KEYWORDS = 'duyetdev'

data = []
for data in search(KEYWORDS, tld='com.vn', lang='vi', stop=10):
	result.append(data)

print data
```



------------------------
Thanks for https://pypi.python.org/pypi/google
