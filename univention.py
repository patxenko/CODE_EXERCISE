import sys
import pwd
import grp
import shutil
import db
import logging
import os
import re
import string

destination_directory = '/mnt/c/Users/lopezfr/Desktop/CODE_CHALLENGE/destination'
username = str(pwd.getpwuid(os.getuid())[0])

'''
-------------------------------------- LOGGER --------------------------------------
'''
logger = logging.getLogger('uninvention')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('grouper.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

db_cls = db.DB()
if len(sys.argv) <= 1:
    print("[error] You must specify the group name as first parameter")
    exit()
pattern = r'[' + string.punctuation + ']'
group_name = re.sub(pattern, '', sys.argv[1])  # Remove special characters from the string
logger.info(username + " launch for group %s " % group_name)
try:
    db_cls.block_group(group_name)  # Check if blocked, if not we block it till the process ends
    g = grp.getgrnam(group_name)
    for member in g.gr_mem:
        user = pwd.getpwnam(member)
        user_dir = user.pw_dir
        group_dir = destination_directory + "/" + group_name
        final_dir = destination_directory + "/" + group_name + "/" + user.pw_name
        if os.path.exists(group_dir):
            shutil.rmtree(group_dir)
        shutil.copytree(user_dir, final_dir, True)
    db_cls.unblock_group(group_name)  # Unblock the group when finished
except Exception as e:
    logger.error("%s" % str(e) + " user: " + username)
