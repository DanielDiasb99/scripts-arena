#*-* coding: utf-8

#Coded by ImChris
#https://imchris.tk
#https://ubge.org

import thread
import urllib
import urllib2

USER_AGENT = "User-Agent", "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/382048415934054400/WZHhD8nPuLAM5yxkq912-hvU1Zox0KitEaDj8-GoPDdEDjNd2GFEpsOD797We8y7pGMC" #Banimentos
SECRETARIA_WEBHOOK_URL = "https://discordapp.com/api/webhooks/387868123803418624/W5xeEVP-qBHzKn42bm5wiTJTkho_MFIezNL8d8wqgU5DG35niyd7LHXldTIXONyVf9jM" 	#Logins

def send_discord_message(connection, message, url=""):
	connection.protocol.discord_say(message, url)

def apply_script(protocol, connection, config):

	class DiscordHelperProtocol(protocol):

		def discord_say(self, message, url=DISCORD_WEBHOOK_URL):
			data = urllib.urlencode({"content": message})
			post_request = urllib2.Request(url, data)
			post_request.add_header("User-Agent", USER_AGENT)
			return urllib2.urlopen(post_request).read()

	class DiscordHelper(connection):

		def on_user_login(self, user_type, verbose = True):
			message = '`%s` efetuou login como `%s`.' % (self.name, user_type)
			thread.start_new_thread(send_discord_message, (self, message, 
				SECRETARIA_WEBHOOK_URL))
			connection.on_user_login(self, user_type, verbose)

	return DiscordHelperProtocol, DiscordHelper