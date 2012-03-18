#!/usr/bin/env python

import os, sys, re, argparse, shutil, tkFileDialog, string 
from bencode import bencode, bdecode
from Tkinter import *


gtorrentlist = []

gdirname ="a "
gfile="a "

gtorrentlist.append("1")

def find(string, list):
    for item in list:
        if item == string:
            return True
    return False


root=Tk()
root.title("utchecker")

#root.geometry("300x400")


label=Label(root,text="utchecker", font="bold 16")
label.grid(row=0,column=0)

dirname_label = StringVar() 
dirname_label.set("Folder to check: ")


def press1():
	global gtorrentlist
	global gfilename
	torrentlist = []
	file = tkFileDialog.askopenfile(parent=root,mode="rb",title="Please select resume.dat")
	if file != None:
		data = file.read()
		file.close()
		content = bdecode(data)
		for torrent_name,torrent_path in content.iteritems():
			if torrent_name != ".fileguard":
				torrentlist.append(torrent_path)
	button2.configure(state=NORMAL)
	gfile=file
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
	file = gfile
	torrentlist = gtorrentlist
	if dirname != "" and file != "" and torrentlist:
		"""
		path dir to check
		path2 resume.dat
		delete
		delete_all
		"""
		for dirname2 in os.listdir(dirname):
			thepath = os.path.join(dirname, dirname2)
			if os.path.isdir(thepath) == True:
				if find(thepath, torrentlist) == False:
					text.insert(END,thepath+"\r\n")

button3 = Button(root, text="Check it", command=press3 ,state=DISABLED)
button3.grid(row=4,column=0)

label2=Label(root,text="Found:", font="12")
label2.grid(row=5,column=0)

text = Text(root)
text.grid(row=6,column=0)

root.mainloop()










