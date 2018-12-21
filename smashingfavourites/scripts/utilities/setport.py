# -*- coding: utf-8 -*-

import xbmc

# defaults
wantedport = 'not set'
toggle = 'false'
endip = 'not set'


def printstar():
    print "***************************************************************************************"
    print "****************************************************************************************"
    
def startaddon():
    global thisaddon, wantedport, toggle
    thisaddon = sys.argv[0]
    if len(sys.argv) > 1:
        input = sys.argv[1]
        if input.isdigit():
            wantedport = input
        elif input == 'default':
            wantedport = '8080'
        elif input == 'ipbased':
            wantedport = 'ipbased'
        elif input == 'toggle':
            toggle = 'true'
        elif input == 'choose':
            wantedport = 'choose'
        else:
            print ('Problem with script: %s'% thisaddon)
            print ('Input not recognised: %s'% input)
            exit()
    else:
        toggle = 'true'
            
def getcurrent():
    global ip, currentport
    # get IP
    ip = xbmc.getIPAddress()
    # get current webserver port
    json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": "services.webserverport"}, "id": 1 }')
    # response is eg >> {"id":1,"jsonrpc":"2.0","result":{"value":8080}}
    start = '"value":'
    finish = '}}'
    json_response = (json_query.split(start))[1].split(finish)[0]
    currentport = int(json_response)
    xbmc.executebuiltin('Notification(IP address is %s, webserver port is %d)'% (ip, currentport))
    
def getwanted():
    global wantedport
    if wantedport == 'ipbased':
        getportfromip()
    elif toggle == 'true':
        if currentport == 8080:
            getportfromip()
        else:
            wantedport = 8080
    elif wantedport.isdigit():
        wantedport = int(wantedport)
    elif wantedport == 'choose':
        chooseport()

def getportfromip():
    global wantedport
    endip = ip[-2:]
    if endip[:1] == '.':
        endip = endip[1:]
    endip = int(endip)
    wantedport = 10000 + endip
    
def chooseport():
    global wantedport
    
def changeport():
    if not wantedport == currentport:
        xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"services.webserverport","value":%d},"id":1}'% wantedport)
        xbmc.executebuiltin('Notification(Webserver port changed to, %d)'% wantedport)
    else:
        xbmc.executebuiltin('Notification(No action, required)')
            
def printoutput():
    printstar()
    print ('%s has started'% thisaddon)
    print ('IP is %s' % ip)
#    print 'json_query is:'
#    print json_query
#    print ('json_response is %d'% json_response)
    print ('current port is %d'% currentport)
#    if not endip == 'not set':
#        print ('endip = %d'% endip)
    print ('wanted port is %d'% wantedport)
    printstar()

startaddon()
getcurrent()
getwanted()
changeport()
printoutput()
exit()




