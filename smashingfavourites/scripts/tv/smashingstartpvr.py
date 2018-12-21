#!/usr/bin/python
# -*- coding: utf-8 -*-
# startpvr.py

######################################################################################################################################################
######################################################################################################################################################
##  Start / stop pvr and change addon data from shortcut or dialog
##  Options
##  -------
##  'pvraddon = xxx' 
##  'pvraddon = choose' - choose pvr group
##  'pvraddon = current' - keep same; if multiple ignore singular flag; assume data is unchanged
##  'disable' - disable all pvr addons
##  'disable = xxx' - disable specific pvr addon
##  'refresh' = refresh the database
##  'cleardb' disable all addons, refresh, swap db for empty one
##  'reset' - cleardb + temp = true + multiple = false
##  'permanent' = enable marker addon; stops automatic disabling by service addon
##  'multiple' - enable multiple simultaneous pvr's
##  'singular' - only 1 enabled, sets multiple to 'false'
##  'temp' = disable marker addon (default!)
##  'group = xxx' / 'group = all' / 'group = choose'
##  'choose' - choose pvraddon; reset; default data (so use 'choose, data = choose' to choose both)
##  'data = xxx' / 'data = current' / data = 'previous' / 'data = default' / 'data = choose' > new data to move in      
##  force = just do it, no prompts
##  quiet = no notifications
##  channels            - jump to
##  guide               - jump to
##  radio               - jump to
##  recordings          - jump to
##  timers              - jump to
##  search              - jump to
##  recordedfiles       - jump to
##  timeshift           - jump to
##  getstatus - show which pvr is / are currently enabled. Also shows data enabled if there is more than 1 option.
##  options - choose what to do from a list
##
##  'settings = xxx'        - open addons/myaddons/pvrthingies and focus on xxx
##                          - alternatively specify pvraddon and just use 'settings'
##                          - or settings with no pvr to choose from all installed
##  'opensettings'          - if 'true' opens them (no, really)
##  'config'                - if 'true' goes straight to the config dialog (direct jump if addon is enabled)- can't disable if use this option
##
##  suggested order of arguments:
##              pvraddon, data, window, group, force / quiet
##              pvraddon, choose
##              choose
##              disable / cleardb / reset / multiple / singular / permanent / temp / getstatus - any of these sets a 'housekeeping' flag
##              options
##  
##              don't mix 1 and 2
##  
######################################################################################################################################################
######################################################################################################################################################

import xbmc
import xbmcgui
import os
import os.path
import sys
import shutil
import json
from time import gmtime, strftime

# define some places
ADDONSFOLDER = os.path.join(xbmc.translatePath('special://home/addons/'))
DEFAULTADDONSFOLDER = os.path.join(xbmc.translatePath('special://xbmc/addons/'))
LOGPATH = xbmc.translatePath('special://logpath')
LOGFILE = os.path.join(LOGPATH, "kodi.log")
# ENABLE = os.path.join(ADDONSFOLDER, "script.me.pvrpermanentenable")
USERDATA = xbmc.translatePath('special://masterprofile')
ADDONDATA = os.path.join(USERDATA, "addon_data")
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
SMASHINGTEMP = os.path.join(USERDATA, "smashing", "smashingtemp")
MULTI = os.path.join(ADDONSFOLDER, "script.me.pvrmultienable")
MISC = os.path.join(SMASHINGFAVOURITES, "miscfiles")
SMASHINGADDONDATA = os.path.join(MISC, "addon_data")
SMASHINGADDONDATAOPTIONS = os.path.join(MISC, "addon_data.options")
markersfolder = os.path.join(SMASHINGTEMP, "markers")
PERMANENT = os.path.join(markersfolder, "pvr.permanentenable.txt")
SMASHINGLOGFOLDER = os.path.join(SMASHINGTEMP, "logfiles")
smashinglog = os.path.join(SMASHINGLOGFOLDER, "smashinglog.log")
smashingoldlog = os.path.join(SMASHINGLOGFOLDER, "smashingoldlog.log")
EMPTYDBFOLDER = os.path.join(MISC, "emptypvrdatabase")


# defaults
activepvr = 'not set'
cleardb = 'not set'
config = 'false'
data = 'not set'            # defaults to current data
dbcleared = 'false'
default = 'false'
disable = 'not set'
disabled = 'false'
endmessage = 'All, done'        # default notification for finish()
error = 'none'       # set default to 'none'; only print if changed
error2 = 'none'
error3 = 'none'
error4 = 'none'
errordialogheader = 'none'
errornotification = 'none'
force = 'false'
forcestop = 'not set'
group = 'not set'               # defaults to choose / 0
groupnumber = 'not set'
home = 'unknown'
housekeeping = 'false'          # cleanup / settings changes
ignorepvr = 'not set'
justvisiting = 'false'
logmessage = 'none'
logmessage2 = 'none'
logmessage3 = 'none'
logmessage4 = 'none'
logmessage5 = 'none'
multiple = 'not set'
opensettings = 'false'
permanent = 'not set'     # can be true, false, all, name of addon (in which case it's additive)
previousdata = 'false'
pvraddon = 'not set'
pvrchecked = 'false'                    # indicates whether getpvrs() has run
pvralreadyrunning = 'not set'           # the requested pvr is already active
quiet = 'false'
refresh = 'not set'
refreshed = 'false'
reset = 'not set'
settings = 'false'
switcheroo = 'false'                     # viewing changes
version = 'unknown'
window = 'not set'             # default to tv channels

def printstar():
    print "****************************************************************************"
    print "***************************************************************************"
    
def getdateandtime():
    global dateandtime
    print 'running getdateandtime()'
    dateandtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

def printlog():
    global logmessage, logmessage2, logmessage3, logmessage4, logmessage5
    print 'running printlog()'
    getdateandtime()
    starter = ('\n%s %s'%(dateandtime, thisaddon))
    starter = (starter+"                                        ")[:55] # this adds 40 spaces to starter but cuts the max length to 55 characters
    message = ('%s %s'%(starter, logmessage))
    with open(smashinglog, "a") as myfile:
        myfile.write(message)
    if not logmessage2 == 'none':
        message = ('%s %s'%(starter, logmessage2))    
        with open(smashinglog, "a") as myfile:
            myfile.write(message)
        logmessage2 = 'none'
        if not logmessage3 == 'none':
            message = ('%s %s'%(starter, logmessage3))    
            with open(smashinglog, "a") as myfile:
                myfile.write(message)
            logmessage3 = 'none'
            if not logmessage4 == 'none':
                message = ('%s %s'%(starter, logmessage4))    
                with open(smashinglog, "a") as myfile:
                    myfile.write(message)
                logmessage4 = 'none'
                if not logmessage5 == 'none':
                    message = ('%s %s'%(starter, logmessage5))    
                    with open(smashinglog, "a") as myfile:
                        myfile.write(message)
                    logmessage5 = 'none'

# errors
def errormessage():
    global error, error2, error3, error4, errornotification, logmessage, logmessage2, logmessage3, logmessage4, logmessage5
    print 'running errormessage()'
    printstar()
    logmessage = ('%s has stopped with an error'% thisaddon)
    print logmessage
    try:
        if not error == 'none':
            logmessage2 = error
            print error
    except:
        pass
    try:
        if not error2 == 'none':
            logmessage3 = error2
            print error2
    except:
        pass
    try:
        if not error3 == 'none':
            logmessage4 = error3
            print error3
    except:
        pass
    try:
        if not error3 == 'none':
            logmessage5 = error4
            print error3
    except:
        pass
    printlog()
    xbmc.executebuiltin('Notification(Problem - check log for details, %s)'% thisaddon)

    try:
        if not errornotification == 'none':
            xbmc.sleep(3000)
            xbmc.executebuiltin('Notification(errornotification)')
    except:
        pass
    try:
        if not errordialogheader == 'none':
            xbmc.sleep(3000)
            xbmcgui.Dialog().ok(errordialogheader, *errordialoglist)    # need * to use with list or errors out
    except:
        pass
    printstar()
    exit() 

def checkfolders():
    global error, error2
    print 'running checkfolders()'
    # check folder structure is in place - make if necessary
    foldersmade = []
    folderstocheck = []
    folderstocheck.append(SMASHINGTEMP)
    folderstocheck.append(SMASHINGLOGFOLDER)
    folderstocheck.append(markersfolder)
    num = len(folderstocheck)
    c = 0
    while c < num:
        check = folderstocheck[c]
        if not os.path.isdir(check):
            os.mkdir(check)
            xbmc.sleep(300)
            if not os.path.isdir(check):
                error = 'Problem in checkfolders()'
                error2 = ('Could not make %s folder'% check)
                errormessage()
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
	
