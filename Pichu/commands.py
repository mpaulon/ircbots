"""Define Pichu's commands."""
from geopy.geocoders import Nominatim
from geopy.distance import distance
import traceback
import sys


def locate_addr(value):
    """Get address from name."""
    geolocator = Nominatim()
    location = geolocator.geocode(value)
    return(location.address, (location.latitude, location.longitude))


def dist_2_points(point_a, point_b):
    """Distance between 2 points."""
    _, cooA = locate_addr(point_a)
    _, cooB = locate_addr(point_b)
    return(distance(cooA, cooB).km)


def do_command(bot, c, e, symb):
    """."""
    command = e.arguments[0].split(' ')[0].strip()
    arguments = ' '.join(e.arguments[0].split(' ')[1:]).split(' | ')
    print(e.source.nick, command, arguments)
    bot.notify(c, "{} tried to use {} {}".format(
        e.source.nick,
        command,
        " ".join(arguments)))
    # Geolocation WIP
    if "{}locate".format(symb) == command and arguments:
        try:
            address, coords = locate_addr(arguments[0])
            if e.type == "pubmsg":
                c.privmsg(e.target, text='{} {}'.format(address, coords))
            else:
                c.privmsg(e.source.nick, text='{} {}'.format(address, coords))
        except:
            traceback.print_exc(file=sys.stderr)
            c.privmsg(e.source.nick, text='Geolocation failed')
    elif "{}dist".format(symb) == command and len(arguments) == 2:
        try:
            dist = dist_2_points(arguments[0], arguments[1])
            if e.type == "pubmsg":
                c.privmsg(e.target, text='{}km'.format(dist))
            else:
                c.privmsg(e.source.nick, text='{}km'.format(dist))
        except:
            c.privmsg(e.source.nick, text='Distance calculation failed')
    # Random shit

    # Utilities
    elif "{}join".format(symb) == command and arguments:
        for chan in arguments:
            c.join(chan)
    elif "{}leave".format(symb) == command:
        c.part(e.target)
    elif "{}code".format(symb) == command:
        c.privmsg(e.source.nick, "My code can be found here : {}".format(
            bot.config.get("git")))
    # Admin commands
    elif ("{}register".format(symb) == command and
          e.source.nick in bot.config.get("admins") and
          e.type == 'privmsg'):
        c.privmsg(target="NickServ", text='REGISTER {} {}'.format(
            bot.config.get("password"),
            bot.config.get("email")))
    elif ("{}identify".format(symb) == command and
          e.source.nick in bot.config.get("admins") and
          e.type == 'privmsg'):
        c.privmsg("NickServ", text='IDENTIFY {}'.format(
            bot.config.get("password")))
    elif "{}recover".format(symb) == command:
        c.privmsg("NickServ", text='RECOVER {} {}'.format(
            bot.config.get("nickname"),
            bot.config.get("password")))
    # Help
    elif "{}help".format(symb) == command:
        help_strings = [
            "{}locate [location]: (WIP) address and GPS coordinates of a location",
            "{}dist [location1] | [location2]: (WIP) distance in km between 2 locations" ,
            "{}join [chan] (| [chan] | ... [chan]): makes me join these chans",
            "{}leave: leave current chan",
            "{}code: display url where my code can be found",
            "{}help: display this",

            "admin only: {0}exit(P), {0}reload, {0}register(P), {0}identify(P), {0}recover"
        ]
        c.privmsg(e.source.nick, "Available commands: (P) are privmsg only")
        for s in help_strings:
            c.privmsg(e.source.nick, s.format(symb))
