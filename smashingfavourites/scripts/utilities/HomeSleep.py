#!/usr/bin/python

import xbmc

xbmc.executebuiltin('PlayerControl(Stop)')
xbmc.executebuiltin('ActivateWindow(Home)')
xbmc.executebuiltin('Shutdown()')

exit(0)