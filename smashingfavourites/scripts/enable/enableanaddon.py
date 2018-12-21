# -*- coding: utf-8 -*-

#####################################################################################################
##   Possible variables:
##   enable / disable
##   include / exclude          - include = only these addons checked (by keyword in addon_id); default is include
##   type                       - keyword or part / whole id - only addon with 'type' in id will be processed
##   typetwo                    - and another
##   typethree                  - etc
##   typefour                   - etc
##   multiple                   - number, how many addon types specced
##   force                      - if there's only one possibility the addon will be enabled / disabled without prompt
##   all                        - all addons that fit the criteria will be enabled / disabled without prompt
##   user                       - only addons in the user-install directory will be checked (ie special/home/addons, not special/xbmc/addons)
##   deleteaddonfolder          - physically delete the addon folder (eg if problems with uninstall via gui) - nuclear option
##   forceuserfalseifwindows    - overrides 'user = true' if using 'deleteaddonfolder' in windows (as addons can be deleted from the directory)
#####################################################################################################

import xbmc
import xbmcgui
import os
import shutil

# path to kodi addons folder:	
ADDONSPATH = os.path.join(xbmc.translatePath('special://home/'), "addons")
DEFAULTADDONSPATH = os.path.join(xbmc.translatePath('special://xbmc/'), "addons")
# marker = os.path.join(xbmc.translatePath('special://masterprofile'), 'smashing', 'smashingtemp', 'markers', 'enableanaddonrunning.txt')
# Make some lists:
ADDONS = []
DISABLED = []
ENABLED = []
NOTFOUND = []
SUCCESS = []
FAIL = []
TYPE = []      # types of addon specced in arguments

# and some defaults
errormessage = 'none'

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def startaddon():
    global thisaddon, a
    thisaddon = sys.argv[0]
#    a = sys.argv[1]
    printstar()
    print ('%s has started'% thisaddon)
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)

def getarguments():	
    global job, include, type, typetwo, typethree, typefour, force, all, user, multiple, TYPE
    job = 'enable'
    include = 'false'
    multiple = 0
    type = 'wibble'
    typetwo = 'wibble'
    typethree = 'wibble'
    typefour = 'wibble'
    force = 'false'
    num = len(sys.argv)
    all = 'false'
    user = 'not set'

    if num > 1:
        c = 1
        while c < num:
            arg = sys.argv[c]
            if arg == 'enable':
                job = 'enable'
            elif arg == 'disable':
                job = 'disable'
            elif arg == 'deleteaddonfolder':
                job = 'deleteaddonfolder'
                user = 'true'
            elif arg == 'include':
                include = 'true'
            elif arg == 'exclude':
                include = 'false'
            elif arg == 'force':
                force = 'true'
            elif arg == 'all':
                all = 'true'
            elif arg == 'user':
                user = 'true'
            elif arg == 'forceuserfalseifwindows':
                if xbmc.getCondVisibility('System.HasAddon(script.windows32)'):
                    user = 'false'
                elif xbmc.getCondVisibility('System.HasAddon(script.windows64)'):
                    user = 'false'
                else:
                    user = 'true'
            else:
                if type == 'wibble':
                    type = arg
                    multiple = 1
                    include = 'true'
                    TYPE.append(arg)
                elif typetwo == 'wibble':
                    typetwo = arg
                    multiple = 2
                    TYPE.append(arg)
                elif typethree == 'wibble':
                    typethree = arg
                    multiple = 3
                    TYPE.append(arg)
                else:
                    typefour = arg
                    multiple = 4
                    TYPE.append(arg)
            c = c + 1
    if user == 'not set':
        user = 'false'
    # check
    print 'check 55'
    print ('job is %s'% job)
    print ('include is %s'% include)
    print ('type is %s'% type)
    print ('multiple is %d'% multiple)
    print ('TYPE is %s'% TYPE)

    
