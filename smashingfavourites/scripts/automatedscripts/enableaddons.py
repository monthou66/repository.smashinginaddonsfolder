# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import os

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# define stuff
USERDATA = xbmc.translatePath('special://masterprofile')	
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")
MARKER = os.path.join(SMASHINGFAVOURITES, "tempfiles", "enableaddonspydone.txt")
# path to kodi addons folder:	
ADDONSPATH = os.path.join(xbmc.translatePath('special://home/'), "addons")
# Make some lists:
ADDONS = []
SUCCESS = []
FAIL = []

# xbmc.sleep(1000)
# Move stuff in or out of addons folder and then:
xbmc.executebuiltin('UpdateLocalAddons')

# Exclude addons I don't want to check (pvr is usually off on my system, metadata is the kodi repo stuff, packages folder obviously)
for i in os.listdir(ADDONSPATH):
    if os.path.isdir(os.path.join(ADDONSPATH,i)) and 'packages' not in i and 'pvr' not in i and 'metadata' not in i:
        ADDONS.append(i)
#printstar()
#print ADDONS
n = len(ADDONS)
#print ("There are %d addons in the kodi addons folder that will be checked." % n)
#printstar()
# Check each addon - if not enabled try enable, then check status again.  Report success or fail.
if n > 0:
    c = 0
    d = 0
    e = 0
    while c < n:
        CHECK = ADDONS[c]
#        print ("Now checking %s ." % CHECK)
        if not xbmc.getCondVisibility('System.HasAddon(%s)' % CHECK):
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":true}}' % CHECK)
            xbmc.sleep(200)
            if xbmc.getCondVisibility('System.HasAddon(%s)' % CHECK):
                d = d + 1
                SUCCESS.append(CHECK)
            else:
                e = e + 1
                FAIL.append(CHECK)				
        c = c + 1
ERROR = len(FAIL)
FAILTOO = []
FAILTOO = FAIL
if ERROR > 0:
    xbmc.sleep(4000)
    c = 0
    while c < ERROR:
        CHECK = FAIL[c]
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":true}}' % CHECK)
        if xbmc.getCondVisibility('System.HasAddon(%s)' % CHECK):
            SUCCESS.append(CHECK)
            FAILTOO.remove(CHECK)
            c = c + 1
            d = d + 1
            e = e - 1
						


# print results to log
if e > 0:
    printstar()
    print ("%s addons were checked" % n)
    print ("%s addons were enabled" % d)
    print ("There were %s failures" % e)
    print ("Enabled addons: %s" % SUCCESS)
    print ("Failures: %s" % FAILTOO)
    printstar()
# If any failures put a message on the screen.
    xbmcgui.Dialog().ok('Some addons were not enabled.', 'Check your log for details.')

open(MARKER, "w").close()

exit()

# Drink beer