FROM  debian:latest

ARG CONFIGPATH
ENV CTMETROBOT_REPO    https://github.com/Warcreed/Telegram-CTMetro-Bot
ENV CTMETROBOT_DIR    /usr/local

RUN apt-get update && \
  apt-get install -y \
	git \	
	python3 \
	python3-pip
	
RUN mkdir -p $CTMETROBOT_DIR && \
  cd $CTMETROBOT_DIR && \
  git clone -b master $CTMETROBOT_REPO ctmetrobot

RUN pip3 install -r $CTMETROBOT_DIR/ctmetrobot/requirements.txt

COPY $CONFIGPATH $CTMETROBOT_DIR/ctmetrobot/config