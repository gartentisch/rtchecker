#!/usr/bin/env python

import os, sys, re, argparse, shutil, tkFileDialog, string 
from bencode import bencode, bdecode
from Tkinter import *


gtorrentlist = []

gdirname =" "
gfile=" "

gtorrentlist.append("1")

root=Tk()
root.title("utchecker")


label=Label(root,text="utchecker", font="bold 16")
label.grid(row=0,column=0)

dirname_label = StringVar() 
dirname_label.set("Folder to check: ")

text = Text(root)
text.grid(row=6,column=0)


def press1():
	global gtorrentlist
	global gfilename
	torrentlist = []
	sfile = tkFileDialog.askopenfile(parent=root,mode="rb",title="Please select resume.dat")
	if sfile != None:
		data = sfile.read()
		sfile.close()
		content = bdecode(data)
		for torrent_name,torrent_data in content.iteritems():
			if type(torrent_data).__name__=='dict':
				torrent_path=torrent_data["path"]
				if torrent_name != ".fileguard":
					torrentlist.append(torrent_path)
	button2.configure(state=NORMAL)
	gfile=sfile
	gtorrentlist=torrentlist

button = Button(root, text="Select resume.dat", command=press1)
button.grid(row=1,column=0)


def press2():
	global gdirname
	dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title="Please select folder to check")
	dirname=os.path.normpath(dirname)
	if dirname != None:
		dirname_label.set("Folder to check: \n"+dirname) 
	button3.configure(state=NORMAL)
	gdirname=dirname


	
button2 = Button(root, text="Select folder to check", command=press2 ,state=DISABLED)
button2.grid(row=2,column=0)

label2=Label(root, font="10",textvariable=dirname_label)
label2.grid(row=3,column=0)


def press3():
	text.delete('1.0',END)
	dirname = gdirname
	sfile = gfile
	torrentlist = gtorrentlist
	if dirname != "" and file != "" and torrentlist:
		for dirname2 in os.listdir(dirname):
			thepath = os.path.join(dirname, dirname2)
			if os.path.isdir(thepath) == True:
				if not thepath.encode("utf-8") in torrentlist:
					text.insert(END,thepath+"\r\n")

button3 = Button(root, text="Check it", command=press3 ,state=DISABLED)
button3.grid(row=4,column=0)

label2=Label(root,text="Found:", font="12")
label2.grid(row=5,column=0)



root.mainloop()
