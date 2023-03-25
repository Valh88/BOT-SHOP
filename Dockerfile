FROM python:3.9-buster
ENV BOT_NAME=$BOT_NAME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"

COPY requirements.txt /usr/src/app/
# COPY alembic /usr/src/app/
# COPY alembic.ini /usr/src/app/
RUN pip install -r /usr/src/app/requirements.txt
# COPY tgbot /usr/src/app/"${BOT_NAME:-tg_bot}"
