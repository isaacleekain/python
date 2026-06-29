FROM python:3.12-slim

# DevContainer 默认用户配置
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

# 安装开发常用系统工具
RUN apt-get update && apt-get install -y \
    git curl ca-certificates build-essential bash sudo \
    && rm -rf /var/lib/apt/lists/*

# 创建普通用户，并允许免密码 sudo
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} \
    && echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

# 添加codex cli的别名到bashrc中
RUN echo '\n# Codex CLI modes' >> /home/${USERNAME}/.bashrc \
    && echo "alias codex-safe='codex --sandbox read-only'" >> /home/${USERNAME}/.bashrc \
    && echo "alias codex-dev='codex --sandbox workspace-write'" >> /home/${USERNAME}/.bashrc \
    && echo "alias codex-full='codex --sandbox danger-full-access --ask-for-approval never'" >> /home/${USERNAME}/.bashrc \
    && chown ${USERNAME}:${USERNAME} /home/${USERNAME}/.bashrc

# 安装 Python 项目管理工具 uv
RUN pip install --no-cache-dir uv

# 设置工作目录
WORKDIR /workspace

# 切换为普通开发用户
USER ${USERNAME}

# 确保用户级命令目录在 PATH 中，可以直接运行 codex 等命令
ENV PATH="/home/${USERNAME}/.local/bin:/home/${USERNAME}/bin:${PATH}"
