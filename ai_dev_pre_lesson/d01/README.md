# EIV AI Python Template
A Python AI development template powered by uv, Docker, DevContainer, and VS Code.
# 开发规范

本项目采用：

```text
Windows
↓
WSL
↓
VS Code Remote WSL
↓
Dev Container
↓
uv
↓
Python
```

开发模式。

---

## 目录规范

### 项目目录

所有项目统一存放于：

```text
/home/<user>/projects
```

例如：

```text
/home/isaacleekain/projects/workspaces_vscode/github/eiv/eiv-docker-template
```

禁止：

```text
D:\Project\xxx
```

直接作为开发目录。

原因：

* 文件监听更稳定
* Git 更快
* Docker 更快
* uv 更快
* Dev Container 更稳定

---

## Git 规范

### Git 运行位置

Git 统一在 WSL 中运行。

推荐：

```bash
git status
git pull
git push
git checkout
git switch
```

均在 WSL 终端执行。

原则：

```text
WSL负责代码管理
Container负责代码运行
```

---

### 分支规范

禁止直接向 main 提交。

开发流程：

```text
main
 └── feature/xxx

main
 └── fix/xxx

main
 └── refactor/xxx
```

示例：

```bash
git switch -c feature/user-login
```

```bash
git switch -c fix/jwt-expire
```

```bash
git switch -c refactor/project-structure
```

---

### Commit 规范

推荐：

```text
feature: 新功能
fix: 修复问题
refactor: 重构
docs: 文档
test: 测试
chore: 配置修改
```

示例：

```bash
git commit -m "feature: add user login"
```

```bash
git commit -m "fix: resolve jwt validation bug"
```

```bash
git commit -m "docs: update readme"
```

---

## Python 规范

### Python 运行位置

统一在 Dev Container 中运行。

禁止：

```text
WSL Python
Windows Python
```

直接参与项目运行。

原则：

```text
项目运行环境必须来自 Container
```

---

### 虚拟环境

统一使用：

```text
uv
```

管理。

禁止：

```bash
pip install
python -m venv
```

创建独立环境。

统一使用：

```bash
uv sync
```

---

### 运行程序

推荐：

```bash
uv run python app/main.py
uv run fastapi dev app/main.py
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

```bash
uv run pytest
```

不强制：

```bash
source .venv/bin/activate
```

因为 uv 会自动处理虚拟环境。

---

## 依赖管理规范

### 新增依赖

```bash
uv add package-name
```

---

### 删除依赖

```bash
uv remove package-name
```

---

### 更新锁文件

```bash
uv lock
```

---

### 同步环境

```bash
uv sync
```

---

## uv.lock 规范

必须提交：

```text
uv.lock
```

原因：

* 保证团队环境一致
* 保证 CI/CD 环境一致
* 保证测试结果一致

禁止忽略：

```gitignore
uv.lock
```

---

## Git Ignore 规范

必须忽略：

```gitignore
.venv/
.pytest_cache/
__pycache__/
*.pyc
.env
```

禁止提交：

```text
虚拟环境
缓存文件
临时文件
密钥文件
```

---

## Dev Container 规范

所有 Python 项目必须支持：

```text
Reopen in Container
```

原则：

```text
新成员 Clone
↓
Open Folder
↓
Reopen in Container
↓
uv sync
↓
立即开始开发
```

无需额外配置。

---

## SSH 规范

SSH Key 统一存放：

```text
~/.ssh
```

推荐：

```text
id_rsa_github_eiv
id_rsa_github_personal
id_rsa_azuredevops
```

使用 SSH Config 管理：

```ssh
Host github-eiv
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa_github_eiv
```

---

## Codex 规范

Codex CLI 统一在 WSL 中运行：

```bash
codex
```

推荐：

```bash
cd <project-root>
codex
```

禁止：

```text
在 Windows 原生目录运行 Codex
```

---

## 项目创建规范

新项目必须从模板复制：

```bash
cp -r eiv-docker-template my-project
```

禁止：

```text
从零手工搭建开发环境
```

所有项目保持统一结构。

---

## 核心原则

```text
Git 在 WSL

SSH 在 WSL

Codex 在 WSL

Docker 在 WSL

Python 在 Container

uv 在 Container

测试在 Container

运行在 Container
```

保持开发环境一致性优先于个人习惯。


## 安全边界
```text
WSL:
- git pull / git push
- 保存 ~/.ssh

DevContainer:
- /workspace 开发
- uv / python / pytest
- codex danger-full-access
- 不挂 ~/.ssh
```


## Branch Naming

Use the following format:

```text
<type>/<short-description>

Examples:
feature/add-fastapi-app
fix/devcontainer-workspace-mount
docs/update-readme
chore/rename-repository
refactor/reorganize-app-layout
test/add-health-test
ci/add-github-actions

Allowed types:
feature, fix, docs, chore, refactor, test, ci, build

Use lowercase English words separated by hyphens.
```

## Commit Messages

Use Conventional Commits:
<type>: <short summary>

Examples:
feat: add FastAPI health check endpoint
fix: correct DevContainer workspace mount
docs: update README setup guide
chore: update gitignore rules
refactor: reorganize app structure
test: add health endpoint test
ci: add GitHub Actions workflow
build: update Docker base image

Rules:
Use lowercase type.
Use English.
Keep the summary short and clear.
Do not end the summary with a period.
One commit should contain one logical change.