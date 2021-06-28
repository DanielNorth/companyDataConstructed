FROM python:3.8-alpine

WORKDIR /application
COPY . .

RUN apk update  && apk add wkhtmltopdf && apk add ttf-dejavu

RUN apk add gcc libc-dev g++ unixodbc-dev gfortran unixodbc mysql-dev openssl-dev libffi-dev freetds freetds-dev xvfb openssl-dev linux-headers

#RUN apk add linux-headers


#RUN python3 -m pip install pyodbc


RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow


RUN pip install pymssql \
  && python3 -m pip install pyodbc \
  && pip install -r requirments.txt


ENTRYPOINT ["python"]
CMD ["run.py"]