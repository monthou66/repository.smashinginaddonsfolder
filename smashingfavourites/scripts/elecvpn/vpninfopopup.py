# -*- coding: utf-8 -*-

import xbmc

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
	
printstar()
print "vpninfopopup.py has just been started"
printstar()
xbmc.executebuiltin('Notification(vpninfopopup.py, started)')
xbmc.executebuiltin("RunScript(/storage/.kodi/addons/service.vpn.manager/infopopup.py)")
