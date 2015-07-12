GPlayWeb: A Web interface for GPlayCli
======================================

Screenshot(s)
-------------

![alt](https://pic.matlink.fr/Uc0u57eC/u8iQf5Mc]

Installation (consider using a virtualenv)
------------------------------------------

- First of all, you need [GPlayCli](https://github.com/matlink/gplaycli).
- Then, clone this repo : 

		git clone https://github.com/matlink/gplayweb

- Copy `gplaycli` in `gplayweb`'s folder to make this module available for `gplayweb`.
- Install `tornado` with `pip` :
	
		pip install tornado

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
