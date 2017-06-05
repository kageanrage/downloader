# load a YT playlist and feed it into the YT downloader software already on my PC
# move that file to a directory, and rename it to something readable if possible
import re, bs4

"""
playlist = r'https://www.youtube.com/playlist?list=PLnwDsHHQyShyCo7o0hUbG23my2ms_Qp_B'


localFile = open(r'C:\Github local repos\downloader\html\yt.html')
exampleSoup = bs4.BeautifulSoup(localFile, "html.parser")  # turns the HTML into a beautiful soup object
htmlString = str(exampleSoup)


# the following regex seems to be able to isolate youtube video IDs from the source code of the playlist
regex = '(v=)([^#\&\?]*)(&amp)'
#regex2 = 'watch'

projectsRegex = re.compile(regex)
#projectsRegex = re.compile(regex2)

mo = projectsRegex.findall(htmlString)

print(mo)

# can't work out why the regex is only returning one search result

"""



import urllib
import re

localFile = open(r'C:\Github local repos\downloader\html\yt.html')
soup = bs4.BeautifulSoup(localFile, "html.parser")  # turns the HTML into a beautiful soup object

linkElems = soup.find_all('a', href=True)
print(linkElems)
