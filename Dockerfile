# build file to configure container for Dockerhub

FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./flask_app/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY ./flask_app /app

# ENTRYPOINT [ "python3" ]

# start flask process and push it to the background
# https://www.py4u.net/discuss/159302
# search for background process by port number "lsof -i :[port number]"
# kill corresponding process "kill -9 [PID]"
CMD [ "python3 app.py > log.txt 2>&1 &" ]