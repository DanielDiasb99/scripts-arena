#Script by MegaStar 6/05/18
#Detects when an ip contains 3 ranges equal to the banned ip (message = Ban Evader Detected)
#Detects when an ip contains 2 ranges equal to the banned ip (message = Possible Ban Evader Detected)
#The script searches the banned IPs in the "bans.txt" file of the dist folder and compares them with the IP of the player that entered your server.

from pyspades.constants import *
from twisted.internet import reactor

def apply_script(protocol, connection, config):
    class RangeConnection(connection):

        def on_login(self,name):
            ip = str(self.address[0])
            nickp = str(self.name)
            pid = str(self.player_id)
            with open("bans.txt","r") as db:
                newlist = []
                newips = []
                cont = db.read()
                arr = eval(cont)
                array = arr
                for x in array:
                    newlist.append(x)
                    
                for x in ip:
                    curip = ''
                    for x in ip:
                        if x == '.':
                            x = ' '
                        curip += x
                su = curip.split()
                
                for x in newlist:
                    nick = x[0]                                                                          
                    newnick = ''.join(nick)
                    ipp = x[1]
                    ips = ipp.replace('.',' ')
                    val = ips.split()
                    val.insert(0,newnick)
                    newips.append(val)
                
                

                for x in newips:
                    if x[1] == su[0] and x[2] == su[1] and x[3] == su[2]:
                        message = '%s (#%s) Ban Evader Detected (3 coincidences found). Banned IP: %s.%s.%s.%s with the nick: %s, Current IP: %s' % (nickp,pid,x[1],x[2],x[3],x[4],x[0],ip)
                        irc_relay = self.protocol.irc_relay     
                        if irc_relay.factory.bot and irc_relay.factory.bot.colors:
                            message = '\x0304' + message + '\x0f'                    
                        reactor.callLater(0.5,irc_relay.send,message)
                        for admins in self.protocol.players.values():
                            if admins.admin:
                                reactor.callLater(0.5,admins.send_chat,message)
                        break
                    elif x[1] == su[0] and x[2] == su[1]:
                        message = '%s (#%s) Possible Ban Evader Detected (2 coincidences found). Banned IP: %s.%s.%s.%s with the nick: %s, Current IP: %s' % (nickp,pid,x[1],x[2],x[3],x[4],x[0],ip)
                        irc_relay = self.protocol.irc_relay 
                        if irc_relay.factory.bot and irc_relay.factory.bot.colors:
                            message = '\x0304' + message + '\x0f'                    
                        reactor.callLater(0.5,irc_relay.send,message)
                        for admins in self.protocol.players.values():
                            if admins.admin:
                                reactor.callLater(0.5,admins.send_chat,message)
                        break                
             
                del(newlist)
                del(newips)
        
            return connection.on_login(self, name)
        
    return protocol, RangeConnection
        
