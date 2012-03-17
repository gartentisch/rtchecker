#!/usr/bin/env python

import os, sys, re, argparse, shutil
from bencode import bencode, bdecode

torrentlist = []

parser = argparse.ArgumentParser(description="Check for files that are on your drive, but aren't present in utorrent", add_help=True)
action = parser.add_mutually_exclusive_group(required=False)
parser.add_argument('path', action="store", help="Directory you want to check")
parser.add_argument('path2', action="store", help="Path to your resume.dat ")
action.add_argument('-d', action="store_true", dest="delete", default=False, help="Delete the files (asks again)")
action.add_argument('-D', action="store_true", dest="delete_all", default=False, help="Delete the files (Doesn't ask again) USE CAREFULLY!!")
args = parser.parse_args()



filename = os.path.join(args.path2, "resume.dat")
path = args.path


def find(string, list):
    for item in list:
        if item == string:
            return True
    return False

content = open(filename,"rb").read()
data = bdecode(content)
for torrent_name,torrent_path in data.iteritems():
	if torrent_name != ".fileguard":
		#print("the name is: "+torrent_name)
		#print("the path is: "+torrent_path["path"])
		torrentlist.append(torrent_path)
		
for dirname in os.listdir(path):
    thepath = os.path.join(path, dirname)
    if os.path.isdir(thepath) == True:
        if find(thepath, torrentlist) == False:
            print("Found: "+os.path.join(path, dirname))
            if args.delete:
                reply = raw_input("Delete directory "+dirname+"? [y/[n]] ")
                if reply=="y" or reply == "Y":
                    shutil.rmtree(thepath,True)
            elif args.delete_all:
                shutil.rmtree(thepath,True)
