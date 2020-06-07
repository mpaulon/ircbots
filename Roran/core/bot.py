"""An irc bot with a hammer"""
import copy
import importlib
import signal
import traceback

import yaml
import irc.bot  # type: ignore


from core import reactions, commands


class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, config: str, logger):
        self.logger = logger
        self.config_path = config
        self._load_config()

        self.server = irc.bot.ServerSpec(
            self.config.get("server", dict()).get("address", "localhost"),
            self.config.get("server", dict()).get("port", 6667)
        )

        super().__init__(
            [self.server],
            self.config.get("nick", "Roran"),
            self.config.get("realname", "Roran")
                )

        self.cache: dict = dict()
        self.reactions = reactions
        self.commands = commands
        signal.signal(signal.SIGHUP, self._handle_signals)
        self.modules = []

    def _handle_signals(self, number, frame):
        self.logger.info(f"Received signal {number}")
        if number == signal.SIGHUP:
            self._reload()

    def _load_config(self):
        with open(self.config_path) as configFile:
            self.config = yaml.load(configFile, Loader=yaml.FullLoader)
        self.logger.info(f"Loaded config from {self.config_path}")
        self.logger.debug(f"{self.config}")

    def _reload(self, c=None):
        self.logger.info(f"Reloading bot")
        try:
            # rechargement du fichier de configuration
            # old_config = copy.deepcopy(self.config)
            self._load_config()
            # TODO: gérer les cas de changement de nick, realname et serveurs
            self.logger.debug(f"Reloading commands")
            importlib.reload(commands)
            self.commands = commands
            self.logger.debug(f"Reloading reactions")
            importlib.reload(reactions)
            self.reactions = reactions
            self.logger.info(f"Reloading done")
        except Exception:
            self.logger.error(f"Reloading failed")
            if c is not None:
                trace = traceback.format_exc()
                self.logger.error(trace)
                for line in trace.split():
                    self.notify(c, line)

    def _get_command(self, message: str):
        if message.startswith(self.config.get("prefix", "!")) and len(message) > 1:
            message = message.split()
            command = message[0][1:]
            args = message[1:] if len(message) > 1 else []
            return (command, args)
        return False

    def notify(self, c, message):
        for admin in self.config.get("admins", list()):
            c.privmsg(admin, text=message)

    def on_welcome(self, c: irc.client.ServerConnection, e: irc.client.Event):
        self.logger.debug(str(e))
        self.reactions.on_welcome(self, c, e)

    def on_join(self, c: irc.client.ServerConnection, e: irc.client.Event):
        self.logger.debug(str(e))
        self.reactions.on_join(self, c, e)

    def on_pubmsg(self, c: irc.client.ServerConnection, e: irc.client.Event):
        self.logger.debug(str(e))
        self.reactions.on_pubmsg(self, c, e)
        if action := self._get_command(e.arguments[0]):
            self.commands.apply(self, c, e, action[0], action[1])

    def on_privmsg(self, c: irc.client.ServerConnection, e: irc.client.Event):
        self.logger.debug(str(e))
        self.reactions.on_privmsg(self, c, e)
        if action := self._get_command(e.arguments[0]):
            self.commands.apply(self, c, e, action[0], action[1])
