GPlayWeb: A Web interface for GPlayCli
======================================

Original work of [@matlink](https://github.com/matlink) forked to use latest versions of fdroid and gplaycli and providing a Dockerfile for easy install.

Docker install (gplayweb + fdroid)
=================================

First, [install docker](https://docs.docker.com/engine/installation/).

Then, to use the last version of container on dockerhub:

    docker run --name gplayweb -p 127.0.0.1:8888:8888 matlink/gplayweb

You can also build the container yourself

    docker build -t gplayweb .

Then run it

    docker run --name gplayweb -p 127.0.0.1::8888:8888 gplayweb

To preserve gplayweb and fdroid data, mount a local folder as docker volume:

    docker run --name gplayweb -p 127.0.0.1:8888:8888 -v ~/fdroid/:/data/fdroid matlink/gplayweb

Then, you may want to expose your (static) fdroid repo using a nginx container

    docker run --name fdroid-nginx -p 8080:80 -v ~/fdroid/repo:/usr/share/nginx/html:ro nginx

As a result, you can access gplayweb on localhost and the fdroid repository on your.ip.address:8080.

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

- Clone this repo:

		$ git clone https://github.com/matlink/gplayweb

- Install `gplayweb` requirements with `pip` :
	
		$ pip install -r requirements.txt

- Copy `gplayweb.conf.example` to `gplayweb.conf` and change the settings (you can comment unwanted lines out with #)
- If you plan to add compatibility with F-Droid repo, ensure to uncomment the two config variables `fdroid_repo_dir` and `fdroid_exec`.
		

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
python-imaging may be needed to update FDroid repository, don't forget to install it.

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
* clone fdroidserver : `cd /opt && git clone https://gitlab.com/fdroid/fdroidserver.git && cd fdroidserver`
* install fdroidserver : `sudo apt-get install fdroidserver`
* go to the folder where you want to host your fdroid repo : `cd /opt/fdroid/`
* give it to gplayweb : `chown gplayweb . -R`
* for android aapt to work, you need these packages : `apt-get install lib32stdc++6 lib32z1`
* initialize fdroid repo : `fdroid init`
* then in /etc/gplayweb/gplayweb.conf : 
	
	folder=/opt/fdroid/repo

	fdroid_repo_dir=/opt/fdroid

	fdroid_exec=/usr/local/bin/fdroid

LSB script
----------
It might still be a bit buggy.
Change `USER` for the user which will run the daemon (gplayweb in this example), and `ANDROID_SDK` for the path of the android-sdk you have configured earlier (/opt/android-sdk-linux in this example).

	$ /etc/init.d/gplayweb {start|stop|restart|status}

Please me hard enough if you want a systemd unit :D

Uninstall
=========
Use `pip uninstall gplayweb`, and remove conf, templates and static files with `rm -rf /etc/gplayweb /usr/share/gplayweb`. Should be clean, except python dependancies for gplayweb and gplaycli.
