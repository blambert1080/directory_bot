FROM python:3.7.4-alpine3.10

ARG DIR_USERNAME
ENV DIR_USERNAME=${DIR_USERNAME}
ARG SECRET_PASS
ENV SECRET_PASS=${SECRET_PASS}
ARG DIR_BOT_TOKEN
ENV DIR_BOT_TOKEN=${DIR_BOT_TOKEN}
ARG DIR_BOT_URL
ENV DIR_BOT_URL=${DIR_BOT_URL}
ARG TEST
ENV TEST=${TEST}}

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "echo", "$TEST"] && [ "python", "./discord_bot.py" ]