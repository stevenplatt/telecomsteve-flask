# build file to configure container for deployment

FROM python:3.10-slim

COPY . /app

WORKDIR /app

RUN pip3 install -r ./.devcontainer/requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "application.py" ]