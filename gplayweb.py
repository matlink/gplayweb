#! /usr/bin/python2
import tornado.ioloop
import tornado.web
import os
import ConfigParser
from gplaycli.gplaycli import GPlaycli

CONFFILE=os.path.dirname(os.path.abspath(__file__))+"/gplayweb.conf"

class MainHandler(tornado.web.RequestHandler):
	def __init__(self, *args, **kwargs):
		tornado.web.RequestHandler.__init__(self,*args, **kwargs)
		self.cli = GPlaycli(CONFFILE)
		self.cli.connect_to_googleplay_api()
		conffile=CONFFILE
		self.configparser = ConfigParser.ConfigParser()
		self.configparser.read(conffile)
		config = self.configparser.items("Server")
		config_dict = dict()
		for key, value in config:
			config_dict[key] = value
		self.apk_folder = config_dict['folder']
		self.root_url = config_dict['root_url']

	# Routes
	def get(self):
		page = self.get_argument('page',None)
		if page == None:
			self.redirect('page=list')
		elif page == 'list':
			self.list()
		elif page == 'search':
			self.search()
		elif page == 'download':
			self.download()
		elif page == 'remove':
			self.remove()
		elif page == 'downloadfromserver':
			self.download_from_server()
		else:
			return

	def redirect(self,url,permanent=False,status=None):
		super(MainHandler,self).redirect(self.root_url+"?"+url, permanent, status)

	# Templates
	def get_template_path(self):
		return os.path.dirname(os.path.abspath(__file__))+"/templates"

	def render(self,mode, items):
		super(MainHandler,self).render(mode+".html", title="GPlayWeb", ROOT=self.root_url, items=items)
	

	# Core
	def list(self):
		results = self.cli.list_folder_apks(self.apk_folder)
		self.render('list', results)
	def search(self):
		search_string = self.get_argument('name', None)
		if search_string == None:
			self.render('form_search', None)
			return
		number = self.get_argument('number',10)
		results = self.cli.search(list(),search_string,number)
		if results == None:
			results = [["No Result"]]
		self.render('search', results)

	def download(self):
		package = self.get_argument('name', None)
		if package == None:
			self.render('download_ask', None)
			return
		self.cli.set_download_folder(self.apk_folder)
		self.cli.download_packages([package])
		self.redirect('page=list')

	def remove(self):
		filename = self.get_argument('name', None)
		filename = os.path.basename(filename)
		os.remove(os.path.join(self.apk_folder, filename))
		self.redirect('page=list')
	
	def download_from_server(self):
		filename = self.get_argument('name', None)
		base_filename = os.path.basename(filename)
		filename = os.path.join(self.apk_folder, base_filename)
		buf_size = 4096
		self.set_header('Content-Type', 'application/octet-stream')
		self.set_header('Content-Disposition', 'attachment; filename=' + base_filename)
		with open(filename, 'r') as f:
			while True:
				data = f.read(buf_size)
				if not data:
					break
				self.write(data)
		self.finish()

conffile=CONFFILE
configparser = ConfigParser.ConfigParser()
configparser.read(conffile)
config = configparser.items("Server")
config_dict = dict()
for key, value in config:
	config_dict[key] = value
config = config_dict

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
	"root_url": r""+config['root_url'],
	"port": r""+config['port'],
	"ip": r""+config['ip']
}
application = tornado.web.Application([
	(settings['root_url'], MainHandler),
	(r"/static/", tornado.web.StaticFileHandler,
	 dict(path=settings['static_path'])),
], **settings)

if __name__ == "__main__":
	application.listen(settings['port'],settings['ip'])
	tornado.ioloop.IOLoop.current().start()