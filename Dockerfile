FROM python:3.11.3

WORKDIR /ultimeet

COPY . /ultimeet/

EXPOSE 8000


RUN pip install -r requirements.txt

CMD ["python3", "manage.py", "runserver"]
