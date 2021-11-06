import requests
import urllib.request
from urllib.request import urlopen
import nltk
from bs4 import BeautifulSoup

# Input url
url = input("Url: ")

# Get html code
html = urlopen(url).read()

# Remove html
soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())

# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)
