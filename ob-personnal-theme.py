#!/usr/bin/python
# -*-coding:utf-8-*

import pygtk
pygtk.require("2.0")
import gtk 
import os
from os import chdir
import shutil, tarfile, threading, time, subprocess, gobject
from xml.etree import ElementTree as  ET

gobject.threads_init()
BASE = os.path.expanduser('/')
HOME_FOLDER = os.path.expanduser('~')
NOM = os.environ['USER']
EMPLACEMENT = os.path.join(HOME_FOLDER, ".sauvegarde_config/")
THEME_PATHS = ['.config/tint2/tint2rc', '.config/nitrogen/bg-saved.cfg', '.conkyrc', '.gtkrc-2.0']  
chdir(HOME_FOLDER)

'''_Création du dossier .sauvegarde_config et déplacement dans celui ci'''
try:
  os.mkdir(".sauvegarde_config")
except OSError:
	pass 
	
chdir(EMPLACEMENT)

'''_Class_fenetre '''
class fenetre :
	def Quitter(self, widget):
		gtk.main_quit()
	
	def sauvegarde_fichier(self, widget):
		THEME_PATHS.append('.config/openbox/rc.xml')
		for path in THEME_PATHS:
			fichier_source = os.path.join(HOME_FOLDER, path)
			nom_fichier = os.path.basename(path)
			try:
				shutil.copyfile(fichier_source, nom_fichier)
			except shutil.Error:
				pass
		THEME_PATHS.remove('.config/openbox/rc.xml')
		self.boutonSauvegarde.set_label("Sauvegarde Réussi")
		
	def restauration_fichier(self, widget):
		THEME_PATHS.append('.config/openbox/rc.xml')
		for path in THEME_PATHS:
			fichier_copier = os.path.join(HOME_FOLDER, path)
			nom_fichier = os.path.basename(path)
			try:
				shutil.copyfile(nom_fichier, fichier_copier)
			except shutil.Error:
				pass
		THEME_PATHS.remove('.config/openbox/rc.xml')	
		''' thread tint2 pour garder la main sur le script'''
		self.tint2 = Tint2_thread(self)	
		self.tint2.start()
		
		subprocess.call("openbox --reconfigure && nitrogen --restore ", shell=True)
		
		self.boutonRestauration.set_label("Restauration Terminée")
		
	def s_complete(self, widget):
		try:
			os.mkdir("configuration_complete")
		except OSError:
			pass
		chdir("configuration_complete")
		self.sauvegarde_fichier(self)
		fichier_en_plus = ['.config/openbox/autostart', '.config/openbox/menu.xml']
		for path in fichier_en_plus:
			fichier_source = os.path.join(HOME_FOLDER, path)
			nom_fichier = os.path.basename(path)
			try:
				shutil.copyfile(fichier_source, nom_fichier)
			except shutil.Error:
				pass	
		self.bouton_sauvegarde_complete.set_label("Sauvegarde Réussie")
			
		chdir(EMPLACEMENT)	
		
	def r_complete(self, widget):
		try:
			chdir("configuration_complete")
		except OSError:
			self.bouton_rest_complete.set_label("Pas de sauvegarde")
		fichier_en_plus = ['.config/openbox/autostart', '.config/openbox/menu.xml']
		
		for path in fichier_en_plus:
			fichier_copier = os.path.join(HOME_FOLDER, path)
			nom_fichier = os.path.basename(path)
			try:
				shutil.copyfile(nom_fichier, fichier_copier)
			except shutil.Error:
				pass	
		self.restauration_fichier(self)
		chdir(EMPLACEMENT)
		self.bouton_rest_complete.set_label("Terminer")
			
	def exportation_theme(self, widget):
		self.theme = Choix_nom_theme(self)																
		
	def importation_theme(self, widget):
		nom_theme_import = SelecteurFichier(self)
		
	def __init__(self):
		
		maFenetre = gtk.Window()
		maFenetre.set_title("Gestion_Config_Thèmes")
		maFenetre.connect("destroy", self.Quitter)
		maFenetre.set_default_size(300, 260)
		
		separateur = gtk.HSeparator()
		separateur.set_size_request(150, 4)
		
		cadre1 = gtk.Frame("Sauvegarde rapide")
		cadre1.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
		
		tableau1 = gtk.Table(2, 2)
		cadre1.add(tableau1)
		
		self.boutonSauvegarde = gtk.ToggleButton(label = "Sauvegarder le thème actuel")
		self.boutonSauvegarde.connect("clicked" ,self.sauvegarde_fichier)
		tableau1.attach(self.boutonSauvegarde, 0, 1, 0, 1)
		
		self.boutonRestauration = gtk.ToggleButton(label = "Restaurer thème")
		self.boutonRestauration.connect("clicked", self.restauration_fichier)
		tableau1.attach(self.boutonRestauration, 0, 1, 1, 2)
		
		cadre2 = gtk.Frame("Exportation Importation")
		cadre2.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
		tableau2 = gtk.Table(2, 2)
		cadre2.add(tableau2)
		
		self.boutonExportation = gtk.ToggleButton(label = "Exporter le thème actuel")
		self.boutonExportation.connect("clicked" ,self.exportation_theme)
		tableau2.attach(self.boutonExportation, 0, 1, 0, 1)
		
		self.boutonImportation = gtk.ToggleButton(label = "Importer un thème")
		self.boutonImportation.connect("clicked" ,self.importation_theme)
		tableau2.attach(self.boutonImportation, 0, 1, 1, 2)
		
		cadre3 = gtk.Frame("Configuration complète")
		cadre3.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
		tableau3 = gtk.Table(2, 2)
		cadre3.add(tableau3)
		
		self.bouton_sauvegarde_complete = gtk.ToggleButton(label = "Sauvegarder")
		self.bouton_sauvegarde_complete.connect("clicked", self.s_complete)
		tableau3.attach(self.bouton_sauvegarde_complete, 0, 1, 0, 1)
		
		self.bouton_rest_complete = gtk.ToggleButton(label = "Restaurer")
		self.bouton_rest_complete.connect("clicked", self.r_complete)
		tableau3.attach(self.bouton_rest_complete, 0, 1, 1, 2) 
		
		separateur2 = gtk.HSeparator()
		separateur2.set_size_request(150, 4)
		
		boutonQuitter = gtk.Button("Quitter", stock = gtk.STOCK_QUIT)
		boutonQuitter.connect("clicked", self.Quitter)
		
		vBox = gtk.VBox()
		vBox.pack_start(separateur, False, True, 4)
		vBox.pack_start(cadre1, False, False, 4)
		vBox.pack_start(cadre2, False, False, 4)
		vBox.pack_start(cadre3, False, False, 4)
		vBox.pack_start(separateur2, False, True, 4)
		vBox.pack_end(boutonQuitter, False, False, 2)
		
		maFenetre.add(vBox)
		maFenetre.show_all()
		
