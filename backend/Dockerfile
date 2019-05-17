FROM python:3.7-alpine
MAINTAINER Benoit Martin "bmartinp@gmail.com"
RUN adduser -D flask
WORKDIR /home/flask
COPY . /home/flask
RUN apk add --no-cache mariadb-connector-c-dev ;\
    apk add --no-cache --virtual .build-deps \
        gcc \
        python-dev \
        libxml2-dev \
        libxslt-dev \
        build-base \
        mariadb-dev ;\
    pip install -r requirements.txt
#    apk del .builddeps
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]
