FROM python:latest
COPY ./FlaskApp /FlaskApp 
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
WORKDIR /FlaskApp
CMD ["python","/FlaskApp/app.py"]
