

def apply(self, c, e, command, arguments):
    self.logger.debug(f"Applying command {command}")
    if command == "reload":
        self._reload(c)
    if command == "join":
        for chan in arguments:
            c.join(chan)