'''_Class_Exportation_thread , suivre etiquette.set_text pour voire les étapes'''
class Exportation_thread(threading.Thread):
	 
	def __init__ (self, fenetre):
		threading.Thread.__init__ (self, target=self)	
		
	def run(self):
		f_tmp = open("fichier_tmp", 'r')
		txt = f_tmp.read()
		nom_theme_perso = txt.rstrip('\n\r')
		emplacement_theme = os.path.join(EMPLACEMENT, '{0}'.format(nom_theme_perso))
		os.remove('fichier_tmp')
		try:
			os.mkdir('{0}'.format(nom_theme_perso))
		except OSError:
			pass
		chdir(emplacement_theme)
		
		fenetre2 = gtk.Window()
		fenetre2.set_default_size(240, 140)
		
		etiquette = gtk.Label()
		etiquette.set_justify(gtk.JUSTIFY_CENTER)
		fenetre2.add(etiquette)
		fenetre2.show_all()
		
		etiquette.set_text("\nCopie des fichiers\nde configuration\n")
		for path in THEME_PATHS:
			fichier_source = os.path.join(HOME_FOLDER, path)
			nom_fichier = os.path.basename(path)
			shutil.copyfile(fichier_source, nom_fichier)
		time.sleep(3)
		
		f_config_wall = open('{0}/{1}'.format(HOME_FOLDER,THEME_PATHS[1]), 'r')
		for ligne in f_config_wall:
			txt = ligne
			if "file=" in txt:
				place_wall = ligne.rstrip('\n\r').lstrip('file=')
				wall_nom = os.path.basename(place_wall)
		shutil.copyfile(place_wall, wall_nom)
				
		etiquette.set_text("\nRecherche et copie icônes théme gtk \nWallpaper\n")		
		f_gtkrc = open('{0}/{1}'.format(HOME_FOLDER,THEME_PATHS[3]), 'r')
		for ligne in f_gtkrc:
			txt = ligne
			if "gtk-theme-name=" in txt:
				nom_theme = ligne.rstrip('\n\r').split("\"")
				theme_source = os.path.join(HOME_FOLDER, ".themes/{0}".format(nom_theme[1]))
				theme_source_2 = os.path.join(BASE, "usr/share/themes/{0}".format(nom_theme[1]))
				if os.path.isdir(theme_source) == True :
					try:
						shutil.copytree(theme_source, nom_theme[1])
					except OSError:
						pass
				else :
					try:
						shutil.copytree(theme_source_2, nom_theme[1])
					except OSError:
						pass
									
			if "gtk-icon-theme-name=" in txt:	
				nom_icons = ligne.rstrip('\n\r').split("\"")
				icons_source = os.path.join(HOME_FOLDER, ".icons/{0}".format(nom_icons[1]))
				icons_source_2 = os.path.join(BASE, "usr/share/icons/{0}".format(nom_icons[1]))
				if os.path.isdir(icons_source) == True :
					try:
						shutil.copytree(icons_source, nom_icons[1])
					except OSError:
						pass
				else : 
					try:
						shutil.copytree(icons_source_2, nom_icons[1])
					except OSError:
						pass
						
		etiquette.set_text("\nRecherche et copie du theme openbox \n ")
		chdir(HOME_FOLDER)
		tree = ET.parse('.config/openbox/rc.xml')
		root = tree.getroot()
		theme_open_box = root.find('{http://openbox.org/3.4/rc}theme/{http://openbox.org/3.4/rc}name').text
		
		theme_box = os.path.join(BASE, "usr/share/themes/{0}".format(theme_open_box))
		chdir(emplacement_theme)
		try:
			shutil.copytree(theme_box, theme_open_box)
		except OSError:
			pass
			
		f_t_box = open("f_t_box.txt", 'w')
		print >> f_t_box, "{0}".format(theme_open_box)
		f_t_box.close()
		time.sleep(3)
		
		etiquette.set_text("\nCréation de l'archive\nle plus long...\n")	
		chdir(EMPLACEMENT)
		tz = tarfile.open('{0}.tar.gz'.format(nom_theme_perso), 'w:gz')
		tz.add(nom_theme_perso)
		tz.close()
		
		etiquette.set_text("suppression des fichiers temporaires")
		shutil.rmtree(nom_theme_perso)
		time.sleep(2)
		chdir(HOME_FOLDER)
		'''déplacement de l'archive'''
		shutil.move('{0}.tar.gz'.format(emplacement_theme), "{0}.tar.gz".format(nom_theme_perso))
		chdir(EMPLACEMENT)
		etiquette.set_text("Exportation Terminée\nVotre theme se trouve \ndans votre dossier personnel")
		time.sleep(4)
		fenetre2.destroy()
		
