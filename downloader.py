# load a YT playlist and feed it into the YT downloader software already on my PC
# move that file to a directory, and rename it to something readable if possible

import re, os, subprocess, time

# sets YT downloader dir depending on if running on Home PC or laptop
def tell_me_which_directory():
    if os.path.exists(r"C:\Program Files\StableBit\DrivePool"):
        print("Kev's Home PC detected, setting YT Downloader directory accordingly\n")
        direc = r"NEED TO ADD THIS"   # note this this the hardcoded directory for when working on Home PC
    else:
        print("This isn't Kev's Home PC, must be laptop, so setting YT Downloader directory accordingly\n")
        direc = r"C:\Users\Admin\Desktop\YT downloader"
    return direc


playlist = r'https://www.youtube.com/playlist?list=PLnwDsHHQyShyCo7o0hUbG23my2ms_Qp_B'  # not yet in use

localFile = open(r'html\yt.html', 'r')  # test mode - uses pre-downloaded HTML
local_string = str((localFile.read()))  # test mode - converts downloaded HTML to string

regex = '(https:\/\/www.youtube.com/watch\?v=)([^#\&\?]*)(&amp)' # find all video IDs in string

projectsRegex = re.compile(regex)       # define Regex
mo = projectsRegex.findall(local_string)    # search string using Regex

ID_list = []
for i in range(0, len(mo) - 1):
    ID_list.append(mo[i][1])    # add all found video IDs to ID_list

set_list = set(ID_list)     # de-dupe ID list by converting list to set

URLs_list = []
for id in set_list:
    URLs_list.append("https://www.youtube.com/watch?v=" + id)   # convert IDs to full Youtube URLs
#print(URLs_list)


ytdl_path = tell_me_which_directory()   # define YT Downloader dir depending on if Home PC or laptop

exe = "youtube-dl.exe"
args = URLs_list[0]             # this uses just the first URL in the list
exe_with_path = os.path.join(ytdl_path, exe)
to_dl = exe_with_path + " " + args
#subprocess.call(to_dl)
#time.sleep(20)

def get_video_filename(fname, folname, abspath):
    movie_extensions = ['.mov', '.mp4', '.mkv', '.avi', '.flv']
    basename, ext = os.path.splitext(fname) # isolate basename and extensions
    if ext in movie_extensions:
        # print('Movie file detected in {}: {}'.format(folname, fname))
        fname_with_path = os.path.join(abspath, folname, fname)    # new name incl path
        return fname_with_path

os.chdir(ytdl_path) # change cwd to the desired directory
abspath = os.path.abspath('.')  # define abspath
movie_files_detected = []
for folderName, subfolders, filenames in os.walk(ytdl_path):
    for filename in filenames:
        if get_video_filename(filename, folderName, abspath) != None:
            movie_files_detected.append(get_video_filename(filename, folderName, abspath))
print('Video files found: {}'.format(movie_files_detected))

# TO DO: currently this script only uses the first ID / URL detected. Need to tell it to use only newly found ones
# TO DO: Move video files to Plex Library directory
# TO DO: send email to kevinjpickett@gmail.com ; or send PB notification, to notify me
# TO DO: set to run at a particular time of day




