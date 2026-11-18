FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8006 \
    DATA_DIR=/data

RUN groupadd --gid 10006 appgroup && \
    useradd --uid 10006 --gid appgroup --no-create-home --shell /usr/sbin/nologin appuser && \
    mkdir -p /data && \
    chown -R appuser:appgroup /data

COPY app.py ./

USER appuser

VOLUME /data

EXPOSE 8006

CMD ["python", "app.py"]