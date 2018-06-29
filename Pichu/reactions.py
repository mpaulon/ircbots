"""."""


def on_invite(bot, c, e):
    """."""
    c.join(e.arguments[0])


def on_welcome(bot, c, e):
    """."""
    c.privmsg("NickServ", text='RECOVER {} {}'.format(
        bot.nickname,
        bot.password))


def on_join(bot, c, e):
    """."""
    pass


def on_privmsg(bot, c, e):
    """."""
    pass


def on_pubmsg(bot, c, e):
    """."""
    pass
