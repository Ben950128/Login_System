FROM ben950128/python3.9.13-slim_psycopg3:1.0

COPY ./requirements.txt /

RUN pip install -r /requirements.txt

ENV TZ="Asia/Taipei"