def startaddon():
    global thisaddon, version, OLDTVDB, NEWTVDB, error, error2
    thisaddon = sys.argv[0]
    checkfolders()
    # get kodi version:
    json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["version", "name"]}, "id": 1 }')
    json_query = unicode(json_query, 'utf-8', errors='ignore')
    # response is eg >> json_query is {"id":1,"jsonrpc":"2.0","result":{"name":"Kodi","version":{"major":17,"minor":4,"revision":"20170717-b22184d","tag":"releasecandidate","tagversion":"1"}}}
    start = 'major":'
    finish = ',"minor'
    version = (json_query.split(start))[1].split(finish)[0]
    version = int(version)
    if version == 17:
        OLDTVDB = os.path.join(USERDATA, "Database", "TV29.db")
        NEWTVDB = os.path.join(EMPTYDBFOLDER, "TV29.db")
    elif version == 18:
        OLDTVDB = os.path.join(USERDATA, "Database", "TV31.db")
        NEWTVDB = os.path.join(EMPTYDBFOLDER, "TV31.db")
    elif version == 16:
        OLDTVDB = os.path.join(USERDATA, "Database", "TV29.db")
        NEWTVDB = os.path.join(EMPTYDBFOLDER, "TV29.db")
    else:
        error = 'Problem in startaddon()'
        error2 = ('NEWTVDB not identified because no setting for version %d.'% version)
        errormessage()
    printstar()
    print ('%s has started'% thisaddon)
    print ('kodi version is %d'% version)
    printstar()
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)
	
def checkpvrnotplaying():
    if (xbmc.getCondVisibility("Player.Playing")):
        xbmc.executebuiltin('Notification(Stop playback, before making changes)')
        exit()
    elif (xbmc.getCondVisibility("Player.HasMedia")):
        xbmc.executebuiltin('Notification(Close player, before making changes)')
        exit()
    elif (xbmc.getCondVisibility("Pvr.IsPlayingTv")):
        xbmc.executebuiltin('Notification(Stop playback, before making changes)')		
        exit()
    elif (xbmc.getCondVisibility("Pvr.IsPlayingRadio")):
        xbmc.executebuiltin('Notification(Stop playback, before making changes)')		
        exit()
    elif (xbmc.getCondVisibility("Pvr.IsPlayingRecording")):
        xbmc.executebuiltin('Notification(Stop playback, before making changes)')		
        exit()

def gohome():
    global home, error
    # check if in home window
    window = xbmcgui.getCurrentWindowId()
    if not window == 10000:
        # add 'back' because Home doesn't work if in groups dialog
        xbmc.executebuiltin( "XBMC.Action(Back)" )
        xbmc.executebuiltin("ActivateWindow(Home)")
        xbmc.sleep(300)
        window = xbmcgui.getCurrentWindowId()        
        if not window == 10000:
            error = 'Problem in gohome()'
            errormessage()
    home = 'true'
        
def getarguments():
#    global pvraddon, window, channels, guide, disable, refresh, cleardb, reset, permanent, temp, group, data, force, quiet, groupnumber, error, error2
    global pvraddon, window, disable, refresh, cleardb, reset, permanent, group, data, multiple, force, quiet, groupnumber, error, error2, arglist, housekeeping, switcheroo, settings, opensettings, config
    print 'running getarguments()'
    number = len(sys.argv)
    arglist = []
    c = 1
    while c < number:
        arg = sys.argv[c]
        print ('arg is %s'% arg)
        if arg[:11] == 'pvraddon = ':
            switcheroo = 'true'
            pvraddon = arg[11:0]        # ie argument is 'pvraddon = xyz', addon (script variable) is 'xyz'
            if not pvraddon[:4] == 'pvr.':
                if pvraddon == 'choose':
                    pvraddon = 'choose'
                elif pvraddon == 'current':
                    pvraddon = 'current'
                else:
                    pvraddon = 'pvr.' + pvraddon
            next = ('pvraddon = %s'% pvraddon)
            arglist.append(next)
            if pvrchecked == 'false':
                getpvrs()                       # generates "pvralreadyrunning = 'true'" (if it is!)
        elif arg[:4] == 'pvr.':
            switcheroo = 'true'
            pvraddon = arg
            next = ('pvraddon = %s'% pvraddon)
            arglist.append(next)
            if pvrchecked == 'false':
                getpvrs()
        elif arg == 'settings':
            if pvraddon[:4] == 'pvr.':
                settings = pvraddon
            else:
                settings = 'none'
        elif arg[:11] == 'settings = ':
            settings = arg[11:]
            if not settings[:4] == 'pvr.':
                settings = 'none'
        elif arg == 'opensettings':
            opensettings = 'true'
        elif arg == 'config':
            config = 'true'
        elif arg == 'choose':
            switcheroo = 'true'
            if pvraddon == 'not set':
                pvraddon = 'choose'
                next = ('pvraddon = %s'% pvraddon)
                arglist.append(next)
            if data == 'not set':
                data = 'choose'
                next = ('data = %s'% data)
                arglist.append(next)
            if group == 'not set':
                group = 'choose'
                next = ('group = %s'% group)
                arglist.append(next)
            if window == 'not set':
                window = 'choose'
                next = ('window = %s'% window)
                arglist.append(next)
#            refresh = 'true'
#            cleardb = 'true'
#            reset = 'true'
#            temp = 'true'
#            permanent = 'false'
#            multiple = 'false'
        elif arg == 'getstatus':
            getcurrentdata()
        elif arg == 'options':
            chooseoptions()
        elif arg[:9] == 'window = ':
            switcheroo = 'true'
            window = arg[9:]
            if number == 2:
                openwindow()
            next = ('window = %s'% window)
            arglist.append(next)
        elif arg == 'channels':
            switcheroo = 'true'
            window = 'channels'
            if number == 2:
                quiet = 'true'
                simpletvchannels()
            elif number == 3:
                if group == 'choose':
                    groupnumber = 0
                    opengroups()
            next = ('window = %s'% window)
            arglist.append(next)
        elif arg == 'guide':
            switcheroo = 'true'
            window = 'guide'
            if number == 2:
                quiet = 'true'
                simpletvguide()
            elif number == 3:
                if group == 'choose':
                    groupnumber = 0
                    opengroups()
            next = ('window = %s'% window)
            arglist.append(next)
        elif arg == 'radio':
            switcheroo = 'true'
            window = 'radio'
            if number == 2:
                quiet = 'true'
                radio()
            next = ('window = %s'% window)
            arglist.append(next)
        elif arg == 'recordings':
            switcheroo = 'true'
            window = 'recordings'
            if number == 2:
                quiet = 'true'
                recordings()
            next = ('window = %s'% window)
            arglist.append(next)
        elif arg == 'timers':
            switcheroo = 'true'
            window = 'timers'
            if number == 2:
                quiet = 'true'
                timers()
            next = ('window = %s'% window)
            arglist.append(next)
        elif arg == 'search':
            switcheroo = 'true'
            window = 'search'
            if number == 2:
                quiet = 'true'
                search()
            next = ('window = %s'% window)
            arglist.append(next)
        elif arg == 'recordedfiles':
            switcheroo = 'true'
            window = 'recordedfiles'
            if number == 2:
                quiet = 'true'
                recordedfiles()
            next = ('window = %s'% window)
            arglist.append(next)
        elif arg == 'timeshift':
            switcheroo = 'true'
            window = 'timeshift'
            if number == 2:
                quiet = 'true'
                timeshift()
            next = ('window = %s'% window)
            arglist.append(next)
        elif arg == 'disable':
            housekeeping = 'true'
            if not disable == 'true':
                disable = 'true'
                next = ('disable = %s'% disable)
                arglist.append(next)
        elif arg[:10] == 'disable = ':
            housekeeping = 'true'
            disable = arg[10:]
            if disable == 'all':
                disable = 'true'
            elif not disable[:4] == 'pvr.':
                disable = 'pvr.' + disable
                next = ('disable = %s'% disable)
                arglist.append(next)
        elif arg == 'refresh':
            housekeeping = 'true'
            if not refresh == 'true':
                refresh = 'true'
                next = ('refresh = %s'% refresh)
                arglist.append(next)
        elif arg == 'cleardb':
            housekeeping = 'true'
            if not cleardb == 'true':
                cleardb = 'true'
                next = ('cleardb = %s'% cleardb)
                arglist.append(next)
        elif arg == 'reset':
            housekeeping = 'true'
            if not reset == 'true':
                reset = 'true'
                next = ('reset = %s'% reset)
                arglist.append(next)
        elif arg == 'temp':
            housekeeping = 'true'
            if not permanent == 'false':
                permanent = 'false'
                next = ('permanent = %s'% permanent)
                arglist.append(next)
        elif arg == 'permanent':
            housekeeping = 'true'
            if not permanent == 'true':
                permanent = 'true'
                next = ('permanent = %s'% permanent)
                arglist.append(next)
        elif arg == 'multiple':
            housekeeping = 'true'
            if not multiple == 'true':
                multiple = 'true'
                next = ('multiple = %s'% multiple)
                arglist.append(next)
        elif arg == 'singular':
            housekeeping = 'true'
            if not multiple == 'false':
                multiple = 'false'
                next = ('multiple = %s'% multiple)
                arglist.append(next)
        elif arg[:8] == 'group = ':
            switcheroo = 'true'
            group = arg[8:]
            next = ('group = %s'% group)
            arglist.append(next)
        elif arg[:7] == 'data = ':
            switcheroo = 'true'
            data = arg[7:]
            next = ('data = %s'% data)
            arglist.append(next)
        elif arg == 'default':
            switcheroo = 'true'
            if not data == 'default':
                data = 'default'
                next = ('data = %s'% data)
                arglist.append(next)
        elif arg == 'force':
            force = 'true'
            next = ('force = %s'% force)
            arglist.append(next)
        elif arg == 'forcestop':
            housekeeping = 'true'
            forcestop == 'true'
            next = ('forcestop = %s'% forcestop)
            arglist.append(next)
        elif arg == 'quiet':
            quiet = 'true'
            next = ('quiet = %s'% quiet)
            arglist.append(next)
        else:
            error = 'Problem in getarguments()'
            error2 = ('Invalid argument can not be processed: %s'% arg)
            errormessage()
        c = c + 1

