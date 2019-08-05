FROM nginx:1.15.2-alpine

RUN apk add --no-cache \
    supervisor \
    python3 \
    build-base \
    postgresql-dev \
    python3-dev \
    musl-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="${PYTHONPATH}:/app/src" \
    DJANGO_SETTINGS_MODULE="settings.base"

COPY ./src /app/src
COPY ./bin /app/bin

WORKDIR /app/src

RUN pip install --upgrade pip
RUN pip install -r requirements.dev.txt

EXPOSE 8000

CMD [ "/app/bin/entrypoint.sh" ]
