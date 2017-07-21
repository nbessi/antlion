FROM python:3.6.2
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install requests
RUN pip install gevent
RUN pip install gunicorn

RUN mkdir /opt/antlion
COPY ./antlion/ /opt/antlion
WORKDIR /opt/antlion
EXPOSE 5000
CMD ['gunicorn', '-w6 antlion:app  -b 127.0.0.1:5000']