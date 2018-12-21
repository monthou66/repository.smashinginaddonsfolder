# -*- coding: utf-8 -*-
# startwindows.py
# restart windows from libreelec
import xbmc
import os

# define stuff
USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
folder = os.path.join(SMASHINGFAVOURITES, "scripts", "libreelecpcscripts")
shellfile = os.path.join(folder, "startwindows.sh")
        
# Do it		
if os.path.isfile(shellfile):
    os.system('sh %s post' % shellfile)
 
# Drink beer