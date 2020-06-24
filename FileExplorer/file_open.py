#!/usr/bin/python

import subprocess
import platform
import sys
import argparse


def command_run(command, stdout=True):
    if stdout:
        stdout = sys.stdout
    else:
        stdout = subprocess.PIPE
    result_ = subprocess.run(command, shell=True, stderr=subprocess.PIPE, stdout=stdout)
    return result_.stdout


def windows_run(file):
    command = "explorer " + file
    return command_run(command, True)


def linux_run(file):
    command = "xdg-open " + file
    return command_run(command, True)


def open_file(file):
    if platform.system() == "Windows":
        windows_run(file)
    else:
        linux_run(file)


parser = argparse.ArgumentParser(description='Python file opening')
parser.add_argument('file', metavar='file', nargs=1, type=str,
                    help='open file, must contain path or be in actual folder')
args = parser.parse_args()
file_ = args.file[0]

try:
    open_file(file_)
except Exception as e:
    print('file_open: ' + str(e))
