#!/usr/bin/python
import os
import fnmatch
import argparse
import platform
import re


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(os.path.join(root, name), pattern):
                result.append(os.path.join(root, name))
                print(os.path.join(root, name))
    return result


def open_file(path):
    path = '\\'.join(path.split('\\')[0:-1])
    os.startfile(path)


parser = argparse.ArgumentParser(description='Python os manager')
parser.add_argument('-i', '--input', dest='input',
                    type=str, help='Searching file, word')
parser.add_argument('-p', '--path', dest='path', help='Path for searching')
parser.add_argument('-o', '--open', action='store_true',
                    help='Open file after search')
args = parser.parse_args()

result = []
if args.path:
    result = find(args.input, args.path)
else:
    if platform.system() == "Windows":
        disks = " ".join(re.sub('Caption|\n|\r', '', os.popen(
            "wmic logicaldisk get caption").read()).split()).split()
        for disk in disks:
            result += find(args.input, disk + '\\')
    else:
        result = find(args.input, path='/')
# print(result)
if args.open:
    for file in result:
        open_file(file)
