import subprocess
import datetime


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
    if command == "cookie":
        if len(arguments) > 0:
            c.privmsg(destination, "Congratulation {' '.join(arguments)}, you deserve a cookie !")
        with open("file/core/cookie.txt", "r") as cookie_file:
            for line in cookie_file:
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
        c.privmsg(destination, "https://git.servens.org/mikachu/ircbots")

    if command == "mark":
        # format commande: !mark [tag] http...URL... [commentaire]*
        # format ligne: [tag] http...URL... ## commentaires ## e.source.nick ## datetime.datetime.now
        tag = ""
        comments = ""
        url = None
        if len(arguments) >= 1:
            print("plop")
            if arguments[0].startswith("http"):
                url = arguments[0]
                if len(arguments) >= 2:
                    comments = " ".join(arguments[1:])
            elif len(arguments) >= 2 and arguments[1].startswith("http"):
                print(arguments[1])
                tag = f"[{arguments[0]}]"
                url = arguments[1]
                if len(arguments) >= 3:
                    comments = " ".join(arguments[2:])
            if url is not None:
                with open("files/core/marks.txt", "a") as bookmarks:
                    self.logger.debug(f"Saving bookmark {url}")
                    bookmarks.write(f"{tag} {url} ## {comments} ## {e.source.nick} ## {datetime.datetime.now()}\n")
                 
    if command == "search":
        if len(arguments) > 1 and arguments[0] == "mark":
            pass

        


    # commandes admin only
    if e.source.nick in self.config.get("admins"):
        if command == "reload":
            self._reload(c)
            return
        if command == "join":
            for chan in arguments:
                c.join(chan)
            return
        if command == "test":
            c.privmsg(destination, str(self.channels))
            return
        # commandes en privé
        if e.type == "privmsg":
            if command == "config":
                c.privmsg(destination, str(self.config))
        # commandes seulement sur un chan
        if e.type == "pubmsg":
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
