import miniflux
import const

client = miniflux.Client(const.MINIFLUX_URL, const.MINIFLUX_USER, const.MINIFLUX_PASS)

feeds = client.get_feeds()

def get_feeds_num():
	return len(feeds)

def discover(url):
	if not url.startswith('http'):
		url = 'http://'+url
	return client.discover(url)

def create_feed(url):
	feedid = -1
	state = ''
	try:
		feedid = client.create_feed(url, 6)
		state = 'ok'
	except miniflux.ClientError as e:
		state = 'error '+ str(e.get_error_reason())
	return feedid,state

def get_latest_entry_id():
	entries =  client.get_entries(status = "unread", limit = 1, order='id', direction = 'asc')
	if len(entries) == 0:
		entries =  client.get_entries(status = "read", limit = 1, order='id', direction = 'asc')
	return entries['entries'][0]['id']-1

def get_entries(after_entry_id):
	if after_entry_id == None:
		return []
	entries =  client.get_entries(status = "unread", limit = 10, order='id', direction = 'asc', after_entry_id=after_entry_id)
	return entries['entries']

def markread(entryid):
	client.update_entries([entryid],'read')

def markunread(entryid):
	client.update_entries([entryid],'unread')

def markstar(entryid):
	os.system('echo %d >> stared.txt'%entryid)
	pass

def markunstar(entryid):
	pass




