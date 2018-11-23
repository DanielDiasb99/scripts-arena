#script by MegaStar

from pyspades.constants import *

def apply_script(protocol, connection, config):
	class HealthPlayerConnection(connection):
 		def on_kill(self, killer, type, grenade):
			if killer != self and killer is not None:
				if killer.hp == None:
					hp = 0
				else:
					hp = killer.hp
				self.send_chat('You were killed by: %s HP : %i' %( killer.name, hp)) 

				return connection.on_kill(self, killer, type, grenade)
	return protocol, HealthPlayerConnection

    
   
