# -*- coding: utf-8 -*-
#smashingskinbackuprestore.py

import xbmc
import xbmcaddon
import xbmcgui
import os
import shutil

# define some stuff
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
SKINBACKUPS = os.path.join(SMASHINGFAVOURITES, "backups", "skins")
skinpath = xbmc.translatePath('special://skin')


def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def error():
    printstar()
    print ('%s has stopped with an error'% thisaddon)
    printstar()
    xbmc.executebuiltin('Notification(Check, %s)'% thisaddon)
    exit()
	
def startaddon():
    global thisaddon
    thisaddon = sys.argv[0]
    printstar()
    print ('%s has started'% thisaddon)
    printstar()
    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)	
	
def getcurrent():
    # get current active skin, plus theme, colour theme and font (get font not working at time of writing).
    # set backup folder and addon_data folder
    global skin, theme, skincolour, font, backupfolder, datafolder, SETTINGS, OLDSETTINGS, OLDTHEME
    skin = os.path.basename(os.path.normpath(skinpath))
    # alternative:  skin = xbmc.getSkinDir()
    theme = xbmc.getInfoLabel('Skin.CurrentTheme')
    skincolour = xbmc.getInfoLabel('Skin.CurrentColourTheme')
    font = xbmc.getInfoLabel('Skin.Font')
    backupfolder = os.path.join(SKINBACKUPS, skin)
    datafolder = os.path.join(USERDATA, "addon_data", skin)
    SETTINGS = os.path.join(datafolder, "settings.xml")
    OLDSETTINGS = os.path.join(datafolder, "oldsettings.xml")
    OLDTHEME = os.path.join(datafolder, 'themebackup.txt')
	# check backup folder exists - make it if not
    if not os.path.exists(backupfolder):
        os.mkdir(backupfolder)
#    printstar()
#    print ('The current skin id is %s'% skin)
#    print ('The current theme is %s'% theme)
#    print ('The current skin colour theme is %s'% skincolour)
#    print ('The current font is %s'% font)
#    printstar()
    listfolders()

def listfolders():
    # list existing backup folders
    global backups, howmany
    LIST = []
    LIST = os.listdir(backupfolder)
    number = len(LIST)
    backups = []	
    # empty backups, in case script has looped back (maybe not needed?)
    if len(backups) > 0:
        del backups[:]	
    # LIST includes files; backups is folders only:	
    c = 0
    while c < number:
        check = LIST[c]
        checkpath = os.path.join(backupfolder, check)
        if os.path.isdir(checkpath):
            backups.append(check)
        c = c + 1
    howmany = len(backups)
    chooseoption()
	
def chooseoption():
    # backup or restore
    # view backup, restore, delete backup, rename backup
    # add more functions - eg switch skin, edit skin, backup different (non-running) skin, reload skin, blah blah
    global OPTION, text, backups
    OPTIONSLIST = ['Restore skin settings from backup', 'Backup skin settings', 'Rename backups', 'Delete Backups', 'Quit']
    back = 'Go back to options list'
    OPTION = xbmcgui.Dialog().select("Smashing Skin Options", OPTIONSLIST)
    # restore
    if OPTION == 0:
        if howmany >= 1:
            text = 'Choose the backup to restore'
        else:
            text = 'There are no existing backups'
        if os.path.isfile(OLDSETTINGS):
            last = 'Restore previous settings'
            backups.append(last)
    # backup
    elif OPTION == 1:
        text = 'Choose where you want to back up.'
        last = 'Make a new backup'
        backups.append(last)
    # rename
    elif OPTION == 2:
        text = 'Choose the backup to rename'
    # delete
    elif OPTION == 3:
        text = 'Choose the backup to delete'
    # quit
    elif OPTION	 == 4:
        xbmc.executebuiltin('Notification(%s, is stopping)'% thisaddon)
        exit()
    else:
        xbmc.executebuiltin('Notification(No option selected, %s is stopping)'% thisaddon)
        exit()	
    choosefromlist()
	
def choosefromlist():
    global FOLDER, FILE, THEMEFILE, FOLDERNAME
    printstar()
    print ('backups are %s'% backups)
    back = 'Go back to options list'
    backups.append(back)
    quit = 'Quit'
    backups.append(quit)
    print ('now backups are %s'% backups)
    printstar()
    length = len(backups)
    CHOOSE = xbmcgui.Dialog().select(text, backups)	
