# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "vpncycle.py has just been started"
printstar()
# xbmc.executebuiltin('Notification(vpncycle.py, started)')
xbmc.executebuiltin("RunScript(/storage/.kodi/addons/service.vpn.manager/cycle.py)")
