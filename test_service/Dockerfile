FROM python:2.7
RUN pip install --upgrade pip
RUN pip install flask
RUN mkdir /opt/dummyservice
COPY ./antlion_dummy.py /opt/dummyservice/
WORKDIR /opt/dummyservice/
EXPOSE 5500
CMD ['python', 'antlion_dummy.py']