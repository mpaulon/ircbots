"""."""


def on_invite(bot, c, e):
    """."""
    c.join(e.arguments[0])


def on_part(bot, c, e):
    """."""
    if e.source.nick == bot.config.get("nickname"):
        bot.config["channels"].remove(e.target)
        bot.dump()


def on_welcome(bot, c, e):
    """."""
    if not bool(bot.config.get("debug")):
        c.privmsg("NickServ", text='RECOVER {} {}'.format(
            bot.config.get("nickname"),
            bot.config.get("password")))
        c.nick(bot.config.get("nickname"))
        c.privmsg("NickServ", text='IDENTIFY {}'.format(
            bot.config.get("password")))
    bot.notify(c, "Hello master")
    for chan in bot.config.get("channels"):
        c.join(chan)


def on_join(bot, c, e):
    """."""
    if e.source.nick == bot.config.get("nickname"):
        bot.notify(c, "{} joined".format(e.target))
        print(e)
        if e.target not in bot.config["channels"]:
            bot.config["channels"] += [str(e.target)]
            bot.dump()


def on_privmsg(bot, c, e):
    """."""
    print(e)


def on_pubmsg(bot, c, e):
    """."""
    pass
