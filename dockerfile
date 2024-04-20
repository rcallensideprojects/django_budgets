# Use an official Python runtime as a parent image
FROM python:3.10.5


# Set environment variables
ENV PYTHONUNBUFFERED 1 \
    DJANGO_SETTINGS_MODULE myproject.settings
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

