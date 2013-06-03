#!/usr/bin/python
# -*-coding:utf-8-*

import os, sys
import optparse

nombreArgs = len(sys.argv)
chemin = os.popen("pwd").read().rstrip('\n\r')
fichiers = os.listdir(chemin)

if (nombreArgs == 1):
  print ("Pas d'arguments donnés")
	
if (nombreArgs == 2):
	i = 0
	for e in fichiers:
		if (e[-3] == "."):
			i += 1
			try:
				os.rename(e, "{0}_n°{1}.{2}".format(sys.argv[1], i, e[:-3]))
			except IndexError:
				pass

if (nombreArgs == 3):
	if (sys.argv[1] == '-s'):
		for e in fichiers:
			if (sys.argv[2] in e):
				newName = e.replace(sys.argv[2], '')
				try:
					os.rename(e, newName)
				except OSError:
					pass
	
