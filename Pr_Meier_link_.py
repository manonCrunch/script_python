#!/usr/bin/python
# -*-coding:utf-8-*

import os
import shutil
from os import chdir
from random import randrange
from time import sleep

HOME_FOLDER = os.path.expanduser('~')
EMPLACEMENT = os.path.join(HOME_FOLDER, ".obpersonnal-theme/")

THEME_PATHS = ['.config/nitrogen/bg-saved.cfg', '.conkyrc']

chdir(EMPLACEMENT)

themesDispo = [nom for nom  in os.listdir(EMPLACEMENT) if os.path.isdir(nom) == True]

def changement_theme():
    for fichierCopie in [os.path.join(HOME_FOLDER, fichier) for fichier in THEME_PATHS]:
			fichierSource = os.path.basename(fichierCopie)
			try:
				shutil.copyfile(fichierSource, fichierCopie)
			except shutil.Error:
				pass

while 1:
	
	sleep(200) # le temps de pause en secondes
	theme = randrange(0,len(themesDispo))
	chdir(themesDispo[theme])
	changement_theme()
	chdir (EMPLACEMENT)
	os.system("nitrogen --restore")
