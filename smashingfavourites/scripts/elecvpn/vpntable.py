# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "vpntable.py has just been started"
printstar()
# xbmc.executebuiltin('Notification(vpntable.py, started)')
xbmc.executebuiltin("RunScript(/storage/.kodi/addons/service.vpn.manager/table.py)")
