FROM python:2.7
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install requests
RUN mkdir /opt/antlion
COPY ./antlion/ /opt/antlion
WORKDIR /opt/antlion
EXPOSE 5000
CMD ['python', 'antlion/antlion.py']