FROM python:3-alpine

COPY ./requirements.txt /tmp/

RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev build-base \
  && pip install --upgrade pip \
  && pip install -r /tmp/requirements.txt --no-cache-dir \
  && apk del build-dependencies \
  && rm /tmp/requirements.txt

COPY app /app

RUN chmod +x /app/entrypoint.sh

WORKDIR /app

ENV AUTHORIZED_CHAT_IDS=[]

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python3", "/app/rpi-telegram-bot.py"]