def logarguments():
    print 'running logarguments()'
    number = len(sys.argv)
    print '%d arguments received:'% number
    c = 1
    while c < number:
        arg = sys.argv[c]
        print arg
        c = c + 1
    print ('housekeeping = %s'% housekeeping)
    print ('switcheroo = %s'% switcheroo)
    if not settings == 'false':
        getsettings()
    if housekeeping == 'true':
        dohousekeeping()
    if switcheroo == 'true':
        doswitcheroo()

def getsettings():
    global error, error2, errornotification
    print 'running getsettings()'
    pvrid = 'none'
    if settings[:4] == 'pvr.':
        pvrid = settings
    if not pvrid == 'none':
        if xbmc.getCondVisibility('System.HasAddon(%s)' % pvrid):
            if configure == 'true':
                xbmc.executebuiltin('Addon.OpenSettings(%s)'% pvrid)
                finish()
    # else do it the hard way
    xbmc.executebuiltin('ActivateWindow(AddonBrowser,"addons://user/xbmc.pvrclient",return)')
    if pvrid == 'none':
        finish()
    # process arguments
    pvrname = xbmc.getInfoLabel('System.AddonTitle(%s)'% pvrid)
    numitems = xbmc.getInfoLabel('Container.NumItems')
    if numitems == "":
        d = 0
        while d < 5:
            xbmc.sleep(300)
            numitems = xbmc.getInfoLabel('Container.NumItems')
            if not numitems == "":
                d = 1000
            else:
                d = d + 1
        if d < 1000:
            error = 'Problem in getsettings()'
            error2 = 'could not find numitems'
            errornotification = 'Problem getting settings, see log for details'
            errormessage()        
    numitems = int(numitems)
    offset = 0
    c = 0
    size = numitems + 1
    while c < size:
        print ('c = %d'% c)
        check = xbmc.getInfoLabel('Container.ListItem(%d).Label'% c)
        print ('check = %s'% check)
        if pvrname in check:
            offset = c
            print ('offset = %s'% offset)
            c = 1000
        c = c + 1
    if c > 999:
        print ('offset is %d'% offset)
    else:
        error = 'Problem in getsettings()'
        error2 = ('could not find offset for'% pvrname)
        errornotification = 'Problem getting settings, see log for details'
        errormessage()
    c = 0
    while c < offset:
        xbmc.executebuiltin("XBMC.Action(Down)")
        c = c + 1
    if opensettings == 'true':
        xbmc.executebuiltin( "XBMC.Action(Select)" )
        if config == 'true':
            xbmc.executebuiltin( "XBMC.Action(FirstPage)" )
            xbmc.executebuiltin( "XBMC.Action(Select)" )        
    print 'leaving getsettings()'
    finish()
    
def dohousekeeping():
    global stopaddon
    print 'running dohousekeeping()'
    if disable == 'true':
        if not disabled == 'true':
            stoppvr()    
    elif disable [:4] == 'pvr.':
        stopaddon = disable
        stoponepvr()
    if refresh == 'true':
        if not refreshed == 'true':
            refreshdb()
    if cleardb == 'true':
        if not disabled == 'true':
            stoppvr()
        if not refreshed == 'true':
            refreshdb()
        if not dbcleared == 'true':
            replacedatabase()
    if reset == 'true':
        if not disabled == 'true':
            stoppvr()
        if not refreshed == 'true':
            refreshdb()
        if not dbcleared == 'true':
            replacedatabase()
        permanentdisable()
        multidisable()
    if permanent == 'false':
        permanentdisable()    
    if permanent == 'true':
        permanentenable()    
    if multiple == 'true':
        multienable()
    if multiple == 'false':
        multidisable()
    
def stoppvr():
    global ignorepvr, activepvrs, activepvrnumber, disabled, quiet, error, error2
    print 'running stoppvr()'
    if not home == 'true':
        gohome()
    if xbmc.getCondVisibility('System.HasPVRAddon'):
        # go through list of enabled pvr's, disable one-by-one:
        if activepvr == 'not set':                  # ie if haven't yet run getpvrs()
            getpvrs()
        c = 0
        while c < activepvrnumber:
            checkpvr = activepvrs[c]
            print ('checking for %s'% checkpvr)
            if xbmc.getCondVisibility('System.HasAddon(%s)'% checkpvr):
                if not checkpvr == ignorepvr:
                    checkreadytostop()
                    print ('stopping %s'% checkpvr)
                    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":false}}'% checkpvr)            
                    xbmc.sleep(1000)
                else:
                    print ('Ignoring %s as it should not be disabled'% checkpvr)
            c = c + 1
        if not quiet == 'true':
            if not xbmc.getCondVisibility('System.HasPVRAddon'):
                xbmc.executebuiltin('Notification(Live TV, has been disabled)')
                print 'All pvr addons disabled'
                disabled = 'true'                
    else:
        print 'No pvr addons were enabled'
        if not quiet == 'true':
            xbmc.executebuiltin('Notification(Live TV, was not enabled)')
        disabled = 'true'

def getpvrs():
    global disabled, pvrs, pvrnumber, activepvrs, activepvrnumber, activepvr, activepvr2, activepvr3, multiple, pvralreadyrunning, error
    print 'running getpvrs()'
    # get list of potentially active pvr's - ones that have folders in addon_data
    check = []
    pvrs = []
    activepvrs = []
    # set defaults
    activepvr = 'none'
    activepvr2 = 'none'
    activepvr3 = 'none'
    if not xbmc.getCondVisibility('System.HasPVRAddon'):
        disabled = 'true'
        print 'disabled = \'true\''
    check = os.listdir(ADDONDATA)
#    print ('check = %s'% check)
    num = len(check)
#    print ('num = %d'% num)
    c = 0
    while c < num:
        next = check[c]
#        print ('next = %s'% next)
        if next[:4] == 'pvr.':
            if 'previous' not in next:
                pvrs.append(next)
#                print ('next(%s) was appended to pvrs list'% next)
                if not disabled == 'true':
                    if xbmc.getCondVisibility('System.HasAddon(%s)'% next):
#                        print ('next(%s) was appended to activepvrs list'% next)
                        activepvrs.append(next)
                        if pvraddon == next:
                            pvralreadyrunning == 'true'
        c = c + 1
    pvrnumber = len(pvrs)
    activepvrnumber = len(activepvrs)
    print ('pvrs list is %s'% pvrs)
    print ('activepvrs list is %s'% activepvrs)
