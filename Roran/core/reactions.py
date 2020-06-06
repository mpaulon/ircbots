import datetime


def on_pubmsg(self, c, e):
    if self.config.get("ratelimit") is not None:
        if self.cache.get("ratelimit") is None:
            self.cache["ratelimit"] = dict()
        if self.cache["ratelimit"].get(e.target) is None:
            self.cache["ratelimit"][e.target] = dict()
        last_spoken = self.cache["ratelimit"][e.target].get(e.source)
        if last_spoken is not None and \
                last_spoken + datetime.timedelta(seconds=self.config["ratelimit"].get("delay", 10)) > datetime.datetime.now():
            c.privmsg(e.target, f"{e.source} parle trop vite")
            c.kick(e.target, e.source.nick, self.config["ratelimit"].get("message", "TG !"))
        self.cache["ratelimit"][e.target][e.source] = datetime.datetime.now()


def on_join(self, c, e):
    pass


def on_welcome(self, c, e):
    for chan in self.config.get("channels", []):
        c.join(chan)