'''_Class_Selecteur_Fichier , choix du fichier a importer.'''
class SelecteurFichier:
    
    def ok_fichier(self, w,):
		chdir(EMPLACEMENT)
		nom_theme_import = self.selectfichier.get_filename()
		self.selectfichier.destroy()

		f_nom_tarGz = open('fichier_tmp', 'w')
		f_nom_tarGz.write('{0}'.format(nom_theme_import))
		f_nom_tarGz.close()
		self.importation = Importation_thread()
		self.importation.start()
		       
    def destroy(self, widget):
         self.selectfichier.destroy()

    def __init__(self, widget): 
		chdir(HOME_FOLDER)
		self.selectfichier = gtk.FileSelection("Selection de fichier")
		self.selectfichier.connect("destroy", self.destroy)
		self.selectfichier.ok_button.connect("clicked", self.ok_fichier)
		self.selectfichier.cancel_button.connect("clicked", lambda w: self.selectfichier.destroy())
		self.selectfichier.set_filename("manon")
		self.selectfichier.show()

class Choix_nom_theme:
	
	def __init__(self, widget):
		self.fenetre = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.fenetre.set_size_request(200, 100)
		self.fenetre.set_title("Nom du theme")
		self.fenetre.connect("delete_event", gtk.main_quit)
		
		etiquette = gtk.Label()
		etiquette.set_text("Nom de votre thème :")
		nom_theme_export = gtk.Entry()
		nom_theme_export.set_text("votre theme")
		nom_theme_export.connect("activate", self.validation, nom_theme_export)
		
		bouton_valider = gtk.Button("Valider")
		bouton_valider.connect("clicked", self.validation, nom_theme_export)
		
		vBox = gtk.VBox()
		vBox.pack_start(etiquette)
		vBox.pack_start(nom_theme_export)
		vBox.pack_start(bouton_valider,  False, False, 2)
		
		self.fenetre.add(vBox)
		self.fenetre.show_all()
		
	def validation(self,fenetre,  nom_theme_export):
		nom_theme = nom_theme_export.get_text()
		f_tmp = open("fichier_tmp", 'w')
		f_tmp.write('{0}'.format(nom_theme))
		f_tmp.close()
		self.quitter(fenetre, nom_theme_export)
		self.exportation = Exportation_thread(self)
		self.exportation.start()
	def quitter(self, widget, nom_theme_export):
		self.fenetre.destroy()
				
