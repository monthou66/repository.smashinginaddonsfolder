# -*- coding: utf-8 -*-
import os
import os.path
import xbmc
import xbmcaddon
import sys
import xbmcgui
import shutil

# check which option wanted. and that it exists
# check which option is open, that it is valid and has a save folder
# move files if necessary
# open favourites

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def printproblem():
    print "There is a problem with smashingfavourites."
    
def refreshfavs():
    xbmc.executebuiltin("System.LogOff")
    xbmc.sleep(300)
    xbmc.executebuiltin("LoadProfile(Master user)")

def finish():
    printstar()
    print ('%s is shutting down'% thisaddon)
    printstar()
    xbmc.executebuiltin('Notification(Favourites updated, all done)')
    exit()

thisaddon = sys.argv[0]
# get kodi version
refresh = 'false'
kodiversion = xbmc.getInfoLabel('System.BuildVersion')
kodiversion = kodiversion[:2]
print 'kodiversion:'
print kodiversion
kodiversion = int(kodiversion)
if kodiversion > 17:
    refresh = 'true'



# exit()

# read wanted favourite
NAME = sys.argv[1]
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
FAVOURITESFOLDER = os.path.join(SMASHINGFAVOURITES, "options")
# check the file path - see if favourites.xml is there
NEWFAVOURITESFILE = os.path.join(FAVOURITESFOLDER, NAME, "favourites.xml")
# read current favourite
# old version before pathsubs: FAVOURITESFILE = os.path.join(xbmc.translatePath('special://masterprofile'), "favourites.xml")
# tried pathsub nogo - cocked up favourites script: FAVOURITESFILE = os.path.join(SMASHINGFAVOURITES, "pathsubs", "favourites.xml")
FAVOURITESFILE = os.path.join(SMASHINGFAVOURITES, "pathsubs", "userdata", "favourites.xml")
DEFAULTFAVLOCATION = os.path.join(USERDATA, "favourites.xml")
# get line 2
line = open(FAVOURITESFILE).readlines()[1]
# get name of current favourites:
CURRENT = line[line.find("/icons/")+7:line.find(".png")]
# for testing:
printstar()
print ('Running %s'% thisaddon)
print ('The currently loaded favourites.xml is %s .' % CURRENT)
printstar()
# if requested favourites isn't in smashingfavourites or userdata print errors and finish
if not os.path.isfile(NEWFAVOURITESFILE):
    if NAME != CURRENT:
        xbmc.executebuiltin('Notification(Check, favourites.xml)')
        printstar()
        printproblem()
        print ('The requested favourites.xml is %s .  This does not seem to exist.  Check it.' % NAME)
        printstar()
        exit()

# make sure the favourites are named and the name is valid
# define location to return current favourites.xml to and check the folder exists
OLDFAVOURITES = os.path.join(FAVOURITESFOLDER, CURRENT)
OLDFAVOURITESFILE = os.path.join(FAVOURITESFOLDER, CURRENT, "favourites.xml")
OLDFAVOURITESBACKUP = os.path.join(FAVOURITESFOLDER, CURRENT, "favouritesbackup.xml")

if not os.path.isdir(OLDFAVOURITES):
    xbmc.executebuiltin('Notification(Check, favourites.xml)')
    printstar()
    printproblem()
    print "The current favourites.xml doesn't have a folder in smashingfavourites/options.  Check it."
    printstar()
    exit()

# Move old favourites out and new ones in, unless they're the same
# Delete oldfavouritesbackup if exists.  Rename oldfavouritesfile to oldfavouritesbackup
# Move favouritesfile to oldfavouritesfile.  Copy newfavouritesfile to favouritesfile.
if NAME != CURRENT:
    if os.path.isfile(OLDFAVOURITESBACKUP):
        os.remove(OLDFAVOURITESBACKUP)
        os.rename(OLDFAVOURITESFILE, OLDFAVOURITESBACKUP)
    else:
        os.rename(OLDFAVOURITESFILE, OLDFAVOURITESBACKUP)
        printstar()
        print 'No OLDFAVOURITESBACKUP file found'
        printstar()
    os.rename(FAVOURITESFILE, OLDFAVOURITESFILE)
    shutil.copy(NEWFAVOURITESFILE, FAVOURITESFILE)
# get it done

# if selected favourites = 'general' copy favourites.xml to real userdata location (to keep script.favourites happy)
if NAME == 'general':
    if os.path.isfile(DEFAULTFAVLOCATION):
        os.remove(DEFAULTFAVLOCATION)
    shutil.copy(FAVOURITESFILE, DEFAULTFAVLOCATION)
    
if refresh == 'true':
    refreshfavs()
    finish()

# check open window and focus - need to know whether favourites sideblade is open / whether to move focus if in a list
win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
focus = win.getFocusId()	
# check if favourites window is visible - no returns 0, yes returns 1
vis = xbmc.getCondVisibility('Window.IsVisible(10134)')
#if favourites are visible move left to close them
if vis == 1:
	xbmc.executebuiltin( "XBMC.Action(Left)" )
	xbmc.sleep(300)
#	Check if using smashingletters whether focus is not on sidebar (2) or (right) scrollbar (60)
# - and move focus to main list if required.
if NAME == 'letters':
	if focus == 2:
		xbmc.executebuiltin( "XBMC.Action(Right)" )
	if focus == 60:
		xbmc.executebuiltin( "XBMC.Action(Left)" )
# And finally...drum roll...
xbmc.executebuiltin("ActivateWindow(Favourites)")
# move focus to top except in smashingletters
if NAME != "letters":
    xbmc.executebuiltin( "XBMC.Action(FirstPage)" )
exit()	