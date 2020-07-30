def on_pubmsg(self, c, e):
    if "Katrina" in e.arguments[0]:
        c.kick(e.target, e.source.nick, "D'où tu parles de ma meuf ? Tu vas tater de mon marteau !")


def on_privmsg(self, c, e):
    pass


def on_namreply(self, c, e):
    pass


def on_invite(self, c, e):
    if e.source.nick not in self.config.get("blacklist"):
        c.join(e.arguments[0])


def on_join(self, c, e):
    if e.source.nick == self.config.get("nick"):
        self.logger.info(f"Joined {e.target}")


def on_welcome(self, c, e):
    if self.config.get("password"):
        c.privmsg("NickServ", text='RECOVER {} {}'.format(
            self.config.get("nick"),
            self.config.get("password")))
        c.nick(self.config.get("nick"))
        c.privmsg("NickServ", text='IDENTIFY {}'.format(
            self.config.get("password")))
    for chan in self.config.get("channels", []):
        c.join(chan)
