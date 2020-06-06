import yaml
import irc.bot  # type: ignore

from core import reactions, commands


class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, config: str, logger):
        with open(config) as configfile:
            self.config = yaml.load(configfile, Loader=yaml.FullLoader)
        print(self.config)
        self.logger = logger
        self.server = irc.bot.ServerSpec(
                self.config.get("server", dict()).get("address", "localhost"),
                self.config.get("server", dict()).get("port", 6667)
        )
        
        self.nick = self.config.get("nick")
        self.realname = self.config.get("realname")
        self.prefix = self.config.get("prefix", "!")

        super().__init__(
            [self.server],
            self.nick,
            self.realname
                )
        
        self.cache: dict = dict()
        self.reactions = reactions
        self.commands = commands






    def _is_command(self, message: str):
        return message.startswith(self.prefix)

    def on_welcome(self, c: irc.client.ServerConnection, e: irc.client.Event):
        self.logger.debug(e)
        self.reactions.on_welcome(self, c, e)

    def on_join(self, c: irc.client.ServerConnection, e: irc.client.Event):
        self.logger.debug(e)
        self.reactions.on_join(self, c, e)

    def on_pubmsg(self, c: irc.client.ServerConnection, e: irc.client.Event):
        self.logger.debug(e)
        self.reactions.on_pubmsg(self, c, e)
        if self._is_command(e.arguments[0]):
            pass
            # self.commands.apply(self, c, e)

    def on_privmsg(self, c: irc.client.ServerConnection, e: irc.client.Event):
        self.logger.debug(e)
