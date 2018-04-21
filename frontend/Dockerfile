FROM node

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    npm install -g yarn gulp bower polymer-cli --unsafe-perm

RUN apt-get install git

RUN git clone https://github.com/leolabs/ip-ml-frontend

WORKDIR /ip-ml-frontend

RUN yarn && bower i --allow-root

ENTRYPOINT polymer serve -H 0.0.0.0
