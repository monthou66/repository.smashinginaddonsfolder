# -*- coding: utf-8 -*-

######################################################################################################################################################
######################################################################################################################################################
##  start custom dialogs from shortcuts, keypresses, whatever.
##  Options
##  -------
##  number = number of custom dialog to open
##  close = close all dialogs
##  back / last = go back to the previous dialog (if dialog is open) / go to the last opened dialog (same function)
##  default = go to 2154 (choose) if no argument set
##  
##
##  history is stored in kodi/userdata/smashing/smashingtemp/miscfiles/dialoghistory.txt
######################################################################################################################################################
######################################################################################################################################################

import xbmc
import xbmcgui
import os

print 'starting opendialog.py'

USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGTEMP = os.path.join(USERDATA, "smashing", "smashingtemp")
TEMPMISC = os.path.join(SMASHINGTEMP, "miscfiles")
history = os.path.join(TEMPMISC, "dialoghistory.txt")
dialog = xbmcgui.getCurrentWindowDialogId()

# defaults:
back = 'false'
close = 'false'
update = 'true'            # do update history
add = 'true'               # add line to history if update = true
remove = 'false'            # don't remove a line
hist = []

def checkfolders():
    global error, error2
    print 'running checkfolders()'
    # check folder structure is in place - make if necessary
    foldersmade = []
    folderstocheck = []
    folderstocheck.append(SMASHINGTEMP)
    folderstocheck.append(TEMPMISC)
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
        
            
def openit():
    global update, add, remove, hist
    print 'starting openit()'
    if dialog == tgt:
        finish()            # nothing to do, it's already there - also no need to update history
    #if dialog = 9999 none are open
    elif dialog == 9999:
        xbmc.executebuiltin('ActivateWindowAndFocus(%d,return)'% target)
#        if not target == 2151:
#            if not target == 2154:
#                update = 'true'
    else:
        xbmc.executebuiltin('Dialog.Close(all,true)')
        xbmc.executebuiltin('ActivateWindowAndFocus(%d,return)'% target)
#        if not target == 2151:
#            if not target == 2154:
#                update = 'true'
    if update == 'true':
        if add == 'true':
            updatehist()
        elif remove == 'true':
            removefromhist()
        else:                       # error condition
            xbmc.executebuiltin('Notification(Check log, problem with opendialog.py)')
            print 'opendialog.py problem ******************************************************************************************************'
            print 'update is true but neither add nor remove specified.'
    finish()           

def updatehist():
    global hist, target
    print 'runningupdatehist()'
    target = str(target)
    if target in hist:
        hist.remove(target)
    hist.append(target)
    if not target in hist:
        print 'problem with opendialog.py updatehist()'
        print 'could not add target to hist'
        finish()
    writehistory()
        
def removefromhist():
    global hist
    print 'running removefromhist()'
    p = len(hist)
    hist = hist[:-1]
    q = len(hist)
    if not p == q + 1:
        print 'problem with opendialog.py removefromhist()'
        print 'could not remove item from hist'
        finish()
    writehistory()
    
    

def readhistory():
    global hist
    print 'starting readhistory()'
    if not os.path.isfile(history):
        f = open(history,"w")
        f.close()
        xbmc.sleep(300)
    f = open(history,"r")
    lines = f.readlines()
    num = len(lines)
    if num > 0:
        c = 0
        while c < num:
            item = lines[c].strip()
            if not item == "":
                hist.append(item)
            c = c + 1
            
def writehistory():
    global hist
    print 'starting writehistory'
    num = len(hist)
    print ('num is %d'% num)
    # set maximum size of history file to write
    if num > 20:
        hist = hist[-20:]
    f = open(history,"w")
    for item in hist:
        f.write("%s\n" % item)
    f.close()        
    finish()

# if dialog is not open (dialog = 9999) should use last item in list but not delete, so set update = false
    
def getlastdialog():
    global target, tgt, update, remove, add
    if dialog == 9999:
        if len(hist) > 0:
            target = hist[-1]
            if target.isdigit():
                target = int(target)
                tgt = 10000 + target
                update = 'false'
                print 'check112'
                print ('target is %d'% target)
                print ('tgt is %d'% tgt)
                print ('dialog is %d'% dialog)
            else:
                target = int(2154)      # problem (non-number) entry should be removed automatically
                tgt = int(12154)
        else:
            target = int(2154)      
            tgt = int(12154)
            update = 'true'         # if no history may as well start some
            remove = 'false'
            add = 'true'
    else:                               # ie if custom dialog already open
        if len(hist) > 0:
            target = hist[-1]
            if target.isdigit():
                target = int(target)
                tgt = 10000 + target
            else:
                target = int(2154)
                tgt = int(12154)
            if tgt == dialog:
                if len(hist) > 1:
                    target = hist[-2]
                    if target.isdigit():
                        target = int(target)
                        tgt = target + 10000
                    else:
                        target = int(2154)      # defaults
                        tgt = int(12154)
                else:
                    target = int(2154)
                    tgt = target + 10000
            else:
                target = int(dialog)
                tgt = 10000 + target
        else:
            target = int(2154)      # defaults
            tgt = 12154
    print ('target is %d'% target)
    print ('tgt is %d'% tgt)
    print ('dialog is %d'% dialog)
            
def finish():
    print 'stopping opendialog.py'
    exit()

# check structure is there:
if not os.path.isfile(history):
    checkfolders()    
# script started with argument - dialog 
if len(sys.argv) > 1:
    target = sys.argv[1]
else:
    target = str(2154)
if target.isdigit():
    target = int(target)
    tgt = int(10000 + target)
    readhistory()
    openit()
else:
    if target == 'back':
        back = 'true'
        remove = 'true'
        add = 'false'
        readhistory()
        getlastdialog()
        openit()
    elif target == 'last':
        back = 'true'
        remove = 'true'
        add = 'false'
        readhistory()
        getlastdialog()
        openit()
    elif target == 'close':
        xbmc.executebuiltin('Dialog.Close(all,true)')
        finish()
    else:
        target = int(2154)      # defaults
        tgt = 12154
        openit()


    
# Drink beer