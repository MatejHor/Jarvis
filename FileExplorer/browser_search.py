#!/bin/usr/python3
import webbrowser
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Value to search')
args = parser.parse_args()

url = "https://www.google.com.tr/search?q={}".format(args.input)
webbrowser.open_new_tab(url)
