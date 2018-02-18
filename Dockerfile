FROM ubuntu

RUN apt-get update && apt-get install -y git python3 nano python3-pip zsh
RUN pip3 install tensorflow keras autobahn image numpy h5py
RUN apt-get install -y python3-pil

WORKDIR /media/
ENTRYPOINT python3 api_py_websocket.py

#ENTRYPOINT while true; do echo "y" > /dev/null; done