def listaddons():
    # start by listing all addons unless using 'exclude'
    if not include == 'true':
        print 'check110'
        for i in os.listdir(PATH):
            if not i[0:5] == 'xbmc.':   # these are system folders - can't be enabled / disabled
                if os.path.isdir(os.path.join(PATH,i)) and 'packages' not in i and 'temp' not in i:
                    ADDONXML = os.path.join(PATH, i, "addon.xml")
                    if os.path.exists(ADDONXML):
                        if i not in ADDONS:
                            ADDONS.append(i)   # this lists all addons in the folder
        # if include == false we need to iterate over the list and remove all types specced.
        if multiple > 0:   # ie at least 1 type specced to exclude
            c = 0
            length = len(ADDONS)
            REMOVED = []
            while c < multiple:
                test = TYPE[c]
                d = 0
                while d < length:
                    ITEM = ADDONS[d]
                    print ('ITEM is %s'% ITEM)
                    print ('checking for %s in %s'% (test, ITEM))
                    if test in ITEM:
                        REMOVED.append(ITEM)
                        print ('%s found in %s'% (test, ITEM))
                        print 'item removed'
                    d = d + 1
                c = c + 1
            # now take REMOVED out of ADDONS
            for x in REMOVED:
                try:
                    ADDONS.remove(x)
                except ValueError:
                    pass
    else:                           # ie if include == 'true'
        c = 0
        while c < multiple:     # multiple must be at least 1 if include == true
            test = TYPE[c]
            for i in os.listdir(PATH):
                if not i[0:5] == 'xbmc.':   # these are system folders - can't be enabled / disabled
                    if os.path.isdir(os.path.join(PATH,i)) and test in i and 'packages' not in i and 'temp' not in i:
                        ADDONXML = os.path.join(PATH, i, "addon.xml")
                        if os.path.exists(ADDONXML):
                            if i not in ADDONS:
                                ADDONS.append(i)                    
            c = c + 1
 
        
    printstar()
    num = len(ADDONS)
    c = 0
    print 'Here be ADDONS:'
    while c < num:
        s = ADDONS[c]
        print s
        c = c + 1
    printstar()                               
                            
def checkaddons(): 
    global ENABLED, DISABLED               
    printstar()
    print ADDONS
    n = len(ADDONS)
    print ("There are %d addons in the kodi addons folders that will be checked." % n)
    printstar()
    # Check each addon - if not enabled add to DISABLED, if enabled add to ENABLED - otherwise add to NOTFOUND.
    if n > 0:
        c = 0
        while c < n:
            CHECK = ADDONS[c]
            print ("Now checking %s ." % CHECK)
            if xbmc.getCondVisibility('System.HasAddon(%s)' % CHECK):
                if CHECK not in ENABLED:
                    ENABLED.append(CHECK)
            else:
                # is addonid same as foldername?  If not get id from addon.xml and try again!        
                ADDONXML = os.path.join(ADDONSPATH, CHECK, "addon.xml")
                if not os.path.exists(ADDONXML):
                    ADDONXML = os.path.join(DEFAULTADDONSPATH, CHECK, "addon.xml")
                # get the addonid
                with open(ADDONXML) as f:
                    for line in f:
                        if 'id="' in line:
