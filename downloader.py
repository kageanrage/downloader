# load a YT playlist and feed it into the YT downloader software already on my PC
# move that file to a directory, and rename it to something readable if possible

import re, os, subprocess, time, shutil, smtplib


def which_pc():
    if os.path.exists(r"C:\Program Files\StableBit\DrivePool"):
        return 'desktop'
    else:
        return 'laptop'


def get_ytdl_dir():
    if machine == 'desktop':
        print("Kev's Home PC detected, setting YT Downloader and Plex library directories accordingly\n")
        direc = r"C:\Users\kevin\Desktop\Youtube Downloader"   # note this this the hardcoded directory for when working on Home PC
    else:
        print("This isn't Kev's Home PC, must be laptop, so setting YT Downloader directory accordingly\n")
        direc = r"C:\Users\Admin\Desktop\YT downloader"
    return direc


def get_library_dir():
    if machine == 'desktop':
        direc = r"C:\Github local repos\test"   # TEST - note this this the hardcoded directory on Home PC
    else:
        direc = r"C:\Users\Admin\Desktop\YT downloader\library_dir"
    return direc


def get_config_file():
    if machine == 'desktop':
        config = r"C:\Github local repos\dont_share\config.txt"   # TEST - note this this the hardcoded directory on Home PC
    else:
        config = r"C:\KP Python\dont_share\config.txt"
    return config


def get_em_access():
    f = open(config_file, 'r')  # import config info
    f_str = str((f.read()))  # import config info
    p = f_str[19:31]
    u = f_str[44:67]
    return u, p


def get_playlist_url():
    f = open(config_file, 'r')  # import config info
    f_str = str((f.read()))  # import config info
    url = f_str[83:155]
    return url


def generate_mo(string_to_search):
    regex = '(https:\/\/www.youtube.com/watch\?v=)([^#\&\?]*)(&amp)'  # find all video IDs in string
    projectsRegex = re.compile(regex)  # define Regex
    match_object = projectsRegex.findall(string_to_search)  # search string using Regex
    return match_object


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


machine = which_pc()    # determine if on Home PC or laptop
config_file = get_config_file()     # access config file
u_and_p = get_em_access()   # returns u p tuple for em access
# send_email(u_and_p[0], u_and_p[1], u_and_p[0], 'subject text is this', 'message body is this text') # send em
playlist = get_playlist_url()  # get yt playlist URL, not yet in use
localFile = open(r'html\yt.html', 'r')  # test mode - uses pre-downloaded HTML
local_string = str((localFile.read()))  # test mode - converts downloaded HTML to string
mo = generate_mo(local_string)

ytid_list = set([mo[i][1] for i in range(0, len(mo) - 1)])  # add all found video IDs to ID_list
URLs_list = ["https://www.youtube.com/watch?v=" + ytid for ytid in ytid_list]   # expand yt ids to yt URLs
print('URLs list is: {}'.format(URLs_list))

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
