# build file to configure container for Dockerhub
# Docker cheatsheet https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes

FROM python:3

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

COPY ./telecomsteve /app

WORKDIR /app

# Install Python dependencies
RUN pip3 install -r requirements.txt
RUN pip3 install python-dateutil
RUN pip3 install firebase_admin

# Install JavaScript dependencies
COPY package*.json ./
RUN npm install

ENTRYPOINT [ "python3" ]
CMD [ "application.py" ]
