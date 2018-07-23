"""Define Pichu's commands."""
from geopy.geocoders import Nominatim
from geopy.distance import distance
import traceback
import sys
import re
import datetime
import os.path


# regex qui matche une date:
re_date = re.compile("[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}:[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}")
re_delay = re.compile("")


def locate_addr(value):
    """Get address from name."""
    geolocator = Nominatim()
    location = geolocator.geocode(value)
    return location.address, (location.latitude, location.longitude)


def dist_2_points(point_a, point_b):
    """Distance between 2 points."""
    _, coo_a = locate_addr(point_a)
    _, coo_b = locate_addr(point_b)
    return distance(coo_a, coo_b).km


class Reminder():
    """."""

    def __init__(self, nickname):
        """."""
        self.filename = ".reminders/{}.remindme".format(nickname)
        if not os.path.isfile(self.filename):
            open(self.filename, "w").close()

    def get(self):
        """."""
        file = open(self.filename, "r")
        for n, line in enumerate(file):
            yield n, line
        file.close()

    def delete(self, id):
        """."""
        final_file = ""
        for n, line in self.get():
            if n != id:
                final_file += line.strip() + "\n"
        file = open(self.filename, "w")
        file.write(final_file)

    def add(self, value):
        """."""
        file = open(self.filename, "a")
        file.write(value.strip() + "\n")


def parse_datetime(date):
    if re_date.fullmatch(date) is not None:
        date = date.split(":")
        day = date[0].split("/")
        hours = date[1]
        minutes = date[2]
        seconds = date[3]
        return datetime.datetime(year, month, day, hours, minutes, seconds)
    else:
        raise ValueError


def do_command(bot, c, e, symb):
    """."""
    command = e.arguments[0].split(' ')[0].strip()
    arguments = ' '.join(e.arguments[0].split(' ')[1:]).split(' | ')
    print(e.source.nick, command, arguments)
    bot.notify(c, "{} tried to use {} {}".format(
        e.source.nick,
        command,
        " ".join(arguments)))
    # Geolocation
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
                c.privmsg(e.target, text='{:.2f}km'.format(dist))
            else:
                c.privmsg(e.source.nick, text='{}km'.format(dist))
        except:
            c.privmsg(e.source.nick, text='Distance calculation failed')
    # Reminder
    elif "{}remindme".format(symb) == command:
        args = arguments[0].strip().split(' ')
        if args[0] == "list":
            for n, line in Reminder(e.source.nick).get():
                c.privmsg(e.source.nick, text="{}: {}".format(n, line))
            c.privmsg(e.source.nick, text="### END of reminder")
        elif args[0] == "date":
                try:
                    datetime.fromisoformat(args[1])
                    if :
                        Reminder(e.source.nick).add({} - {} - {}.format(args[2], "", ))
                except ValueError:
                    c.privmsg(e.source.nick, text="Invalid date format, should be YYYY/MM/DD-hh:mm:ss")
        elif args[0] == "delay":
            pass
        elif args[0] == "delete":
            pass

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

            "{}locate [location]: address and GPS coordinates of a location",
            "{}dist [location1] | [location2]: distance in km between 2 locations" ,
            "{}join [chan] (| [chan] | ... [chan]): makes me join these chans",
            "{}leave: leave current chan",
            "{}code: display url where my code can be found",
            "{}remindme: reminder management",
            "{}help: display this",

            "admin only: {0}exit(P), {0}reload, {0}register(P), {0}identify(P), {0}recover"
        ]
        c.privmsg(e.source.nick, "Bonjour, je suis la version de dev de Pichu.")
        print(bool(bot.config.get("debug")))
        if not bool(bot.config.get("debug")):
            c.privmsg(e.source.nick, "Available commands: (P) are privmsg only")
            for s in help_strings:
                c.privmsg(e.source.nick, s.format(symb))
