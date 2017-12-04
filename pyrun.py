#!/usr/bin/env python


import os
import sys



path = './prepare'
os.chdir(path)
command = 'python 04_files_finder.py'
os.system(command)


path = '../hw2'
os.chdir(path)
command = 'python 01_m.py'
os.system(command)

command = 'python 02_m.py'
os.system(command)


path = '../count'
os.chdir(path)
command = 'python users.py'
os.system(command)

command = 'python 03_m.py'
os.system(command)

command = 'python dates_users.py'
os.system(command)

command = 'python 04_2_m.py'
os.system(command)


path = '../transfer'
os.chdir(path)
command = 'python 03_transfer.py'
os.system(command)

command = 'python 04_1_transfer.py'
os.system(command)

command = 'python 04_2_transfer.py'
os.system(command)


path = '../count/facebook'
os.chdir(path)
command = 'python new_facebook_users.py'
os.system(command)

command = 'python signup.py'
os.system(command)

command = 'python fs.py'
os.system(command)

path = '../../transfer'
os.chdir(path)
command = 'python 05_transfer.py'
os.system(command)


path = '../count/'
os.chdir(path)

command = 'python timestamp.py'
os.system(command)

command = 'python 01_m.py'
os.system(command)


path = '../transfer'
os.chdir(path)

command = 'python 01_transfer.py'
os.system(command)

command = 'python 02_transfer.py'
os.system(command)
