#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

FRONTEND_DIR="$ROOT_DIR/frontend"
BACKEND_DIR="$ROOT_DIR/backend"

RUN_DIR="$ROOT_DIR/.run"
LOG_DIR="$ROOT_DIR/logs"

FRONTEND_PORT=8100
BACKEND_PORT=8101

mkdir -p "$RUN_DIR" "$LOG_DIR"

check_port_free() {
  local port="$1"
  local name="$2"

  if ss -ltnp 2>/dev/null | grep -q ":$port "; then
    echo "ERROR: $name port $port is already in use."
    echo "Run ./stop.sh first."
    exit 1
  fi
}

start_frontend() {
  echo "Starting frontend..."

  check_port_free "$FRONTEND_PORT" "frontend"

  setsid bash -c "
    cd '$FRONTEND_DIR'
    exec npm run dev -- --host 0.0.0.0 --port 8100 --strictPort
  " > "$LOG_DIR/frontend.log" 2>&1 &

  local pid=$!
  echo "$pid" > "$RUN_DIR/frontend.pid"

  echo "Frontend started, pgid=$pid"
  echo "Log: $LOG_DIR/frontend.log"
}

start_backend() {
  echo "Starting backend..."

  check_port_free "$BACKEND_PORT" "backend"

  setsid bash -c "
    cd '$BACKEND_DIR'
    exec uv run python -m app.main
  " > "$LOG_DIR/backend.log" 2>&1 &

  local pid=$!
  echo "$pid" > "$RUN_DIR/backend.pid"

  echo "Backend started, pgid=$pid"
  echo "Log: $LOG_DIR/backend.log"
}

start_frontend
start_backend

echo
echo "All services started."
echo "Frontend: http://0.0.0.0:${FRONTEND_PORT}"
echo "Backend:  http://0.0.0.0:${BACKEND_PORT}"
