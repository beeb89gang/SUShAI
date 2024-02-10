FROM python:3.9-slim-bullseye

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]