#                        if "<addon id=" in line:
                            start = "id=\""
                            end = "\""
                            ADDONID = (line.split(start))[1].split(end)[0]
                            print ('Folder is %s' % CHECK)
                            print ('Addonid to check is %s' % ADDONID)
                            if not CHECK == ADDONID:
                                if xbmc.getCondVisibility('System.HasAddon(%s)' % ADDONID):
                                    if ADDONID not in ENABLED:
                                        if ADDONID not in DISABLED:
                                            ENABLED.append(ADDONID)
                                else:
                                    if ADDONID not in DISABLED:
                                        if ADDONID not in ENABLED:
                                            DISABLED.append(ADDONID)
                            else:
                                if CHECK not in DISABLED:
                                    if CHECK not in ENABLED:
                                        DISABLED.append(CHECK)
                                
            c = c + 1
        d = len(DISABLED)
        e = len(ENABLED)
        # check all addons are accounted for
        if not n == d + e:
            xbmc.executebuiltin('Notification(problem with enableanaddon.py, check log for details)')
            printstar()
            print 'Problem with enableanaddon.py.'
            print ('n = %d'% n)
            print ('d = %d'% d)
            print ('e = %d'% e)
            print 'So d + e != n'
            print ADDONS
            print ENABLED
            print DISABLED
       
            printstar()
            exit()
    else:
        xbmc.executebuiltin('Notification(No relevant addons, installed to check)')        
        printstar()
        print 'No addons installed to check.'
        printstar()
        exit()

    if d == 0:
        if job == 'enable':
            xbmc.executebuiltin('Notification(No relevant addons, are currently disabled)')
            printstar()
            print 'No relevant disabled addons found'
            printstar()
            exit()
            
    if e == 0:
        if job == 'disable':
            xbmc.executebuiltin('Notification(No relevant addons, are currently enabled)')
            printstar()
            print 'No relevant enabled addons found'
            printstar()
            exit()

def test():
    # testing
    print ('Disabled addons are %s'% DISABLED)
    g = 0
    while g < d:
        thingy = DISABLED[g]
        print ('when g = %d:'% g)
        print ('addon is %s'% thingy)
        g = g + 1
        
    print ('Enabled addons are %s'% ENABLED)
    g = 0
    while g < d:
        thingy = ENABLED[g]
        print ('when g = %d:'% g)
        print ('addon is %s'% thingy)
        g = g + 1        

def chooseaddontoenable():
    global SUCCESS, FAIL, CHOICE
    if force == 'true' and len(DISABLED) == 1:
        CHOOSE = 0
        CHOICE = DISABLED[0]
    else:
        # List disabled addons, so can choose one to enable
        # Display list and get choice
        CHOOSE = xbmcgui.Dialog().select("Choose an addon to enable", DISABLED)
        # if don't select CHOOSE is -1, which selects last item.
        if CHOOSE == -1:
            xbmc.executebuiltin('Notification(No addon, selected)')
            exit()
        CHOICE = DISABLED[CHOOSE]
    printstar()
    print ('Choose is %d'% CHOOSE)
    print ("Choice = %s" % CHOICE)
    printstar()
    enable()
        
def chooseaddontodisable():
    global SUCCESS, FAIL, CHOICE
    if force == 'true' and len(ENABLED) == 1:
        CHOOSE = 0
        CHOICE = ENABLED[0]
    else:
        # List enabled addons, so can choose one to disable
        # Display list and get choice
        CHOOSE = xbmcgui.Dialog().select("Choose an addon to disable", ENABLED)
        # if don't select CHOOSE is -1, which selects last item.
        if CHOOSE == -1:
            xbmc.executebuiltin('Notification(No addon, selected)')
            exit()
        CHOICE = ENABLED[CHOOSE]
    printstar()
    print ('Choose is %d'% CHOOSE)
    print ("Choice = %s" % CHOICE)
    printstar()
    disable()

def manualfolderdelete():
    global DELETEFOLDER, error
    print 'running manualfolderdelete()'
    # List disabled addons, so can choose one to enable
    # Display list and get choice
    CHOOSE = xbmcgui.Dialog().select("Choose a folder to delete", ADDONS)
    # if don't select CHOOSE is -1, which selects last item.
    if CHOOSE == -1:
        xbmc.executebuiltin('Notification(No addon, selected)')
        exit()
    CHOICE = ADDONS[CHOOSE]
    printstar()
    print ('Choose is %d'% CHOOSE)
    print ("Choice = %s" % CHOICE)
    printstar()
    DELETEFOLDER = os.path.join(ADDONSPATH, CHOICE)
    if os.path.isdir(DELETEFOLDER):
        removedeletefolder()
    if not user == 'true':
        DELETEFOLDER = os.path.join(DEFAULTADDONSPATH, CHOICE)
        if os.path.isdir(DELETEFOLDER):
            removedeletefolder()
        

