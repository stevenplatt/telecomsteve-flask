# build file to configure container for Dockerhub
# Docker cheatsheet https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes

FROM ubuntu:20.04

RUN apt-get update -y \
    && apt-get install -y python3-pip python3-dev \

RUN git clone https://github.com/stevenplatt/arxivpy
RUN cd arxivpy
RUN python3 setup.py install
RUN cd ../

# We copy just the requirements.txt first to leverage Docker cache
COPY ./telecomsteve/requirements.txt /app/requirements.txt

WORKDIR /app

COPY ./telecomsteve /app

ENTRYPOINT [ "python3" ]

CMD [ "application.py" ]