#!/bin/sh
set -eu

required="git curl jq python3"
optional="docker psql"

missing_required=0
printf 'Required dependencies:\n'
for cmd in $required; do
  if command -v "$cmd" >/dev/null 2>&1; then
    printf '  [ok] %s\n' "$cmd"
  else
    printf '  [missing] %s\n' "$cmd"
    missing_required=1
  fi
done

printf 'Optional dependencies:\n'
if command -v docker >/dev/null 2>&1; then
  if docker compose version >/dev/null 2>&1 || command -v docker-compose >/dev/null 2>&1; then
    printf '  [found] docker compose\n'
  else
    printf '  [not found] docker compose\n'
  fi
else
  printf '  [not found] docker\n'
fi

for cmd in psql; do
  if command -v "$cmd" >/dev/null 2>&1; then
    printf '  [found] %s\n' "$cmd"
  else
    printf '  [not found] %s\n' "$cmd"
  fi
done

if [ "$missing_required" -ne 0 ]; then
  exit 1
fi
