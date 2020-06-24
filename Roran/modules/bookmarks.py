import datetime
import re


def start():
    return


def stop():
    return


def apply_command(self, c, e, command, arguments):
    destination = e.target if e.type == "pubmsg" else e.source.nick
    if command == "mark":
        # format commande: !mark [tag] http...URL... [commentaire]*
        # format ligne: [tag] http...URL... ## commentaires ## e.source.nick ## datetime.datetime.now
        tag = ""
        comments = ""
        url = None
        if len(arguments) >= 1:
            if arguments[0].startswith("http"):
                url = arguments[0]
                if len(arguments) >= 2:
                    comments = " ".join(arguments[1:])
            elif len(arguments) >= 2 and arguments[1].startswith("http"):
                tag = f"[{arguments[0]}]"
                url = arguments[1]
                if len(arguments) >= 3:
                    comments = " ".join(arguments[2:])
            if url is not None:
                if "##" in e.arguments[0]:
                    c.privmsg(destination, "Sorry, ## is not accepted in bookmarks for technical reasons")
                    return
                with open("files/core/marks.txt", "r") as bookmarks:
                    regex = re.compile(" "+url+" ")
                    for line in bookmarks:
                        if regex.search(line):
                            c.privmsg(destination, f"Bookmark already registered")
                            line = line.split("##")
                            c.privmsg(
                                destination,
                                f"{line[0].strip()+' '}{line[1].strip()+' '}~ {line[2].strip()} ({line[3].strip()} {line[4].strip()})")
                            return
                with open("files/core/marks.txt", "a") as bookmarks:
                    self.logger.debug(f"Saving bookmark {url}")
                    bookmarks.write(f"{tag} {url} ## {comments} ## {e.source.nick} ## {destination} ## {datetime.datetime.now()}\n")
                    c.privmsg(destination, "Bookmark saved")
    if command == "search":
        if len(arguments) > 1 and arguments[0] == "mark":
            try:
                regex = re.compile(" ".join(arguments[1:]))
            except re.error:
                c.privmsg(destination, "Invalid regex")
                return
            with open("files/core/marks.txt", "r") as bookmarks:
                for line in bookmarks:
                    if regex.search(line):
                        line = line.split("##")
                        c.privmsg(
                            destination,
                            f"{line[0].strip()+' '}{line[1].lstrip()}~ {line[2].strip()} ({line[3].strip()} {line[4].strip()})")


def on_welcome(self, c, e):
    pass


def on_invite(self, c, e):
    pass


def on_join(self, c, e):
    pass


def on_namreply(self, c, e):
    pass


def on_pubmsg(self, c, e):
    pass


def on_privmsg(self, c, e):
    pass
