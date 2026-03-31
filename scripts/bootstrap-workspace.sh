#!/bin/bash
set -euo pipefail

TARGET_DIR="$HOME/.openclaw/workspace/.evolution"
DEFAULT_LEGACY_DIR="$HOME/.openclaw/workspace/.learnings"
FORCE=false
MIGRATE_FROM=""
ASSET_DIR="$(cd "$(dirname "$0")/../assets" && pwd)"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUNTIME="$SCRIPT_DIR/evolution_runtime.py"

usage() {
  cat <<'EOF'
Usage:
  bootstrap-workspace.sh [target-dir] [--force] [--migrate-from <legacy-.learnings-dir>]

Examples:
  bootstrap-workspace.sh
  bootstrap-workspace.sh ~/.openclaw/workspace/.evolution --force
  bootstrap-workspace.sh ~/.openclaw/workspace/.evolution --migrate-from ~/.openclaw/workspace/.learnings
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      FORCE=true
      shift
      ;;
    --migrate-from)
      if [[ $# -lt 2 ]]; then
        echo "Missing path after --migrate-from" >&2
        usage >&2
        exit 1
      fi
      MIGRATE_FROM="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      if [[ "$TARGET_DIR" != "$HOME/.openclaw/workspace/.evolution" ]]; then
        echo "Unexpected argument: $1" >&2
        usage >&2
        exit 1
      fi
      TARGET_DIR="$1"
      shift
      ;;
  esac
done

mkdir -p "$TARGET_DIR"
mkdir -p \
  "$TARGET_DIR/records/learnings" \
  "$TARGET_DIR/records/errors" \
  "$TARGET_DIR/records/feature_requests" \
  "$TARGET_DIR/records/capabilities" \
  "$TARGET_DIR/records/training_units" \
  "$TARGET_DIR/records/evaluations" \
  "$TARGET_DIR/records/agenda" \
  "$TARGET_DIR/index"

copy_seed_records() {
  local source_root="$ASSET_DIR/records"
  local target_root="$TARGET_DIR/records"

  if [[ ! -d "$source_root" ]]; then
    echo "Seed record directory not found: $source_root" >&2
    exit 1
  fi

  while IFS= read -r source_file; do
    local rel="${source_file#$source_root/}"
    local dest="$target_root/$rel"
    mkdir -p "$(dirname "$dest")"

    if [[ -f "$dest" && "$FORCE" != true ]]; then
      echo "keep  $dest"
      continue
    fi

    cp "$source_file" "$dest"
    echo "write $dest"
  done < <(find "$source_root" -type f ! -name '.DS_Store' | sort)
}

copy_seed_records

if [[ -n "$MIGRATE_FROM" ]]; then
  echo
  migrate_args=(python3 "$SCRIPT_DIR/migrate-self-improving.py" --target-dir "$TARGET_DIR" --source-dir "$MIGRATE_FROM")
  if [[ "$FORCE" == true ]]; then
    migrate_args+=(--force)
  fi
  "${migrate_args[@]}"
elif [[ -d "$DEFAULT_LEGACY_DIR" ]]; then
  echo
  echo "Detected legacy self-improving-agent logs at $DEFAULT_LEGACY_DIR"
  echo "Re-run with --migrate-from $DEFAULT_LEGACY_DIR to import them into $TARGET_DIR/legacy-self-improving."
fi

python3 "$RUNTIME" rebuild-index --workspace "$TARGET_DIR" >/dev/null

echo
echo "Workspace bootstrap complete."
echo "Target: $TARGET_DIR"
echo "Canonical records: $TARGET_DIR/records"
echo "Manifest: $TARGET_DIR/index/manifest.json"
echo "Use --force to overwrite existing seed records before rebuilding."
echo "Use --migrate-from <legacy-.learnings-dir> to import self-improving-agent history."