#    print ('pvrnumber is %d'% pvrnumber)
#    print ('activepvrnumber is %d'% activepvrnumber)
    if pvrnumber == 0:
        xbmc.executebuiltin('Notification(No potentially active, pvr addons found)')
        error = 'No potentially active pvr addons found - none have folders in addon_data.'
        errormessage()
    if activepvrnumber >= 1:
       activepvr = activepvrs[0]
       print ('activepvr is %s'% activepvr)
    if activepvrnumber >= 2:
#        activepvr = 'multiple'
        multiple = 'true'
        activepvr2 = activepvrs[1]
        print ('activepvr2 is %s'% activepvr2)
    if activepvrnumber == 3:
        activepvr3 = activepvrs[2]
        print ('activepvr3 is %s'% activepvr3)
       
def getcurrentdata():
    global endmessage, justvisiting, currentsettings, activepvrdata, activepvrdata2, activepvrdata3, activepvrdatalist
    print 'running getcurrentdata()'
    if activepvr == 'not set':              # ie haven't already run it - or it would be 'none or an addon id
        getpvrs()
    currentsettings = []
    activepvrdatalist = []
    # defaults
    activepvrdata = 'usual'
    activepvrdata2 = 'usual'
    activepvrdata3 = 'usual'
    c = 0
    while c < activepvrnumber:
        checkaddon = activepvrs[c]
        currentdata = 'usual'
        checkfile = os.path.join(ADDONDATA, checkaddon, "version.txt")
        if os.path.isfile(checkfile):
#            currentdata = 'usual'
            f = open(checkfile, "r")
            currentdata = f.read()
            currentdata = currentdata.strip()
        activepvrdatalist.append(currentdata)
        print ('currentdata for %s is %s'% (checkaddon, currentdata))                  # currentdata is 'usual' by default
        if not currentdata == 'usual':
            pvrsettings = ('%s enabled with %s data'% (checkaddon, currentdata))
        else:
            pvrsettings = ('%s enabled'% checkaddon)
#        pvrsettings = ('%s enabled with %s data'% (checkaddon, currentdata))
        currentsettings.append(pvrsettings)
        c = c + 1
    num = len(currentsettings)                  # should be same as activepvrnumber
    if num == 0:
        add = 'No pvr addons are currently enabled'
        currentsettings.append(add)
    if num >= 1:
        activepvrdata = activepvrdatalist[0]
    if num >= 2:
        activepvrdata2 = activepvrdatalist[1]
    if num == 3:
        activepvrdata3 = activepvrdatalist[2]
    if justvisiting == 'false':                 # ie running from getarguments()
        # get status of permanent, multi
        if os.path.isfile(PERMANENT):
            perm = 'Addons have permanent status - they will not time -out.'
        else:
            perm = 'Addons have temporary status - they will time -out.'
        currentsettings.append(perm)
        if os.path.isfile(MULTI):
            mult = 'Multiple status active'
        else:
            mult = 'Multiple status not active'
        currentsettings.append(mult)        
        end = 'Hit anything to close the script'
        currentsettings.append(end)
        CHOOSE = xbmcgui.Dialog().select("Current settings", currentsettings)
        finish()
    else:
        justvisiting = 'false'                  # and back from whence we came
    
def stoponepvr():
    global error, error2
    print 'running stoponepvr()'
    if not home == 'true':
        gohome()
    print ('Stopping %s'% stopaddon)
    if xbmc.getCondVisibility('System.HasAddon(%s)'% stopaddon):
        checkreadytostop()
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":false}}'% stopaddon)
        xbmc.sleep(1000)
    if xbmc.getCondVisibility('System.HasAddon(%s)'% stopaddon):
        error = 'Problem in stoponepvr()'
        error2 = ('%s was not disabled.'% stopaddon)
        errormessage() 
    else:
        print ('%s disabled'% stopaddon)
        if not quiet == 'true':
            xbmc.executebuiltin('Notification(%s, has been disabled)'% stopaddon)
            
def checkreadytostop():
    print 'running checkreadytostop()'
    # check the pvr info box isn't showing - if it is, wait!
    if xbmc.getCondVisibility('System.HasPVRAddon'):
#        xbmc.executebuiltin("ActivateWindow(Home)")   
        v = 0
        while v < 120:                                                              # ie 2 minutes
            pvrloading = xbmc.getCondVisibility('Window.IsVisible(10151)')          # extendeddialoginfo
            if pvrloading == 0:                                                     # ie dialog not visible
                xbmc.executebuiltin('Notification(Stopping, now)')
                xbmc.sleep(5000)                                                    # wait 5 sec
                pvrloadingcheck = xbmc.getCondVisibility('Window.IsVisible(10151)')
                if pvrloadingcheck == 0:                                            # and check again
                    v = 1000
                else:
                    xbmc.executebuiltin('Notification(False alarm, waiting to stop safely)')
                    v = v + 1
            else:
                xbmc.sleep(1000)
                xbmc.executebuiltin('Notification(Hang on a tick, waiting to stop safely)')
                v = v + 1
        if v < 1000:
            xbmc.executebuiltin('Notification(Not safe to stop pvr, try again)')
            exit()
            
def refreshdb():
    global refreshed
    print 'running refreshdb()'
    # refresh the pvr database	
    xbmc.executebuiltin("ActivateWindow(10021)")
    xbmc.executebuiltin("UnloadSkin()")
    xbmc.executebuiltin("SetFocus(-70)")
    xbmc.executebuiltin( "XBMC.Action(Select)" )
    xbmc.executebuiltin('SendClick(11)')
    xbmc.executebuiltin("ActivateWindow(Home)")
    xbmc.executebuiltin("ReloadSkin()")
    refreshed = 'true'
    home = 'true'
    if not quiet == 'true':
        xbmc.executebuiltin('Notification(Live TV, has been refreshed)')
        
def replacedatabase():
    global error
    # delete the old database
    c = 0
    while c < 50:
        try:
            os.remove(OLDTVDB)
            xbmc.sleep(300)
        except:
            pass
        if not os.path.isfile(OLDTVDB):    
            c = 1000
        else:
            if not quiet == 'true':
                xbmc.executebuiltin('Notification(TV database, refreshing)')
            xbmc.sleep(1000)
            c = c + 1
    if c < 1000:
        error = ('Could not delete OLDTVDB(%s)'% OLDTVDB)
        errormessage()
    # and move in a new empty one
    c = 0
    while c < 50:
        try:
            shutil.copyfile(NEWTVDB, OLDTVDB)
            xbmc.sleep(300)
        except:
            pass
        if os.path.isfile(OLDTVDB):
            if not quiet == 'true':
                xbmc.executebuiltin('Notification(TV database, refreshed)')
            c = 1000
        else:
            if not quiet == 'true':
                xbmc.executebuiltin('Notification(TV database, refreshing)')
            xbmc.sleep(1000)
            c = c + 1
    if c < 1000:
        error = ('Could not copy NEWTVDB (%s) into the Database folder'% NEWTVDB)
        errormessage()

# Check if PERMANENT file (smashing/miscfiles/markers/pvr.permanentenable.txt) exists.  If not make it.
def permanentenable():
    global error
    print 'running permanentenable()'
    if not os.path.isfile(PERMANENT):
        open(PERMANENT,"w").close()
        xbmc.sleep(300)
        if os.path.isfile(PERMANENT):
            if not quiet == 'true':
                xbmc.executebuiltin('Notification(Permanent, marker set)')
        else:
            error = ('PERMANENT marker(%s) not created'% PERMANENT)
            errormessage()
                
def permanentdisable():
    print 'running permanentdisable()'
    if os.path.isfile(PERMANENT):
        os.remove(PERMANENT)
        xbmc.sleep(300)
        if not os.path.isfile(PERMANENT):
            if not quiet == 'true':
                xbmc.executebuiltin('Notification(Permanent, marker removed)')
        else:
            error = ('PERMANENT marker(%s) not removed'% PERMANENT)
            errormessage()

# Check if MULTI file (smashing/miscfiles/markers/pvr.multienable.txt) exists.  If not make it.
def multienable():
    global error
    print 'running multienable()'
    if not os.path.isfile(MULTI):
        open(MULTI,"w").close()
        xbmc.sleep(300)
        if os.path.isfile(MULTI):
            if not quiet == 'true':
                xbmc.executebuiltin('Notification(Multiple pvr, marker set)')
        else:
            error = ('MULTI marker(%s) not created'% MULTI)
            errormessage()
                
