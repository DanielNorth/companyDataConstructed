FROM python:3.8-alpine

WORKDIR /application
COPY . .

RUN apk update \
  && apk add gcc libc-dev g++ \
  && apk add unixodbc-dev \
  && apk add gfortran \
  && apk add unixodbc

RUN apk add linux-headers
RUN apk add libffi-dev
RUN apk add openssl-dev
RUN apk add mysql-dev
RUN apk add openssl-dev

RUN apk add xvfb
RUN apk add --no-cache wkhtmltopdf

RUN apk add freetds freetds-dev
RUN pip install pymssql

RUN python3 -m pip install pyodbc
#RUN pip install apache-airflow[pymssql]


RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow



RUN pip install -r requirments.txt

ENTRYPOINT ["python"]
CMD ["run.py"]