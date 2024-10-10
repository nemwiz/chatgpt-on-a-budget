FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends curl vim python3.12 python3-pip python3.12-venv python3.12-dev openssl jq gcc git-all ca-certificates && update-ca-certificates \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

CMD ["sleep", "infinity"]
