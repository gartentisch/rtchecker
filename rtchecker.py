#!/usr/bin/python2

import xmlrpclib, sys, os, signal, argparse, shutil 
import  xmlrpc2scgi as xs

#####################
#   CONFIG PART     #
#                   #
#####################

#Enter your scgi address here:
rtorrent_host = "scgi://localhost:5000"

rtc = xs.RTorrentXMLRPCClient(rtorrent_host)



parser = argparse.ArgumentParser(description="Check for files that are on your drive, but aren't present in rtorrent", add_help=True)
action = parser.add_mutually_exclusive_group(required=False)
parser.add_argument('path', action="store",  help="Directory you want to check")
parser.add_argument('-r', action="store_true", dest="refresh", default=False, help="Refresh the list")
action.add_argument('-d', action="store_true", dest="delete", default=False, help="Delete the files (asks again)")
action.add_argument('-D', action="store_true", dest="delete_all", default=False, help="Delete the files (Doesn't ask again) USE CAREFULLY!!")
args =  parser.parse_args()


def signal_handler(signal, frame):
	print "\n\naborting...\n"
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def find(string, list):
	for item in list:
		if item == string:
			return True
	return False	
	
def refresher():
	print "Refreshing list. This may take some time depending on the number of torrents..."
	torrents = rtc.download_list('')
	numtorr = len(torrents)
	f = open(filename, "w")
	counter = 0
	for torrent in torrents:
		message = rtc.d.get_directory(torrent)
		f.write(unicode(message).encode("utf-8")+"\n")
		counter = counter + 1
		sys.stdout.write("\r"+str(counter)+" / "+str(numtorr)+" ("+str(int(round((100.0*counter)/numtorr)))+"%)")
		sys.stdout.flush()
	f.close()
	sys.stdout.write("\n")
	print "Refreshed list!"
path = args.path
torrentlist = []
filename = "checker.list"

if args.refresh  or not os.path.exists("checker.list"):
	refresher()


f = open(filename, "r")
for line in f:
	torrentlist.append(line[:-1])
f.close()


for dirname in os.listdir(path):
	thepath = os.path.join(path, dirname)
	if os.path.isdir(thepath) == True:
		if find(thepath, torrentlist) == False:
			print "Found: "+os.path.join(path, dirname)
			if args.delete:
				reply = raw_input("Delete directory "+dirname+"? [y/[n]] ")
				if reply=="y" or reply == "Y":
					shutil.rmtree(thepath,True)
#					print "rm"
					#os.system("rm -r "+thepath)
			elif args.delete_all:
				shutil.rmtree(thepath,True)
#				print "RM"
