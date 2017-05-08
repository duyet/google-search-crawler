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

```json
[
  {
    "url": "http://blog.duyet.net/",
    "description": "ext { global sitemap | archive | google site | levanduyet.xyz | drop me a line me(a)\nduyetdev.com } [c] 2014-2016 duyetdev mọi quyền được bảo lưu DMCA.com ...",
    "title": "Tôi là Duyệt"
  },
  {
    "url": "https://github.com/duyetdev",
    "description": "duyetdev has 298 repositories available. Follow their code on GitHub.",
    "title": "duyetdev (Van-Duyet Le) · GitHub"
  },
  {
    "url": "https://me.duyetdev.com/",
    "description": "Full-Stack Developer - I am passion about building awesome products, also rock \nin Javascript, Nodejs and Machine Learning.",
    "title": "Van-Duyet Le - duyetdev"
  },
  {
    "url": "http://ask.duyetdev.com/",
    "description": "10 Tháng 2 2016 ... Mỗi khi có ai đó hỏi về anh, mình thường trả lời rằng đây là “bạn em\". Đó không \nphải vì ngại ngần khi giới thiệu đây là “người yêu” hay “bạn ...",
    "title": "#duyetdev"
  },
  {
    "url": "https://kipalog.com/tags/duyetdev",
    "description": "JavaPoly.js: Java(script) in the Browser Polyfills native, hỗ trợ JVM, bạn có thể \nimport file Jar, biên dịch và chạy trực tiếp mã Java ngay trên t... Duyệt viết 11 ...",
    "title": "duyetdev - Kipalog"
  },
  {
    "url": "https://duyetdev.wordpress.com/",
    "description": "",
    "title": ""
  },
  {
    "url": "https://duyetdev.github.io/",
    "description": "Backend Development. node.js. Installation paths: use one of these techniques to \ninstall node and npm without having to sudo. Node.js HOWTO: Install ...",
    "title": "duyetdev –"
  },
  {
    "url": "https://nodejs.vn/user/duyetdev",
    "description": "Posts made by duyetdev. RE: Framework nào tối ưu và tiết kiệm thời gian cho \nviệc làm Web? Mình dùng qua cũng nhiều framework rồi. Thích nhất là SailJS và\n ...",
    "title": "duyetdev | A Community Node.js - Nodejs.vn"
  },
  {
    "url": "https://trello.com/duyetdev",
    "description": "Organize anything, together. Trello is a collaboration tool that organizes your \nprojects into boards. In one glance, know what's being worked on, who's working\n ...",
    "title": "Lê Văn Duyệt (duyetdev) - Trello"
  }
]
```

------------------------
Thanks for https://pypi.python.org/pypi/google