'''_Class_Importation_thread , Suivre etiquette.set_text (étapes)'''
class Importation_thread(threading.Thread):
	def __init__ (self):
		threading.Thread.__init__ (self, target=self)
		
	def run(self):
		
		fenetre2 = gtk.Window()
		fenetre2.set_default_size(240, 140)
		etiquette = gtk.Label()
		etiquette.set_justify(gtk.JUSTIFY_CENTER)
		fenetre2.add(etiquette)
		fenetre2.show_all()
		txt_nom_Archive = open('fichier_tmp', 'r') 
		txt = txt_nom_Archive.read()
		nom_tar_gz = txt.split('.tar.gz')
		nom_dossier = os.path.basename(nom_tar_gz[0])
		txt_nom_Archive.close()
		os.remove('fichier_tmp')
		
		etiquette.set_text("extraction de l'archive\nle plus long...")
		tz = tarfile.open('{0}.tar.gz'.format(nom_tar_gz[0]), 'r')
		tz.extractall()
		tz.close()
		time.sleep(2)
		'''Deplacement dans le dossier crée a la décompression de l'archive'''
		chdir("{0}{1}/".format(EMPLACEMENT, nom_dossier))
		
		etiquette.set_text("récupération de l'emplacement \n du wallpaper")
		
		f_config_wall = open('{0}/{1}'.format(HOME_FOLDER,THEME_PATHS[1]), 'r')
		f_config_wall_theme  = open("bg-saved.cfg", 'r')
		f_tmp = open("fichier_tmp.cfg", 'w')
		for ligne in f_config_wall_theme:
			txt = ligne
			if "file=" in txt:
				wall_nom = os.path.basename(ligne.rstrip('\n\r'))
				for ligne in f_config_wall:
					txt2 = ligne
					if "file=" in txt2:
						wall_base = os.path.basename(ligne.rstrip('\n\r'))
						wall_p = ligne.rstrip('\n\r').lstrip('file=')
						wall_position = wall_p.strip(wall_base)
						
				print >> f_tmp, "file={0}{1}".format(wall_position, wall_nom)
			else:
				print >> f_tmp,"{0}".format(txt)
		f_config_wall.close()
		f_config_wall_theme.close()
		f_tmp.close()
		os.remove("bg-saved.cfg")
		os.rename("fichier_tmp.cfg", "bg-saved.cfg")
		time.sleep(2)
		
		etiquette.set_text("copie du wallpaper au bon emplacement")
		shutil.copyfile(wall_nom, "{0}{1}".format(wall_position, wall_nom))	
		time.sleep(2)
		
		etiquette.set_text("recherche et copie du theme et des icônes")
		f_gtkrc = open(".gtkrc-2.0", 'r')
		for ligne in f_gtkrc:
			txt = ligne
			if "gtk-theme-name=" in txt:
				nom_theme = ligne.rstrip('\n\r').split("\"")
				theme_copie  = os.path.join(HOME_FOLDER, ".themes/{0}".format(nom_theme[1]))
				try:
					shutil.copytree(nom_theme[1], theme_copie)
				except OSError:
					pass
			
			if "gtk-icon-theme-name=" in txt:
				nom_icons = ligne.rstrip('\n\r').split("\"")
				icons_copier = os.path.join(HOME_FOLDER, ".icons/{0}".format(nom_icons[1]))
				try:
					shutil.copytree(nom_icons[1], icons_copier)
				except OSError:
					pass
		time.sleep(2)
		
		etiquette.set_text("copie des fichiers")
		for path in THEME_PATHS:
			nom_fichier = os.path.basename(path)
			fichier_copier = os.path.join(HOME_FOLDER, path)
			shutil.copyfile(nom_fichier, fichier_copier)
		time.sleep(2)
		
		etiquette.set_text("recherche et copie theme openbox")
		f_t_box = open('f_t_box.txt', 'r') 
		txt = f_t_box.read()
		nom_t_box = txt.rstrip('\n\r')
		f_t_box.close()
		
		theme_box = os.path.join(HOME_FOLDER, ".themes/{0}".format(nom_t_box))
		theme_base = os.path.join(BASE, "usr/share/themes/{0}".format(nom_t_box))
		'''si le theme est deja présent on ne copie pas'''
		if os.path.isdir(theme_base) == True :
			pass
		else:
			try:
				shutil.copytree(nom_t_box, theme_box)
			except OSError:
				pass
			
		chdir(HOME_FOLDER)
		if ET.VERSION[0:3] == '1.2':
			def fixtag(tag, namespaces):
				import string
				if isinstance(tag, ET.QName):
					tag = tag.text
				namespace_uri, tag = string.split(tag[1:], "}", 1)
				prefix = namespaces.get(namespace_uri)
				if namespace_uri not in namespaces:
					prefix = ET._namespace_map.get(namespace_uri)
					if namespace_uri not in ET._namespace_map:
						prefix = "ns%d" % len(namespaces)
					namespaces[namespace_uri] = prefix
					if prefix == "xml":
						xmlns = None
					else:
						if prefix is not None:
							nsprefix = ':' + prefix
						else:
							nsprefix = ''
						xmlns = ("xmlns%s" % nsprefix, namespace_uri)
				else:
					xmlns = None
				if prefix is not None:
					prefix += ":"
				else:
					prefix = ''

				return "%s%s" % (prefix, tag), xmlns
			ET.fixtag = fixtag
			ET._namespace_map['http://openbox.org/3.4/rc'] = None
		else:
			ET.register_namespace('', 'http://openbox.org/3.4/rc')
			
		tree = ET.parse(".config/openbox/rc.xml")
		root = tree.getroot()
		root.find('{http://openbox.org/3.4/rc}theme/{http://openbox.org/3.4/rc}name').text = nom_t_box
		tree.write('.config/openbox/rc.xml')
		
		
		etiquette.set_text("Mise en place du theme")	
		'''_Appel a la Class_Tint2_thread pour garder la main sur le script'''
		self.tint2 = Tint2_thread(self)	
		self.tint2.start()
		subprocess.call("openbox --reconfigure && nitrogen --restore ", shell=True)
		time.sleep(2)
		
		etiquette.set_text("suppression des fichiers temporaires")
		shutil.rmtree("{0}{1}/".format(EMPLACEMENT, nom_dossier))
		time.sleep(2)
		chdir(EMPLACEMENT)
		etiquette.set_text("Importation Terminée")
		time.sleep(2)
		
		fenetre2.destroy()
					
class Tint2_thread(threading.Thread):
	
	def __init__ (self, tint2):
		threading.Thread.__init__ (self, target=self)
	def run(self):
		os.system("pkill tint2 && tint2 &")

if __name__ == "__main__":
	fenetre()
	gtk.main()

