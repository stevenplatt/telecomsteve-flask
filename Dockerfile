# build file to configure container for Dockerhub
# Docker cheatsheet https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes

FROM python:3

# Install Node.js and npm
RUN apt-get update && apt-get install -y curl \
    && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs

COPY ./telecomsteve /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install python-dateutil

# Install the Firebase JavaScript SDK
RUN npm install firebase

ENTRYPOINT [ "python3" ]
CMD [ "application.py" ]
