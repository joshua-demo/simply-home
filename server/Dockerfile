FROM python:3.12-slim

WORKDIR /server

RUN apt-get update

COPY ./server/requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "run.py"]