#!/usr/bin/python
# -*-coding:utf-8-*

import os, sys 
from os import chdir

HOME_FOLDER = os.path.expanduser('~')
chdir(HOME_FOLDER)

class PyPipeSeparator:
    """Classe pour les separator pour un pipe menu"""
    def __init__(self, name):
        """Init"""
        self.name = name
        
    def construct(self):
        """Construction method"""
        print '<separator label="{0}" />'.format(self.name)

class PyPipeItem:
    """Classe pour construire un item pour un pipe menu"""
    def __init__(self, label, cmd=None):
        """Init"""
        self.label = label
        self.cmd = cmd

    def construct(self):
        """Construction method"""
        print '<item label="{0}">'.format(self.label)
        if self.cmd is not None:
            print '<action name="Execute">'
            print '<execute>{0}</execute>'.format(self.cmd)
            print '</action>'
        print '</item>'

class PyPipeSubMenu:
    """Classe pour construire un submenu pour un pipe menu"""
    def __init__(self, label):
        """Init"""
        self.label = label
        self.items = []

    def add_item(self,label, cmd):
        """Ajoute un item au submenu"""
        self.items.append(PyPipeItem(label, cmd))

    def construct(self):
        """Construction method"""
        print '<menu id="{0}" label="{0}">'.format(self.label)
        for item in self.items:
            item.construct()
        print '</menu>'

class PyPipeMenu:
    """Classe pour construire pipe menu"""
    def __init__(self):
        """Init"""
        self.contents = []

    def add_submenu(self, name):
        """Ajoute un submenu au pipe menu"""
        self.contents.append(PyPipeSubMenu(name))

    def add_item(self, name, cmd=None):
        """Ajoute un item au pipe menu"""
        self.contents.append(PyPipeItem(name,cmd))
        
    def add_separator(self, name):
        """Ajoute un separator"""
        self.contents.append(PyPipeSeparator(name))

    def construct(self):
        """Construction method"""
        print '<openbox_pipe_menu>'
        for c in self.contents:
            c.construct()
        print '</openbox_pipe_menu>'


def affiche():
  
	liste = [x for x  in os.listdir(HOME_FOLDER) if x[0] != '.']
	liste_dossier = [nom for nom in liste if os.path.isdir(nom) == True]
	liste_dossier.sort() 
	pipe = PyPipeMenu()
	
	for nom in liste_dossier :
		cmd = os.path.join('pcmanfm {0}'.format(nom))
		pipe.add_item(nom, cmd)
		
	pipe.construct()
	
if __name__ == '__main__':
	affiche()
	
	
