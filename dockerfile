FROM python:slim

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install "django<5" gunicorn

COPY src /src

WORKDIR /src
ENV DJANGO_DEBUG_FALSE=1
CMD gunicorn --bind :8888 superlists.wsgi:application