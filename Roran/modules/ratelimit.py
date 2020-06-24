import datetime


def start():
    return


def stop():
    return


def apply_command(self, c, e, command, arguments):
    destination = e.target if e.type == "pubmsg" else e.source.nick
    if e.type == "pubmsg" and e.source in self.config.get("admins"):
        if command == "ratelimit":
            if len(arguments) == 1 and arguments[0] == "on":
                self.logger.info(f"Ratelimiting {e.target}")
                c.mode(destination, "+m")
                for user in self.channels[e.target].users():
                    c.mode(destination, f"+v {user}")
                return
            if len(arguments) == 1 and arguments[0] == "off":
                self.logger.debug("Removing ratelimit on {e.target}")
                c.mode(destination, "-m")
                for user in self.channels[e.target].users():
                    c.mode(destination, f"-v {user}")
                return


def on_welcome(self, c, e):
    pass


def on_invite(self, c, e):
    pass


def on_join(self, c, e):
    pass


def on_namreply(self, c, e):
    pass


def on_pubmsg(self, c, e):
    if False and self.config.get("ratelimit") is not None:
        if self.cache.get("ratelimit") is None:
            self.cache["ratelimit"] = dict()
        if self.cache["ratelimit"].get(e.target) is None:
            self.cache["ratelimit"][e.target] = dict()
        last_spoken = self.cache["ratelimit"][e.target].get(e.source)
        if (
                last_spoken is not None and
                last_spoken + datetime.timedelta(
                    seconds=self.config["ratelimit"].get("delay", 10)
                ) > datetime.datetime.now() and (
                    self.config.get("blacklist") is None or
                    e.source.nick in self.config["ratelimit"].get("blacklist"))):
            self.logger.info(f"{e.source} exceeds ratelimit")
            if self.config["ratelimit"].get("notify", False):
                c.privmsg(e.target, f"{e.source.nick} parle trop vite")
            c.kick(e.target, e.source.nick, self.config["ratelimit"].get("message", "TG !"))
        self.cache["ratelimit"][e.target][e.source] = datetime.datetime.now()


def on_privmsg(self, c, e):
    pass
