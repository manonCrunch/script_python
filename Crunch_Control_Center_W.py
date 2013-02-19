#!/usr/bin/python
# -*-coding:utf-8-*

# Centre de control CrunchBang Version Waldorf #
# Dépendances: gtk2-engines-pixbuf

import pygtk
pygtk.require("2.0")
import gtk
import os
import shutil
import threading
import gobject
import subprocess
import time

HOME_FOLDER = os.path.expanduser('~') 
gobject.threads_init()

class CrunchControl:
  
	def Quitter(self, widget):
		gtk.main_quit()
		
	def __init__(self):
		
		maFenetre = gtk.Window()
		maFenetre.set_title("Crunch_Control_Center")
		maFenetre.connect("destroy", self.Quitter)
		maFenetre.set_default_size(380, 400)
		
		cadre1 = gtk.Frame("Apparence")
		cadre1.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
		
		vabox = gtk.VBox(homogeneous=False, spacing=2)
		
		hbox1 = gtk.HBox(homogeneous=True, spacing=2)
		gbox1 = gtk.VBox(homogeneous=True, spacing=2)
		gbox2 = gtk.VBox(homogeneous=True, spacing=2)
		hbox2 = gtk.HBox(homogeneous=True, spacing=2)
		
		image1 = gtk.Image()
		image1.set_from_file("/usr/share/controlCenter/applications-graphics.png")
		image1.show()
		gbox1.add(image1)
		
		self.boutonObmenu = gtk.ToggleButton(label = "Editer menu")
		self.boutonObmenu.connect("clicked" ,self.fonctions ,"obmenu &")
		gbox1.add(self.boutonObmenu)
		
		self.boutonTint2 = gtk.ToggleButton(label = "Configuration Tint2")
		self.boutonTint2.connect("clicked" ,self.fonctions , "geany ~/.config/tint2/tint2rc &")
		gbox1.add(self.boutonTint2)
		
		self.boutonComposite = gtk.ToggleButton(label = "Configuration Composite")
		self.boutonComposite.connect("clicked", self.fonctions, "geany ~/.config/compton.conf &")
		gbox1.add(self.boutonComposite)
		
		self.boutonFondecran = gtk.ToggleButton(label = "Fond écran")
		self.boutonFondecran.connect("clicked" ,self.fonctions ,"nitrogen ~/images/wallpapers/ &")
		gbox2.add(self.boutonFondecran)
		
		self.boutonGtkTheme = gtk.ToggleButton(label = "Gtk themes")
		self.boutonGtkTheme.connect("clicked" ,self.fonctions ,"lxappearance &")
		gbox2.add(self.boutonGtkTheme)
		
		self.boutonObox = gtk.ToggleButton(label = "Themes Openbox")
		self.boutonObox.connect("clicked" ,self.fonctions ,"obconf &")
		gbox2.add(self.boutonObox)
		
		self.boutonSlim = gtk.ToggleButton(label = "Ecran de démarrage")
		self.boutonSlim.connect("clicked" ,self.fonctions ,"gksudo slimconf &")
		gbox2.add(self.boutonSlim)
		
		self.boutonConky = gtk.ToggleButton(label = "Editer Le Fichier Conky")
		self.boutonConky.connect("clicked" ,self.fonctions , "geany ~/.conkyrc &")
		hbox2.add(self.boutonConky)
		
		hbox1.add(gbox1)
		hbox1.add(gbox2)
		
		vabox.add(hbox1)
		vabox.add(hbox2)
		
		cadre1.add(vabox)
		
		cadre2 = gtk.Frame("Système")
		cadre2.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
		
		sysbox = gtk.VBox(homogeneous=False, spacing=2)
		
		hbox3 = gtk.HBox(homogeneous=True, spacing=2)
		gbox3 = gtk.VBox(homogeneous=True, spacing=2)
		gbox4 = gtk.VBox(homogeneous=True, spacing=2)
		hbox4 = gtk.HBox(homogeneous=True, spacing=2)
		
		image2 = gtk.Image()
		image2.set_from_file("/usr/share/controlCenter/applications-system.png")
		image2.show()
		gbox3.add(image2)
		
		self.boutonSons = gtk.ToggleButton(label = "Sons")
		self.boutonSons.connect("clicked" ,self.fonctions  ,"pavucontrol &")
		gbox3.add(self.boutonSons)
		
		self.boutonEnergie = gtk.ToggleButton(label = "Energie")
		self.boutonEnergie.connect("clicked" , self.fonctions, "xscreensaver-demo &")
		gbox3.add(self.boutonEnergie)
		
		self.boutonSynaptic = gtk.ToggleButton(label = "Synaptic")
		self.boutonSynaptic.connect("clicked" , self.fonctions ,"gksudo synaptic &")
		gbox3.add(self.boutonSynaptic)
		
		self.boutonAutostart = gtk.ToggleButton(label = "Editer Autostart")
		self.boutonAutostart.connect("clicked" ,self.fonctions , "geany ~/.config/openbox/autostart &")
		gbox4.add(self.boutonAutostart)
		
		self.boutonInfo = gtk.ToggleButton(label = "Information Système")
		self.boutonInfo.connect("clicked" ,self.fonctions ,"conky -c /usr/share/controlCenter/.conkyrc3 &")
		gbox4.add(self.boutonInfo)
		
		self.boutonNettoyage = gtk.ToggleButton(label = "Nettoyage Système")
		self.boutonNettoyage.connect("clicked" , self.nettoyage)
		gbox4.add(self.boutonNettoyage)
		
		self.boutonMiseAJours = gtk.ToggleButton(label = "Mises A Jour")
		self.boutonMiseAJours.connect("clicked" ,self.fonctions , "terminator --command=\"sudo misesAjour\" &")
		gbox4.add(self.boutonMiseAJours)
		
		self.boutonAppliParDefaut = gtk.ToggleButton(label = "Editer les applications par defaut")
		self.boutonAppliParDefaut.connect("clicked" ,self.fonctions, "terminator --command=\"sudo update-alternatives --all\" &")
		hbox4.add(self.boutonAppliParDefaut)
		
		hbox3.add(gbox3)
		hbox3.add(gbox4)
		
		sysbox.add(hbox3)
		sysbox.add(hbox4)
		
		cadre2.add(sysbox)
		
		separateur = gtk.HSeparator()
		separateur.set_size_request(150, 4)
		separateur2 = gtk.HSeparator()
		separateur2.set_size_request(150, 4)
		
		
		boutonQuitter = gtk.Button("Quitter", stock = gtk.STOCK_QUIT)
		boutonQuitter.connect("clicked", self.Quitter)
	
		vBox = gtk.VBox()
		vBox.pack_start(separateur, False, True, 2)
		vBox.pack_start(cadre1, False, False, 4)
		vBox.pack_start(cadre2, False, False, 4)
		vBox.pack_start(separateur2, False, True, 2)
		vBox.pack_end(boutonQuitter, False, False, 2)
		
		maFenetre.add(vBox)
		maFenetre.show_all()
		
		
	def fonctions(self, widget, valeur):
		os.system(str(valeur))
		
		
	def nettoyage(self, widget):
		
		self.boutonNettoyage.set_label("Nettoyage en Cours")
		
		paths = ['.local/share/Trash/files', '.local/share/Trash/info', '.macromedia/Flash_Player/macromedia.com', '.macromedia/Flash_Player/#SharedObjects', '.thumbnails/normal', '.thumbnails/large', '.local/share/recently-used.xbel']
		for path in paths:
			complete_path = os.path.join(HOME_FOLDER, path)
			try:
				shutil.rmtree(complete_path)
			except:
				pass
			
		subprocess.call("find ~/ -name '*~' -exec rm {} \;", shell=True)
		
		self.boutonNettoyage.set_label("Nettoyage Terminé")
		
		
		
if __name__ == "__main__":
	
	CrunchControl()
	gtk.main()
			
