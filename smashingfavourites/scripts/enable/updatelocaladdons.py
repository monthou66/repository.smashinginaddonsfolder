# -*- coding: utf-8 -*-
# update local addons

import xbmc

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# sleep or it won't work!	
xbmc.sleep(300)
xbmc.executebuiltin('Action(UpdateLocalAddons)')		# no error   no action

xbmc.sleep(300)
xbmc.executebuiltin('Notification(Local addons, updated)')
printstar()
print 'Local addons updated.'
printstar()
exit()

# Drink beer