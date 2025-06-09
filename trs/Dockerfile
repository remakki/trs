FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY uv.lock pyproject.toml ./

RUN uv sync

COPY . .

CMD ["uv", "run", "python", "-m", "src.main"]
