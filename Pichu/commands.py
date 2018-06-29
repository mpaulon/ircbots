"""Define Pichu's commands."""
from geopy.geocoders import Nominatim
from geopy.distance import distance


def locate_addr(value):
    """Get address from name."""
    geolocator = Nominatim()
    address, (latitude, longitude) = geolocator.geocode(value)
    return(address, (latitude, longitude))


def dist_2_points(point_a, point_b):
    """Distance between 2 points."""
    _, cooA = locate_addr(point_a)
    _, cooB = locate_addr(point_b)
    return(distance(cooA, cooB).km)


def do_command(bot, c, e, symb):
    """."""
    command = e.arguments[0].split(' ')[0].strip()
    arguments = ' '.join(e.arguments[0].split(' ')[1:]).split(' ! ')
    print(e.source.nick, command, arguments)
    if "{}locate".format(symb) == command and arguments:
        try:
            address, coords = locate_addr(' '.join(arguments[0]))
            c.privmsg(e.target, text='{} {}'.format(address, coords))
        except:
            c.privmsg(e.target, text='Geolocation failed')
    elif "{}dist".format(symb) == command and len(arguments) == 2:
        try:
            dist = dist_2_points(arguments[0], arguments[1])
            c.privmsg(e.target, text='{}km'.format(dist))
        except:
            c.privmsg(e.target, text='Distance calculation failed')
    elif "{}join".format(symb) == command and arguments:
        for chan in arguments:
            c.join(chan)
    elif "{}register".format(symb) == command:
        c.privmsg(target="NickServ", text='REGISTER {} {}'.format(
            bot.password,
            bot.email))
    elif "{}identify".format(symb) == command:
        c.privmsg("NickServ", text='IDENTIFY {}'.format(bot.password))
    elif "{}recover".format(symb) == command:
        c.privmsg("NickServ", text='RECOVER {} {}'.format(
            bot.nickname,
            bot.password))
