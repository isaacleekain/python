#!/usr/bin/env bash
set -e

uv sync || true

mkdir -p "$HOME/.codex"

cat > "$HOME/.codex/config.toml" <<'EOF'
sandbox_mode = "danger-full-access"
approval_policy = "never"
EOF

if ! command -v codex >/dev/null 2>&1; then
  echo "Installing Codex CLI..."

  curl -fsSL https://chatgpt.com/codex/install.sh -o /tmp/codex-install.sh

  # 自动回答不启动，避免 postCreateCommand 卡在 Codex 交互界面
  yes n | sh /tmp/codex-install.sh || {
    echo "Codex CLI install failed, skipping. You can install it manually later."
  }

  rm -f /tmp/codex-install.sh
else
  echo "Codex CLI already installed:"
  command -v codex
  codex --version || true
fi

echo "Codex configured:"
command -v codex || true
codex --version || true
