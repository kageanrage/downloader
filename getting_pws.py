localFile = open(r'C:\KP Python\dont_share\config.txt', 'r')  # import config info
local_string = str((localFile.read()))  # import config info
pw = local_string[19:30]
