# load a YT playlist and feed it into the YT downloader software already on my PC
# move that file to a directory, and rename it to something readable if possible

import re, os, subprocess

playlist = r'https://www.youtube.com/playlist?list=PLnwDsHHQyShyCo7o0hUbG23my2ms_Qp_B'

localFile = open(r'html\yt.html', 'r')

local_string = str((localFile.read()))

regex = '(https:\/\/www.youtube.com/watch\?v=)([^#\&\?]*)(&amp)' # find all video IDs on page

projectsRegex = re.compile(regex)
mo = projectsRegex.findall(local_string)

ID_list = []
for i in range(0, len(mo) - 1):
    ID_list.append(mo[i][1])    # add all video IDs to ID_list

set_list = set(ID_list)     # de-dupe by converting list to set
#print(set_list)

URLs_list = []
for id in set_list:
    URLs_list.append("https://www.youtube.com/watch?v=" + id)
#print(URLs_list)


os.chdir(r"C:\Users\Admin\Desktop\YT downloader")
args = "youtube-dl.exe " + URLs_list[0]
subprocess.call(args)

# this is now working - I can add sophistication around sourcing directory name etc later
