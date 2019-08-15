FROM python:3.7.4-alpine3.10

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python ./discord_bot.py