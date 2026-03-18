#!/bin/bash
# One-time VPS setup. Run as root on a fresh Ubuntu machine.
# Usage: ./setup.sh <github-runner-token> <repo-owner/repo-name>
set -e

TOKEN="$1"
REPO="$2"
if [ -z "$TOKEN" ] || [ -z "$REPO" ]; then
  echo "Usage: ./setup.sh <runner-registration-token> <owner/repo>"
  exit 1
fi

apt update && apt install -y git curl jq
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
curl -fsSL https://opencode.ai/install | bash
echo 'export PATH="$HOME/.opencode/bin:$HOME/.local/bin:$PATH"' >> /etc/profile.d/theo.sh

RUNNER_DIR=/opt/actions-runner
mkdir -p "$RUNNER_DIR" && cd "$RUNNER_DIR"
RUNNER_VERSION=$(curl -s https://api.github.com/repos/actions/runner/releases/latest | jq -r .tag_name | sed 's/^v//')
curl -o actions-runner.tar.gz -L "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz"
tar xzf actions-runner.tar.gz && rm actions-runner.tar.gz

useradd -m -s /bin/bash theo || true
chown -R theo:theo "$RUNNER_DIR"
su - theo -c "cd $RUNNER_DIR && ./config.sh --url https://github.com/$REPO --token $TOKEN --unattended --name theo-vps"
./svc.sh install theo
./svc.sh start

REPO_DIR=/opt/theo
git clone "https://github.com/$REPO.git" "$REPO_DIR"
chown -R theo:theo "$REPO_DIR"

echo "Setup complete. Now:"
echo "  1. Create /opt/theo/.env with your secrets"
echo "  2. Run: cd /opt/theo && ./vps/sync-schedule.sh"
