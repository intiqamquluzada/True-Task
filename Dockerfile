FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y chromium-driver chromium
RUN pip install django-celery-beat
RUN pip install -r requirements.txt
