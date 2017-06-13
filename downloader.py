# load a YT playlist and feed it into the YT downloader software already on my PC
# move that file to a directory, and rename it to something readable if possible

import re, os, subprocess, time, shutil, smtplib, requests, bs4


def which_pc():
    if os.path.exists(r"C:\Program Files\StableBit\DrivePool"):
        return 'desktop'
    else:
        return 'laptop'


def get_config_file():
    if machine == 'desktop':
        config = r"C:\Github local repos\dont_share\config.txt"
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


def get_ytdl_dir():
    if machine == 'desktop':
        direc = r"C:\Users\kevin\Desktop\Youtube Downloader"   # note this this the hardcoded directory for when working on Home PC
        # print("Kev's Home PC detected, setting YT Downloader dir to {}".format(direc))
    else:

        direc = r"C:\Users\Admin\Desktop\YT downloader"
        # print("This isn't Kev's Home PC, must be laptop, so setting YT Downloader dir to {}\n".format(direc))
    return direc


def get_library_dir():
    if machine == 'desktop':
        direc = r"H:\Downloads\Server Downloads\Complete\Other video\AutoDownload"   # TEST - note this this the hardcoded directory on Home PC
    else:
        direc = r"C:\Users\Admin\Desktop\YT downloader\library_dir"
    return direc


def get_base_dir():
    if machine == 'desktop':
        direc = r"C:\Github local repos\downloader"   # TEST - note this this the hardcoded directory on Home PC
    else:
        direc = r"C:\KP Python\downloader"
    return direc


def generate_mo(string_to_search):
    regex = '(\/watch\?v=)([^#\&\?]*)(&amp)'  # find all video IDs in string
    projectsRegex = re.compile(regex)  # define Regex
    match_object = projectsRegex.findall(string_to_search)  # search string using Regex
    return match_object


def get_URLs_list(m_o):
    ytid_list = set([m_o[i][1] for i in range(0, len(m_o) - 1)])  # add all found video IDs to ID_list
    URLs_list = ["https://www.youtube.com/watch?v=" + ytid for ytid in ytid_list]   # expand yt ids to yt URLs
    # print('URLs list is: {}'.format(URLs_list))
    return URLs_list


def download_videos(urlz):
    os.chdir(get_ytdl_dir())
    exe = "youtube-dl.exe"
    exe_with_path = os.path.join(ytdl_path, exe)
    for url in urlz:
        args = url
        command = exe_with_path + " " + args
        # print('TEST - pretending to download {}'.format(command))
        subprocess.call(command)
        # print('Sleeping for 3 sec...')
        # time.sleep(3)


def move_videos(ytdl_path2, movie_extensions2, lib_dir2):
    os.chdir(ytdl_path2)  # change cwd to the desired directory
    abspath_yt = os.path.abspath('.')  # define abspath
    for filename in os.listdir(ytdl_path2):  # for each file in folder
        basename, ext = os.path.splitext(filename)  # isolate basename and extensions
        if ext in movie_extensions2:
            original_fullname = os.path.join(abspath_yt, filename)
            new_fullname = os.path.join(lib_dir2, filename)
            # print('Original fullname is {} \n New fullname is {}\n'.format(original_fullname, new_fullname))
            print('moving {} to {}'.format(original_fullname, new_fullname))
            shutil.move(original_fullname, new_fullname)  # move the video files to the library folder
        else:
            print('{} not a video file so not moving'.format(filename))


def check_for_new_urls(urlz):
    os.chdir(get_base_dir())
    urls_file = open(os.path.join(os.getcwd(), 'urls.txt'), 'r')
    content = urls_file.read()
    new_urlz = []
    for url in urlz:
        if url not in content:
            urls_file.close()
            urls_file = open(os.path.join(os.getcwd(), 'urls.txt'), 'a')
            print('New URL found and added to URLs.txt: {}'.format(url))
            urls_file.write(str(url) + '\n')
            new_urlz.append(url)
    urls_file.close()
    return new_urlz


def send_email(u, p, recipient, subject, urlz):

    gm_u = u
    gm_p = p
    FROM = u
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = 'The following videos have been downloaded: {}'.format(urlz)

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


def get_local_string():
    if test_mode:
        file = open(r'html\yt.html', 'r')  # test mode - uses pre-downloaded HTML
        string = str((file.read()))
        return string

    else:
        res = requests.get(playlist)
        data = res.text
        soup = bs4.BeautifulSoup(data, "lxml").encode("ascii") # encode is to neutralise weird characters
        the_string = str(soup)
        # print('Soup is {}'.format(soup))
        # print('String is {}'.format(string))
        os.chdir(get_base_dir())
        # source_file = open(os.path.join(os.getcwd(), 'source.txt'), 'w')  # just to view source if desired
        # source_file.write(the_string)  # just to view source if desired
        # source_file.close()  # just to view source if desired
        return the_string

test_mode = False

machine = which_pc()    # determine if on Home PC or laptop
config_file = get_config_file()     # access config file
u_and_p = get_em_access()   # returns u p tuple for em access
playlist = get_playlist_url()  # get yt playlist URL, not yet in use
local_string = get_local_string()
mo = generate_mo(local_string)  # pass in string to search and return match object
urls = get_URLs_list(mo)    # pass in mo and return list of YT video URLs
ytdl_path = get_ytdl_dir()   # define YT Downloader dir depending on if Home PC or laptop
new_urls = check_for_new_urls(urls) # return any URLs which were not in the txt file, as a list, and add them to txt
download_videos(new_urls)   # download the videos, CURRENTLY WILL ONLY DL FIRST IN LIST
if len(new_urls) > 0:
    abspath = os.path.abspath('.')  # define abspath
    lib_dir = get_library_dir()     # define library dir (depends which PC I'm on)
    movie_extensions = ['.mov', '.mp4', '.mkv', '.avi', '.flv', '.webm']
    move_videos(ytdl_path, movie_extensions, lib_dir)  # TO DO: currently this script only uses the first ID / URL detected. Need to tell it to use only newly found ones
    send_email(u_and_p[0], u_and_p[1], u_and_p[0], 'Py Script - new vids DLed from YT', new_urls)  # send em