# remove a folder recursively
def removedeletefolder():		
    # delete folder
    # DELETEFOLDER = the full path of the folder to be removed
    print 'running DELETEFOLDER'
    print ('DELETEFOLDER is %s'% DELETEFOLDER)
    if os.path.exists(DELETEFOLDER):
        count = 0
        while count < 50:
            try:
                shutil.rmtree(DELETEFOLDER)
            except:
                pass
            if not os.path.exists(DELETEFOLDER):
                count = count + 50
            xbmc.sleep(300)
            count = count + 1
    if os.path.exists(DELETEFOLDER):
        error = ('Problem with removedeletefolder() function in %s.'% thisaddon)
        error2 = ('Could not delete the folder at %s'% DELETEFOLDER)
        printstar()
        errornotification = ('Something went wrong, Could not delete %s'% DELETEFOLDER)
        errormessage()
    else:
        printstar()
        print ('%s has deleted %s'% (thisaddon, DELETEFOLDER))
        printstar()
        xbmc.executebuiltin('Notification(%s, has been deleted)'% DELETEFOLDER)
    xbmc.sleep(300)    
    
    
    
def enableall():
    global SUCCESS, FAIL, CHOICE
    num = len(DISABLED)
    c = 0
    while c < num:
        CHOICE = DISABLED[c]
        enable()
        xbmc.sleep(200)
        c = c + 1
        
def disableall():
    global SUCCESS, FAIL, CHOICE
    num = len(ENABLED)
    c = 0
    while c < num:
        CHOICE = ENABLED[c]
        disable()
        xbmc.sleep(200)
        c = c + 1

def enable():
    global SUCCESS, FAIL
    if not xbmc.getCondVisibility('System.HasAddon(%s)' % CHOICE):
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":true}}' % CHOICE)
        xbmc.sleep(200)
    if not xbmc.getCondVisibility('System.HasAddon(%s)' % CHOICE):
        xbmc.executebuiltin('Notification(Oops, That did nuffin)')
        FAIL.append(CHOICE)
    else:
        xbmc.executebuiltin('Notification(Addon, has been enabled)')
        SUCCESS.append(CHOICE)

def disable():
    global SUCCESS, FAIL
    if xbmc.getCondVisibility('System.HasAddon(%s)' % CHOICE):
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid": "%s","enabled":false}}' % CHOICE)
        xbmc.sleep(200)
    if xbmc.getCondVisibility('System.HasAddon(%s)' % CHOICE):
        xbmc.executebuiltin('Notification(Oops, That did nuffin)')
        FAIL.append(CHOICE)
    else:
        xbmc.executebuiltin('Notification(Addon, has been disabled)')
        SUCCESS.append(CHOICE)

        
startaddon()
getarguments()
# Check current state:
xbmc.executebuiltin( 'UpdateLocalAddons' )
PATH = ADDONSPATH
listaddons()
if not user == 'true':
    PATH = DEFAULTADDONSPATH
    listaddons()
    # sort created folders list alphabetically:
    ADDONS.sort()
checkaddons()
if job == 'enable':
    if len(DISABLED) > 0:
        if all == 'true':
            enableall()
        else:
            chooseaddontoenable()
    else:
        print 'No addon to enable'
        xbmc.executebuiltin('Notification(No installed Addon, needs to be enabled)')
elif job == 'disable':
    if len(ENABLED) > 0:
        if all == 'true':
            disableall()
        else:
            chooseaddontodisable()
    else:
        print 'No addon to disable'
        xbmc.executebuiltin('Notification(No Addon, needs to be disabled)')
elif job == 'deleteaddonfolder':
    manualfolderdelete()
if len(FAIL) > 0:
    xbmc.executebuiltin('Notification(Problem, check log for details)')
    printstar()
    print ('Problem with %s'% thisaddon)
    print ('Not %sd: %s'% (job, FAIL))
    printstar()

exit()


# Drink beer