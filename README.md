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

```
[{'description': u'ext { global sitemap | archive | google site | levanduyet.xyz | drop me a line me(a)\nduyetdev.com } [c] 2014-2016 duyetdev m\u1ecdi quy\u1ec1n \u0111\u01b0\u1ee3c b\u1ea3o l\u01b0u DMCA.com\xa0...',
  'title': u'T\xf4i l\xe0 Duy\u1ec7t',
  'url': u'http://blog.duyet.net/'},
 {'description': u'duyetdev has 298 repositories available. Follow their code on GitHub.',
  'title': u'duyetdev (Van-Duyet Le) \xb7 GitHub',
  'url': u'https://github.com/duyetdev'},
 {'description': u'Full-Stack Developer - I am passion about building awesome products, also rock \nin Javascript, Nodejs and Machine Learning.',
  'title': u'Van-Duyet Le - duyetdev',
  'url': u'https://me.duyetdev.com/'},
 {'description': u'10 Th\xe1ng 2 2016 ... M\u1ed7i khi c\xf3 ai \u0111\xf3 h\u1ecfi v\u1ec1 anh, m\xecnh th\u01b0\u1eddng tr\u1ea3 l\u1eddi r\u1eb1ng \u0111\xe2y l\xe0 \u201cb\u1ea1n em". \u0110\xf3 kh\xf4ng \nph\u1ea3i v\xec ng\u1ea1i ng\u1ea7n khi gi\u1edbi thi\u1ec7u \u0111\xe2y l\xe0 \u201cng\u01b0\u1eddi y\xeau\u201d hay \u201cb\u1ea1n\xa0...',
  'title': u'#duyetdev',
  'url': u'http://ask.duyetdev.com/'},
 {'description': u'JavaPoly.js: Java(script) in the Browser Polyfills native, h\u1ed7 tr\u1ee3 JVM, b\u1ea1n c\xf3 th\u1ec3 \nimport file Jar, bi\xean d\u1ecbch v\xe0 ch\u1ea1y tr\u1ef1c ti\u1ebfp m\xe3 Java ngay tr\xean t... Duy\u1ec7t vi\u1ebft 11\xa0...',
  'title': u'duyetdev - Kipalog',
  'url': u'https://kipalog.com/tags/duyetdev'},
 {'description': '', 'title': u'', 'url': u'https://duyetdev.wordpress.com/'},
 {'description': u'Backend Development. node.js. Installation paths: use one of these techniques to \ninstall node and npm without having to sudo. Node.js HOWTO: Install\xa0...',
  'title': u'duyetdev \u2013',
  'url': u'https://duyetdev.github.io/'},
 {'description': u'Posts made by duyetdev. RE: Framework n\xe0o t\u1ed1i \u01b0u v\xe0 ti\u1ebft ki\u1ec7m th\u1eddi gian cho \nvi\u1ec7c l\xe0m Web? M\xecnh d\xf9ng qua c\u0169ng nhi\u1ec1u framework r\u1ed3i. Th\xedch nh\u1ea5t l\xe0 SailJS v\xe0\n\xa0...',
  'title': u'duyetdev | A Community Node.js - Nodejs.vn',
  'url': u'https://nodejs.vn/user/duyetdev'},
 {'description': u"Organize anything, together. Trello is a collaboration tool that organizes your \nprojects into boards. In one glance, know what's being worked on, who's working\n\xa0...",
  'title': u'L\xea V\u0103n Duy\u1ec7t (duyetdev) - Trello',
  'url': u'https://trello.com/duyetdev'}]

```

------------------------
Thanks for https://pypi.python.org/pypi/google
