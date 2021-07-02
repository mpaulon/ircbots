import subprocess


def apply(self, c, e, command, arguments):
    # punis !
    if e.source.nick in self.config.get("blacklist", []):
        return

    self.logger.debug(f"Applying command {command} with arguments {arguments}")
    destination = e.target if e.type == "pubmsg" else e.source.nick

    if command == "joke":
        with open("files/core/joke.txt", "r") as joke_file:
            for line in joke_file:
                c.privmsg(destination, line.strip("\n"))
    if command == "bilan_moral":
        c.privmsg(destination, "Cette année le moral a été bon.")
    if command == "bilan_technique":
        c.privmsg(destination, "Cette année la technique a été bonne.")
    if command == "bilan_financier":
        c.privmsg(destination, "Cette année les financiers étaient bons.")
    if command == "bilan_mere":
        c.privmsg(destination, "Cette année ta mère a été bonne.")
    if command == "dalek":
        with open("files/core/dalek.txt", "r") as dalek_file:
            for line in dalek_file:
                c.privmsg(destination, line.strip("\n"))
    if command == "cookie":
        if len(arguments) > 0:
            c.privmsg(destination, f"Congratulations {' '.join(arguments)}, you deserve a cookie ! 🍪")
        return
        with open("files/core/cookie.txt", "r") as cookie_file:
            for line in cookie_file:
                c.privmsg(destination, line.strip("\n"))
    if command == "zayo":
        with open("files/core/zayo.txt", "r") as zayo_file:
            for line in zayo_file:
                c.privmsg(destination, line.strip("\n"))
    if command == "orly":
        with open("files/core/orly.txt", "r") as orly_file:
            for line in orly_file:
                c.privmsg(destination, line.strip("\n"))
    if command == "help":
        c.privmsg(destination, "no help for now, but the code says it works")

    if command == "git":
        if len(arguments) == 1 and arguments[0] == "describe":
            commit_hash = subprocess.check_output(["git", "describe", "--always", "--dirty"]).strip().decode("utf-8")
            c.privmsg(destination, f"Currently running commit {commit_hash}")
        if len(arguments) == 1 and arguments[0] == "ls-files":
            modified = subprocess.check_output(["git", "ls-files", "-m"]).strip().decode("utf-8").split("\n")
            c.privmsg(destination, f"{len(modified)} dirty files")
            for f_modified in modified:
                c.privmsg(destination, f" - {f_modified}")

    if command == "code":
        url = subprocess.check_output(["git", "remote", "get-url", "origin"]).strip().decode("utf-8")
        c.privmsg(destination, url)

    # commandes admin only
    if e.source.nick in self.config.get("admins"):
        if command == "reload":
            self._reload(c)
            return
        if command == "join":
            for chan in arguments:
                c.join(chan)
            return
        # commandes en privé
        if e.type == "privmsg":
#            if command == "config":
#                c.privmsg(destination, str(self.config))
            if command == "register":
                self.logger.debug("Registering")
                c.privmsg(target="NickServ", text='REGISTER {} {}'.format(
                    self.config.get("password"),
                    self.config.get("email")))
            if command == "identify":
                self.logger.debug("Identifying")
                c.privmsg("NickServ", text='IDENTIFY {}'.format(
                    self.config.get("password")))
            if command == "recover":
                self.logger.debug("Recovering")
                c.privmsg("NickServ", text='RECOVER {} {}'.format(
                    self.config.get("nick"),
                    self.config.get("password")))
