FROM python:3.8

ADD . .


RUN pip install --upgrade pip
RUN pip install -r requirments.txt

CMD ["python", "./run.py" ]