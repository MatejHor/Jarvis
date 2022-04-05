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
parser.add_argument('input', nargs=1, type=str, help='Searching file, word')
parser.add_argument('-p', '--path', nargs='*', dest='path', help='Path for searching')
parser.add_argument('-o', '--open', action='store_true',help='Open file after search')
args = parser.parse_args()

result = []
if not args.path:
    if platform.system() == "Windows":
        windows_disks = "wmic logicaldisk get caption"
        args.path = " ".join(re.sub('Caption|\n|\r', '', os.popen(
            windows_disks).read()).split()).split()
        args.path = [path + '\\' for path in args.path]
    else:
        args.path = ['/']
print("[+] Searching file", args.input[0], "in path\s", args.path)
result = [find(args.input[0], path) for path in args.path]
if args.open:
    for file in result:
        open_file(file)
