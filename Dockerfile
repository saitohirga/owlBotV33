FROM gorialis/discord.py:3.11.2-bullseye-master-extras

COPY . /app
WORKDIR /app

ENV PYTHON_BIN python3

RUN \
    apt-get update && \
    echo "**** install runtime packages ****" && \
    apt-get install -y --no-install-recommends \
        libxml2-dev \
        libxslt1-dev \
        && \
    echo "**** install pip packages ****" && \
    pip3 install -U pip setuptools wheel && \
    pip3 install -r requirements.txt && \
    echo "**** clean up ****" && \
    rm -rf \
        /root/.cache \
        /tmp/* \
        /var/lib/apt/lists/*

CMD ["/bin/sh", "run.sh", "--pass-errors", "--no-botenv"]