# add this or get error?
    FOLDER = datafolder	
    # read the choice
    if not 0 <= CHOOSE <= length:
        xbmc.executebuiltin('Notification(No option selected, %s is stopping)'% thisaddon)
        exit()
    if backups[CHOOSE] == quit:
        xbmc.executebuiltin('Notification(%s, is stopping)'% thisaddon)
        exit()
    elif backups[CHOOSE] == back:
        listfolders()
    elif backups[CHOOSE] == 'Restore previous settings':  # ie last
        FOLDER = datafolder  # already set to this but what the heck
        FOLDERNAME = 'previous settings'   # use in notification at the end of restore()
        FILE = OLDSETTINGS
    elif backups[CHOOSE] == 'Make a new backup':
        FOLDERNAME = 'new'
    else:
        FOLDERNAME = backups[CHOOSE]
        FOLDER = os.path.join(backupfolder, FOLDERNAME)	
        FILE = os.path.join(FOLDER, "settings.xml")
    THEMEFILE = os.path.join(FOLDER, 'themebackup.txt')
    # And go
    if OPTION == 0:
        restore()
    if OPTION == 1:
        backup()
    if OPTION == 2:
        renamebackup()
    if OPTION == 3:
        deletebackup()
				
def restore():
    global theme, skincolour, font, FILE, OLDSETTINGS, THEMEFILE, DELETE, FILETOMOVE, FILETOCOPY, TARGETFILE
    # switch into another skin
    if not skin == 'skin.estuary':
#        SWITCH = 'skin.estuary'    # assumes skin.estuary is present - so needs adjustment for pre-krypton
        if xbmc.getCondVisibility('System.HasAddon(skin.estuary)'):
            SWITCH = 'skin.estuary'
    if not SWITCH == 'skin.estuary':
        if xbmc.getCondVisibility('System.HasAddon(skin.estouchy)'):
            SWITCH = 'skin.estouchy'
        elif xbmc.getCondVisibility('System.HasAddon(skin.confluence)'):
            SWITCH = 'skin.confluence'
        else:
            printstar()
            print ('No skin available to switch into. %s has stopped'% thisaddon)
            printstar()
            error()	
    xbmc.executebuiltin('UnloadSkin()')
    xbmc.sleep(300)	
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"%s"}}'% SWITCH)
    xbmc.executebuiltin('SendClick(11)')
    xbmc.executebuiltin('UnloadSkin()')
    # use TEMPFILE as staging post for new settings (had problems with direct copy)
    TEMPFILE = os.path.join(datafolder, 'tempsettings.xml')
    TEMPTHEMEFILE = os.path.join(datafolder, 'tempthemebackup.txt')
    if os.path.exists(TEMPFILE):
        DELETE = TEMPFILE
        deletefile()	
    if os.path.exists(TEMPTHEMEFILE):
        DELETE = TEMPTHEMEFILE
        deletefile()		
    if not os.path.exists(TEMPFILE):
        if os.path.exists(FILE):
            if FILE == OLDSETTINGS:
                FILETOMOVE = FILE
                TARGETFILE = TEMPFILE
                renamefile()
                if os.path.isfile(THEMEFILE):
                    FILETOMOVE = THEMEFILE
                    TARGETFILE = TEMPTHEMEFILE
                    renamefile()
            else:
                FILETOCOPY = FILE
                TARGETFILE = TEMPFILE
                copyfile()	
		
    # Get info from THEMEFILE:
    newtheme = theme
    newskincolour = skincolour
    newfont = font
    mylist = []
    if os.path.exists(THEMEFILE):
        with open(THEMEFILE) as f:
            mylist = f.read().splitlines()
            length = len(mylist)
        if len(mylist) == 7:
            newtheme = mylist[2]
            newskincolour = mylist[4]
            newfont = mylist[6]    # this may not be valid - if not it will be ignored
