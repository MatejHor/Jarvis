#!/usr/bin/python

import os
import subprocess
import platform
import sys
import argparse


def get_drives():
    response = os.popen("wmic logicaldisk get caption")
    list1 = []
    total_file = []
    for line in response.readlines():
        line = line.strip("\n")
        line = line.strip("\r")
        line = line.strip(" ")
        if (line == "Caption" or line == ""):
            continue
        list1.append(line)
    return list1


def windows_search(file, path='C:\\\\', stdout=True):
    command = "where /R " + path + " " + file
    return command_run(command, stdout)


def linux_search(file, path='/', stdout=True):
    command = "find " + path + " -name \"" + file + "\""
    return command_run(command, stdout)


def command_run(command, stdout=True):
    if stdout:
        stdout = sys.stdout
    else:
        stdout = subprocess.PIPE
    result_ = subprocess.run(command, shell=True, stderr=subprocess.PIPE, stdout=stdout)
    return result_.stdout


def search(file, path):
    if platform.system() == "Windows":
        # print(get_drives())
        if path:
            windows_search(file=file, path=path + "\\\\")
        else:
            [windows_search(file=file, path=drive + "\\\\") for drive in get_drives()]
    else:
        linux_search(file=file, path=path)

def findall(directory):
    files=os.listdir(directory)
    for fl in files:
        path=os.path.join(directory,fl)
        if os.path.isdir(path):
            findall(path)
        else:
            # TODO dosomethingwithfile(path)
            pass
    return


parser = argparse.ArgumentParser(description='Python file searching')
parser.add_argument('file', metavar='file', nargs=1, type=str,
                    help='searching file, word')
parser.add_argument('-er', '--end-regex', action='store_true', dest='end_regex',
                    help='searching for file and add wild card (after word could be any letter) on end')
parser.add_argument('-sr', '--start-regex', action='store_true', dest='start_regex',
                    help='searching for file and add wild card (before word could be any letter) on start')
parser.add_argument('-r', '--full-regex', action='store_true', dest='full_regex',
                    help='searching for file and add wild card arround the letters')
parser.add_argument('-p', '--path', dest='path',
                    help='Path')
    

args = parser.parse_args()
file_ = args.file[0]
path_ = args.path
try:
    if args.end_regex:
        file_ = file_ + "*"
    if args.start_regex:
        file_ = "*" + file_
    if args.full_regex:
        file_ = "*" + file_ + "*"    
    print('[+] Searching ->', file_)
    search(file_, path=path_)
except Exception as e:
    print('[-] file_search: ' + str(e))
