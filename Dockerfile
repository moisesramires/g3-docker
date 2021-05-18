FROM python:3.8-slim-buster
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 9595
COPY . .
CMD ["python3", "flapp.py"]
