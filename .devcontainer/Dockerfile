FROM python:3.12-slim

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

RUN apt-get update && apt-get install -y \
    git curl ca-certificates build-essential sudo \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} \
    && echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME} \
    && mkdir -p /home/${USERNAME}/.cache/uv \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.cache

RUN pip install --no-cache-dir uv

USER ${USERNAME}
ENV PATH="/home/${USERNAME}/.local/bin:/home/${USERNAME}/bin:${PATH}"
ENV UV_CACHE_DIR="/home/${USERNAME}/.cache/uv"

RUN curl -fsSL https://chatgpt.com/codex/install.sh | sh

WORKDIR /workspace
