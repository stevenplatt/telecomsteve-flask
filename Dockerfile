# build file to configure container for Dockerhub
# Docker cheatsheet https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes

FROM python:3

COPY ./telecomsteve /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install python-dateutil
RUN pip3 install firebase_admin

ENTRYPOINT [ "python3" ]
CMD [ "application.py" ]
