# -*- coding: utf-8 -*-
import os
import os.path
import xbmc
import xbmcgui
import xbmcvfs
import shutil

# copy keymap to keymaps folder or remove from keymaps folder
# reload keymaps

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def printproblem():
    print "There is a problem with smashingkeymaps."
	
def printnoaction():
    print "No action taken."
	
def printworking():
    print "Smashingkeymaps is doing its stuff."

# Start with argument (keymap name or bulk) from remote or shortcut
FILE = sys.argv[1]
MOVE = sys.argv[2]

# MOVE = load, remove, backup
# FILE = keymap name, temp (load/remove anything starting with 'zztemp') or default (restore keymaps to just maps starting 'zdefault' + xonfluence if already there)

#define sources / destinations
KEYMAPSOURCEFILE = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/scripts/smashingkeymaps/ %s .xml" % FILE)
KEYMAPDESTFILE = os.path.join(xbmc.translatePath('special://masterprofile/'), "keymaps/ %s .xml" % FILE)
KEYMAPSFOLDER = os.path.join(xbmc.translatePath('special://masterprofile/keymaps'))
KEYMAPSBACKUP = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/customkeymaps/keymapsbackup")
DEFAULTKEYMAPSBACKUP = os.path.join(xbmc.translatePath('special://masterprofile/'), "smashingfavourites/customkeymaps/defaultkeymapsbackup")
# YESNOBACKUP = xbmcgui.Dialog().yesno("A backup folder already exists","Do you want to replace it with the current keymaps folder?")
# YESNORESTORE = xbmcgui.Dialog().yesno("Do you want to restore the backed up keymaps?","This will delete your current keymaps.")
# YESNODEFAULTBACKUP = xbmcgui.Dialog().yesno("A backup already exists","Do you want to replace it with the","current default keymaps?")
# YESNODEFAULTRESTORE = xbmcgui.Dialog().yesno("Do you want to restore the backed up default keymaps?","This will delete your current keymaps","and restore just the defaults.")

#  Load individual keymap. Check if FILE is a valid keymap, copy it to keymaps folder and reload keymaps
def loadkeymap():
    if os.path.isfile(KEYMAPSOURCEFILE):
        xbmcvfs.copy(KEYMAPSOURCEFILE, KEYMAPDESTFILE)
        xbmc.executebuiltin('Action(reloadkeymaps)')
        xbmc.sleep(300)
        xbmcgui.Dialog().ok('Keymap loaded.', 'Pressing exit will remove', 'temporary keymaps.')
        printstar()
        printworking()
        print ("Loaded %s .xml to keymaps.  Pressing 'exit' will remove any temporary keymaps." % FILE)
        printstar()
        exit()
    else:
        xbmc.executebuiltin('Notification(Problem, keymap not loaded)')
        printstar()	
        printproblem()	
        print ("%s .txt is not a valid keymap.  No keymap was loaded." % FILE)
        printstar()	
        exit()

# Remove individual keymap.  Check the keymap exists, delete it, reload keymaps.  If no file exists reload anyway.		
def removekeymap():
    if os.path.isfile(KEYMAPDESTFILE):
        os.remove(OLDFAVOURITESFILE)
        xbmc.executebuiltin('Action(reloadkeymaps)')
        xbmc.sleep(300)
        xbmc.executebuiltin('Notification(keymap, removed)')
        printstar()
        printworking()
        print ("Removed %s .xml to keymaps." % FILE)
        printstar()
        exit()
    else:
        xbmc.executebuiltin('Action(reloadkeymaps)')
        xbmc.sleep(300)        
        xbmc.executebuiltin('Notification(Keymap , not found)')
        printstar()	
        printproblem()	
        print ("%s .txt was not found in the keymaps folder.  Keymaps were reloaded in any case.")    
        printstar()	
        exit()

# Backup keymaps
# Check for presence of keymapsbackup folder.  If it exists ask if want to delete existing backups.
# Yes > remove keymapsbackup, No > Do it manually then.
# Copy contents of keymaps folder to keymapsbackup folder
def backupkeymaps():
    if os.path.isdir(KEYMAPSBACKUP):
        YESNOBACKUP = xbmcgui.Dialog().yesno("A backup folder already exists","Do you want to replace it with the current keymaps folder?")
        if not YESNOBACKUP:
            xbmcgui.Dialog().ok('Back up manually', 'before continuing.')		
            printstar()
            printworking()
            print "Keymaps folder contents not saved to smashingfavourites/customkeymaps/keymapsbackup.  Back up keymaps manually."			
            printstar()
            exit()
    os.remove(KEYMAPSBACKUP)
    printstar()
    printworking()
    print "smashingfavourites/customkeymaps/keymapsbackup has been removed"						
    shutil.copy(KEYMAPSFOLDER, KEYMAPSBACKUP)
    xbmc.executebuiltin('Notification(keymaps, saved)')            		
    print "Keymaps folder contents saved to smashingfavourites/customkeymaps/keymapsbackup"			
    printstar()
    exit()
		