def multidisable():
    print 'running multidisable()'
    if os.path.isfile(MULTI):
        os.remove(MULTI)
        xbmc.sleep(300)
        if not os.path.isfile(MULTI):
            if not quiet == 'true':
                xbmc.executebuiltin('Notification(Multiple pvr, marker removed)')
        else:
            error = ('MULTI marker(%s) not removed'% MULTI)
            errormessage()
        
def doswitcheroo():
    global ignorepvr, stopaddon, pvraddon, dataoptionsfolder, defaultfile, addondatasub, oldaddon, previousdatasub, tempaddon, tempdatasub, data
    print 'running doswitcheroo()'
    if activepvr == 'not set':
        getpvrs()
    # Make sure we know what pvraddon is!
    if pvraddon == 'choose':
        justvisiting = 'true'
        getcurrentdata()
        choosepvr()
    if pvraddon == 'not set':
        pvraddon = 'current'
    if pvraddon == 'current':
        if not xbmc.getCondVisibility('System.HasPVRAddon'):
            error = 'No pvr addon was active so could not set pvr == current'
            errormessage()
        if activepvrnumber == 1:            # ie only one enabled
            pvraddon = activepvr
        else:
            print 'pvr set to current but more than one pvr enabled.  Guess we\'ll muddle through'
    # knowing pvraddon we can set some more paths:
    if pvraddon == 'current':
        data = 'current'        # have to assume that
    else:
        dataoptionsfolder = os.path.join(SMASHINGADDONDATAOPTIONS, pvraddon)
        defaultfile = os.path.join(dataoptionsfolder, "default.txt")
        addondatasub = os.path.join(ADDONDATA, pvraddon)
        oldaddon = pvraddon + '.previous settings'
        previousdatasub = os.path.join(ADDONDATA, oldaddon)
        tempaddon = pvraddon + '.temp'
        tempdatasub = os.path.join(ADDONDATA, tempaddon)
        processdatafiles() 
        print ('data = %s'% data)
        if data == 'choose':
            getdataoptions()
    # assume data = 'not set = 'current':
    if data == 'not set':
        data = 'current'
    # Check if need to switch data - 1) is there a folder 2) is data specified 3) does it match? - close addon if necessary
    if not data == 'current':
        if xbmc.getCondVisibility('System.HasAddon(%s)'% pvraddon):
            stopaddon = pvraddon
            stoponepvr()
            if not xbmc.getCondVisibility('System.HasPVRAddon'):    # ie all closed, might as well clean up
                refreshdb()
                replacedatabase()
        checkdata()
    # Check if multiple == 'false' and multiples (or another addon) enabled
    if multiple == 'false':
        if xbmc.getCondVisibility('System.HasPVRAddon'):
            if not pvraddon == 'current':
                ignorepvr = pvraddon
                stoppvr()
                if not xbmc.getCondVisibility('System.HasPVRAddon'):    # ie all closed, might as well clean up
                    refreshdb()
                    replacedatabase()            
    # Check if need to open an addon
    if pvraddon == 'current':
        if not xbmc.getCondVisibility('System.HasPVRAddon'):
            error = 'No pvr addon was active so could not set pvr == current'
            errormessage() 
    else:
        # start that sucker
        startpvr()
        wait()
    # now deal with windows, groups
    openwindow()
    
    
def choosepvr():
    global pvraddon, justvisiting, currentsettings, activepvrdata, activepvrdata2, activepvrdata3, stopaddon, endmessage, error
    print 'running choosepvr()'
    print ('activepvrdata = %s'% activepvrdata)
    print ('activepvrdata2 = %s'% activepvrdata2)
    print ('activepvrdata3 = %s'% activepvrdata3)
    # List current settings, give options to quit, keep current and change other, change current, add new
    next = 'Select any option to continue'
    currentsettings.append(next)
    CHOOSE = xbmcgui.Dialog().select("Current settings are:", currentsettings)
    if CHOOSE == -1:
        endmessage = 'Action, cancelled'
        finish()
    if activepvrnumber > 0:
        options = []
        # set default values
        one = 'Keep current settings'
        two = ('Close %s'% activepvr)
        three = ('Close %s and open a new pvr addon'% activepvr)
        four = 'not set'
        five = 'not set'
        six = 'not set'
        seven = 'not set'
        eight = 'not set'
        nine = 'not set'
        ten = 'not set'
        eleven = 'not set'
        twelve = 'cancel operation'
        if not activepvrdata == 'usual':
            four = ('Close %s and choose new data'% activepvr)
        if activepvrnumber < 3:
            eleven = 'Open another pvr addon'
        if activepvrnumber >1:
            five = ('Close %s'% activepvr2)
            six = ('Close %s and open a new pvr addon'% activepvr2)
            if not activepvrdata2 == 'usual':
                seven = ('Close %s and choose new data'% activepvr2)
        if activepvrnumber ==3:
            eight = ('Close %s'% activepvr3)
            nine = ('Close %s and open a new pvr addon'% activepvr3)
            if not activepvrdata3 == 'usual':
                ten = ('Close %s and choose new data'% activepvr3)                
        options.append(one)
        options.append(two)
        options.append(three)
        if not four == 'not set':
            options.append(four)
        if not five == 'not set':
            options.append(five)
        if not six == 'not set':
            options.append(six)
        if not seven == 'not set':
            options.append(seven)
        if not eight == 'not set':
            options.append(eight)
        if not nine == 'not set':
            options.append(nine)
        if not ten == 'not set':
            options.append(ten)
        if not eleven == 'not set':
            options.append(eleven)
        options.append(twelve)
        CHOOSE = xbmcgui.Dialog().select("Options", options)
        CHOICE = options[CHOOSE]
        if CHOOSE == -1:
            endmessage = 'Action, cancelled'
            finish()
        elif CHOICE == twelve:
            endmessage = 'Action, cancelled'
            finish()
        elif CHOICE == one:
            endmessage = 'Current settings, retained'
            finish()
        elif CHOICE == two:
            stopaddon = activepvr
            stoponepvr()
            finish()
        elif CHOICE == three:
            stopaddon = activepvr
            stoponepvr()
        elif CHOICE == four:
            stopaddon = activepvr
            pvraddon = activepvr
            stoponepvr()
            choosedata()
            # choose group / channels / whatever / don't forget refresh etc
        elif CHOICE == five:
            stopaddon = activepvr2
            stoponepvr()
            finish()
        elif CHOICE == eight:
            stopaddon = activepvr3
            stoponepvr()
            finish()
        print ('CHOICE is %s'% CHOICE)
        endmessage = 'Woo, hoo'
        finish()
    # list possibles from addondata, smashingaddondata, smashingaddondataoptions
    check = []
    pvrchoice = []
    check = os.listdir(ADDONDATA)
    num = len(check)
    c = 0
    while c < num:
        next = check[c]
        if next[:4] == 'pvr.':
            if 'previous' not in next:
                pvrchoice.append(next)
        c = c + 1
    check = []
    check = os.listdir(SMASHINGADDONDATA)
    num = len(check)
    c = 0
    while c < num:
        next = check[c]
        if next[:4] == 'pvr.':
            if next not in pvrchoice:
                pvrchoice.append(next)
        c = c + 1
    check = []
    check = os.listdir(SMASHINGADDONDATAOPTIONS)
    num = len(check)
    c = 0
    while c < num:
        next = check[c]
        if next[:4] == 'pvr.':
            if next not in pvrchoice:
                pvrchoice.append(next)
        c = c + 1
    num = len(pvrchoice)
    add = 'There are no valid pvr addons to choose from'
    if num == 0:
        pvrchoice.append(add)
    cancel = 'Cancel operation'
    pvrchoice.append(cancel)
    # Choose
    CHOOSE = xbmcgui.Dialog().select("Choose pvr addon", pvrchoice)
    CHOICE = pvrchoice[CHOOSE]
    if CHOOSE == -1:
        endmessage = 'Action, cancelled'    
        finish()
    elif CHOICE == add:
        endmessage = 'Action, cancelled'    
        finish()
    elif CHOICE == cancel:
        endmessage = 'Action, cancelled'    
        finish()
    else:
        pvraddon = CHOICE
 
