# load a YT playlist and feed it into the YT downloader software already on my PC
# move that file to a directory, and rename it to something readable if possible

import re, os, subprocess, time, shutil, smtplib


def get_ytdl_dir():
    if os.path.exists(r"C:\Program Files\StableBit\DrivePool"):
        print("Kev's Home PC detected, setting YT Downloader and Plex library directories accordingly\n")
        direc = r"NEED TO ADD THIS"   # note this this the hardcoded directory for when working on Home PC
    else:
        print("This isn't Kev's Home PC, must be laptop, so setting YT Downloader directory accordingly\n")
        direc = r"C:\Users\Admin\Desktop\YT downloader"
    return direc


def get_library_dir():
    if os.path.exists(r"C:\Program Files\StableBit\DrivePool"):
        direc = r"NEED TO ADD THIS"   # note this this the hardcoded directory for when working on Home PC
    else:
        direc = r"C:\Users\Admin\Desktop\YT downloader\library_dir"
    return direc


def get_gm_access():
    f = open(r'C:\KP Python\dont_share\config.txt', 'r')  # import config info
    f_str = str((f.read()))  # import config info
    p = f_str[19:30]
    u = f_str[43:66]
    return u, p


def send_email(u, p, recipient, subject, body):

    gm_u = u
    gm_p = p
    FROM = u
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gm_u, gm_p)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print('failed to send mail')


u_and_p = get_gm_access()   # returns u p tuple for gm

send_email(u_and_p[0], u_and_p[1], u_and_p[0], 'subject text is this', 'message body is this text')


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


ytdl_path = get_ytdl_dir()   # define YT Downloader dir depending on if Home PC or laptop

exe = "youtube-dl.exe"
args = URLs_list[0]             # this uses just the first URL in the list
exe_with_path = os.path.join(ytdl_path, exe)
to_dl = exe_with_path + " " + args
#subprocess.call(to_dl)
#time.sleep(20)

os.chdir(ytdl_path) # change cwd to the desired directory
abspath = os.path.abspath('.')  # define abspath
lib_dir = get_library_dir()     # define library dir (depends which PC I'm on)
movie_extensions = ['.mov', '.mp4', '.mkv', '.avi', '.flv']
for filename in os.listdir(ytdl_path):  # for each file in folder
    basename, ext = os.path.splitext(filename) # isolate basename and extensions
    if ext in movie_extensions:
        original_fullname = os.path.join(abspath, filename)
        new_fullname = os.path.join(lib_dir, filename)
        # print('Original fullname is {} \n New fullname is {}\n'.format(original_fullname, new_fullname))
        print('moving {} to {}'.format(original_fullname, new_fullname))
        shutil.move(original_fullname, new_fullname)    # move the video files to the library folder


# TO DO: currently this script only uses the first ID / URL detected. Need to tell it to use only newly found ones
# TO DO: send email to kevinjpickett@gmail.com ; or send PB notification, to notify me
# TO DO: set to run at a particular time of day
