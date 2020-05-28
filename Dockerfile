# Base image
FROM python:3.8.2-alpine3.11

# Add a token argument
ARG DB_HOST
ARG DB_USER
ARG DB_NAME
ARG DB_PASSWORD


# Working directory
WORKDIR /www/api

# Copy the app to working directory
COPY . ./

# Upgrade pip
RUN pip3 install --upgrade pip

# RUN pip3 install virtualenv
# RUN virtualenv env
# RUN source env/bin/activate

# Run install the modules
RUN set -e; \
  apk update \
  && apk add --virtual .build-deps gcc python3-dev musl-dev libffi-dev \
  && pip3 install --no-cache-dir -r requirements.txt \
  && apk del .build-deps

# Database environment during build
ENV DB_HOST=${DB_HOST}
ENV DB_USER=${DB_USER}
ENV DB_NAME=${DB_NAME}
ENV DB_PASSWORD=${DB_PASSWORD}


# Export port 80
EXPOSE 80


# Run
CMD ["python3","main.py"]