def processdatafiles():
    global data, currentdataversion, previousdataversion, defaultdataversion
    print 'running processdatafiles()'
    # set defaults
    currentdataversion = 'none'
    previousdataversion = 'none'
    defaultdataversion = 'none'    
    currentdataversionfile = os.path.join(addondatasub, "version.txt")
    previousdataversionfile = os.path.join(previousdatasub, "version.txt")    
    if os.path.exists(currentdataversionfile):
        f = open(currentdataversionfile, "r")
        currentdataversion = f.read()
        currentdataversion = currentdataversion.strip()
        if data == currentdataversion:
            data = 'current'
            print 'data set to current'            
    print ('currentdataversion is %s'% currentdataversion)                  # currentdataversion is 'none' if not read here    
    if os.path.exists(previousdataversionfile):
        f = open(previousdataversionfile, "r")
        previousdataversion = f.read()
        previousdataversion = previousdataversion.strip()
    print ('previousdataversion is %s'% previousdataversion)                  # previousdataversion is 'none' if not read here
    if os.path.exists(defaultfile):
        f = open(defaultfile, "r")
        defaultdataversion = f.read()
        defaultdataversion = defaultdataversion.strip()
    print ('defaultdataversion is %s'% defaultdataversion)          # defaultdataversion is 'none' if not read here   

def getdataoptions():
    global pvraddon, data, previousdatasub, previousdata, backup, error, error2, currentdataversion, previousdataversion, defaultdataversion
    print 'running getdataoptions()'
    # list current state before proceeding: ie currentdataversion, previousdataversion, defaultdataversion
    dialoglist = []
    a = ('Current version is %s'% currentdataversion)
    b = ('Previous version is %s'% previousdataversion)
    c = ('Default version is %s'% defaultdataversion)
    dialoglist.append(a)
    dialoglist.append(b)
    dialoglist.append(c)
    xbmcgui.Dialog().ok(pvraddon, *dialoglist)    # need * to use with list or errors out
   
    previous = 'false'
    removebackup = 'false'
    # list alternatives (if any)
#    dataoptionsfolder = os.path.join(SMASHINGADDONDATAOPTIONS, addon)
    # check folder exists - if not create it:
    if not os.path.isdir(dataoptionsfolder):
        os.mkdir(dataoptionsfolder)
    # list subfolders - exclude any files
    datafoldercontents = []
    dataoptions = []
    datafoldercontents = os.listdir(dataoptionsfolder)
    num = len(datafoldercontents)
    c = 0
    while c < num:
        check = datafoldercontents[c]
        trypath = os.path.join(dataoptionsfolder, check)
        if os.path.isdir(trypath):
            dataoptions.append(check)
        c = c + 1
    # add extra choices
    if os.path.isdir(previousdatasub):
        previous = 'Load previous addon data'
        dataoptions.append(previous)
    cancel = 'Cancel script'
    dataoptions.append(cancel)
    CHOOSE = xbmcgui.Dialog().select("Choose addon data", dataoptions)
    CHOICE = dataoptions[CHOOSE]
    if CHOICE == cancel:
        error = 'Stopped in getdataoptions()'
        error2 = 'Script cancelled by user'
        errormessage()
    elif CHOOSE == -1:
        error = 'Stopped in getdataoptions()'
        error2 = 'No valid choice made by user'
        errormessage()
    elif CHOICE == previous:
        previousdata = 'true'
        data = 'previous'
        print ('data is %s'% data)
        switchtopreviousdata()
    else:
        data = CHOICE
        print ('data is %s'% data)
        switchdata()

def checkdata():
    global data, error, error2, previousdatasub
    print 'running checkdata()'
    # check specified data subfolder exists
    trypath = os.path.join(SMASHINGADDONDATAOPTIONS, pvraddon, data)
    if previousdata == 'true':
        if os.path.isdir(previousdatasub):
            print 'checkdata() passed'
            switchtopreviousdata() 
        else:
            xbmc.executebuiltin('Notification(Script cancelled, previous addon data not found)')
            error = 'Problem in checkdata'
            error2 = ('previousdatasub (%s) does not exist'% previousdatasub)
            errormessage()    
    elif os.path.isdir(trypath):
        print 'checkdata() passed'
        print ('data is %s'% data)
        switchdata()
    else:
        xbmc.executebuiltin('Notification(Script cancelled, addon_data folder not found)')
        error = 'Problem in checkdata'
        error2 = ('data subfolder (%s) does not exist'% trypath)
        errormessage()

def switchtopreviousdata():
#    global 
    print 'running switchtopreviousdata()'
    # check if addon is running
#    disableaddon()    
    # do the switcheroo    
    shutil.move(previousdatasub, tempdatasub)
    shutil.move(addondatasub, previousdatasub)
    xbmc.sleep(300)
    shutil.move(tempdatasub, addondatasub)
    # (re)enable addon
#    enableaddon()    
    
def switchdata():
    global data
    print 'running switchdata()'
    # check if addon is running
#    disableaddon()
    # do the switcheroo
    newdatasub = os.path.join(dataoptionsfolder, data)
    if not os.path.isdir(tempdatasub):
        os.mkdir(tempdatasub)
    if os.path.isdir(previousdatasub):
        shutil.move(previousdatasub, tempdatasub)
    shutil.move(addondatasub, previousdatasub)
    xbmc.sleep(300)
    shutil.copytree(newdatasub, addondatasub)
    xbmc.sleep(300)
    shutil.rmtree(tempdatasub)
    # (re)enable addon
#    enableaddon()

def startpvr():	
    global pvraddon
    print 'running startpvr()'
    print ('%s is not running'% pvraddon)
    # check system has the addon in the argument - otherwise generate a notification
    PATH = os.path.join(ADDONSFOLDER, pvraddon)
    ALTPATH = os.path.join(DEFAULTADDONSFOLDER, pvraddon)
    print ('PATH is %s'% PATH)
    print ('ALTPATH is %s'% ALTPATH)
    if not os.path.exists(PATH):
        if os.path.exists(ALTPATH):
            PATH = ALTPATH
        else:
            printstar()
            print ('Tried to start %s but the addon is not installed.'% pvraddon)
            printstar()
            xbmc.executebuiltin('Notification(%s, is not installed)'% pvraddon)
#            error()
            exit()
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":true}}'% pvraddon)

def wait():
    print 'running wait()'
    # check the pvr info box isn't showing - if it is, wait!
    if xbmc.getCondVisibility('System.HasPVRAddon'):
#        xbmc.executebuiltin("ActivateWindow(Home)")   
        v = 0
        while v < 120:                                                              # ie 2 minutes
            pvrloading = xbmc.getCondVisibility('Window.IsVisible(10151)')          # DialogExtendedProgressBar.xml
            if pvrloading == 0:                                                     # ie dialog not visible
                xbmc.executebuiltin('Notification(Please, wait)')
                xbmc.sleep(5000)                                                    # wait 5 sec
                pvrloadingcheck = xbmc.getCondVisibility('Window.IsVisible(10151)')
                if pvrloadingcheck == 0:                                            # and check again
                    v = 1000
                else:
                    xbmc.executebuiltin('Notification(Please, wait)')
                    v = v + 1
            else:
                xbmc.sleep(1000)
                xbmc.executebuiltin('Notification(Please, wait)')
                v = v + 1
        if v < 1000:
            xbmc.executebuiltin('Notification(Timed out, please try again)')
            exit()

def radio():
    print 'running radio()'
    xbmc.executebuiltin('ActivateWindow(radiochannels)')
    finish()	

def recordings():
    print 'running recordings()'
    xbmc.executebuiltin('ActivateWindow(tvrecordings)')
    finish()

def timers():
    print 'running timers()'
    xbmc.executebuiltin('ActivateWindow(tvtimers)')
    finish()
	
def search():
    print 'running search()'
    xbmc.executebuiltin('ActivateWindow(tvsearch)')
    finish()
	
def recordedfiles():
    print 'running recordedfiles()'
    xbmc.executebuiltin('Videos,smb://SourceTVRecordings/,return')
    finish()
	
def timeshift():
    print 'running timeshift()'
    xbmc.executebuiltin('Videos,smb://SourceTVTimeshift/,return')   # opens the timeshift folder directly
    finish()
    
def simpletvchannels():
    print 'running simpletvchannels()'
    xbmc.executebuiltin('ActivateWindow(TVChannels)')       # opens pvr://channels/tv/All channels/
    finish()
    
