# build file to configure container for deployment

FROM python:3

COPY . /app

WORKDIR /app

RUN pip3 install -r ./.devcontainer/requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "application.py" ]