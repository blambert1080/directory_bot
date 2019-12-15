FROM python:3.8.1-alpine3.10

COPY requirements.txt ./
RUN apk add py-pip python-dev libffi-dev openssl-dev gcc libc-dev make && pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD python3 ./discord_bot.py