def simpletvguide():
    print 'running simpletvguide()'
    xbmc.executebuiltin('ActivateWindow(TVGuide)')
    finish()

def openwindow():
    global groupnumber, window, group
    print 'running openwindow()'
    print ('window is %s'% window)
    print ('group is %s'% group)
    if window == 'not set':
        window = 'channels'
    if window == 'channels':
        if group == 'not set':
            print check1298
            simpletvchannels()
        elif group == 'choose':
            print 'check1301'
            groupnumber = 0
            opengroups()
        elif group == 'All channels':
            print 'check1305'
            groupnumber = 1
            opengroups()
    elif window == 'guide':
        if group == 'not set':
            simpletvguide()
        elif group == 'choose':
            groupnumber = 0
        elif group == 'All channels':
            groupnumber = 1
        opengroups() 
    elif window == 'radio':
        radio()
    elif window == 'recordings':
        recordings()
    elif window == 'timers':
        timers()
    elif window == 'search':
        search()
    elif window == 'recordedfiles':
        recordedfiles()
    elif window == 'timeshift':
        timeshift()
    elif window == 'not set':
        simpletvchannels()
    else:
        simpletvchannels()
        
def getchannelgroups():
    global CHANNELGROUPS, channelgroups, numbergroups, endmessage
    print 'running getchannelgroups()'
    CHANNELGROUPS = []
    c = 0
    while c < 60:
        try:
            ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "PVR.GetChannelGroups", "params":{"channeltype":"tv"} }'))
            c = 1000
        except:
            xbmc.executebuiltin('Notification(Waiting, for channel groups)')
            xbmc.sleep(1000)
            c = c + 1
    if c == 1000:
        channelgroups = ret['result']['channelgroups']
        for channelgroup in channelgroups:
#            printstar()
#            print channelgroup
            chanstring = str(channelgroup)
            start = "u'label': u'"
            end = "'}"		
            group = (chanstring.split(start))[1].split(end)[0]
            CHANNELGROUPS.append(group)
#        print CHANNELGROUPS
        numbergroups = len(CHANNELGROUPS)
        print ('There are %d channel groups' % numbergroups)
        c = 0
        while c < numbergroups:
            print CHANNELGROUPS[c]
            c = c + 1
    else:
        print 'Could not load channel groups'
        endmessage = 'All done, could not load channel groups'
        finish()
        
def checkchannelgroup():
    global group
    print 'running checkchannelgroup()'
    # only works in pvr window
    grp =  xbmc.getInfoLabel('Control.GetLabel(28)')
    if len(grp) > 7:
        grp = grp[7:]
        grp = grp.strip()
        print ('grp is %s'% grp)
        if grp == group:
            group = 'not set'
            openwindow()
            finish()
        else:
            getchannelgroups()
            setchannelgroup()
            # takes us back to opengroups()
            
def setchannelgroup():
    global group, groupnumber, numbergroups, CHANNELGROUPS, error        
    print 'running setchannelgroup()'    
    print ('There are %d channel groups'% numbergroups)
    print ('Channel groups are: %s'% CHANNELGROUPS)
    print ('The wanted group is %s'% group)
    c = 0
    groupnumber = 0             # defaults to 'choose'
    while c < numbergroups:
        GRP = CHANNELGROUPS[c]
        if group == GRP:
            groupnumber = c + 1
        c = c + 1
    if group in ["Choose", "choose", "Choose Group", "choose group"]:
        groupnumber = 0
    print ('Channel group number set to %d'% groupnumber)

    
# open channel or guide windows	- f = 1,2
def opengroups():
    global groupnumber
    print 'running opengroups()'
    if window == 'guide':
#    if guide == 'true': 
	    xbmc.executebuiltin('ActivateWindow(TVGuide)')	
    else:
	    xbmc.executebuiltin('ActivateWindow(TVChannels)')
    if groupnumber == 'not set':
        if group == 'not set':
            group = 0               # ie choose
        else:
            checkchannelgroup()
    xbmc.executebuiltin('SendClick(28)')
    xbmc.executebuiltin( "XBMC.Action(FirstPage)" )
    # loop move down to correct group (if necessary)
    c = 1
    if groupnumber > 1:
	    while (c < groupnumber):	
		    c = c + 1
		    xbmc.executebuiltin( "XBMC.Action(Down)" )			
    # open group if not using 'choose' option.		
    if groupnumber >= 1:		
	    xbmc.executebuiltin( "XBMC.Action(Select)" )
	    xbmc.executebuiltin( "XBMC.Action(Right)" )
	    xbmc.executebuiltin( "ClearProperty(SideBladeOpen)" )  

def chooseoptions():
#    global
    print 'running chooseoptions()'
    # pick from the list
        
def finish():
    global endmessage
    print 'running finish()'
    print ('%s stopping'% thisaddon)
    # notifications:
    if not quiet == 'true':
        if not endmessage == 'none':
            xbmc.executebuiltin('Notification(%s)'% endmessage)
    exit()
        
        


    
    
    

            
def checkwantedsettings():
    global pvraddon, disabled, refreshed, dbcleared, justvisiting, dataoptionsfolder, defaultfile, addondatasub, previousdatasub, tempdatasub, endmessage
    print 'running checkwantedsettings()'
    # checking
    print ('pvraddon is %s'% pvraddon)
    if disable == 'true':
        if not disabled == 'true':
            stoppvr()
    print ('refresh = %s'% refresh)
    if refresh == 'true':
        refreshdb()
    if cleardb == 'true':
        if not disabled == 'true':
            stoppvr()
        if not refreshed == 'true':
            refreshdb()
        replacedatabase()
    if reset == 'true':
        if not disabled == 'true':
            stoppvr()
        if not refreshed == 'true':
            refreshdb()
        if not dbcleared == 'true':
            replacedatabase()
        permanentdisable()
        multidisable()
    if forcestop == 'true':
        print 'forcestop pvr'
        forcestoppvr()
        refreshdb()
        replacedb()
        finish()
    if permanent == 'true':
        permanentenable()
    if permanent == 'false':
        permanentdisable()
    if multiple == 'true':
        multienable()
    if multiple == 'false':
        multidisable()
    if pvraddon == 'none':
        finish()
    if pvraddon == 'choose':
        justvisiting = 'true'
        getcurrentdata()
        choosepvr()
#    if pvraddon == 'current':
#        if xbmc.getCondVisibility('System.HasPVRAddon'):
#        # data stays unchanged, check channels / groups / group = and go
#            setf()                                                            # change name!
#        else:
#            if activepvrnumber == 0:
#                error = 'No pvr addon was active so could not set pvr == current'
#                errormessage()
#            elif activepvrnumber == 1:
#                pvraddon = activepvrs[0]
#                                            # start single pvr
#            else:
#                pvraddons = []
#                pvraddons = activepvrs
#                                                # start multiple pvrs
    if pvraddon == 'not set':
        pvraddon = 'current'
    if pvraddon == 'current':
        if not xbmc.getCondVisibility('System.HasPVRAddon'):
            error = 'No pvr addon was active so could not set pvr == current'
            errormessage()
    else:
        # process pvraddon
        if not xbmc.getCondVisibility('System.HasAddon(%s)'% pvraddon):
            if not multiple == 'true':
                if not disabled == 'true':
                    stoppvr()
                    if not refreshed == 'true':
                        refreshdb()
                        replacedatabase()
            # start that sucker
            startpvr()
            wait()
    if not group == 'none':
        getchannelgroups()
                 
    # At this point we must know what pvraddon is, so can set more variables:
    dataoptionsfolder = os.path.join(SMASHINGADDONDATAOPTIONS, pvraddon)
    defaultfile = os.path.join(dataoptionsfolder, "default.txt")
    addondatasub = os.path.join(ADDONDATA, pvraddon)
    oldaddon = pvraddon + '.previous settings'
    previousdatasub = os.path.join(ADDONDATA, oldaddon)
    tempaddon = pvraddon + '.temp'
    tempdatasub = os.path.join(ADDONDATA, tempaddon)
    processdatafiles() 
    print ('data = %s'% data)
    if data == 'choose':
        getdataoptions()
    elif not data == 'current':
        checkdata()


        

        
