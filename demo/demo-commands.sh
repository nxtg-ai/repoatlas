#!/usr/bin/env bash
# Demo commands for terminal recording
# Simulates typing for a natural-looking demo

type_cmd() {
  local cmd="$1"
  local delay="${2:-0.04}"
  echo ""
  for ((i=0; i<${#cmd}; i++)); do
    printf "%s" "${cmd:$i:1}"
    sleep "$delay"
  done
  sleep 0.3
  echo ""
  eval "$cmd"
  sleep 1.5
}

clear
sleep 0.5

# Show the portfolio dashboard
type_cmd "atlas status"

sleep 2

# Show cross-project intelligence
type_cmd "atlas connections"

sleep 2

# Show a single project deep-dive
type_cmd "atlas inspect atlas"

sleep 3
