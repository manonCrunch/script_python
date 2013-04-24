#!/usr/bin/python
# -*-coding:utf-8-*

import os
import sys
import shutil
import optparse
from os import chdir
from random import randrange
from time import sleep

HOME_FOLDER = os.path.expanduser('~')
EMPLACEMENT = sys.argv[1]
CONFIG_WALL = os.path.join(HOME_FOLDER, '.config/nitrogen/bg-saved.cfg')

chdir(EMPLACEMENT)
wallDispo = os.listdir(EMPLACEMENT)
while 1:
    sleep(30) # le temps de pause en secondes
	wall = randrange(0,len(wallDispo))
	configBase = open(CONFIG_WALL, 'r')
	newConfig = open("newsConfigWall", 'w')
	for ligne in configBase:
		if "file=" in ligne:
			print >> newConfig, "file={0}".format(wallDispo[wall])
			
		else:
			print >> newConfig, "{0}".format(ligne)		
	configBase.close()
	newConfig.close()
			
	os.remove(CONFIG_WALL)
	os.rename("newsConfigWall", os.path.basename(CONFIG_WALL))
	try:
		shutil.copyfile('bg-saved.cfg', '{0}'.format(CONFIG_WALL))
	except shutil.Error:
		pass
		
	os.system("nitrogen --restore")	
	
