FROM python:3.8.6

ADD . /app

EXPOSE 8000

WORKDIR /app
RUN pip install -r requirements.txt

CMD ["python", "run.py"]
