# -*- coding: utf-8 -*-
# backtohome.py
# go back to home page 1 step at a time
import xbmc

# Check where we are
# if necessary go back 1 level
# repeat until at home screen

while not xbmc.getCondVisibility("Window.Is(home)"):
    xbmc.executebuiltin( "XBMC.Action(Back)" )

# Drink beer        
