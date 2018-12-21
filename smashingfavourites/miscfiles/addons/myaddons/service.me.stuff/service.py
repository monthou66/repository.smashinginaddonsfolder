#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
import os
import shutil


# define stuff
count = 0
dvbviewcount = 0
lastidlecount = 0
# define file locations
ADDONS = os.path.join(xbmc.translatePath('special://home/addons/'))
PVRIPTVSIMPLE = os.path.join(ADDONS, "pvr.iptvsimple")
ALTERNATE = os.path.join(xbmc.translatePath('special://xbmc/addons/pvr.iptvsimple'))


def printstar():
    print "********************************************************************************************************************************************************************************************************************************************************************************"
    print "*********************************************************************************************************************************************************************************************************************************************************************************"

def checkpvriptvupdate():
    global PVRIPTVSIMPLE
    global ALTERNATE
    if not os.path.exists(PVRIPTVSIMPLE):
#        print 'PVRIPTVSIMPLE does not exist.'
        if not os.path.exists(ALTERNATE):
#            print 'ALTERNATE does not exist either.'
            checkxonfluenceupdate()
        else:
            PVRIPTVSIMPLE = ALTERNATE
    MARKER = os.path.join(PVRIPTVSIMPLE, "cloned.txt")
    if os.path.isfile(MARKER):
#        print 'pvr.iptvsimple checked - all is well.'
        checkxonfluenceupdate()
    else:
        xbmc.executebuiltin('RunScript(special://masterprofile/smashing/smashingfavourites/scripts/utilityscripts/clonepvr.iptvsimple.py)')
        xbmc.sleep(10000)
        checkxonfluenceupdate()
		
def checkxonfluenceupdate():
	



    carryon()
	
def dostuff():
#    printstar()
#    print 'Doing stuff'
    printstar()
	# stop playback if have video
    if xbmc.getCondVisibility("Player.HasVideo"):
        xbmc.executebuiltin( "XBMC.Action(Stop)" )	
    # Go back to home if not already there.
    while not xbmc.getCondVisibility("Window.Is(home)"):
        xbmc.executebuiltin( "XBMC.Action(Back)" )
        # ActivateScreensaver
        xbmc.sleep(300)
        xbmc.executebuiltin('ActivateScreensaver')		
    xbmc.executebuiltin('ActivateScreensaver')	
    # turn off pvr if running
    if xbmc.getCondVisibility('System.HasPVRAddon'):
        if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):		
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimple","enabled":false}}')	
            xbmc.sleep(10000)
#            printstar()
            print 'Doing service stuff - disabling pvr.iptvsimple****************************************************************************************************************************************************************************************************************************************'
#            printstar()
            carryon()
    if xbmc.getCondVisibility('System.HasPVRAddon'):
        if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimplefab)'):		
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.iptvsimplefab","enabled":false}}')	
            xbmc.sleep(10000)
#            printstar()
            print 'Doing service stuff - disabling pvr.iptvsimplefab****************************************************************************************************************************************************************************************************************************************'
#            printstar()
    if xbmc.getCondVisibility('System.HasPVRAddon'):		
        if xbmc.getCondVisibility('System.HasAddon(pvr.dvbviewer)'):		
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":8,"params":{"addonid":"pvr.dvbviewer","enabled":false}}')	
            xbmc.sleep(10000)
#            printstar()
            print 'Doing service stuff - disabling dvbviewer****************************************************************************************************************************************************************************************************************************************'
#            printstar()
        if xbmc.getCondVisibility('System.HasPVRAddon'):
            printstar()
            print 'There was a problem disabling pvr addons with service.me.stuff****************************************************************************************************************************************************************************************************************************************'
            printstar()
            xbmcgui.Dialog().ok('There was a problem disabling pvr addons.', 'Check your log for details.')

    checkpvriptvupdate()
    checkxonfluenceupdate()
			
    printstar()
    print 'Service stuff checked***********************************************************************************************************************************************************************************************************************************************************'
    printstar()
    		
# Check it's started 

xbmc.sleep(6000)





# xbmc.sleep(60000)
#printstar()
print 'service thingy has started up ****************************************************************************************************************************************************************************************************************************************'
#printstar()	

def carryon():
    xbmc.sleep(1000)
	
# Do the biz
# while (not xbmc.abortRequested) == 'true':
# while count < 1000000:
while not xbmc.abortRequested:
#    xbmc.sleep(600000)				# 600000 = checks every minute > 2 hrs
    xbmc.sleep(8000)				# 1000 = checks every 8 seconds > 16 mins (testing)
#    xbmc.sleep(1000)				# 1000 = checks every second > 2 mins (testing)

    IDLE = xbmc.getGlobalIdleTime()
#    print ('IDLE is %s seconds'% IDLE)
    if IDLE > lastidlecount:
        lastidlecount = IDLE
        if not (xbmc.getCondVisibility("Player.Playing")):
            count = count + 1
            printstar()
            print 'count has been increased by 1'
            print ('count = %d' % count)
            print ('lastidlecount has been set to %s'% lastidlecount)
    else:
        count = 0
        lastidlecount = 0
        printstar()
        print 'count and lastidlecount have been reset to zero'
        print ('count = %d' % count)
        print ('lastidlecount = %d' % lastidlecount)


    if count >= 5:

		
#    if count >= 120:
        count = 0
        dostuff()

		
# 
# Want to monitor:
# check open window - return to homescreen after a time									30 min
# check if player has media - stop and return to homescreen after a (longer) time		2 hrs
# check for skin changes - restore power menus and anything else?						2 hrs
# disable pvr if not been watched for a while (and no flag set)							2 hrs
# need an enable / disable function
# update pvr clones if needed
# if not xbmc.getCondVisibility("Pvr.IsTimeShift") and not xbmc.getCondVisibility("Pvr.IsPlayingRadio"):











