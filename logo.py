# Coded by ImChris
# http://imchris.tk
# http://ubge.org

import Image
from pyspades.constants import CTF_MODE

LOGO_PATH = "resources/logo.png"
color_key = True

def apply_script(protocol, connection, config):

	class UBGELogoConnection(connection):

		def on_position_update(self):
			x, y, z = self.get_location()	
			if self.protocol.on_logo((x, y, z)):
				self.set_hp(self.hp - 20)
				self.send_chat("FICAR EM CIMA DA LOGO NAO E PERMITIDO!")
			connection.on_position_update(self)

		def on_spawn_location(self, pos):
			x, y, z = pos		
			if self.protocol.on_logo(pos):
				z = self.protocol.map.get_z(x, y, 1)
				return x, y, z
			return connection.on_spawn_location(self, pos)

	class UBGELogo(protocol):

		logo = Image.open(LOGO_PATH).convert('RGBA')
		logo_pixels = logo.load()
		logo_blocks = set()

		def on_update_entity(self, entity):
			x, y, z = entity.x, entity.y, entity.z
			if self.on_logo((x, y, z)):
				entity.z = self.map.get_z(x, y, start=2)
				entity.update()
			return protocol.on_update_entity(self, entity)

		def on_logo(self, pos):
			x, y, z = pos
			if self.logo_blocks:
				x, y, z = int(x), int(y), int(z) 				
				return z <= 0 and (x, y) in [(bx, by) for bx, by, bz in self.logo_blocks]
			return False

		def on_map_change(self, map):
			print("Applying logo...")
			width, height =  self.logo.size
			logo_position = {}
			logo_position['x'] = (512 / (512 / width)) + (512 / (512 / width)) / 2
			logo_position['y'] = 512 - (512 / (512 / height))	

			for x in xrange(width):
				for y in range(height):
					pixel = self.logo_pixels[x,y]
					condition = pixel == self.logo_pixels[0,0] if color_key else pixel[3] < 0
					if not condition:
						z = map.get_z(x, y) if self.game_mode == CTF_MODE else 0
						block_position = (logo_position['x'] + x, logo_position['y'] + y, z)
						map.set_point(logo_position['x'] + x, logo_position['y'] + y, z, pixel)
						if self.game_mode != CTF_MODE:
							if self.god_blocks is None:
								self.god_blocks = set()
							self.god_blocks.add(block_position)
							self.logo_blocks.add(block_position)
			protocol.on_map_change(self, map)

	return UBGELogo, UBGELogoConnection