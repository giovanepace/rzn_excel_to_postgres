FROM python:3.7.6-buster
# set work directory
WORKDIR /usr/src/app
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# install dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade cython
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
# copy project
COPY . /usr/src/app/
RUN ls -la app/
RUN cd app
ENTRYPOINT ["scripts/entrypoint.sh"]