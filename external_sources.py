#!/usr/bin/env python
#import urllib2
#from bs4 import BeautifulSoup
## or if your're using BeautifulSoup4:
## from bs4 import BeautifulSoup
#
#soup = BeautifulSoup(requests.get('http://www.timeanddate.com/worldclock/astronomy.html??n=78').text)
#
#for row in soup('table', {'class' : 'spad'})[0].tbody('tr'):
#  tds = row('td')
#  print tds[0].string, tds[1].string
#  # will print date and sunrise
#
from html5lib import * 
import urllib2 
import re

#TODO: [d] See http://www.ehow.co.uk/how_8521125_use-html5lib-python.html
#parser = html5lib.HTMLParser() 
def scrape_edubase(urn = "138825"):#TODO: [i] [refactor] as API that returns specific scraped components of pages (e.g. given URN, get size of school & website).
  """Returns the full HTML as text for a given school Edubase page, found by number. Uses html5lib to scrape Edubase."""
  #HACK: If no URN, uses GCS. Remove.
  constructed_URI = "http://www.education.gov.uk/edubase/establishment/summary.xhtml?urn=" + urn 
  text = urllib2.urlopen(constructed_URI).read() 
  #At this point, text is full HTML, including unsafe and unwanted links to CSS, javscript etc..
  text = re.subn(r'<(script).*?</\1>(?s)', '', text)[0]#My attempt: re.sub(r"((<)script(>)).*((<)(/)script(>))?", "", text)
  #text = re.sub("</script>", "", text)
  return text

if __name__ == '__main__':
  print("manual test of external checks using a specific URN")
  urn = "138825"
  print(scrape_edubase())
