import os

directory = os.getcwd()
print directory

path = directory + "/shell.avi"
print path

os.remove(path)
