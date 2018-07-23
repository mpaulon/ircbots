"""Pichu bot."""
import importlib
import irc.bot
# import argparse as ap
import asyncio
import threading
import json
import traceback
import sys
from random import randint

import commands
import reactions
import routines


class Bot(irc.bot.SingleServerIRCBot):
    """Main bot class."""

    def __init__(self):
        """."""
        self.config = json.load(open("config", 'r'))
        if not self.config.get("debug"):
            init_nick = self.config.get("nickname") + str(randint(0, 1000))
        else:
            init_nick = self.config.get("nickname")
        super().__init__([irc.bot.ServerSpec(self.config.get("server"))],
                         init_nick,
                         self.config.get("realname"))
        self.reactions = reactions
        self.commands = commands.do_command

    def on_welcome(self, c, e):
        """."""
        self.reactions.on_welcome(self, c, e)

    def on_join(self, c, e):
        """."""
        self.reactions.on_join(self, c, e)

    def on_part(self, c, e):
        """."""
        self.reactions.on_part(self, c, e)

    def on_pubmsg(self, c, e):
        """."""
        if e.arguments[0][0] == self.config.get("symb"):
            self.do_command(c, e)
        self.reactions.on_pubmsg(self, c, e)

    def on_privmsg(self, c, e):
        """."""
        if e.arguments[0][0] == self.config.get("symb"):
            self.do_command(c, e)
        self.reactions.on_privmsg(self, c, e)

    def on_invite(self, c, e):
        """."""
        self.reactions.on_invite(self, c, e)

    def do_command(self, c, e):
        """."""
        command = e.arguments[0].split(' ')[0].strip()
        if ("{}exit".format(self.config.get("symb")) == command and
                e.source.nick in self.config.get("admins") and
                e.type == 'privmsg'):
            exit(0)
        elif ("{}reload".format(self.config.get("symb")) == command and
                e.source.nick in self.config.get("admins")):
            try:
                importlib.reload(commands)
                importlib.reload(reactions)
                importlib.reload(routines)
                self.commands = commands.do_command
                self.reactions = reactions
                self.routines = routines
                self.config = json.load(open("config", 'r'))
                if e.type == 'privmsg':
                    c.notice(e.source.nick, text="config reloaded")
                else:
                    c.notice(e.target, text="config reloaded")
                print("config reloaded")
            except:
                if e.type == 'privmsg':
                    c.notice(e.source.nick, text="reload failed")
                else:
                    c.notice(e.target, text="reload failed")
                print("reload failed")
                traceback.print_exc(file=sys.stderr)
        else:
            print("plop")
            self.commands(self, c, e, self.config.get("symb"))

    def dump(self):
        """Dump config."""
        open("config", "w").write(json.dumps(self.config, indent=True))

    def notify(self, c, message):
        """Notify admins."""
        for adm in self.config.get("admins"):
            c.privmsg(adm, text=message)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    bot = Bot()
    bot_t = threading.Thread(target=bot.start)
    bot_t.start()
