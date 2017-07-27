FROM python:3.6.2
RUN pip install --upgrade pip
RUN pip install gevent
RUN pip install gunicorn

RUN mkdir /opt/antlion
COPY . /opt/antlion
WORKDIR /opt/antlion
RUN python setup.py develop
EXPOSE 5000
CMD ['gunicorn', '-w6', '-b 0.0.0.0:5000', 'antlion.antlion:app' ]