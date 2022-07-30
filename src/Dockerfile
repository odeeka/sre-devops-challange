FROM python:3.8-slim-buster

WORKDIR /app

RUN python3 -m pip install --upgrade pip

#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt

COPY . .

RUN pip3 install -e .

#ENV FLASK_APP=run
#ENV FLASK_ENV=development
#CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]

CMD [ "python3","run.py" ]