# FROM python:3.9-alpine
FROM ubuntu:latest
WORKDIR /app
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
RUN apt update && apt install -y gcc musl-dev 
RUN apt install -y python3-pip
COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3", "/app/dash_app.py"]