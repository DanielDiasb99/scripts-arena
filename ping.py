from pyspades.constants import *
from commands import add, get_player
from twisted.internet.reactor import callLater

#script by MegaStar 27/09/18

def cycleping(connection, user = None):
    if connection.cycleping == False:
        msg = ""
        if user is not None:
            user = get_player(connection.protocol, user)
            if user not in connection.protocol.players:
                return connection.send_chat("The user "+user+" does not exist.")
            msg += "Starting the cycleping of the player %s." % user.name
        else:
            user = connection
            msg += "Starting your cycleping."


        connection.cycleping = True
        connection.cycle_player = user
        connection.send_chat(msg)
        connection.cycle_ping(user)
    else:
        connection.cycleping = False
        connection.cycle_player = None
        connection.send_chat("Cycleping has been stopped.")

add(cycleping)

def apply_script(protocol, connection, config):
    class CyclepingConnection(connection):
        cycleping = False
        cycle_player = None

        def cycle_ping(self, user):
            if self.cycleping:
                if user not in self.protocol.players.values():
                    self.send_chat("Cycleping has been stopped, the player was left.")
                    self.cycleping = False
                    self.cycle_player = None
                    return
                self.send_chat("%s ping: %s" % (user.name, user.latency))
                callLater(1, self.cycle_ping, user)

        def on_disconnect(self):
            if self.cycleping:
                self.cycleping = False
                self.cycle_player = None
            return connection.on_disconnect(self)

    return protocol, CyclepingConnection
