# build file to configure container for Dockerhub
# Docker cheatsheet https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes

FROM ubuntu:20.04

# install dependencies
RUN apt-get update -y && apt-get install -y python3-pip python3-dev git
RUN pip3 install --upgrade pip
RUN pip3 install git+https://github.com/stevenplatt/arxivpy

# mount login credentials as ENV values within docker image
# source: https://andrei-calazans.com/posts/2021-06-23/passing-secrets-github-actions-docker
RUN --mount=type=secret,id=USERNAME
RUN --mount=type=secret,id=PASSWORD
RUN export USERNAME=$(cat /run/secrets/USERNAME)
RUN export PASSWORD=$(cat /run/secrets/PASSWORD)

COPY ./telecomsteve /app

WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "application.py" ]