"""."""


def on_invite(bot, c, e):
    """."""
    c.join(e.arguments[0])


def on_welcome(bot, c, e):
    """."""
    c.privmsg("NickServ", text='RECOVER {} {}'.format(
        bot.nickname,
        bot.password))
    c.nick(bot.nickname)
    c.privmsg("NickServ", text='IDENTIFY {}'.format(
        bot.password))

def on_join(bot, c, e):
    """."""
    pass


def on_privmsg(bot, c, e):
    """."""
    print(e)


def on_pubmsg(bot, c, e):
    """."""
    pass
