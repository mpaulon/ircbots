from geopy.geocoders import Nominatim
from geopy.distance import distance


def locate_addr(value):
	geolocator = Nominatim()
	address, (latitude, longitude) = geolocator.geocode(value)
	return(address, (latitude, longitude))


def dist_2_points(pointA, pointB):
	_, cooA = locate_addr(pointA)
	_, cooB = locate_addr(pointB)
	return(distance(cooA,cooB).km)

def do_command(bot, c, e, COMM_SYMB):
	command = e.arguments[0].split(' ')[0].strip()
	print(command)
	arguments = ' '.join(e.arguments[0].split(' ')[1:]).split(' ! ')
	print(arguments)

	if "{}locate".format(COMM_SYMB) == command and arguments:
		try:
			address, coords = locate_addr(' '.join(arguments[0]))
			c.privmsg(e.target, text='{} {}'.format(address, coords))
		except:
			c.privmsg(e.target, text='Geolocation failed')
	elif "{}dist".format(COMM_SYMB) == command and len(arguments) == 2:
		try:
			dist = dist_2_points(arguments[0], arguments[1])
			c.privmsg(e.target, text='{}km'.format(dist))
		except:
			c.privmsg(e.target, text='Distance calculation failed')
	elif "{}join".format(COMM_SYMB) == command and arguments:
		for chan in arguments:
			c.join(chan)