# save current settings:
    # remove existing backup from addon_data folder	
    if os.path.isfile(OLDSETTINGS):
        DELETE = OLDSETTINGS
        deletefile()
    if os.path.isfile(OLDTHEME):
        DELETE = OLDTHEME
        deletefile()
    # save existing settings plus theme etc to addon_data
    FILETOMOVE = SETTINGS
    TARGETFILE = OLDSETTINGS
    renamefile()
    f = open(OLDTHEME, 'w')
    f.write('This file has the Theme, Colours and Font associated with the backup of %s\n'% skin)
    f.write('Theme:\n')
    f.write('%s\n'% theme)
    f.write('Skincolours:\n')
    f.write('%s\n'% skincolour)
    f.write('Font:\n')
    f.write('%s\n'% font)
    f.close()
    # move new settings.xml in:
    FILETOMOVE = TEMPFILE
    TARGETFILE = SETTINGS		
    renamefile()
    # restart skin
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"%s"}}'% skin)        
    xbmc.executebuiltin('SendClick(11)')
    # set theme and colours if necessary	
    theme = xbmc.getInfoLabel('Skin.CurrentTheme')
    skincolour = xbmc.getInfoLabel('Skin.CurrentColourTheme')
    font = xbmc.getInfoLabel('Skin.Font')
    if not newtheme ==  theme:
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skintheme","value":"%s"}}'% newtheme)
    if not newskincolour == skincolour:
        print ('newskincolour is %s'% newskincolour)
        print ('skincolour is %s'% skincolour)
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skincolors","value":"%s"}}'% newskincolour)
    if not newfont == font:
	# if font is 'Skin.Font' ignore - function is not implemented yet.
        if not newfont == 'Skin.Font':
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.font","value":"%s"}}'% newfont)		
    xbmc.executebuiltin('Notification(%s has been, restored from %s)'% (skin, FOLDERNAME))
    exit()

def deletefile():
    if os.path.exists(DELETE):
        count = 0
        while count < 50:
            try:
                os.remove(DELETE)
            except:
                pass
            if not os.path.exists(DELETE):
#                print ('count (%s) is %d'% (DELETE, count))
                count = count + 50
            xbmc.sleep(300)
            count = count + 1
    if os.path.exists(DELETE):
        printstar()
        print ('Problem with %s.  Could not delete %s'% (thisaddon, DELETE))
        printstar()
        xbmc.executebuiltin('ReloadSkin()')
        error()

def renamefile():
    global DELETE
    if os.path.exists(TARGETFILE):
        DELETE = TARGETFILE
        deletefile()
    if os.path.exists(FILETOMOVE):
        count = 0
        while count < 50:
            try:
                os.rename(FILETOMOVE, TARGETFILE)
            except:
                pass
            if os.path.exists(TARGETFILE):
#                print ('count (%s) is %d'% (TARGETFILE, count))
                count = count + 50
            xbmc.sleep(300)
            count = count + 1
    if not os.path.exists(TARGETFILE):
        printstar()
        print ('Problem with %s.  Could not move %s'% (thisaddon, FILETOMOVE))
        printstar()
        xbmc.executebuiltin('ReloadSkin()')
        error()

def copyfile():
    global DELETE
    if os.path.exists(TARGETFILE):
        DELETE = TARGETFILE
        deletefile()
    if os.path.exists(FILETOCOPY):
        count = 0
        while count < 50:
            try:
                shutil.copyfile(FILETOCOPY, TARGETFILE)
            except:
                pass
            if os.path.exists(TARGETFILE):
#                print ('count (%s) is %d'% (TARGETFILE, count))
                count = count + 50
            xbmc.sleep(300)
            count = count + 1
    if not os.path.exists(TARGETFILE):
        printstar()
        print ('Problem with %s.  Could not copy %s'% (thisaddon, FILETOCOPY))
        printstar()
        xbmc.executebuiltin('ReloadSkin()')
        error()

def makefolder():
    if not os.path.isdir(FOLDER):
        count = 0
        while count < 50:
            try:
                os.mkdir(FOLDER)
            except:
                pass
            if os.path.isdir(FOLDER):
#                print ('count (%s) is %d'% (FOLDERNAME, count))
                count = count + 50
            xbmc.sleep(300)
            count = count + 1
    if not os.path.isdir(FOLDER):
        printstar()
        print ('Problem with %s.  Could not create %s folder'% (thisaddon, FOLDERNAME))
        printstar()
        error()
				
