#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_DIR="$ROOT_DIR/.run"

FRONTEND_PORT=8100
BACKEND_PORT=8101

kill_group_by_pid_file() {
  local name="$1"
  local pid_file="$RUN_DIR/$name.pid"

  if [ ! -f "$pid_file" ]; then
    echo "$name: pid file not found, skip."
    return
  fi

  local pid
  pid="$(cat "$pid_file" 2>/dev/null || true)"

  if [ -z "$pid" ]; then
    rm -f "$pid_file"
    return
  fi

  echo "$name: killing process group $pid..."

  # 杀整个进程组，注意这里是 -$pid
  kill -TERM -- "-$pid" 2>/dev/null || true

  sleep 2

  # 兜底强杀整个进程组
  kill -KILL -- "-$pid" 2>/dev/null || true

  rm -f "$pid_file"
}

kill_port() {
  local port="$1"

  echo "Cleaning port $port..."

  if command -v fuser >/dev/null 2>&1; then
    fuser -k "$port"/tcp 2>/dev/null || true
    sleep 1
    fuser -k -9 "$port"/tcp 2>/dev/null || true
    return
  fi

  if command -v lsof >/dev/null 2>&1; then
    local pids
    pids="$(lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)"

    if [ -n "$pids" ]; then
      echo "$pids" | xargs -r kill -TERM 2>/dev/null || true
      sleep 1
      echo "$pids" | xargs -r kill -KILL 2>/dev/null || true
    fi

    return
  fi

  echo "No fuser or lsof found, skip port cleanup."
}

echo "Stopping services..."

kill_group_by_pid_file frontend
kill_group_by_pid_file backend

echo
echo "Fallback port cleanup..."

kill_port "$FRONTEND_PORT"
kill_port "$BACKEND_PORT"

echo
echo "Remaining ports:"
ss -ltnp 2>/dev/null | grep -E ":$FRONTEND_PORT |:$BACKEND_PORT " || true

echo
echo "Remaining related processes:"
ps -ef | grep -E "npm run dev|vite|uv run python -m app.main|app.main" | grep -v grep || true

echo
echo "Stopped."
