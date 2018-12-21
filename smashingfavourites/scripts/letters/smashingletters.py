# -*- coding: utf-8 -*-
# jump to a letter in lists.
import os
import os.path
import xbmc
import sys

# define some stuff
USERDATA = xbmc.translatePath('special://masterprofile')
SMASHINGFAVOURITES = os.path.join(USERDATA, "smashing", "smashingfavourites")

def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"

def startaddon():
    global thisaddon, a
    thisaddon = sys.argv[0]
    a = sys.argv[1]
    printstar()
    print ('%s has started'% thisaddon)
    printstar()
#    xbmc.executebuiltin('Notification(%s, started)'% thisaddon)

def checkfirst():
    # get first letter
    global first, checkfirstletter
    name = 'xxxxx'
    first = 'yyy'
    checkfirstletter = 'unknown'
    name = xbmc.getInfoLabel('System.CurrentControl')
    if not name == 'xxxxx':
        first = name[:1]
        if first == '[':
            first = name[1]
        if first.isdigit():
            checkfirstletter = 'digit'
        else:
            if name == '[..]':			# ie top of list
                checkfirstletter = 'digit'	# treat as digit so next jump is to 'A'
    print ('name is %s'% name)
    print ('first is %s'% first)
    print ('checkfirstletter is %s'% checkfirstletter)
	
def gotoA():
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	
def gotoZ():
	xbmc.executebuiltin( "XBMC.Action(JumpSMS8)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )		
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	
def gotofirst():
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	
def gototop():
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )	
	xbmc.executebuiltin( "XBMC.Action(Up)" )

# Do stuff
startaddon()
xbmc.sleep(300)    
    

# Define buttons

if a == 'Next Letter':	
	xbmc.executebuiltin( "XBMC.Action(NextLetter)" )
# check this...???:
	xbmc.executebuiltin('XBMC.RunScript(special://userdata/favourites/scripts/tempfavourites.py, smashingletters)')
if a == 'skinNext Letter':
    checkfirst()
    if checkfirstletter == 'digit':
        gotoA()
    elif first == 'Z' or first =='z':
        gotofirst()
    else:
        xbmc.executebuiltin( "XBMC.Action(NextLetter)" )
    # reload dialog, so can click down 'next letter' easily - poss to just change focus?
    xbmc.executebuiltin('XBMC.ActivateWindow(2159)')
    xbmc.executebuiltin( "XBMC.Action(Down)" )
    xbmc.executebuiltin( "XBMC.Action(Down)" )
    xbmc.executebuiltin( "XBMC.Action(Down)" )
elif a == 'Previous Letter':	
	xbmc.executebuiltin( "XBMC.Action(PrevLetter)" )
# check this...???:
	xbmc.executebuiltin('XBMC.RunScript(special://userdata/favourites/scripts/tempfavourites.py, smashingletters)')
elif a == 'skinPrevious Letter':
    checkfirst()
    if checkfirstletter == 'digit':
        gotoZ()
    elif first == 'A' or first == 'a':
        gotofirst()
    else:
        xbmc.executebuiltin( "XBMC.Action(PrevLetter)" )
    xbmc.executebuiltin('XBMC.ActivateWindow(2159)')
    xbmc.executebuiltin( "XBMC.Action(Down)" )
    xbmc.executebuiltin( "XBMC.Action(Down)" )
    xbmc.executebuiltin( "XBMC.Action(Down)" )
    xbmc.executebuiltin( "XBMC.Action(Down)" )
    # reload dialog, so can click down 'next letter' easily - poss to just change focus?
    xbmc.executebuiltin('XBMC.ActivateWindow(2159)')
elif a == 'Top':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(Up)" )
elif a == 'A':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
elif a == 'B':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
elif a == 'C':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
elif a == 'D':
    xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
    xbmc.executebuiltin( "XBMC.Action(JumpSMS3)" )
elif a == 'E':
    xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
    xbmc.executebuiltin( "XBMC.Action(JumpSMS3)" )
    xbmc.executebuiltin( "XBMC.Action(JumpSMS3)" )	
elif a == 'F':
    xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
    xbmc.executebuiltin( "XBMC.Action(JumpSMS3)" )
    xbmc.executebuiltin( "XBMC.Action(JumpSMS3)" )
    xbmc.executebuiltin( "XBMC.Action(JumpSMS3)" )
elif a == 'G':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS4)" )
elif a == 'H':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS4)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS4)" )	
elif a == 'I':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS4)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS4)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS4)" )
elif a == 'J':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS5)" )
elif a == 'K':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS5)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS5)" )	
elif a == 'L':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS5)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS5)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS5)" )
elif a == 'M':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS6)" )
elif a == 'N':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS6)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS6)" )	
elif a == 'O':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS6)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS6)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS6)" )
elif a == 'P':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS7)" )
elif a == 'Q':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS7)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS7)" )	
elif a == 'R':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS7)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS7)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS7)" )
elif a == 'S':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS7)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS7)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS7)" )		
	xbmc.executebuiltin( "XBMC.Action(JumpSMS7)" )		
elif a == 'T':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS8)" )
elif a == 'U':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS8)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS8)" )	
elif a == 'V':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS8)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS8)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS8)" )
elif a == 'W':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS8)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
elif a == 'X':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS8)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )	
elif a == 'Y':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS8)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
elif a == 'Z':
	xbmc.executebuiltin( "XBMC.Action(JumpSMS8)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )		
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
elif a == 'Bottom':
	xbmc.executebuiltin("SetFocus(55)")
	xbmc.executebuiltin( "XBMC.Action(JumpSMS9)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(JumpSMS2)" )
	xbmc.executebuiltin( "XBMC.Action(Up)" )
	xbmc.executebuiltin( "XBMC.Action(Up)" )	
else:
    xbmc.executebuiltin('Notification(Check, letters)')
    printstar()
    print ('Problem with %s: Script started with argument %s which was not recognised'%(thisaddon, a))
    
	
