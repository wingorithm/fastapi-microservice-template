#!/bin/bash

# ==============================================================================
# inject_config.sh
#
# A script to read a .env-style configuration file and inject its key-value
# pairs into the HashiCorp Consul KV store.
#
# Usage:
# ./inject_config.sh path/to/your/config.env
#
# ==============================================================================

# --- Configuration ---
# Set the Consul address if it's not the default localhost:8500
# export CONSUL_HTTP_ADDR="http://172.20.0.100:8500"

# --- Script Logic ---

# 1. Check if a config file was provided as an argument
if [ -z "$1" ]; then
  echo "Error: No configuration file specified."
  echo "Usage: $0 <config_file>"
  exit 1
fi

CONFIG_FILE="$1"

# 2. Check if the config file exists and is readable
if [ ! -f "$CONFIG_FILE" ]; then
  echo "Error: File not found: $CONFIG_FILE"
  exit 1
fi

echo "Starting KV injection from '$CONFIG_FILE'..."

# 3. Read the file line by line
PREFIX="config/service-b/"

while IFS= read -r line || [[ -n "$line" ]]; do
  # Skip empty lines and comments
  if [[ -z "$line" || "$line" =~ ^# ]]; then
    continue
  fi

  # Parse the key and value
  # This handles cases where the value might contain an '=' sign
  KEY="${line%%=*}"
  VALUE="${line#*=}"

  # 4. Put the key-value pair into Consul
  echo "-> Putting key: '$PREFIX$KEY'"
  docker exec "consul" consul kv put "$PREFIX$KEY" "$VALUE"

done < "$CONFIG_FILE"

echo ""
echo "✅ Injection complete."