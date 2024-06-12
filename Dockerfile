FROM python:3.10.4-slim

LABEL RPG Dashboard Service

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    bind9utils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "rpg_dashboard_service.wsgi:application"]
