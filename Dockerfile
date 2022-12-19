# pull official base image
FROM python:3.10-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
  apt-get install -y \
    netcat gettext

# install dependencies
RUN pip install --no-cache --upgrade pip
COPY ./requirements.txt .
RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt

RUN useradd -ms /bin/bash app
# create the appropriate directories

ENV HOME=/home/app
ENV APP_HOME=/home/app/web

RUN mkdir -p $APP_HOME /static /media /uploads/tmp /uploads/final

WORKDIR $APP_HOME

# copy project
COPY --chown=app:app . $APP_HOME

RUN chown -R app:app /static /media /uploads

# change to the app user
USER app

RUN python manage.py compilemessages && python manage.py collectstatic

ENTRYPOINT ["/home/app/web/entrypoint.sh"]

CMD uvicorn --host 0.0.0.0 --port 8000 core.asgi:application 