def oldchoosepvr():
    global pvraddon, endmessage
    print 'running choosepvr()'
    # list possibles from addondata, smashingaddondata, smashingaddondataoptions
    check = []
    pvrchoice = []
    check = os.listdir(ADDONDATA)
    num = len(check)
    c = 0
    while c < num:
        next = check[c]
        if next[:4] == 'pvr.':
            if 'previous' not in next:
                pvrchoice.append(next)
        c = c + 1
    check = []
    check = os.listdir(SMASHINGADDONDATA)
    num = len(check)
    c = 0
    while c < num:
        next = check[c]
        if next[:4] == 'pvr.':
            if next not in pvrchoice:
                pvrchoice.append(next)
        c = c + 1
    check = []
    check = os.listdir(SMASHINGADDONDATAOPTIONS)
    num = len(check)
    c = 0
    while c < num:
        next = check[c]
        if next[:4] == 'pvr.':
            if next not in pvrchoice:
                pvrchoice.append(next)
        c = c + 1
    num = len(pvrchoice)
    if num == 0:
        add = 'There are no valid pvr addons to choose from'
        pvrchoice.append(add)
    cancel = 'Cancel operation'
    pvrchoice.append(cancel)
    # Choose
    CHOOSE = xbmcgui.Dialog().select("Choose pvr addon", pvrchoice)
    CHOICE = pvrchoice[CHOOSE]
    if CHOOSE == -1:
        endmessage = 'Action, cancelled'    
        finish()
    elif CHOICE == add:
        endmessage = 'Action, cancelled'    
        finish()
    elif CHOICE == cancel:
        endmessage = 'Action, cancelled'    
        finish()
    else:
        pvraddon = CHOICE
    
 
    

    




def checkcurrentpvr():
    global STOP
    # check if the addon is already running - if not continue startup
	# check if any pvr running - if so stop.
    # then start pvraddon
    if not xbmc.getCondVisibility('System.HasAddon(%s)'% pvraddon):
        if xbmc.getCondVisibility('System.HasPVRAddon'):
            stoppvr()
            xbmc.executebuiltin('Notification(Stopping, %s)'% STOP)
            refreshdb()

#            exit()
            checkready()
        startpvr()
        xbmc.executebuiltin('Notification(Starting, %s)'% pvraddon)
#        exit()		
        checkstarted()
        

    
    

        
def oldgetchannelgroups():
    global CHANNELGROUPS, channelgroups, numbergroups
    print 'running getchannelgroups()'
    CHANNELGROUPS = []
    ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "PVR.GetChannelGroups", "params":{"channeltype":"tv"} }'))
    channelgroups = ret['result']['channelgroups']
    for channelgroup in channelgroups:
#        printstar()
#        print channelgroup
        chanstring = str(channelgroup)
        start = "u'label': u'"
        end = "'}"		
        group = (chanstring.split(start))[1].split(end)[0]
        CHANNELGROUPS.append(group)
#    print CHANNELGROUPS
    numbergroups = len(CHANNELGROUPS)
    print ('There are %d channel groups' % numbergroups)
    c = 0
    while c < numbergroups:
        print CHANNELGROUPS[c]
        c = c + 1


    
		

    

        
        

    
def forcestoppvr():
    global ignorepvr, activepvrs, activepvrnumber, disabled, quiet, error, error2
    print 'running forcestoppvr()'
    if not home == 'true':
        gohome()
    if not activepvr == 'none':
        # go through list of enabled addons:
#        print ('%s check 11'% thisaddon)
        c = 0
        checkreadytostop()
        while c < activepvrnumber:
            checkpvr = activepvrs[c]
            print ('stopping %s'% checkpvr)
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"%s","enabled":false}}'% checkpvr)            
            xbmc.sleep(1000)
            c = c + 1
        if xbmc.getCondVisibility('System.HasPVRAddon'):
            error = 'Problem in forcestoppvr()'
            error2 = 'Not all pvrs were disabled.'
            errormessage()
        else:
            print 'All pvr addons disabled'
            if not quiet == 'true':
                xbmc.executebuiltin('Notification(Live TV, has been disabled)')                
    else:
        print 'No pvr addons were enabled'
        if not quiet == 'true':
            xbmc.executebuiltin('Notification(Live TV, was not enabled)')
    disabled = 'true'
    



    
	


	
# try again
def try2checkready():	
    global LOGFILE, starttime, length, startlog	
    found = 'false'
    h = 1
    w = startlog
    while h <= 49:
        with open(LOGFILE) as f:
            lines = f.readlines()            
            finishline = lines[w]
            if 'radio channel groups loaded' in finishline:
                finishlog = w + 1
                h = 50
                print ('finishline is %s'% finishlog)
                xbmc.sleep(300)
                xbmc.executebuiltin('Notification(finishline is line, %s)'% finishlog)
            w = w + 1
        xbmc.sleep(1000)
        h = h + 1
    if not h == 51:
        printstar()
        print ('finishline not found.  %s will close now.'% thisaddon)
#        error()
        exit()
    else:
        xbmc.executebuiltin('Notification(finishline is line, %s)'% finishlog)

# and again
def checkready():	
    global STOP	
    print 'running checkready()'
    xbmc.executebuiltin('Notification(Hang on, a tick)')
    xbmc.sleep(2000)
    xbmc.executebuiltin('Notification(Hang on, a tick)')
    checkcount = 0
    while checkcount < 30:
        if not xbmc.getCondVisibility('System.HasAddon(%s)'% STOP):
            if not xbmc.getCondVisibility('Pvr.HasTVChannels'):
                checkcount = 30
                xbmc.sleep(1000)
        checkcount = checkcount + 1
    if checkcount == 30:
#        xbmc.executebuiltin('Notification(Oh, poop)')
        exit()

def checkstarted():
    global pvraddon
    xbmc.executebuiltin('Notification(Hang on, a tick)')
    xbmc.sleep(2000)
    xbmc.executebuiltin('Notification(Hang on, a tick)')
    checkcount = 0
    while checkcount < 30:
        if xbmc.getCondVisibility('System.HasAddon(%s)'% pvraddon):
            if xbmc.getCondVisibility('Pvr.HasTVChannels'):
                checkcount = 30
                xbmc.sleep(1000)
        checkcount = checkcount + 1
        xbmc.sleep(300)
    if checkcount == 30:
#        xbmc.executebuiltin('Notification(Oh, poop)')
        exit()
	
# lose this
def realcheckready():
    # check the log for 'radio channel groups loaded' after the script started - if that appears it's safe to switch to a pvr window
    global LOGFILE, starttime
    found = 'false'
    h = 1
    while h <= 49:
        with open(LOGFILE) as f:
            lines = f.readlines()
            w = 1
            while w < 500:
                finishline = lines[-w]
                if ('%s has started'% thisaddon) in finishline:
                    xbmc.sleep(300)
                    w = 500				
                elif 'radio channel groups loaded' in finishline:
                    printstar()
                    print ('finishline is %s'% finishline)
                    printstar()
                    found = 'true'
                    w = 500
                w = w + 1
#                print ('w is %s'% w)
        if found == 'false':
            h = h + 1
            printstar()
#            print ('h is %s'% h)
        else:
            h = 50
#            h = h + 20
            printstar()
            print ('h is %s'% h)
    if found == 'false':
        printstar()
        print ('finishline not found. %s will stop'% thisaddon)
        printstar()		
        exit()				
    h = finishline[:2]
    m = finishline[3:5]
    s = finishline[6:8]
    # printstar()
    # print ('h is %s'% h)
    # print ('m is %s'% m)
    # print ('s is %s'% s)
    # printstar()
    # exit()
    h = int(h)
    m = int(m)
    s = int(s)
    # get time in seconds
    finishtime = (h*3600) + (m*60) + s
    timetaken = finishtime - starttime		
    printstar()
    print ('starttime is %d'% starttime)
    print ('starttime is %d'% starttime)
    print ('timetaken is %d'% timetaken)
    printstar()
    if starttime > finishtime:
        printstar()
        print ('starttime > finishtime: %s will exit'% thisaddon)		
        printstar()
    xbmc.sleep(300)
#    xbmc.executebuiltin('ActivateWindow(TVChannels)')
#    exit()	


		
      
# Get on with it.

startaddon()
checkpvrnotplaying()
getarguments()
logarguments()


# if pvrchecked == 'false':
#    getpvrs()   # list what's potentially running now, to check
# justvisiting = 'true'
# getcurrentdata()





#            checkwantedsettings()
# print ('%s check 5'% thisaddon)
#               checkcurrentpvr()
# print ('%s check 6'% thisaddon)
# follow it through gets to end of startpvr() if required - chosen pvr is running, now look at window.
# checkready()

finish()


	
