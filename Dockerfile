FROM python:3.10 as app

WORKDIR app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY assistant ./assistant

CMD ["python", "main.py"]

#FROM app as dummy

