#!/bin/bash
set -euo pipefail

TARGET_DIR="${1:-$HOME/.openclaw/workspace/.evolution}"
FORCE="${2:-}"
ASSET_DIR="$(cd "$(dirname "$0")/../assets" && pwd)"

mkdir -p "$TARGET_DIR"

copy_file() {
  local name="$1"
  local src="$ASSET_DIR/$name"
  local dest="$TARGET_DIR/$name"

  if [[ -f "$dest" && "$FORCE" != "--force" ]]; then
    echo "keep  $dest"
    return
  fi

  cp "$src" "$dest"
  echo "write $dest"
}

copy_file "LEARNINGS.md"
copy_file "ERRORS.md"
copy_file "FEATURE_REQUESTS.md"
copy_file "CAPABILITIES.md"
copy_file "LEARNING_AGENDA.md"
copy_file "TRAINING_UNITS.md"
copy_file "EVALUATIONS.md"

echo
echo "Workspace bootstrap complete."
echo "Target: $TARGET_DIR"
echo "Use --force as the second argument to overwrite existing ledgers."
