# set base image (host OS)
FROM python:alpine

# Environment Settings
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV GEOIP_PATH "/data/geo"

RUN apk add --no-cache \
            --upgrade \
            --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        postgresql-client \
        libpq \
    && apk add --no-cache \
               --upgrade \
               --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
               --virtual .build-deps \
        postgresql-dev \
        zlib-dev jpeg-dev \
        alpine-sdk \
    && apk add --no-cache \
               --upgrade \
               --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        geos \
        proj \
        gdal \
        binutils \
    && ln -s /usr/lib/libproj.so.15 /usr/lib/libproj.so \
    && ln -s /usr/lib/libgdal.so.20 /usr/lib/libgdal.so \
    && ln -s /usr/lib/libgeos_c.so.1 /usr/lib/libgeos_c.so \
    && mkdir /var/run/nginx

# set the working directory in the container
WORKDIR /peaks
# copy the dependencies file to the working directory
COPY requirements.txt .

# copy geip lib
RUN mkdir -p "$GEOIP_PATH"
COPY PEAKY/lib/python3.6/site-packages/geoip2/GeoLite2-City.mmdb "$GEOIP_PATH"
COPY PEAKY/lib/python3.6/site-packages/geoip2/GeoLite2-Country.mmdb "$GEOIP_PATH"

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY PEAKY_API/ .

# command to run on container start
CMD ["python", "./manage.py", "collectstatic", "--no-input"]
CMD ["python", "./manage.py", "makemigrations"]
CMD ["python", "./manage.py", "migrate"]
CMD ["python", "./manage.py", "runserver", "127.0.0.1:8080"]

