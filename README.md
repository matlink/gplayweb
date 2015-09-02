GPlayWeb: A Web interface for GPlayCli
======================================

Screenshot(s)
-------------

![alt](https://pic.matlink.fr/8RApkXw7/QPjlfSbX)

Installation (consider using a virtualenv)
=========================================
For both methods, you'll need those packages
 		
	# apt-get install python-dev python-pip libffi-dev

pip method
----------
Use `pip install gplayweb` to install it. If you got a SandboxViolation for gplaycli, install it before with `pip install gplaycli`.
After that, rename /etc/gplayweb/gplayweb.conf.example to /etc/gplayweb/gplayweb.conf and change parameters.

git method
----------
It requires [GPlayCli](https://github.com/matlink/gplaycli), but will be added automatically if you clone this repo recursively.

- Clone this repo recursively for submodules (gplaycli) : 

		$ git clone https://github.com/matlink/gplayweb --recursive 

- Install `gplaycli` requirements : 

		$ pip install -r gplaycli/requirements.txt

- Install `gplayweb` requirements with `pip` :
	
		$ pip install -r requirements.txt

- Copy `gplayweb.conf.example` to `gplayweb.conf` and change the settings (you can comment unwanted lines out with #)
- If you plan to add compatibility with F-Droid repo, ensure that you use [my fork of fdroidserver](https://github.com/matlink/fdroidserver) since the original, for now, doesn't support call from another Python script (it's only usable via command line)
		

Usage
-----

	$ ./gplayweb -h
	usage: gplayweb.py [-h] [-c CONF_FILE]

	A web interface for GPlayCli

	optional arguments:
	  -h, --help            show this help message and exit
	  -c CONF_FILE, --config CONF_FILE
	                        Use a different config file than gplayweb.conf

FDroid Compatibility
====================
Based on https://f-droid.org/wiki/page/Installing_the_Server_and_Repo_Tools

* create user gplayweb : `adduser gplayweb --disabled-password`
* go to /opt directory : `cd /opt`
* get android SDK : `wget https://dl.google.com/android/android-sdk_r24.3.4-linux.tgz`
* untar it : `tar xvfz android-sdk_r24.3.4-linux.tgz`
* give it to gplayweb : `chown gplayweb android-sdk-linux -R`
* put ANDROID_HOME env variable to your .bashrc : `echo export ANDROID_HOME=/opt/android-sdk-linux >> ~/.bashrc`
* put android tools to your PATH variable : `echo 'export PATH=$PATH:$ANDROID_HOME/tools' >> ~/.bashrc`
* reload .bashrc : `source ~/.bashrc`
* if you don't have java (`java -version`) : `apt-get install openjdk-7-jdk`
* install Android 22 SDK : `android update sdk --no-ui -a --filter 4`
* install platform-tools : `android update sdk --no-ui --filter platform-tools`
* clone fdroidserver : `cd /opt && git clone https://github.com/matlink/fdroidserver && cd fdroidserver`
* install fdroidserver : `python setup.py install`
* go to the folder where you want to host your fdroid repo : `cd /opt/gplayweb`
* give it to gplayweb : `chown gplayweb . -R`
* for android aapt to work, you need these packages : `apt-get install lib32stdc++6 lib32z1`
* initialize fdroid repo : `fdroid init`
* then in /etc/gplayweb/gplayweb.conf : 
	
	folder=/opt/gplayweb/repo

	fdroid_repo_dir=/opt/gplayweb

	fdroid_script_dir=/opt/fdroidserver

LSB script
----------
It might still be a bit buggy.
Change `USER` for the user which will run the daemon (gplayweb in this example), and `ANDROID_SDK` for the path of the android-sdk you have configured earlier (/opt/android-sdk-linux in this example).

	$ /etc/init.d/gplayweb {start|stop|restart|status}

Please me hard enough if you want a systemd unit :D

Uninstall
=========
Use `pip uninstall gplayweb`, and remove conf, templates and static files with `rm -rf /etc/gplayweb /usr/share/gplayweb`. Should be clean, except python dependancies for gplayweb and gplaycli.
