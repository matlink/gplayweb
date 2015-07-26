GPlayWeb: A Web interface for GPlayCli
======================================

Screenshot(s)
-------------

![alt](https://pic.matlink.fr/8RApkXw7/QPjlfSbX)

Installation (consider using a virtualenv)
------------------------------------------
It requires [GPlayCli](https://github.com/matlink/gplaycli), but will be added automatically if you clone this repo recursively.

- Clone this repo recursively for submodules (gplaycli) : 

		$ git clone https://github.com/matlink/gplayweb --recursive 
- Install `gplaycli` requirements : 

 		# apt-get install python-dev python-pip libffi-dev
		$ pip install -r gplaycli/requirements.txt

- Install `gplayweb` requirements with `pip` :
	
		$ pip install -r requirements.txt
- Copy `gplayweb.conf.example` to `gplayweb.conf` and change the settings (you can comment unwanted lines out with #)
- If you plan to add compatibility with F-Droid repo, ensure that you use [my fork of fdroidserver](https://github.com/matlink/fdroidserver) since the original, for now, doesn't support call from another Python script (it's only usable via command line)
		

Usage
-----

	$ ./gplayweb.py -h
	usage: gplayweb.py [-h] [-c CONF_FILE]

	A web interface for GPlayCli

	optional arguments:
	  -h, --help            show this help message and exit
	  -c CONF_FILE, --config CONF_FILE
	                        Use a different config file than gplayweb.conf

LSB script
----------
Change `PROGRAM_HOME` in the init script to match your `gplayweb`'s folder location, and `USER` for the user which will run the daemon.

	$ /etc/init.d/gplayweb {start|stop|restart|status}
