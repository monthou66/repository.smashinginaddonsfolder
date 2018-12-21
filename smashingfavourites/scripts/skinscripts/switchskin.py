#!/usr/bin/python
# -*- coding: utf-8 -*-
#switchskin.py
import xbmc
import xbmcgui
import os

# define some stuff
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
SMASHINGTEMP = os.path.join(USERDATA, "smashing", "smashingtemp")
markersfolder = os.path.join(SMASHINGTEMP, "markers")
lastskin = os.path.join(markersfolder, "lastskin.txt")
defaultskin = os.path.join(markersfolder, "defaultskin.txt")
skinpath = xbmc.translatePath('special://skin')

def printstar():
    print "****************************************************************************"
    print "***************************************************************************"

def error():
    printstar()
    print ('%s has stopped with an error'% thisaddon)
    printstar()
    xbmc.executebuiltin('Notification(Check, %s)'% thisaddon)
    exit()
    
def checkfolders():
    global error, error2
    print 'running checkfolders()'
    # check folder structure is in place - make if necessary
    foldersmade = []
    folderstocheck = []
    folderstocheck.append(SMASHINGTEMP)
    folderstocheck.append(markersfolder)
    num = len(folderstocheck)
    c = 0
    while c < num:
        check = folderstocheck[c]
        if not os.path.isdir(check):
            os.mkdir(check)
            xbmc.sleep(300)
            if not os.path.isdir(check):
                print 'Problem in checkfolders()'
                print ('Could not make %s folder'% check)
                xbmc.executebuiltin('Notification(Problem, check log)')
                exit()
            foldersmade.append(check)
        c = c + 1
    size = len(foldersmade)
    if size > 0:
        print ('New folders made: %d'% size)
        e = 0
        while e < size:
            next = foldersmade[e]
            print next
            e = e + 1
	
def startscript():
    global thisaddon
    thisaddon = sys.argv[0]
    printstar()
    print ('%s has started'% thisaddon)
    printstar()
    if not os.path.isdir(markersfolder):
        checkfolders()
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)


def getcurrent():
    # get current active skin and theme
    global skin, theme, skincolour
    skin = os.path.basename(os.path.normpath(skinpath))
    theme = xbmc.getInfoLabel('Skin.CurrentTheme')
    skincolour = xbmc.getInfoLabel('Skin.CurrentColourTheme')
    # unhash for checking if errors:
#    printstar()
#    print ('The current skin id is %s'% skin)
#    print ('The current theme is %s'% theme)
#    print ('The current skin colour theme is %s'% skincolour)
#    printstar()
	
def getlast():
    global lastskin, newskin, newtheme, newskincolour
    mylist = []
    if os.path.exists(lastskin):
        with open(lastskin) as f:
            mylist = f.read().splitlines()
            length = len(mylist)
        if len(mylist) == 3:
            newskin = mylist[0]
            newtheme = mylist[1]
            newskincolour = mylist[2]
        else:
            error()
        # unhash for checking if errors:
#        printstar()
#        print ('mylist is %s'% mylist)
#        print ('newskin is %s'% newskin)
#        print ('newtheme is %s'% newtheme)
#        print ('newskincolour is %s'% newskincolour)		
#        printstar()	

def savecurrent():
    global lastskin, skin, theme, skincolour, settingdefault
    f = open(lastskin, 'w')
    f.write('%s\n'% skin)
    f.write('%s\n'% theme)
    f.write('%s\n'% skincolour)
    f.close()

def savedefault():
    f = open(defaultskin, 'w')
    f.write('%s\n'% skin)
    f.write('%s\n'% theme)
    f.write('%s\n'% skincolour)
    f.close()    
#        printstar()
#        print 'Current skin settings have been saved as default'
#        printstar()
    xbmc.executebuiltin('Notification(Current skin settings, have been set as default)')	
    exit()
		
def getarguments():	
    global newskin, newtheme, newskincolour, settingdefault, lastskin
    newskin = sys.argv[1]
    if len(sys.argv) > 2:
        newtheme = sys.argv[2]
        if len(sys.argv) > 3:
            newskincolour = sys.argv[3]
        else:
            newskincolour = 'SKINDEFAULT'
    else:
        newtheme = 'SKINDEFAULT'
        newskincolour = 'SKINDEFAULT'
    if newskin == 'previous skin':    
        getlast()
        savecurrent()
        checkenabled()
    elif newskin == 'set default':
        savedefault()
    elif newskin == 'restore default':
        savecurrent()
        lastskin = defaultskin
        getlast()
        checkenabled()
    elif newskin == 'choose':
        savecurrent()
        choosenewskin()
    elif newskin == 'choosenoprompt':
        savecurrent()
        choosenewskinnoprompt()
    else:
        savecurrent()
        checkenabled() 

def checkenabled():
    global newskin, newtheme, newskincolour
    # unhash for checking if errors:
#    printstar()
#    print ('Requested skin id is %s'% newskin)
#    print ('Requested theme is %s'% newtheme)
#    print ('Requested skin colour is %s'% newskincolour)
#    printstar()

    if not xbmc.getCondVisibility('System.HasAddon(%s)'% newskin):
        choosenewskin()
    else:
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"%s"}}'% newskin)
        xbmc.executebuiltin('SendClick(11)')
        if not newtheme == 'SKINDEFAULT':
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skintheme","value":"%s"}}'% newtheme)
        if not newskincolour == 'SKINDEFAULT':
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skincolors","value":"%s"}}'% newskincolour)
    
def choosenewskin():
    xbmc.executebuiltin('Addon.Default.Set(xbmc.gui.skin)')
    
def choosenewskinnoprompt():
    xbmc.executebuiltin('Addon.Default.Set(xbmc.gui.skin)')
    c = 0
    while c < 60:
        dialog = xbmcgui.getCurrentWindowDialogId()
        if dialog == 10100:
            xbmc.sleep(100)
            xbmc.executebuiltin('SendClick(11)')
            c = 30
        else:
            c = c + 1
            xbmc.sleep(300)   

startscript()            
            
getcurrent()

getarguments()

exit()