#!/usr/bin/python
# -*- coding: utf-8 -*-
# getaddonsettings.py

import xbmc

# defaults
# testing
# configure = 'true'
config = 'false'

def printstar():
    print "****************************************************************************"
    print "***************************************************************************"
   
def finish():
    print ('Closing %s'% thisaddon)
    exit()
   
def getsettings():
    global error, error2, errornotification
    print 'running getsettings()'
    if xbmc.getCondVisibility('System.HasAddon(%s)' % ADDON):
        if config == 'true':
            xbmc.executebuiltin('Addon.OpenSettings(%s)'% ADDON)
            finish()
    # else do it the hard way
    xbmc.executebuiltin('ActivateWindow(AddonBrowser,"addons://user/all",return)')
    # process arguments
    addonname = xbmc.getInfoLabel('System.AddonTitle(%s)'% ADDON)
    xbmc.sleep(300)
    numitems = xbmc.getInfoLabel('Container.NumItems')
    numitems = int(numitems)
    offset = 0
    c = 0
    size = numitems + 1
    while c < size:
#        print ('c = %d'% c)
        check = xbmc.getInfoLabel('Container.ListItem(%d).Label'% c)
#        print ('check = %s'% check)
        if addonname in check:
            offset = c
#            print ('offset = %s'% offset)
            c = 1000
        c = c + 1
    if c > 999:
#        print ('offset is %d'% offset)
        pass
    else:
        print 'Problem in getsettings()'
        print ('could not find offset for'% addonname)
        xbmc.executebuiltin('Notification(Problem getting settings, see log for details)')
        exit()
    c = 0
    while c < offset:
        xbmc.executebuiltin("XBMC.Action(Down)")
        c = c + 1
    xbmc.executebuiltin( "XBMC.Action(Select)" )
    if config == 'true':
        xbmc.executebuiltin( "XBMC.Action(FirstPage)" )
        xbmc.executebuiltin( "XBMC.Action(Select)" )
    print 'leaving getsettings()'
    finish()
    
def startaddon():
    global thisaddon, ADDON, config
    thisaddon = sys.argv[0]
    print ('starting %s'% thisaddon)
    if len(sys.argv) > 1:
        try:
            ADDON = sys.argv[1]
        except:
            xbmc.executebuiltin('Notification(Problem, getting addon settings)')
            printstar()
            print 'Problem with getaddonsettings.py'
            print 'Invalid argument specified - it needs to be a valid addon id'
            printstar()
            exit()
    else:
        xbmc.executebuiltin('Notification(Problem, getting addon settings)')
        printstar()
        print 'Problem with getaddonsettings.py'
        print 'No argument specified - needs to be a valid addon id'
        printstar()
        exit()
    if len(sys.argv) > 2:
        if sys.argv[2] == 'config':
            config = 'true'
        
startaddon()
getsettings()
        