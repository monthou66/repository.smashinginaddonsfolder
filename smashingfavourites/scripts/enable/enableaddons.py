# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import os

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# marker - file present when script is running; use this if calling script from another script
marker = os.path.join(xbmc.translatePath('special://masterprofile'), 'smashing', 'smashingtemp', 'markers', 'enableaddonsrunning.txt')
# path to kodi addons folder:	
PATH = os.path.join(xbmc.translatePath('special://home/'), "addons")
# Make some lists:
ADDONS = []
SUCCESS = []
FAIL = []

# create marker file
if not os.path.isfile(marker):
    open(marker, 'w').close()

# Move stuff in or out of addons folder and then:
xbmc.executebuiltin( 'UpdateLocalAddons' )

# Exclude addons I don't want to check (pvr is usually off on my system, metadata is the kodi repo stuff, packages folder obviously)
for i in os.listdir(PATH):
    if os.path.isdir(os.path.join(PATH,i)) and 'packages' not in i and 'pvr' not in i and 'metadata' not in i and 'temp' not in i:
        ADDONS.append(i)
printstar()
print ADDONS
n = len(ADDONS)
print ("There are %d addons in the kodi addons folder that will be checked." % n)
printstar()
# Check each addon - if not enabled try enable, then check status again.  Report success or fail.
if n > 0:
    c = 0
    d = 0
    e = 0
    while c < n:
        CHECK = ADDONS[c]
        print ("Now checking %s ." % CHECK)
        if not xbmc.getCondVisibility('System.HasAddon(%s)' % CHECK):
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":true}}' % CHECK)
            xbmc.sleep(200)
            if xbmc.getCondVisibility('System.HasAddon(%s)' % CHECK):
                d = d + 1
                SUCCESS.append(CHECK)
            else:
                # is addonid same as foldername?  If not get id from addon.xml and try again!
                ADDONXML = os.path.join(PATH, CHECK, "addon.xml")
                # get the addonid
                with open(ADDONXML) as f:
                    for line in f:
                        if "<addon id=" in line:
                            start = "<addon id=\""
#                            end = "\" name="
                            end = "\""
                            ADDONID = (line.split(start))[1].split(end)[0]
                            print ('Folder is %s' % CHECK)
                            print ('Addonid to enable is %s' % ADDONID)
                            if not xbmc.getCondVisibility('System.HasAddon(%s)' % ADDONID):
                                xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":7,"params":{"addonid": "%s","enabled":true}}' % ADDONID)			
                                xbmc.sleep(200)
                                if xbmc.getCondVisibility('System.HasAddon(%s)' % ADDONID):
                                    d = d + 1
                                    SUCCESS.append(CHECK)
                                else:
                                    e = e + 1
                                    FAIL.append(CHECK)
				
        c = c + 1

		
		# Put results up on the screen:
    line1 = ('%d addons enabled'% d)
    line2 = ('%d addons not enabled'% e)
    line3 = 'Check the log for details.'
	
if d > 0 and e > 0:
    xbmcgui.Dialog().ok(line1, line2, line3)
elif e > 0:
    xbmcgui.Dialog().ok(line2, line3)
elif d > 0:
    xbmcgui.Dialog().ok(line1, line3)
elif d == 0 and e == 0:
    line3 = 'No action taken.'
    xbmcgui.Dialog().ok(line1, line3)
else:
    line1 = 'Something funny going on.'
    xbmcgui.Dialog().ok(line1, line3)

	# print results to log
printstar()
print "enableaddons.py has done its thing."
print ("%s addons were checked" % n)
print ("%s addons were enabled" % d)
print ("There were %s failures" % e)
print ("Enabled addons: %s" % SUCCESS)
print ("Failures: %s" % FAIL)
printstar()

# remove marker file
os.remove(marker)
print 'finishing now'
exit()

# Drink beer