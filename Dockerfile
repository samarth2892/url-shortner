FROM python:3.6.4-slim-jessie

RUN pip install pandas
RUN pip install CherryPy
RUN pip install mysql-connector-python
RUN pip install python-baseconv

ADD ./src /

EXPOSE 8888

ENTRYPOINT ["python", "api.py"]