# Restore keymaps from backup			
# Check for presence of keymapsbackup folder.  If it exists ask if want to replace existing keymaps.			
# Copy contents of keymapsbackup folder to keymaps folder
def restorekeymaps():
    if os.path.isdir(KEYMAPSBACKUP):
        YESNORESTORE = xbmcgui.Dialog().yesno("Do you want to restore the backed up keymaps?","This will delete your current keymaps.")
        if not YESNORESTORE:
            xbmc.executebuiltin('Notification(Keymaps restore, was cancelled)')		
            printstar()
            printworking()
            print "Keymaps folder restore was cancelled."			
            printstar()
            exit()				
    os.remove(KEYMAPSFOLDER)
    shutil.copy(KEYMAPSBACKUP, KEYMAPSFOLDER)
    xbmc.executebuiltin('Action(reloadkeymaps)')			
    xbmc.executebuiltin('Notification(keymaps, restored)')            		
    printstar()
    printworking()
    print "Keymapsbackup folder contents restored to keymaps folder."			
    printstar()
    exit()
			
# Backup any keymaps starting with 'zdefault' to smashingfavourites/customkeymaps/defaultkeymapsbackup.
# Backup Xonfluence.xml if present.			
def backupdefaultkeymaps():
    printstar()
    printworking()
    if os.path.isdir(DEFAULTKEYMAPSBACKUP):
        YESNODEFAULTBACKUP = xbmcgui.Dialog().yesno("A backup already exists","Do you want to replace it with the","current default keymaps?")
        if not YESNODEFAULTBACKUP:
            xbmcgui.Dialog().ok('Back up manually', 'before continuing.')		
            print "Keymaps folder contents not saved to smashingfavourites/customkeymaps/keymapsbackup.  Back up keymaps manually."			
            printstar()
            exit()				
#    os.remove(DEFAULTKEYMAPSBACKUP)
    shutil.rmtree(DEFAULTKEYMAPSBACKUP)
    os.mkdir(DEFAULTKEYMAPSBACKUP)			
    files = []
    for i in os.listdir(KEYMAPSFOLDER):
        if os.path.isfile(os.path.join(KEYMAPSFOLDER,i)) and 'zdefault' in i:
            files.append(i)
    print files
    n = len(files)
    print ("There are %d default files to back up" % n)
    if n > 0:
        c = 0
        while c < n:
            REM = files[c]
            print ("File to backup is %s ." % REM)
            shutil.copy(KEYMAPSFOLDER + '/' + REM, DEFAULTKEYMAPSBACKUP)            			
            c = c + 1
        xbmc.executebuiltin('Action(reloadkeymaps)')
        xbmc.executebuiltin('Notification(%s  keymaps, saved) % n')
    print ("%d  default keymap files were saved." % n)
    print "Keymaps saved to smashingfavourites/customkeymaps/defaultkeymapsbackup"			
    printstar()
    exit()

def restoredefaultkeymaps():			
    if os.path.isdir(DEFAULTKEYMAPSBACKUP):
        YESNODEFAULTRESTORE = xbmcgui.Dialog().yesno("Do you want to restore the backed up default keymaps?","This will delete your current keymaps","and restore just the defaults.")
        if YESNODEFAULTRESTORE:
            os.remove(KEYMAPSFOLDER)
            shutil.copy(DEFAULTKEYMAPSBACKUP, KEYMAPSFOLDER)
            xbmc.executebuiltin('Action(reloadkeymaps)')
            xbmc.executebuiltin('Notification(Default keymaps, restored)')            		
            printstar()
            printworking()
            print "Keymaps have been restored to defaults"			
            printstar()
            exit()
        else:
            xbmc.executebuiltin('Notification(Action, cancelled)')		
            printstar()
            printworking()
            print "Default keymaps restore was cancelled."			
            printstar()
            exit()			
			
def removetempkeymaps():			
    printstar()
    printworking()
    files = []
    for i in os.listdir(KEYMAPSFOLDER):
        if os.path.isfile(os.path.join(KEYMAPSFOLDER,i)) and 'zztemp' in i:
            files.append(i)
    print files
    n = len(files)
    print ("There are %d files to remove" % n)
    if n > 0:
        c = 0
        while c < n:
            REM = files[c]
            print ("File to delete is %s ." % REM)
            delete = os.path.join(xbmc.translatePath('special://masterprofile/keymaps'), "%s" % REM)
            os.remove(delete)			
            c = c + 1
        xbmc.executebuiltin('Action(reloadkeymaps)')
    if n == 1:
        xbmc.executebuiltin('Notification(1 keymap, removed)')
    else:
        xbmc.executebuiltin('Notification(%s  keymaps, removed) % n')
    print ("%d  temporary keymap files were removed." % n)
    printstar()
    exit()	
	
# Get on with it
if FILE == 'default':
    if MOVE == 'backup':
        backupdefaultkeymaps()
    elif MOVE == 'load':
        restoredefaultkeymaps()
    else:
        printstar()
        printproblem()
        printnoaction()
        printstar()
        exit()

if FILE == 'temp':
    if MOVE == 'remove':
        removetempkeymaps()
    else:		
        printstar()
        printproblem()
        printnoaction()
        printstar()
        exit()

if MOVE == 'load':
    loadkeymap()
elif MOVE == 'remove':	
    removekeymap()		
elif MOVE == 'backup':		
    backupkeymaps()
elif MOVE == 'restore':
    restorekeymaps()
else:
    printstar()
    printproblem()
    printnoaction()
    printstar()
    exit()	
		
		
		
		