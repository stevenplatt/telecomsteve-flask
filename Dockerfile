# build file to configure container for Dockerhub
# Docker cheatsheet https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes

FROM ubuntu:20.04

# install dependencies
RUN apt-get update -y && apt-get install -y python3-pip python3-dev
RUN pip3 install --upgrade pip
RUN pip3 install https://github.com/stevenplatt/arxivpy/tarball/master

COPY ./telecomsteve /app

WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "application.py" ]
