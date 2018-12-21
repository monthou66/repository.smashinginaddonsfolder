# -*- coding: utf-8 -*-
# startwindows.py
# restart windows from libreelec
import xbmc
import os
import shutil

# define stuff
USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
folder = os.path.join(SMASHINGFAVOURITES, "scripts", "libreelecpcscripts")
flashrw = os.path.join(folder, "makeflashrw.sh")
flashro = os.path.join(folder, "makeflashro.sh")
libreelec = os.path.join("/flash", "libreelec.txt")
menulst = os.path.join("/flash", "menu.lst")
source = os.path.join("/flash", "stuff", "menus", "windows")
newlibreelec = os.path.join(source, "libreelec.txt")
newmenulst = os.path.join(source, "menu.lst")

       
# Do it		
os.system('sh %s post' % flashrw)
xbmc.sleep(300)
if os.path.exists(libreelec):
    os.remove(libreelec)
if os.path.exists(menulst):
    os.remove(menulst)
shutil.copy(newlibreelec, libreelec)
shutil.copy(newmenulst, menulst)
os.system('sh %s post' % flashro)
xbmc.sleep(300)

xbmc.executebuiltin('Reboot')

 
# Drink beer