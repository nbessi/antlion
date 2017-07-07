FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install requests
RUN mkdir /opt/antlion
COPY ./antlion/ /opt/antlion
WORKDIR /opt/antlion
EXPOSE 5000
CMD ['python', 'antlion/antlion.py']