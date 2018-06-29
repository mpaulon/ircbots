import importlib
import irc.bot
import argparse as ap

import commands
import reactions

SRV_LST = [
	irc.bot.ServerSpec('irc.crans.org')
	]

NICK = "Pichu"
REALNAME = "Pichu"
COMM_SYMB = "!"
ADMINS = ["Mikachu", "Mikachu_G"]
CHANS = ["#bots"]

class Bot(irc.bot.SingleServerIRCBot):
	def __init__(self, server_list=SRV_LST,
		nickname=NICK,
		realname=REALNAME,
		channels=CHANS):
		super().__init__(server_list, nickname, realname)
		self.chans_autojoin = channels

	def on_welcome(self, c, e):
		for chan in self.chans_autojoin:
			c.join(chan)
		reactions.on_welcome(self, c, e)

	def on_join(self, c, e):
		reactions.on_join(self, c, e)

	def on_pubmsg(self, c, e):
		if e.arguments[0][0] == COMM_SYMB:
			self.do_command(c, e)
		reactions.on_pubmsg(self, c, e)

	def on_privmsg(self, c, e):
		print(e)
		if e.arguments[0][0] == COMM_SYMB:
			self.do_command(c, e)
		reactions.on_privmsg(self, c, e)

	def on_invite(self, c, e):
		reactions.on_invite(self, c, e)


	def do_command(self, c, e):
		command = e.arguments[0].split(' ')[0].strip()
		if "{}exit".format(COMM_SYMB) == command and e.source.nick in ADMINS and e.type == 'privmsg':
			exit(0)
		elif "{}reload".format(COMM_SYMB) == command:
			try:
				importlib.reload(commands)
				importlib.reload(reactions)
				if e.type == 'privmsg':
					c.notice(e.source.nick, text="config reloaded")
				else:
					c.notice(e.target, text="config reloaded")
			except:
				if e.type == 'privmsg':
					c.notice(e.source.nick, text="reload failed")
				else:
					c.notice(e.target, text="reload failed")
		else:
			print("plop")
			commands.do_command(self, c, e, COMM_SYMB)





if __name__ == "__main__":
	parser = ap.ArgumentParser(description='Todo list')
	parser.add_argument('-s', '--server')
	parser.add_argument('-p', '--port')
	parser.add_argument('-c', '--chan')
	parser.add_argument('-n', '--nick')
	parser.add_argument('-r', '--realname')

	args = parser.parse_args()



bot = Bot(
	server_list=[irc.bot.ServerSpec(args.server)],
	nickname=args.nick,
	realname=args.realname,
	channels=[
		args.chan
		])
bot.start()

