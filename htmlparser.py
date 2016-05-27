from HTMLParser import HTMLParser
import urllib2

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    print attr[1]

address='www.address.com'
html = urllib2.urlopen(address).read()
f = open('parsedoutput.txt', 'wb')
f.write(html)
f.close()

parser = MyHTMLParser()
parser.feed(html)
