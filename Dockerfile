FROM ubuntu:18.04
MAINTAINER Francois-Xavier Aguessy <fxaguessy@users.noreply.github.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:guardianproject/ppa
RUN apt-get update && apt-get install -y \
	fdroidserver \
	git \
	lib32stdc++6 \
	lib32gcc1 \
	lib32z1 \
	lib32ncurses5 \
	libffi-dev \
	libssl-dev \
	libjpeg-dev \
	locales \
	python-dev \
	python-pip \
	python3 \
	python3-pip \
	openjdk-8-jdk \
	virtualenv \
	wget \
	zlib1g-dev

RUN apt-get clean

RUN locale-gen en_US.UTF-8
RUN echo -e "LC_ALL=en_US.UTF8\nLANG=en_US.UTF8\nLC_CTYPE=en_US.UTF8\nLC_COLLATE=en_US.UTF8" > /etc/default/locale
RUN chmod 0755 /etc/default/locale
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

RUN mkdir -p /data/fdroid/repo

# Install gplayweb
RUN git clone https://github.com/matlink/gplayweb.git /opt/gplayweb
WORKDIR /opt/gplayweb
RUN pip install -r requirements.txt

# Install Android SDK and build tools 22
WORKDIR /opt/
RUN wget https://dl.google.com/android/android-sdk_r24.3.4-linux.tgz \
    && echo "fb293d7bca42e05580be56b1adc22055d46603dd  android-sdk_r24.3.4-linux.tgz" | sha1sum -c \
    && tar xzf android-sdk_r24.3.4-linux.tgz \
    && rm android-sdk_r24.3.4-linux.tgz

ENV ANDROID_HOME=/opt/android-sdk-linux
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
RUN echo 'y' | android update sdk --no-ui -a --filter platform-tools,build-tools-22.0.1,android-22

COPY ./gplayweb.conf.example /etc/gplayweb/gplayweb.conf

VOLUME /data/fdroid
WORKDIR /data/fdroid
CMD /opt/gplayweb/gplayweb
