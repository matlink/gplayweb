#! /usr/bin/python2
import tornado.ioloop
import tornado.web
import os
import ConfigParser, argparse
from gplaycli.gplaycli import GPlaycli

# Main handler
class MainHandler(tornado.web.RequestHandler):
	def __init__(self, *args, **kwargs):
		tornado.web.RequestHandler.__init__(self,*args, **kwargs)
		# Parsing conffile
		self.cli = GPlaycli(cli_args.CONFFILE)
		# Connect to API
		self.cli.connect_to_googleplay_api()
		# Get conf
		# Where apk are stored
		self.apk_folder = config['folder']
		if not os.path.isdir(self.apk_folder):
			os.mkdir(self.apk_folder)
		# Root of the HTTP URL
		self.root_url = config['root_url']

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

	def render(self, mode, items, **kwargs):
		super(MainHandler,self).render(mode+".html", title="GPlayWeb", ROOT=self.root_url, items=items, **kwargs)
	

	# Core
	# Show the list of downloaded apks
	def list(self):
		results = self.cli.list_folder_apks(self.apk_folder)
		self.render('list', results)

	# Search an apk by string
	def search(self):
		search_string = self.get_argument('name', None)
		if search_string == None:
			self.render('form_search', None)
			return
		number = self.get_argument('number',10)
		results = self.cli.search(list(),search_string,number)
		if results == None:
			results = [["No Result"]]
		self.render('search', results, string=search_string, number=number)

	# Download an apk by codename to the server (org.mozilla.firefox)
	def download(self):
		package = self.get_argument('name', None)
		if package == None:
			self.render('download_ask', None)
			return
		self.cli.set_download_folder(self.apk_folder)
		self.cli.download_packages([package])
		self.redirect('page=list')

	# Remove the apk from the folder
	def remove(self):
		filename = self.get_argument('name', None)
		filename = os.path.basename(filename)
		os.remove(os.path.join(self.apk_folder, filename))
		self.redirect('page=list')
	
	# Download the available apk from the server
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

def default_params():
	config = {
		'ip': '0.0.0.0',
		'port': '8888',
		'root_url': '/',
		'folder': 'repo',
	}
	return config

# Parsing CLI arguments
parser = argparse.ArgumentParser(description="A web interface for GPlayCli")
parser.add_argument('-c','--config',action='store',dest='CONFFILE',metavar="CONF_FILE",nargs=1,
		type=str,default=os.path.dirname(os.path.abspath(__file__))+"/gplayweb.conf",
		help="Use a different config file than gplayweb.conf")
cli_args = parser.parse_args()
configparser = ConfigParser.ConfigParser()
configparser.read(cli_args.CONFFILE)
config_list = configparser.items("Server")
# Get default params
config = default_params()
# Override default params
for key, value in config_list:
	config[key] = value

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