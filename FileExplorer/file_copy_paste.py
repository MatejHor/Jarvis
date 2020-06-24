#!/usr/bin/python

import os
import sys
import shutil
import argparse


def _get_dict(path):
    destination_dic = path.split('/') if '/' in path else path.split('\\')
    destination_dic.pop()
    # Add \ for windows "Drive:\"
    destination_dic[0] = destination_dic[0] if ':' not in destination_dic[0] else destination_dic[0] + '\\'
    # Add / for linux "/path"
    destination_dic[0] = '/' + destination_dic[0] if '/' in path else destination_dic[0]
    destination_dic = os.path.join(*destination_dic)
    destination_dic = destination_dic + ('/' if '/' in path else '\\')
    if os.path.exists(destination_dic):
        return destination_dic
    else:
        return False


def move(source_path, destination_path):
    if _get_dict(destination_path) and os.path.exists(source_path):
        shutil.move(source_path, destination_path)
    else:
        if not _get_dict(destination_path):
            raise Exception("Destination path doesn't exist")
        elif not os.path.exists(source_path):
            raise Exception("Source path or file doesn't exist")


def copy_paste(source_path, destination_path):
    if _get_dict(destination_path) and os.path.exists(source_path):
        shutil.copy2(source_path, destination_path)
    else:
        if not _get_dict(destination_path):
            raise Exception("Destination path doesn't exist")
        elif not os.path.exists(source_path):
            raise Exception("Source path or file doesn't exist")


def rename(old_name, new_name):
    if os.path.exists(old_name):
        if len(old_name.split('/') if '/' in old_name else old_name.split('\\')) > 1:
            new_path = os.path.join(_get_dict(old_name), new_name)
        else:
            new_path = new_name
        os.rename(old_name, new_path)
    else:
        raise Exception("Source file doesn't exist")


def remove(source_path):
    if os.path.exists(source_path):
        os.remove(source_path)


parser = argparse.ArgumentParser(description='Python file copy past')
parser.add_argument('-d', '--delete', help='delete file', nargs=1, type=str)
parser.add_argument('-r', '--rename', help='rename file', nargs=2, type=str)
parser.add_argument('-m', '--move', help='move file', nargs=2, type=str)
parser.add_argument('-c', '--copy', help='copy file with all meta and permissions', nargs=2, type=str)
args = parser.parse_args()

try:
    if args.delete:
        source_file = args.delete[0]
        remove(source_path=source_file)

    if args.rename:
        source_file = args.renanem[0]
        destination_file = args.renanem[1]
        rename(old_name=source_file, new_name=destination_file)

    if args.move:
        source_file = args.move[0]
        destination_file = args.move[1]
        move(source_path=source_file, destination_path=destination_file)

    if args.copy:
        source_file = args.copy[0]
        destination_file = args.copy[1]
        copy_paste(source_path=source_file, destination_path=destination_file)

except Exception as e:
    print('file_copy_paste: ' + str(e))