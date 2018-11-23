#*-* coding: utf-8

#Coded by ImChris
#https://imchris.tk
#https://ubge.org

import urllib
import urllib2
import thread
from commands import get_ban_arguments, get_player, admin, add, join_arguments

def prettify_timespan(total, get_seconds = False):
    total = int(total)
    days = total / (1440 * 60)
    total -= days * 1440 * 60
    hours = total / (60 * 60)
    total -= hours * 60 * 60
    minutes = total / 60
    seconds = total - minutes * 60 if get_seconds else 0
    if days == hours == minutes == seconds == 0:
        return 'menos de um %s' % 'segundo' if get_seconds else 'minuto'
    days_s = '%s dia' % days if days > 0 else None
    hours_s = '%s hora' % hours if hours > 0 else None
    minutes_s = '%s minuto' % minutes if minutes > 0 else None
    seconds_s = '%s segundo' % seconds if seconds > 0 else None
    if days > 1: days_s += 's'
    if hours > 1: hours_s += 's'
    if minutes > 1: minutes_s += 's'
    if seconds > 1: seconds_s += 's'
    text = ', '.join([s for s in (days_s, hours_s, minutes_s, seconds_s) if s])
    return text

def publish_ban(connection, player, duration, reason):
    ban_duration = "por %s" % prettify_timespan(duration * 60)
    ban_reason = reason    
    if not duration:
        ban_duration = "permanentemente"
    if not reason:
        ban_reason = "Não declarado"    
    connection.protocol.discord_say("**%s** baniu **%s** %s.\n**Motivo**: %s." % (connection.name, player.name, 
        ban_duration, ban_reason))

@admin
def ban(connection, value, *arg):
    duration, reason = get_ban_arguments(connection, arg)
    player = get_player(connection.protocol, value)
    if player:      
        thread.start_new_thread(publish_ban, (connection, player, 
            duration, reason))
    player.ban(reason, duration)
add(ban)

@admin
def hban(connection, value, *arg):
    duration = int(60)
    reason = join_arguments(arg)
    player = get_player(connection.protocol, value)
    if player:      
        thread.start_new_thread(publish_ban, (connection, player, 
            duration, reason))
    player.ban(reason, duration)
add(hban)

@admin
def dban(connection, value, *arg):
    duration = int(1440)
    reason = join_arguments(arg)
    player = get_player(connection.protocol, value)
    if player:      
        thread.start_new_thread(publish_ban, (connection, player, 
            duration, reason))
    player.ban(reason, duration)
add(dban)

@admin
def wban(connection, value, *arg):
    duration = int(10080)
    reason = join_arguments(arg)
    player = get_player(connection.protocol, value)
    if player:      
        thread.start_new_thread(publish_ban, (connection, player, 
            duration, reason))
    player.ban(reason, duration)
add(wban)

def apply_script(protocol, connection, config):
    return protocol, connection