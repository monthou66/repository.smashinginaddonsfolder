# -*- coding: utf-8 -*-
# reload keymaps

import xbmc

#Makes log easier to follow:
def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

# sleep or it won't work!	
xbmc.sleep(300)
xbmc.executebuiltin('Action(reloadkeymaps)')		# no error   no action

xbmc.sleep(300)
xbmc.executebuiltin('Notification(keymaps, reloaded)')
printstar()
print 'Keymaps have been reloaded.'
printstar()
exit()

# Drink beer