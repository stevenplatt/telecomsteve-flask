# build file to configure container for Dockerhub

FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./telecomsteve/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY ./telecomsteve /app

ENTRYPOINT [ "python3" ]

CMD [ "application.py" ]