def backup():
    # if new backup get name
    global DELETE, FOLDER, FOLDERNAME, FILETOCOPY, TARGETFILE
    if FOLDERNAME == 'new':
        YESNONAME = xbmcgui.Dialog().yesno("You have chosen to make a new backup", "", "Confirm action?")	
        if not YESNONAME:	
            startagain()
        # get name
        keyboard = xbmc.Keyboard("", "Enter new backup name", False)
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText() != "":
            FOLDERNAME = keyboard.getText()
            yesnowindow = xbmcgui.Dialog().yesno('New backup name entered is', FOLDERNAME, "", "Click Yes to proceed")
            if not yesnowindow:
                startagain()

    FOLDER = os.path.join(backupfolder, FOLDERNAME)
    FILE = os.path.join(FOLDER, "settings.xml")
    # check if folder / file exist.  Make folder if not.  Delete file if there.
    if os.path.exists(FOLDER):
        if os.path.isdir(FOLDER):
            if os.path.exists(FILE):
                DELETE = FILE
                deletefile()
    else:
        makefolder()
    # copy settings.xml into folder
    FILETOCOPY = SETTINGS
    TARGETFILE = FILE
    copyfile()	
    # save existing settings plus theme etc to addon_data
    THEMEFILE = os.path.join(FOLDER, 'themebackup.txt')
    f = open(THEMEFILE, 'w')
    f.write('This file has the Theme, Colours and Font associated with the backup of %s\n'% skin)
    f.write('Theme:\n')
    f.write('%s\n'% theme)
    f.write('Skincolours:\n')
    f.write('%s\n'% skincolour)
    f.write('Font:\n')
    f.write('%s\n'% font)	# might be ignored
    f.close()	
    # Finish it off nicely	
    xbmc.executebuiltin('Notification(Backed up, to %s)'% FOLDERNAME )
    xbmc.sleep(1000)
    getcurrent()

def renamebackup():
    # confirm backup to rename
    YESNORENAME = xbmcgui.Dialog().yesno("You have chosen to rename", FOLDERNAME, "", "Confirm action?")	
    if not YESNORENAME:	
        startagain()
    # get new name
    keyboard = xbmc.Keyboard("", "Enter new name", False)
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText() != "":
        NEWNAME = keyboard.getText()
        yesnowindow = xbmcgui.Dialog().yesno('New name entered is', NEWNAME, "", "Click Yes to proceed")
        if not yesnowindow:
            startagain()
    else:
        startagain()
    # rename the crap outofit
    FOLDER = os.path.join(backupfolder, FOLDERNAME)
    NEWNAMEPATH = os.path.join(backupfolder, NEWNAME)
    count = 0
    while count < 50:
        try:
            os.rename(FOLDER, NEWNAMEPATH)
        except:
            pass
        if os.path.exists(NEWNAMEPATH):
#            print ('count (%s) is %d'% (NEWNAME, count))
            count = count + 50
        xbmc.sleep(300)
        count = count + 1
    if os.path.exists(NEWNAMEPATH):
        printstar()
        print ('%s has renamed %s to %s'% (thisaddon, FOLDERNAME, NEWNAME))
        printstar()
        xbmc.executebuiltin('Notification(%s has been renamed, to %s)'% (FOLDERNAME, NEWNAME) )
    else:		
        printstar()
        print ('Problem with %s.  Could not rename %s'% (thisaddon, FOLDERNAME))
        printstar()
        xbmc.executebuiltin('Notification(Something went wrong, Could not rename %s)'% FOLDERNAME )
    #backtostart
    xbmc.sleep(1000)
    getcurrent()		


def deletebackup():
    # confirm backup to delete
    YESNODELETE = xbmcgui.Dialog().yesno("You have chosen to delete", FOLDERNAME, "", "Confirm delete?")	
    if not YESNODELETE:	
        startagain()		
    # delete folder
    FOLDER = os.path.join(backupfolder, FOLDERNAME)
    if os.path.exists(FOLDER):
        count = 0
        while count < 50:
            try:
                shutil.rmtree(FOLDER)
            except:
                pass
            if not os.path.exists(FOLDER):
#                print ('count (%s) is %d'% (FOLDERNAME, count))
                count = count + 50
            xbmc.sleep(300)
            count = count + 1
    if os.path.exists(FOLDER):
        printstar()
        print ('Problem with %s.  Could not delete %s'% (thisaddon, FOLDERNAME))
        printstar()
        xbmc.executebuiltin('Notification(Something went wrong, Could not delete %s)'% FOLDERNAME )	
    else:
        printstar()
        print ('%s has deleted %s'% (thisaddon, FOLDERNAME))
        printstar()
        xbmc.executebuiltin('Notification(%s, has been deleted)'% FOLDERNAME )
    #backtostart
    xbmc.sleep(1000)
    getcurrent()	

def startagain():
        xbmcgui.Dialog().ok('The action has been cancelled', 'Choose a new option.')
        listfolders()		
		

		
startaddon()
getcurrent()
exit()


# drink beer, eat pies

	

