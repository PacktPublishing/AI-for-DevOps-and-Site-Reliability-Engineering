FROM python:3.9

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    curl \
    gnupg \
    sudo \
    pkg-config \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app/tfx
RUN chmod -R a+rwx /app/tfx
RUN groupadd -r tfx && useradd -m -r -g tfx tfx
RUN chown -R tfx:tfx /app/tfx

COPY app/ /app/tfx
WORKDIR /app/tfx

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt
RUN chown -R tfx:tfx /home/tfx

USER tfx
CMD ["python3", "tfx_pipeline.py"]