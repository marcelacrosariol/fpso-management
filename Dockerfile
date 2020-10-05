FROM python:3.7-alpine
LABEL author="Marcela Crosariol"

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /app
COPY ./app /app
WORKDIR /app

RUN python manage.py collectstatic --noinput

# evitar o uso de um usuário com privilégios de root
RUN adduser -D user
USER user